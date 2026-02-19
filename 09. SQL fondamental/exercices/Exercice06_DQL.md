# Exercices DQL 

## SELECT FROM

Essayons maintenant nous-même de récupérer les données de la table **Users** de notre base de données.
1) Dans un premier temps, récupérez l'intégralité de la table **Users**
2) Modifiez la requête pour n'afficher que les colonnes **first_name**, **last_name** et **job**

## SELECT WHERE

Essayons maintenant nous-même de filtrer les données de la table **Users** de notre base de données.
1) Dans une première requête, récupérez tous les utilisateurs dont le métier n'est pas développeur
2) Dans une seconde requête, récupérez tous les utilisateurs dont le prénom est John.
3) Dans une dernière requête, récupérez tous les utilisateurs dont le salaire est supérieur ou égal à 3000.

## SELECT OR AND 

Dans notre table **Users**, essayez de filtrer de cette manière:
1) Dans un première requête, récupérez tous les utilisateurs dont l'âge est inférieur à 30ans ou supérieur et égal à 35ans.
2) Récupérez ensuite tous les utilisateurs dont le métier est professeur et le salaire est supérieur à 2600.


## SELECT NOT 

Créez une requête qui permet de récupérer toutes les personnes qui sont nées à New York, dont le salaire est compris entre 3000 et 3500 (compris) et qui ne sont ni docteur ni avocat.

- Toutes les conditions doivent tenir en une seule requête
- Les trois opérateurs logiques : AND, OR et NOT doivent être utilisés.

## SELECT BETWEEN IN 

Dans notre table **Users**, en utilisant au moins pour une requête IN et pour une autre BETWEEN:
1) Sélectionnez tous les enregistrements où le métier est "Engineer"
2) Sélectionnez les prénoms et les noms de famille des utilisateurs nés à Londres, Paris ou Berlin
3) Sélectionnez les utilisateurs dont l'âge est compris entre 25 et 35 ans
4) Sélectionnez les utilisateurs qui sont à la fois des développeurs et dont le salaire est supérieur à 2500€

## SELECT LIKE

Dans notre table USERS, construisez les requêtes suivantes:

1) Sélectionnez les utilisateurs ayant un prénom qui commence par "D".
2) Trouvez les utilisateurs dont le nom de famille se termine par "son".
3) Identifiez les utilisateurs dont le prénom contient exactement 5 caractères.
4) Sélectionnez les utilisateurs ayant "Doctor" dans leur métier. (caractère générique obligatoire )

## SELECT ORDER BY, LIMIT, OFFSET

Toujours au sein de notre table Users, construisez les requêtes suivantes:

1) Sélectionnez les cinq utilisateurs les plus âgés de la table "Users", triés par ordre décroissant d'âge.
2) Affichez les enregistrements 6 à 10 triés par ordre alphabétique du prénom.
3) Sélectionnez les trois utilisateurs ayant les salaires les plus élevés de la table "Users", triés par ordre décroissant de salaire.

## SELECT (aggregation)

Dans ma table Users, trouvez les requêtes suivantes **en utilisant à chaque fois des alias**:

1) Quel est le salaire minimum parmi tous les utilisateurs ?
2) Quel est l'âge maximum parmi les utilisateurs ayant le métier "Engineer" ?
3) Trouvez le salaire moyen des utilisateurs dont le métier est "Teacher".
4) Trouvez le montant total des salaires de tous les utilisateurs.

## SELECT GROUP BY et HAVING 

1) Affichez le nombre d'utilisateurs par lieu de naissance, mais ne montrez que les lieux avec plus d'un utilisateur.

2) Sélectionnez la profession et la moyenne des salaires pour chaque profession, mais ne montrez que celles avec une moyenne de salaire supérieure à 2500.

3) Affichez la somme des salaires pour chaque lieu de naissance, mais ne montrez que les lieux dont la somme des salaires est supérieure à 5000.

4) Sélectionnez la date de naissance et le nombre d'utilisateurs nés à chaque date, mais ne montrez que les dates où il y a plus d'un utilisateur né.

5) Affichez la profession, le lieu de naissance, et le salaire maximum pour chaque profession et lieu, mais ne montrez que les résultats où le salaire maximum est supérieur à 3000.


   
