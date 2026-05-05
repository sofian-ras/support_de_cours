import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mlflow
import mlflow.sklearn
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, ConfusionMatrixDisplay,
    roc_curve, auc, RocCurveDisplay
)

url = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
)
columns = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal", "target"
]
df = pd.read_csv(url, names=columns, na_values="?")

# Cible binaire : 0 = pas de maladie, 1 = maladie
df["target"] = (df["target"] > 0).astype(int)

print(df.shape)
print(df.isnull().sum())
print(df["target"].value_counts())

# 2.1 Suppression des lignes avec valeurs manquantes (6 lignes concernées)
df_clean = df.dropna()
print(f"\nNombre de lignes après nettoyage: {len(df_clean)}")

# 2.2 Séparation features / cible
X = df_clean.drop("target", axis=1)
y = df_clean["target"]

mlflow.set_experiment("heart_disease_eda")

with mlflow.start_run(run_name="EDA"):

    # --- Figure 1 : Distribution de la cible ---
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    df_clean["target"].value_counts().plot(kind="bar", ax=ax1, color=["skyblue", "salmon"])
    ax1.set_title("Distribution de la cible (Heart Disease)")
    ax1.set_xlabel("Classe")
    ax1.set_ylabel("Nombre de patients")
    ax1.set_xticklabels(["Sain", "Malade"], rotation=0)
    plt.tight_layout()
    mlflow.log_figure(fig1, "target_distribution.png")
    plt.close(fig1)

    # --- Figure 2 : Distribution de l'âge par classe ---
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    df_clean.boxplot(column="age", by="target", ax=ax2)
    ax2.set_title("Distribution de l'âge par classe")
    ax2.set_xlabel("Classe (0=Sain, 1=Malade)")
    ax2.set_ylabel("Âge")
    plt.tight_layout()
    mlflow.log_figure(fig2, "age_by_target.png")
    plt.close(fig2)

    # --- Figure 3 : Heatmap des corrélations ---
    fig3, ax3 = plt.subplots(figsize=(12, 10))
    corr = df_clean.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax3, center=0)
    ax3.set_title("Matrice de corrélation")
    plt.tight_layout()
    mlflow.log_figure(fig3, "correlation_heatmap.png")
    plt.close(fig3)

    mlflow.log_param("n_samples", len(df_clean))
    mlflow.log_param("n_features", X.shape[1])

    print("EDA terminé")


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

mlflow.set_experiment("heart_disease_svc")

# 5.1 Pipeline : StandardScaler → SVC
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svc", SVC(random_state=42, probability=True))
])

# 5.2 Grille — préfixe "svc__" pour cibler les params du SVC dans le pipeline

param_grid = {
    "svc__C": [0.1, 1, 10, 100],
    "svc__kernel": ["linear", "rbf", "poly"],
    "svc__gamma": ["scale", "auto"]
}

gs = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring="recall",
    n_jobs=-1,
    verbose=1
)

gs.fit(X_train, y_train)


with mlflow.start_run(run_name="SVC_GridSearch"):

    # 5.3 Log des meilleurs hyperparamètres ---
    # On nettoie le préfixe "svc__" pour plus de lisibilité dans l'UI
    best_params_clean = {
        k.replace("svc__", ""): v for k, v in gs.best_params_.items()
    }
    mlflow.log_params(best_params_clean)
    mlflow.log_metric("best_cv_score", gs.best_score_)

    # 5.4 Évaluation sur le test set
    y_pred = gs.predict(X_test)
    y_pred_proba = gs.predict_proba(X_test)[:, 1]

    test_accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric("test_accuracy", test_accuracy)

    # 5.5 Calcul de l'AUC-ROC
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    mlflow.log_metric("test_auc_roc", roc_auc)
    print(f"AUC-ROC: {roc_auc:.4f}")

    # --- Figure 1 : Matrice de confusion ---
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Sain", "Malade"])
    disp.plot(ax=ax4, cmap="Blues", values_format="d")
    ax4.set_title("Matrice de confusion - Test Set")
    plt.tight_layout()
    mlflow.log_figure(fig4, "confusion_matrix.png")
    plt.close(fig4)

    # --- Figure 2 : Courbe ROC ---
    fig5, ax5 = plt.subplots(figsize=(8, 6))
    RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc).plot(ax=ax5)
    ax5.plot([0, 1], [0, 1], "k--", label="Chance (AUC = 0.5)")
    ax5.set_title("Courbe ROC - SVC")
    ax5.legend()
    plt.tight_layout()
    mlflow.log_figure(fig5, "roc_curve.png")
    plt.close(fig5)

    # 5.6 Log du modèle
    mlflow.sklearn.log_model(
        gs.best_estimator_,
        "model",
        input_example=X_train.iloc[:5]
    )

    print("modèle sauvegardé")