CREATE SCHEMA IF NOT EXISTS exercice4;

CREATE TABLE exercice4.utilisateurs (
	id_utilisateurs INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nom VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	date_inscription DATE DEFAULT NOW(),
	pays VARCHAR(255)
);

CREATE TABLE exercice4.chansons (
	id_chansons INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	titre VARCHAR(255) NOT NULL,
	nom_artiste VARCHAR(255) NOT NULL,
	nom_album VARCHAR(255) NOT NULL,
	duree TIME,
	genre VARCHAR(255), 
	annee_sortie DATE CHECK (annee_sortie < NOW())
);

CREATE TABLE exercice4.playlist (
	id_playlist INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nom VARCHAR(255) NOT NULL,
	id_utilisateurs INT NOT NULL,
	id_chansons INT NOT NULL,
	CONSTRAINT kf_id_utilisateurs FOREIGN KEY (id_utilisateurs) REFERENCES exercice4.utilisateurs(id_utilisateurs),
	CONSTRAINT kf_id_chansons FOREIGN KEY (id_chansons) REFERENCES exercice4.chansons(id_chansons)
)