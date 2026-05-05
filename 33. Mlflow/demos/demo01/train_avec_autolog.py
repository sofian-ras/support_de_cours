from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import mlflow

# Activer l'autolog - tout sera loggé automatiquement
mlflow.sklearn.autolog()

test_size = 0.2
X,y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

# Configurer MlFlow
mlflow.set_experiment("wine-classification-autolog")

with mlflow.start_run(run_name="random-forest-baseline"):
    n_estimators = 100
    max_depth = 5
    random_state = 42

    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    score = model.score(X_test, y_test)

    print("Model enregistré !")