### Exercice : Utilisation des Volumes Docker avec PostgreSQL

### Étape 1 : Créer un volume Docker

Créez un volume nommé `pgdata_exercice` :

```bash
docker volume create pgdata_exercice
```

### Étape 2 : Démarrer un conteneur PostgreSQL en utilisant le volume

Lancez un conteneur PostgreSQL en utilisant le volume `pgdata_exercice` :

```bash
docker run -d -e POSTGRES_PASSWORD=secret -v pgdata_exercice:/var/lib/postgresql --name first_db postgres
```

### Étape 3 : Créer une base de données, des tables et insérer des données

1. Entrer dans le conteneur :

```bash
docker exec -it first_db bash
```

2. Accéder à PostgreSQL :

```bash
psql -U postgres
```

3. Créer une base de données `school` :

```sql
CREATE DATABASE school;
```

4. Se connecter à la base de données `school` : (\c [nom_bdd])

```sql
\c school 
```

5. Créer une table `students` :

```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    age INT
);
```

6. Insérer des données dans la table `students` :

```sql
INSERT INTO students (name, age) VALUES ("toto", 30); 
```

7. Vérifier que les données ont été insérées :

```sql
SELECT * FROM students; 
```

8. Sortir de PostgreSQL et du conteneur :

```bash
\q 
exit
```

### Étape 4 : Arrêter et redémarrer le conteneur

1. Arrêter le conteneur :
2. Supprimer le conteneur
3. Recréer un nouveau conteneur avec le volume `pgdata_exercice` :

```bash
docker stop first_db
docker rm first_db

docker run -d -e POSTGRES_PASSWORD=secret -v pgdata_exercice:/var/lib/postgresql --name second_db postgres 
```

### Étape 5 : Vérifier la persistance des données après le redémarrage

1. Entrer dans le conteneur :

```bash
docker exec -it second_db bash
```

2. Accéder à PostgreSQL :

```bash
psql -U postgres
```

3. Se connecter à la base de données `school` :

```bash
\c school
```

4. Vérifier que les données sont toujours présentes :

```sql
SELECT * FROM students;
```