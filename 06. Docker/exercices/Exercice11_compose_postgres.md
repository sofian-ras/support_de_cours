# Docker compose avec Postgres et Pgadmin

## Objectifs

Créer un docker-compose.yml qui permet de créer 2 conteneurs partageant un volume et un réseau. 

## Taches 

1. Créer un fichier docker-compose dans un dossier de travail. 

2. Créer un premier service `db` :
    - Il sera base sur l'image de postgres
    - Il aura pour nom de conteneur : local_pgdb
    - Préciser les variables d'environment nécessaire
    - Assigner lui les ports correspondant à PostgreSQL
    - Attribuer lui un volume `local_pgdata`
    - Attribuer lui un network `db_network`

2. Créer un second service `pgadmin` :
    - Il sera base sur l'image de `pgadmin4`
    - Il aura pour nom de conteneur : pgadmin_gui
    - Préciser les variables d'environment nécessaire
    - Assigner lui les ports correspondant à PostgreSQL
    - Attribuer lui un volume `local_pgdata`
    - Attribuer lui un network `db_network`

3. Créer le volume `local_pgdata`
4. Créer le network `db_network`
