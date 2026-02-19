CREATE SCHEMA IF NOT EXISTS exercice2;

CREATE TABLE exercice2.utilisateurs (
	id_utilisateurs INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nom VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	age INT CONSTRAINT chk_age CHECK (age >= 18),
	pays VARCHAR(255) DEFAULT 'France'
);

ALTER TABLE exercice2.utilisateurs
	RENAME TO users; 

ALTER TABLE exercice2.users
	ADD COLUMN prenom VARCHAR(255);

ALTER TABLE exercice2.users
	DROP CONSTRAINT chk_age;

ALTER TABLE exercice2.users
	ALTER COLUMN nom TYPE VARCHAR(200);