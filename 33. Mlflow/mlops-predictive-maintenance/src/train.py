import os
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from mlflow.models import infer_signature
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

from src.preprocess import add_engineered_features, get_feature_pipeline, load_raw_data


def train() -> dict:
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "ai4i2020.csv"

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    model_name = os.getenv("MODEL_NAME", "predictive-maintenance-model")

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("predictive-maintenance")

    df = load_raw_data(str(data_path))
    df = add_engineered_features(df)

    X = df.drop(columns=["machine_failure"])
    y = df["machine_failure"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", get_feature_pipeline()),
            ("smote", SMOTE(random_state=42)),
            (
                "clf",
                RandomForestClassifier(
                    n_estimators=300,
                    class_weight="balanced",
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1", n_jobs=-1)

    with mlflow.start_run(run_name="rf-smote"):
        mlflow.log_params(
            {
                "model_name": model_name,
                "n_estimators": 300,
                "use_smote": True,
                "test_size": 0.2,
            }
        )

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        y_proba = pipeline.predict_proba(X_test)[:, 1]

        metrics = {
            "f1_score": float(f1_score(y_test, y_pred)),
            "recall": float(recall_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred)),
            "roc_auc": float(roc_auc_score(y_test, y_proba)),
            "cv_f1_mean": float(cv_scores.mean()),
        }
        mlflow.log_metrics(metrics)

        input_example = X_train.iloc[:5].copy()
        signature = infer_signature(input_example, pipeline.predict(input_example))
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="model",
            signature=signature,
            input_example=input_example,
            registered_model_name=model_name,
        )

    return metrics


if __name__ == "__main__":
    output = train()
    print(pd.Series(output).to_string())
