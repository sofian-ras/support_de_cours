CREATE SCHEMA IF NOT EXISTS exercice3;

CREATE TABLE exercice3.clients (
	id_clients INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	nom VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE exercice3.commandes (
	id_commandes INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	date_commande DATE NOT NULL,
	montant NUMERIC(10,2) NOT NULL CHECK (montant > 0),
	id_client INT NOT NULL,
	CONSTRAINT fk_id_client FOREIGN KEY (id_client) REFERENCES exercice3.clients(id_clients)
);

