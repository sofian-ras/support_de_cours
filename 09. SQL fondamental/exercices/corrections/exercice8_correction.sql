-- Correction exercice 8 - Sous-requete

--1. Affichez les utilisateurs nés dans le même lieu que celui du plus jeune utilisateur.

SELECT *
FROM Users
WHERE lieu_naissance = (
    SELECT lieu_naissance
    FROM Users
    ORDER BY date_naissance DESC
    LIMIT 1
);

--2. Sélectionnez les utilisateurs dont le salaire est inférieur à la moyenne des salaires des "Developers".

SELECT *
FROM Users
WHERE salaire < (
    SELECT AVG(salaire)
    FROM Users
    WHERE profession = 'Developer'
);

--3. Affichez les utilisateurs dont le salaire est supérieur à la moyenne des salaires des utilisateurs nés dans la même ville que "John Doe".

SELECT *
FROM Users
WHERE salaire > (
    SELECT AVG(salaire)
    FROM Users
    WHERE lieu_naissance = (
        SELECT lieu_naissance
        FROM Users
        WHERE nom = 'John Doe'
        LIMIT 1
    )
);