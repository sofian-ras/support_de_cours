# Exercice docker compose

On souhaite dockerise notre application back_employee et front_employee ainsi que la bdd mysql utilisé dans ce projet fullstack.

On ajoutera les dockerfile a la racine de chaque projet ainsi qu'un docker compose afin de lance l'integralite du projet.

Pour le projet back (dans le docker-compose), nous aurons besoin des variables d'environment suivantes : 

SPRING_DATASOURCE_URL: jdbc:mysql://nom_conteneur_bdd:3306/employee
SPRING_DATASOURCE_PASSWORD: password
SPRING_DATASOURCE_USERNAME: root