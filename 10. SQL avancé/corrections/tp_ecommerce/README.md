# Projet Supershop — PostgreSQL + Docker + Génération de Rapport Python

Ce projet propose un environnement complet pour :
- créer et initialiser une base de données **PostgreSQL** avec des scripts SQL,
- gérer facilement la base via **pgAdmin**,
- exécuter un script **Python Dockerisé** générant un **rapport d'analyse métier** à partir des données,
- produire automatiquement un fichier texte `rapport_supershop.txt` dans un dossier dédié.

L'ensemble s'exécute entièrement via **Docker Compose**, sans installation locale de PostgreSQL ni Python.

![diagramme](./diagramme/schemas.png)

---

## Structure du Projet

```
│
├── docker-compose.yml             # Orchestration Docker (PostgreSQL, pgAdmin, script Python)
│
├── scripts/                       # Scripts SQL exécutés automatiquement au 1er démarrage
│   ├── 01_schema.sql
│   └── 02_data.sql
│
├── python/                        # Script Python + Dockerfile dédié
│   ├── Dockerfile
│   └── report_supershop.py
│
└── rapport/                       # Dossier où sera généré le rapport final
    └── rapport_supershop.txt      # (généré après exécution du script)

````

---

## Technologies Utilisées

- **Docker & Docker Compose**
- **PostgreSQL 18+**
- **pgAdmin 4**
- **Python 3.12 (Dockerisé)**
- **psycopg (driver PostgreSQL)**

![](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

---

## Installation & Lancement

Assurez-vous simplement d’avoir **Docker** installé.

### 1️⃣ Lancer PostgreSQL + pgAdmin

Depuis la racine du projet :

```bash
docker compose up -d db pgadmin
````

Cela va :

* créer le conteneur PostgreSQL,
* exécuter automatiquement les scripts SQL dans `scripts/`,
* démarrer pgAdmin sur `http://localhost:8080`.

### Identifiants pgAdmin :

* **Email** : `admin@admin.com`
* **Mot de passe** : `admin`

La base PostgreSQL est disponible sur :

* **hôte Docker** : `db`
* **port** : `5432`
* **utilisateur** : `admin`
* **mot de passe** : `admin`
* **base** : `supershop`

---

##  2️⃣ Construire l’image Docker du script Python

Dans la racine du projet :

```bash
docker compose build report
```

---


## 3️⃣ Générer le rapport Supershop

Exécuter simplement :

```bash
docker compose run --rm report
```

Le rapport généré sera disponible dans :

```
./rapport/rapport_supershop.txt
```

Ce fichier contient :

* Chiffre d’affaires total
* Panier moyen
* Produit le plus vendu
* Top 3 clients
* CA par catégorie

---

## 🔁 Réinitialiser complètement l’environnement

Pour effacer la base PostgreSQL, pgAdmin et les volumes :

```bash
docker compose down -v
```

Puis relancer :

```bash
docker compose up -d
```

---

##  Personnaliser ou Étendre le Projet

* Ajouter d’autres scripts SQL dans `scripts/` → ils s’exécuteront au premier démarrage.
* Modifier ou ajouter des rapports Python → placer les fichiers dans `python/`.
* Ajouter un cron dans Docker pour générer un rapport quotidien.
* Connecter un frontend ou une API au PostgreSQL du conteneur.