-- ----------------------------------------------------------
-- DONNÉES : CATEGORIES
-- Correspond au bloc "Catégories" du sujet
-- ----------------------------------------------------------
INSERT INTO categories (name, description) VALUES
  ('Électronique',       'Produits high-tech et accessoires'),
  ('Maison & Cuisine',   'Électroménager et ustensiles'),
  ('Sport & Loisirs',    'Articles de sport et plein air'),
  ('Beauté & Santé',     'Produits de beauté, hygiène, bien-être'),
  ('Jeux & Jouets',      'Jouets pour enfants et adultes');

  -- ----------------------------------------------------------
-- DONNÉES : PRODUITS
-- Correspond au bloc "Produits" du sujet
-- ----------------------------------------------------------
INSERT INTO products (name, price, stock, category_id) VALUES
  ('Casque Bluetooth X1000',         79.99,  50,
     (SELECT category_id FROM categories WHERE name = 'Électronique')),
  ('Souris Gamer Pro RGB',           49.90, 120,
     (SELECT category_id FROM categories WHERE name = 'Électronique')),
  ('Bouilloire Inox 1.7L',           29.99,  80,
     (SELECT category_id FROM categories WHERE name = 'Maison & Cuisine')),
  ('Aspirateur Cyclonix 3000',      129.00,  40,
     (SELECT category_id FROM categories WHERE name = 'Maison & Cuisine')),
  ('Tapis de Yoga Comfort+',         19.99, 150,
     (SELECT category_id FROM categories WHERE name = 'Sport & Loisirs')),
  ('Haltères 5kg (paire)',           24.99,  70,
     (SELECT category_id FROM categories WHERE name = 'Sport & Loisirs')),
  ('Crème hydratante BioSkin',       15.90, 200,
     (SELECT category_id FROM categories WHERE name = 'Beauté & Santé')),
  ('Gel douche FreshEnergy',          4.99, 300,
     (SELECT category_id FROM categories WHERE name = 'Beauté & Santé')),
  ('Puzzle 1000 pièces "Montagne"',  12.99,  95,
     (SELECT category_id FROM categories WHERE name = 'Jeux & Jouets')),
  ('Jeu de société "Galaxy Quest"',  29.90,  60,
     (SELECT category_id FROM categories WHERE name = 'Jeux & Jouets'));


-- ----------------------------------------------------------
-- DONNÉES : CLIENTS
-- Correspond au bloc "Clients" du sujet
-- ----------------------------------------------------------
INSERT INTO customers (firstname, lastname, email, created_at) VALUES
  ('Alice',  'Martin',    'alice.martin@mail.com',    '2024-01-10 14:32'),
  ('Bob',    'Dupont',    'bob.dupont@mail.com',      '2024-02-05 09:10'),
  ('Chloé',  'Bernard',   'chloe.bernard@mail.com',   '2024-03-12 17:22'),
  ('David',  'Robert',    'david.robert@mail.com',    '2024-01-29 11:45'),
  ('Emma',   'Leroy',     'emma.leroy@mail.com',      '2024-03-02 08:55'),
  ('Félix',  'Petit',     'felix.petit@mail.com',     '2024-02-18 16:40'),
  ('Hugo',   'Roussel',   'hugo.roussel@mail.com',    '2024-03-20 19:05'),
  ('Inès',   'Moreau',    'ines.moreau@mail.com',     '2024-01-17 10:15'),
  ('Julien', 'Fontaine',  'julien.fontaine@mail.com', '2024-01-23 13:55'),
  ('Katia',  'Garnier',   'katia.garnier@mail.com',   '2024-03-15 12:00');

  -- ----------------------------------------------------------
-- DONNÉES : COMMANDES
-- Correspond au bloc "Commandes" du sujet
-- On récupère le customer_id à partir de l'email
-- ----------------------------------------------------------
INSERT INTO orders (customer_id, order_date, status) VALUES
  ((SELECT customer_id FROM customers WHERE email = 'alice.martin@mail.com'),
    '2024-03-01 10:20', 'PAID'),
  ((SELECT customer_id FROM customers WHERE email = 'bob.dupont@mail.com'),
    '2024-03-04 09:12', 'SHIPPED'),
  ((SELECT customer_id FROM customers WHERE email = 'chloe.bernard@mail.com'),
    '2024-03-08 15:02', 'PAID'),
  ((SELECT customer_id FROM customers WHERE email = 'david.robert@mail.com'),
    '2024-03-09 11:45', 'CANCELLED'),
  ((SELECT customer_id FROM customers WHERE email = 'emma.leroy@mail.com'),
    '2024-03-10 08:10', 'PAID'),
  ((SELECT customer_id FROM customers WHERE email = 'felix.petit@mail.com'),
    '2024-03-11 13:50', 'PENDING'),
  ((SELECT customer_id FROM customers WHERE email = 'hugo.roussel@mail.com'),
    '2024-03-15 19:30', 'SHIPPED'),
  ((SELECT customer_id FROM customers WHERE email = 'ines.moreau@mail.com'),
    '2024-03-16 10:00', 'PAID'),
  ((SELECT customer_id FROM customers WHERE email = 'julien.fontaine@mail.com'),
    '2024-03-18 14:22', 'PAID'),
  ((SELECT customer_id FROM customers WHERE email = 'katia.garnier@mail.com'),
    '2024-03-20 18:00', 'PENDING');


-- ----------------------------------------------------------
-- DONNÉES : LIGNES DE COMMANDE (ORDER_ITEMS)
-- Correspond au bloc "Lignes de commande" du sujet
-- On récupère :
--   - order_id via (email + date commande)
--   - product_id via nom de produit
-- ----------------------------------------------------------
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'alice.martin@mail.com'
       AND o.order_date = '2024-03-01 10:20'),
    (SELECT product_id FROM products WHERE name = 'Casque Bluetooth X1000'),
    1,
    79.99
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'alice.martin@mail.com'
       AND o.order_date = '2024-03-01 10:20'),
    (SELECT product_id FROM products WHERE name = 'Puzzle 1000 pièces "Montagne"'),
    2,
    12.99
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'bob.dupont@mail.com'
       AND o.order_date = '2024-03-04 09:12'),
    (SELECT product_id FROM products WHERE name = 'Tapis de Yoga Comfort+'),
    1,
    19.99
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'chloe.bernard@mail.com'
       AND o.order_date = '2024-03-08 15:02'),
    (SELECT product_id FROM products WHERE name = 'Bouilloire Inox 1.7L'),
    1,
    29.99
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'chloe.bernard@mail.com'
       AND o.order_date = '2024-03-08 15:02'),
    (SELECT product_id FROM products WHERE name = 'Gel douche FreshEnergy'),
    3,
    4.99
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'david.robert@mail.com'
       AND o.order_date = '2024-03-09 11:45'),
    (SELECT product_id FROM products WHERE name = 'Haltères 5kg (paire)'),
    1,
    24.99
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'emma.leroy@mail.com'
       AND o.order_date = '2024-03-10 08:10'),
    (SELECT product_id FROM products WHERE name = 'Crème hydratante BioSkin'),
    2,
    15.90
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'julien.fontaine@mail.com'
       AND o.order_date = '2024-03-18 14:22'),
    (SELECT product_id FROM products WHERE name = 'Jeu de société "Galaxy Quest"'),
    1,
    29.90
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'katia.garnier@mail.com'
       AND o.order_date = '2024-03-20 18:00'),
    (SELECT product_id FROM products WHERE name = 'Souris Gamer Pro RGB'),
    1,
    49.90
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'katia.garnier@mail.com'
       AND o.order_date = '2024-03-20 18:00'),
    (SELECT product_id FROM products WHERE name = 'Gel douche FreshEnergy'),
    2,
    4.99
  );