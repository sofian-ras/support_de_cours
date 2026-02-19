CREATE SCHEMA IF NOT EXISTS exercice1;

CREATE TABLE exercice1.livres (
	id_livre INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	titre VARCHAR(255), 
	auteur VARCHAR(255),
	annee_publication DATE,
	genre VARCHAR(255),
	exemplaires_disponibles INT
);