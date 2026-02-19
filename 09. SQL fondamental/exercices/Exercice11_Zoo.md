
## Exercice 10 – Gestion d’animaux pour un zoo

### Objectif

Créer une application pour gérer les animaux d’un zoo.

---

### 1. Modèle d’animal

Chaque animal doit avoir les attributs suivants :

* `id` (clé primaire, auto-incrémentée)
* `nom` (texte)
* `age` (entier)
* `regime_alimentaire` (enum : par exemple `herbivore`, `carnivore`, `omnivore`)
* `date_arrivee` (date d’arrivée au zoo)

---

### 2. Fonctions à créer

1. **Création d’un animal**

   * Ajouter un nouvel animal dans la base de données.

2. **Recherche par ID**

   * Retourner un animal correspondant à un identifiant donné.

3. **Recherche par nom**

   * Retourner tous les animaux ayant un nom donné (le nom n’est pas forcément unique).

## Bonus

* Créer une table `regimes_alimentaires` contenant la liste des régimes possibles.
* Modifier la table `animaux` pour remplacer `regime_alimentaire` par une clé étrangère `regime_id` pointant vers la table `regimes_alimentaires`.
* Adapter les opérations de création et de recherche en conséquence (ex. recherche par nom de régime via un `JOIN`).


### 3. Contraintes et bonnes pratiques

* Utiliser `psycopg` pour interagir avec la base PostgreSQL.
* Toujours fermer les connexions et les curseurs, de préférence avec le mot-clé `with`.
* Prévoir la gestion des exceptions pour les erreurs de connexion ou de requêtes SQL.
