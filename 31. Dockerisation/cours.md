## Etape 1 : Installation

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
venv/Scripts/activate
```

## Etape 2 : Explorer une image python

```bash
# Télécharger une image 
docker pull python:3.9-slim

# Vérifier que l'image est bien téléchargée
docker images

# Lancer python dans un conteneur interactif
docker run -it python:3.9-slim python

# Lancer le conteneur en mode bash
docker run -it python:3.9-slim bash

# Exécuter un script local via Docker
docker run -v ${PWD}:/app python:3.9-slim python /app/test.py
```

- `-v ${PWD}:/app` : Monte le répertoire courant dans `/app`du conteneur

## Etape 3 : Gérer les conteneurs

```bash
# Lancer un conteneur en arrière-plan
docker run -d --name mon_python python:3.9-slim

# Voir les conteneurs en cours d'exécution
docker ps

# Arrêter le conteneur
docker stop mon_python

# Supprimer le conteneur
docker rm mon_python
```

## Etape 4 : premier projet ML conteneurisé

### Structure du projet

```
demo_ml/
├── venv
├── train_simple.py
├── requirements.txt
├── Readme.md
└── Dockerfile
```
## Fichiers

**requirements.txt** :

```
joblib==1.5.3
numpy==2.4.4
pandas==3.0.2
python-dateutil==2.9.0.post0
scikit-learn==1.8.0
scipy==1.17.1
six==1.17.0
threadpoolctl==3.6.0
tzdata==2026.1
```

**Dockerfile** :

```dockerfile
FROM python:3.11.9-slim

WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le script
COPY train_simple.py .

# Exécuter le script
# CMD ["python", "train_simple.py"]
ENTRYPOINT ["python", "train_simple.py"]
```

### Construction et exécution

```bash
# Construire l'image
docker build -t demo_simple_ml .

# Exécuter le conteneur
docker run demo_simple_ml
```