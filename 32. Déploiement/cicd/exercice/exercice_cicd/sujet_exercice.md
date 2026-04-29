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

### **Exercice 3 : Tests et Pull Request**

**Objectif** : Protéger la branche principale avec des tests obligatoires

**Consignes** :

1. Créer une branche `feature/add-documentation`
2. Ajouter des commentaires de documentation dans `app_satisfaction.py`
3. Créer une Pull Request vers `main`
4. Modifier le workflow pour qu'il s'exécute sur les PR
5. Observer que les tests s'exécutent automatiquement

**Validation** : Les tests doivent s'exécuter sur votre PR et afficher un statut vert

### **Exercice 4 : Artéfacts et rapports de couverture**

**Objectif** : Générer et sauvegarder un rapport de couverture de code

**Consignes** :

1. Modifier le workflow `02_test.yml` pour ajouter (gardez les étapes précédentes) :
   - Générer un rapport de couverture avec `pytest --cov=. --cov-report=html --cov-report=term`
   - Uploader le rapport HTML comme artéfact nommé `coverage-report`
   - (bonus) Créer un output qui affiche le pourcentage de couverture

2. Ajouter un second job `report` qui :
   - Dépend du job `test` (utilisez `needs`)
   - Affiche un message de succès avec le résultat des tests

**Validation** : Téléchargez l'artéfact depuis GitHub Actions et consultez le rapport HTML

### **Exercice 5 : Matrice de tests multi-versions**


**Objectif** : Tester l'API sur plusieurs versions de Python et systèmes d'exploitation

**Consignes** :

1. Créer un workflow `03_matrix.yml` qui teste sur :
   - Python : `3.9`, `3.10`, `3.11`
   - OS : `ubuntu-latest`, `windows-latest`
2. Utiliser une stratégie de matrice
3. Les tests doivent s'exécuter en parallèle
4. Afficher la version Python et l'OS utilisés dans les logs

**Validation** : Observer 6 jobs qui s'exécutent en parallèle (3 versions × 2 OS)