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

3. Créer le volume `local_pgadmin_data`
4. Créer le network `db_network`
