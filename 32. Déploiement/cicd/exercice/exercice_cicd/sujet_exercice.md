# Projet Fil Rouge - CI/CD pour API de Prédiction ML

## Structure du projet

```
api_prediction/
├── app_satisfaction.py          # API Flask principale
├── test_app_satisfaction.py     # Tests unitaires (pytest)
├── requirements.txt             # Dépendances Python (à créer)
├── Dockerfile                   # Image Docker (à créer)
└── .github/workflows/           # Workflows GitHub Actions (à créer)
```

## Exercices progressifs

### **Exercice 1 : Premier workflow - Hello CI/CD**

**Objectif** : Créer votre premier workflow GitHub Actions

**Consignes** :

1. Créer le dossier `.github/workflows/` dans votre projet
2. Créer un fichier `01_hello.yml` qui :
   - Se déclenche sur chaque push
   - Affiche "Bienvenue dans la CI/CD pour l'API de satisfaction !"
   - Affiche la date et l'heure du déclenchement


### **Exercice 2 : Workflow de test automatique**

**Objectif** : Automatiser l'exécution des tests à chaque push

**Consignes** :

1. Créer un workflow `02_test.yml` qui :
   - Se déclenche sur push et pull request
   - Configure Python 3.11.9
   - Installe les dépendances
   - Exécute les tests avec pytest
