import mlflow
from mlflow.tracking import MlflowClient
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import pandas as pd

X, y = make_classification(
    n_samples=1500,
    n_features=18,
    n_informative=10,
    random_state=0
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

mlflow.set_tracking_uri("http://localhost:5000")
client = MlflowClient()

existing = client.get_experiment_by_name("spam_detection")
if existing:
    client.delete_experiment(existing.experiment_id)

exp_id = client.create_experiment(
    name="spam_detection",
    tags={"team": "data-science", "project": "spam-v1", "owner": "Christophe"}
)

exp = client.get_experiment_by_name("spam_detection")
print(exp.experiment_id, exp.lifecycle_stage)


param_grid = [
    {"model": "random_forest", "n_estimators": 50,  "max_depth": 3},
    {"model": "random_forest", "n_estimators": 100, "max_depth": 5},
    {"model": "logistic_reg",  "C": 0.1,            "max_iter": 200},
    {"model": "logistic_reg",  "C": 1.0,            "max_iter": 200},
]

run_ids = []

for i, params in enumerate(param_grid):
    model_type = params["model"]
    run_name   = f"{model_type}_trial_{i+1}"

    run    = client.create_run(experiment_id=exp_id, run_name=run_name, tags={"model_type": model_type})
    run_id = run.info.run_id

    try:
        for k, v in params.items():
            if k != "model":
                client.log_param(run_id, k, v)
        client.log_param(run_id, "model_type", model_type)
        client.log_param(run_id, "test_size", 0.2)

        if model_type == "random_forest":
            model = RandomForestClassifier(
                n_estimators=params["n_estimators"],
                max_depth=params["max_depth"],
                random_state=42
            )
        else:
            model = LogisticRegression(
                C=params["C"],
                max_iter=params["max_iter"],
                random_state=42
            )

        cv_acc = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
        model.fit(X_train, y_train)
        y_pred  = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        client.log_metric(run_id, "cv_accuracy_mean", round(cv_acc.mean(), 4))
        client.log_metric(run_id, "cv_accuracy_std",  round(cv_acc.std(),  4))
        client.log_metric(run_id, "test_accuracy",    round(accuracy_score(y_test, y_pred), 4))
        client.log_metric(run_id, "test_roc_auc",     round(roc_auc_score(y_test, y_proba), 4))
        client.log_metric(run_id, "test_f1",          round(f1_score(y_test, y_pred), 4))

        client.set_terminated(run_id, "FINISHED")
        run_ids.append(run_id)

    except Exception as e:
        client.set_terminated(run_id, "FAILED")
        raise e
    
# 3a — Tous les runs triés
all_runs = client.search_runs(
    experiment_ids=[exp_id],
    order_by=["metrics.test_roc_auc DESC"]
)
for r in all_runs:
    print(f"{r.info.run_name:<25} roc={r.data.metrics.get('test_roc_auc', 0):.3f} | acc={r.data.metrics.get('test_accuracy', 0):.3f}")

# 3b — Seuil sur métrique
filtered = client.search_runs(
    experiment_ids=[exp_id],
    filter_string="metrics.test_roc_auc > 0.85"
)
print(f"{len(filtered)} runs passent le seuil roc_auc > 0.85")

# 3c — Filtrage par tag
rf_runs = client.search_runs(
    experiment_ids=[exp_id],
    filter_string="tags.model_type = 'random_forest'"
)
for r in rf_runs:
    print(r.info.run_name)

# 3d — Combinaison
combined = client.search_runs(
    experiment_ids=[exp_id],
    filter_string="tags.model_type = 'random_forest' AND metrics.test_accuracy > 0.88"
)
for r in combined:
    print(r.info.run_name, r.data.metrics.get("test_accuracy"))


runs_data = client.search_runs(
    experiment_ids=[exp_id],
    filter_string="attributes.status = 'FINISHED' AND metrics.test_roc_auc > 0"
)

df = pd.DataFrame([{
    "run_name":      r.info.run_name,
    "model_type":    r.data.tags.get("model_type", ""),
    "test_accuracy": r.data.metrics.get("test_accuracy"),
    "test_roc_auc":  r.data.metrics.get("test_roc_auc"),
    "test_f1":       r.data.metrics.get("test_f1"),
    "run_id":        r.info.run_id,
} for r in runs_data])

df_sorted = df.sort_values("test_roc_auc", ascending=False)
print(df_sorted[["run_name", "model_type", "test_accuracy", "test_roc_auc", "test_f1"]].to_string(index=False))

best_run_id = df_sorted.iloc[0]["run_id"]

client.set_tag(best_run_id, "status", "champion")
client.set_tag(best_run_id, "promoted_at", time.strftime("%Y-%m-%d"))

updated = client.get_run(best_run_id)
print(updated.data.tags)

for _, row in df_sorted.iloc[1:].iterrows():
    client.set_tag(row["run_id"], "status", "challenger")