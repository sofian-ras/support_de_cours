import os
import pickle
from datetime import datetime
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_model():
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Précision du modèle: {accuracy:.2%}")

    return model, accuracy

def save_model(model):
    os.makedirs('/app/models', exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f'/app/models/model_{timestamp}.pkl'

    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print(f"Modèle sauvegardé : {model_path}")

    models = os.listdir('/app/models')
    print(f"Total de {len(models)} modèles enregistrés")

def save_metrics(accuracy):
    os.makedirs('/app/logs', exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = f'/app/logs/metrics_{timestamp}.txt'

    with open(log_path, 'w') as f:
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Accuracy: {accuracy:.2%}\n")

    print(f"Métriques sauvegardées : {log_path}")

    logs = os.listdir('/app/logs')
    print(f"Total de {len(logs)} entraînements enregistrés")

def main():
    model, accuracy = train_model()

    save_model(model)

    save_metrics(accuracy)

if __name__ == '__main__':
    main()