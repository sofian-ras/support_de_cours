-- ==========================================================
-- FICHIER : schema.sql
-- OBJET   : Création du schéma PostgreSQL pour SuperShop
-- CONTENU : Tables, clés primaires, clés étrangères, contraintes
-- ==========================================================

-- ----------------------------------------------------------
-- Nettoyage préalable (pour rejouer le script facilement)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS order_items   CASCADE;
DROP TABLE IF EXISTS orders        CASCADE;
DROP TABLE IF EXISTS products      CASCADE;
DROP TABLE IF EXISTS categories    CASCADE;
DROP TABLE IF EXISTS customers     CASCADE;

-- ----------------------------------------------------------
-- TABLE : categories
-- Modèle métier :
--  - nom de catégorie (obligatoire, unique)
--  - description (facultative)
-- ----------------------------------------------------------
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

-- ----------------------------------------------------------
-- TABLE : products
-- Modèle métier :
--  - nom (obligatoire)
--  - prix (numérique > 0)
--  - stock (entier >= 0)
--  - catégorie (clé étrangère vers categories)
-- ----------------------------------------------------------
CREATE TABLE products (
    product_id  SERIAL PRIMARY KEY,
    name        VARCHAR(150) NOT NULL,
    price       NUMERIC(10, 2) NOT NULL CHECK (price > 0),
    stock       INTEGER NOT NULL CHECK (stock >= 0),
    category_id INTEGER NOT NULL REFERENCES categories(category_id)
);

-- ----------------------------------------------------------
-- TABLE : customers
-- Modèle métier :
--  - prénom (obligatoire)
--  - nom (obligatoire)
--  - email (obligatoire, unique)
--  - date/heure de création (obligatoire)
-- ----------------------------------------------------------
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    firstname   VARCHAR(100) NOT NULL,
    lastname    VARCHAR(100) NOT NULL,
    email       VARCHAR(200) NOT NULL UNIQUE,
    created_at  TIMESTAMP NOT NULL
);

-- ----------------------------------------------------------
-- TABLE : orders
-- Modèle métier :
--  - client (FK vers customers)
--  - date/heure de commande (obligatoire)
--  - statut (PENDING, PAID, SHIPPED, CANCELLED)
-- ----------------------------------------------------------
CREATE TABLE orders (
    order_id    SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date  TIMESTAMP NOT NULL,
    status      VARCHAR(20) NOT NULL CHECK (
        status IN ('PENDING', 'PAID', 'SHIPPED', 'CANCELLED')
    )
);


-- ----------------------------------------------------------
-- TABLE : order_items
-- Modèle métier :
--  - commande (FK vers orders)
--  - produit (FK vers products)
--  - quantité (entier > 0)
--  - prix unitaire facturé (numérique > 0)
-- ----------------------------------------------------------
CREATE TABLE order_items (
    item_id     SERIAL PRIMARY KEY,
    order_id    INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id  INTEGER NOT NULL REFERENCES products(product_id),
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    unit_price  NUMERIC(10, 2) NOT NULL CHECK (unit_price > 0)
);