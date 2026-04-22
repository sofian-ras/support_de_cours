import os
import json
from datetime import datetime

# Récupérer la configuration depuis l'environnement
ENV = os.getenv('ENVIRONMENT', 'development')
MODEL_TYPE = os.getenv('MODEL_TYPE', 'simple')
N_ESTIMATORS = int(os.getenv('N_ESTIMATORS', '10'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
ENABLE_MONITORING = os.getenv('ENABLE_MONITORING', 'false').lower() == 'true'

def log(message, level='INFO'):
    """Log avec niveau de détail configurable"""
    if LOG_LEVEL == 'DEBUG' or level != 'DEBUG':
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] [{level}] {message}")

def train_model():
    log(f"CONFIGURATION - Environnement: {ENV}")

    log(f"Model Type: {MODEL_TYPE}")
    log(f"N Estimators: {N_ESTIMATORS}")
    log(f"Log Level: {LOG_LEVEL}")
    log(f"Monitoring: {'Enabled' if ENABLE_MONITORING else 'Disabled'}")

    log("\nDémarrage de l'entraînement...", 'INFO')

    # Simuler un entraînement
    if MODEL_TYPE == 'simple':
        log("Utilisation d'un modèle simple (rapide)", 'DEBUG')
        training_time = 2
    else:
        log("Utilisation d'un modèle optimisé (lent)", 'DEBUG')
        training_time = 10

    log(f"Temps d'entraînement estimé: {training_time}s", 'DEBUG')

    # Simuler des étapes
    for i in range(N_ESTIMATORS // 10):
        log(f"Entraînement de l'arbre {i+1}...", 'DEBUG')

    log("Entraînement terminé!", 'INFO')

    # Monitoring
    if ENABLE_MONITORING:
        log("\nMONITORING", 'INFO')
        metrics = {
            'environment': ENV,
            'model_type': MODEL_TYPE,
            'n_estimators': N_ESTIMATORS,
            'timestamp': datetime.now().isoformat()
        }
        log(f"Metrics: {json.dumps(metrics, indent=2)}", 'DEBUG')

if __name__ == '__main__':
    train_model()