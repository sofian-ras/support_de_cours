import json
import os
from datetime import datetime
import random

def train_model():
    # Simuler un entraînement
    accuracy = random.uniform(0.7, 0.95)
    loss = random.uniform(0.1, 0.5)

    # Créer un log
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'accuracy': accuracy,
        'loss': loss,
        'model_version': 'v1.0'
    }

    # Sauvegarder dans un fichier
    os.makedirs('logs', exist_ok=True)
    log_file = f'logs/training_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

    with open(log_file, 'w') as f:
        json.dump(log_entry, f, indent=2)

    print(f"Modèle entraîné!")
    print(f"   Accuracy: {accuracy:.2%}")
    print(f"   Loss: {loss:.4f}")
    print(f"Log sauvegardé: {log_file}")

    # Lister tous les logs
    logs = os.listdir('logs')
    print(f"Total de {len(logs)} entraînements enregistrés")

if __name__ == '__main__':
    train_model()