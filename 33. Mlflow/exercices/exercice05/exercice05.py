import mlflow
import mlflow.sklearn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from mlflow.tracking import MlflowClient

# Charger les données
X, y = load_digits(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

mlflow.set_experiment("registry-exercice")

model_name = "digits-classifier"

# Modèle 1 : Logistic Regression
with mlflow.start_run(run_name="logistic-regression"):
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    mlflow.log_params({"model_type": "LogisticRegression"})
    mlflow.log_metric("test_accuracy", accuracy)


    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name=model_name
    )

    print(f"Logistic Regression - Accuracy: {accuracy:.4f}")

# Modèle 2 : Random Forest
with mlflow.start_run(run_name="random-forest"):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    mlflow.log_params({"model_type": "RandomForest", "n_estimators": 100})
    mlflow.log_metric("test_accuracy", accuracy)

    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name=model_name
    )

    print(f"Random Forest - Accuracy: {accuracy:.4f}")

# Identifier et promouvoir le meilleur


client = MlflowClient()

versions = client.search_model_versions(f"name='{model_name}'")

# Trouver la meilleure version
best_version = None
best_accuracy = 0

for v in versions:
    run = client.get_run(v.run_id)
    accuracy = run.data.metrics.get('test_accuracy', 0)

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_version = v

# Promouvoir en Production
if best_version:
    client.transition_model_version_stage(
        name=model_name,
        version=best_version.version,
        stage="Production",
        archive_existing_versions=True
    )

    print(f"\nVersion {best_version.version} promue en Production (accuracy: {best_accuracy:.4f})")