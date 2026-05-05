from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix, ConfusionMatrixDisplay
import mlflow
import matplotlib.pyplot as plt

test_size = 0.2
X,y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

mlflow.set_experiment("wine-classification-visu")

with mlflow.start_run(run_name="with-visu"):
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")

    # Logger les métrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)

    # matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.title("Confusion Matrix")
    plt.savefig("confusion_matrix.png")
    mlflow.log_artifact("confusion_matrix.png")
    plt.close()

    # Feature importance
    feature_importance = model.feature_importances_
    plt.figure(figsize=(10,6))
    plt.bar(range(len(feature_importance)), feature_importance)
    plt.xlabel("Feature Index")
    plt.ylabel("Importance")
    plt.title("Feature importance")
    plt.savefig("feature_importance.png")
    mlflow.log_artifact("feature_importance.png")
    plt.close()

    # Logger directement la figure
    plt.figure(figsize=(10,6))
    plt.hist(y_pred, bins=3,alpha=0.7, label="Predictions")
    plt.hist(y_test, bins=3,alpha=0.7, label="True")
    plt.legend()
    plt.title("Prédiction vs True")
    mlflow.log_figure(plt.gcf(), "prediction.png")
    plt.close()
