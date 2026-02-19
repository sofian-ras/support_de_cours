
-- ----------------------------------------------------------
-- NOUVELLES CATEGORIES (EN PLUS DES EXISTANTES)
-- ----------------------------------------------------------
INSERT INTO categories (name, description) VALUES
  ('Informatique',       'Ordinateurs, écrans et périphériques'),
  ('Jardin & Extérieur', 'Mobilier de jardin, outils et plein air');


-- ----------------------------------------------------------
-- NOUVEAUX PRODUITS (EN PLUS DES EXISTANTS)
-- ----------------------------------------------------------
INSERT INTO products (name, price, stock, category_id) VALUES
  ('Laptop Ultra 14"',              999.00,  20,
     (SELECT category_id FROM categories WHERE name = 'Informatique')),
  ('Écran 27" IPS 144Hz',           299.00,  35,
     (SELECT category_id FROM categories WHERE name = 'Informatique')),
  ('Clavier Mécanique RedSwitch',    89.00,  60,
     (SELECT category_id FROM categories WHERE name = 'Informatique')),
  ('Tondeuse Électrique GreenCut',  199.00,  15,
     (SELECT category_id FROM categories WHERE name = 'Jardin & Extérieur')),
  ('Salon de jardin 4 places',      449.00,  10,
     (SELECT category_id FROM categories WHERE name = 'Jardin & Extérieur')),
  ('Guirlande LED Extérieure 10m',   24.90, 120,
     (SELECT category_id FROM categories WHERE name = 'Jardin & Extérieur'));


-- ----------------------------------------------------------
-- NOUVEAUX CLIENTS
-- ----------------------------------------------------------
INSERT INTO customers (firstname, lastname, email, created_at) VALUES
  ('Laura',   'Carpentier',  'laura.carpentier@mail.com',  '2024-02-01 09:00'),
  ('Nicolas', 'Gilbert',     'nicolas.gilbert@mail.com',   '2024-02-10 16:30'),
  ('Olivier', 'Masson',      'olivier.masson@mail.com',    '2024-02-15 11:45'),
  ('Pauline', 'Chevalier',   'pauline.chevalier@mail.com', '2024-02-20 14:10'),
  ('Quentin', 'Lambert',     'quentin.lambert@mail.com',   '2024-02-25 18:20'),
  ('Raphaël', 'Fernandez',   'raphael.fernandez@mail.com', '2024-03-05 10:05'),
  ('Sophie',  'Renaud',      'sophie.renaud@mail.com',     '2024-03-06 13:30'),
  ('Thomas',  'Legrand',     'thomas.legrand@mail.com',    '2024-03-07 17:15'),
  ('Ursula',  'Perrot',      'ursula.perrot@mail.com',     '2024-03-09 19:40'),
  ('Victor',  'Lemoine',     'victor.lemoine@mail.com',    '2024-03-12 08:50');


-- ----------------------------------------------------------
-- NOUVELLES COMMANDES
-- (on évite de réutiliser les mêmes couples email + date)
-- ----------------------------------------------------------
INSERT INTO orders (customer_id, order_date, status) VALUES
  ((SELECT customer_id FROM customers WHERE email = 'alice.martin@mail.com'),
    '2024-03-22 10:15', 'PAID'),
  ((SELECT customer_id FROM customers WHERE email = 'alice.martin@mail.com'),
    '2024-03-25 16:45', 'SHIPPED'),

  ((SELECT customer_id FROM customers WHERE email = 'bob.dupont@mail.com'),
    '2024-03-26 09:05', 'PAID'),

  ((SELECT customer_id FROM customers WHERE email = 'chloe.bernard@mail.com'),
    '2024-03-27 14:30', 'PAID'),

  ((SELECT customer_id FROM customers WHERE email = 'emma.leroy@mail.com'),
    '2024-03-28 11:20', 'CANCELLED'),

  ((SELECT customer_id FROM customers WHERE email = 'felix.petit@mail.com'),
    '2024-03-29 15:40', 'PAID'),

  ((SELECT customer_id FROM customers WHERE email = 'hugo.roussel@mail.com'),
    '2024-03-30 18:10', 'PAID'),

  ((SELECT customer_id FROM customers WHERE email = 'laura.carpentier@mail.com'),
    '2024-03-21 09:30', 'PAID'),
  ((SELECT customer_id FROM customers WHERE email = 'nicolas.gilbert@mail.com'),
    '2024-03-21 19:45', 'SHIPPED'),
  ((SELECT customer_id FROM customers WHERE email = 'olivier.masson@mail.com'),
    '2024-03-22 13:00', 'PAID'),
  ((SELECT customer_id FROM customers WHERE email = 'pauline.chevalier@mail.com'),
    '2024-03-23 16:10', 'PAID'),
  ((SELECT customer_id FROM customers WHERE email = 'quentin.lambert@mail.com'),
    '2024-03-24 11:55', 'PENDING'),
  ((SELECT customer_id FROM customers WHERE email = 'raphael.fernandez@mail.com'),
    '2024-03-25 08:40', 'PAID'),
  ((SELECT customer_id FROM customers WHERE email = 'sophie.renaud@mail.com'),
    '2024-03-26 14:05', 'PAID'),
  ((SELECT customer_id FROM customers WHERE email = 'thomas.legrand@mail.com'),
    '2024-03-27 17:50', 'SHIPPED'),
  ((SELECT customer_id FROM customers WHERE email = 'ursula.perrot@mail.com'),
    '2024-03-28 20:10', 'PAID'),
  ((SELECT customer_id FROM customers WHERE email = 'victor.lemoine@mail.com'),
    '2024-03-29 09:25', 'PAID');


-- ----------------------------------------------------------
-- NOUVELLES LIGNES DE COMMANDE
-- On mélange anciens et nouveaux produits pour changer les stats
-- ----------------------------------------------------------

-- Alice : commande du 22/03, beaucoup d'informatique
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'alice.martin@mail.com'
       AND o.order_date = '2024-03-22 10:15'),
    (SELECT product_id FROM products WHERE name = 'Laptop Ultra 14"'),
    1,
    999.00
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'alice.martin@mail.com'
       AND o.order_date = '2024-03-22 10:15'),
    (SELECT product_id FROM products WHERE name = 'Clavier Mécanique RedSwitch'),
    1,
    89.00
  );

-- Alice : commande du 25/03, produits de beauté & jouets
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'alice.martin@mail.com'
       AND o.order_date = '2024-03-25 16:45'),
    (SELECT product_id FROM products WHERE name = 'Crème hydratante BioSkin'),
    3,
    15.90
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'alice.martin@mail.com'
       AND o.order_date = '2024-03-25 16:45'),
    (SELECT product_id FROM products WHERE name = 'Jeu de société "Galaxy Quest"'),
    2,
    29.90
  );

-- Bob : commande du 26/03, écran et souris gamer
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'bob.dupont@mail.com'
       AND o.order_date = '2024-03-26 09:05'),
    (SELECT product_id FROM products WHERE name = 'Écran 27" IPS 144Hz'),
    1,
    299.00
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'bob.dupont@mail.com'
       AND o.order_date = '2024-03-26 09:05'),
    (SELECT product_id FROM products WHERE name = 'Souris Gamer Pro RGB'),
    2,
    49.90
  );

-- Chloé : commande du 27/03, maison & beauté
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'chloe.bernard@mail.com'
       AND o.order_date = '2024-03-27 14:30'),
    (SELECT product_id FROM products WHERE name = 'Aspirateur Cyclonix 3000'),
    1,
    129.00
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'chloe.bernard@mail.com'
       AND o.order_date = '2024-03-27 14:30'),
    (SELECT product_id FROM products WHERE name = 'Crème hydratante BioSkin'),
    4,
    15.90
  );

-- Félix : commande du 29/03, beaucoup de tapis de yoga
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'felix.petit@mail.com'
       AND o.order_date = '2024-03-29 15:40'),
    (SELECT product_id FROM products WHERE name = 'Tapis de Yoga Comfort+'),
    5,
    19.99
  );

-- Hugo : commande du 30/03, jardin & extérieur
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'hugo.roussel@mail.com'
       AND o.order_date = '2024-03-30 18:10'),
    (SELECT product_id FROM products WHERE name = 'Tondeuse Électrique GreenCut'),
    1,
    199.00
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'hugo.roussel@mail.com'
       AND o.order_date = '2024-03-30 18:10'),
    (SELECT product_id FROM products WHERE name = 'Guirlande LED Extérieure 10m'),
    4,
    24.90
  );

-- Laura : laptop + tapis de yoga
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'laura.carpentier@mail.com'
       AND o.order_date = '2024-03-21 09:30'),
    (SELECT product_id FROM products WHERE name = 'Laptop Ultra 14"'),
    1,
    999.00
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'laura.carpentier@mail.com'
       AND o.order_date = '2024-03-21 09:30'),
    (SELECT product_id FROM products WHERE name = 'Tapis de Yoga Comfort+'),
    2,
    19.99
  );

-- Nicolas : salon de jardin
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'nicolas.gilbert@mail.com'
       AND o.order_date = '2024-03-21 19:45'),
    (SELECT product_id FROM products WHERE name = 'Salon de jardin 4 places'),
    1,
    449.00
  );

-- Olivier : écran + clavier
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'olivier.masson@mail.com'
       AND o.order_date = '2024-03-22 13:00'),
    (SELECT product_id FROM products WHERE name = 'Écran 27" IPS 144Hz'),
    2,
    299.00
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'olivier.masson@mail.com'
       AND o.order_date = '2024-03-22 13:00'),
    (SELECT product_id FROM products WHERE name = 'Clavier Mécanique RedSwitch'),
    1,
    89.00
  );

-- Pauline : jouets et jeux
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'pauline.chevalier@mail.com'
       AND o.order_date = '2024-03-23 16:10'),
    (SELECT product_id FROM products WHERE name = 'Jeu de société "Galaxy Quest"'),
    3,
    29.90
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'pauline.chevalier@mail.com'
       AND o.order_date = '2024-03-23 16:10'),
    (SELECT product_id FROM products WHERE name = 'Puzzle 1000 pièces "Montagne"'),
    4,
    12.99
  );

-- Quentin : commande PENDING, non prise en compte dans le CA (selon ta logique métier)
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'quentin.lambert@mail.com'
       AND o.order_date = '2024-03-24 11:55'),
    (SELECT product_id FROM products WHERE name = 'Casque Bluetooth X1000'),
    1,
    79.99
  );

-- Raphaël : sport & beauté
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'raphael.fernandez@mail.com'
       AND o.order_date = '2024-03-25 08:40'),
    (SELECT product_id FROM products WHERE name = 'Haltères 5kg (paire)'),
    2,
    24.99
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'raphael.fernandez@mail.com'
       AND o.order_date = '2024-03-25 08:40'),
    (SELECT product_id FROM products WHERE name = 'Crème hydratante BioSkin'),
    2,
    15.90
  );

-- Sophie : beaucoup de "Gel douche FreshEnergy" pour faire monter cette ligne
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'sophie.renaud@mail.com'
       AND o.order_date = '2024-03-26 14:05'),
    (SELECT product_id FROM products WHERE name = 'Gel douche FreshEnergy'),
    10,
    4.99
  );

-- Thomas : électronique et informatique
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'thomas.legrand@mail.com'
       AND o.order_date = '2024-03-27 17:50'),
    (SELECT product_id FROM products WHERE name = 'Casque Bluetooth X1000'),
    2,
    79.99
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'thomas.legrand@mail.com'
       AND o.order_date = '2024-03-27 17:50'),
    (SELECT product_id FROM products WHERE name = 'Souris Gamer Pro RGB'),
    3,
    49.90
  );

-- Ursula : jardin & maison
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'ursula.perrot@mail.com'
       AND o.order_date = '2024-03-28 20:10'),
    (SELECT product_id FROM products WHERE name = 'Guirlande LED Extérieure 10m'),
    6,
    24.90
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'ursula.perrot@mail.com'
       AND o.order_date = '2024-03-28 20:10'),
    (SELECT product_id FROM products WHERE name = 'Bouilloire Inox 1.7L'),
    1,
    29.99
  );

-- Victor : mix maison, sport et beauté
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'victor.lemoine@mail.com'
       AND o.order_date = '2024-03-29 09:25'),
    (SELECT product_id FROM products WHERE name = 'Aspirateur Cyclonix 3000'),
    1,
    129.00
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'victor.lemoine@mail.com'
       AND o.order_date = '2024-03-29 09:25'),
    (SELECT product_id FROM products WHERE name = 'Tapis de Yoga Comfort+'),
    3,
    19.99
  ),
  (
    (SELECT o.order_id
     FROM orders o
     JOIN customers c ON c.customer_id = o.customer_id
     WHERE c.email = 'victor.lemoine@mail.com'
       AND o.order_date = '2024-03-29 09:25'),
    (SELECT product_id FROM products WHERE name = 'Crème hydratante BioSkin'),
    1,
    15.90
  );
