-- ==========================================================
-- PARTIE 3 – REQUÊTES DE BASE
-- ==========================================================

-- 3.1 Lister tous les clients triés par date de création de compte (plus anciens → plus récents)
SELECT
    customer_id,
    firstname,
    lastname,
    email,
    created_at
FROM customers
ORDER BY created_at ASC;

-- 3.2 Lister tous les produits (nom + prix) triés par prix décroissant
SELECT
    product_id,
    name,
    price
FROM products
ORDER BY price DESC;

-- 3.3 Lister les commandes passées entre deux dates (ex : 1er au 15 mars 2024)
SELECT
    order_id,
    customer_id,
    order_date,
    status
FROM orders
WHERE order_date BETWEEN '2024-03-01' AND '2024-03-15 23:59:59'
ORDER BY order_date;

-- 3.4 Lister les produits dont le prix est strictement supérieur à 50 €
SELECT
    product_id,
    name,
    price
FROM products
WHERE price > 50
ORDER BY price DESC;

-- 3.5 Lister tous les produits d’une catégorie donnée (ex : "Électronique")
SELECT
    p.product_id,
    p.name,
    p.price,
    c.name AS category_name
FROM products p
JOIN categories c ON c.category_id = p.category_id
WHERE c.name = 'Électronique'
ORDER BY p.name;

-- ==========================================================
-- PARTIE 4 – JOINTURES SIMPLES
-- ==========================================================

-- 4.1 Lister tous les produits avec le nom de leur catégorie
SELECT
    p.product_id,
    p.name AS product_name,
    p.price,
    c.name AS category_name
FROM products p
JOIN categories c ON c.category_id = p.category_id
ORDER BY c.name, p.name;

-- 4.2 Lister toutes les commandes avec le nom complet du client
SELECT
    o.order_id,
    o.order_date,
    o.status,
    c.firstname,
    c.lastname
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_date;

-- 4.3 Lister toutes les lignes de commande avec nom du client, produit, quantité, prix unitaire
SELECT
    oi.item_id,
    c.firstname,
    c.lastname,
    o.order_date,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price
FROM order_items oi
JOIN orders o     ON o.order_id = oi.order_id
JOIN customers c  ON c.customer_id = o.customer_id
JOIN products p   ON p.product_id = oi.product_id
ORDER BY o.order_date, c.lastname, p.name;

-- 4.4 Lister toutes les commandes dont le statut est PAID ou SHIPPED
SELECT
    o.order_id,
    o.order_date,
    o.status,
    c.firstname,
    c.lastname
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status IN ('PAID', 'SHIPPED')
ORDER BY o.order_date;

-- ==========================================================
-- PARTIE 5 – JOINTURES AVANCÉES
-- ==========================================================

-- 5.1 Détail complet de chaque commande :
--     - date
--     - nom client
--     - produits
--     - quantités
--     - prix unitaire
--     - montant de la ligne (quantité * prix unitaire)
SELECT
    o.order_id,
    o.order_date,
    c.firstname || ' ' || c.lastname AS customer_name,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS line_total
FROM order_items oi
JOIN orders o     ON o.order_id = oi.order_id
JOIN customers c  ON c.customer_id = o.customer_id
JOIN products p   ON p.product_id = oi.product_id
ORDER BY o.order_id, p.name;

-- 5.2 Montant total de chaque commande (par client)
SELECT
    o.order_id,
    c.firstname || ' ' || c.lastname AS customer_name,
    SUM(oi.quantity * oi.unit_price) AS order_total
FROM orders o
JOIN customers c  ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id, customer_name
ORDER BY o.order_id;

-- 5.3 Commandes dont le montant total dépasse 100 €
SELECT
    o.order_id,
    c.firstname || ' ' || c.lastname AS customer_name,
    SUM(oi.quantity * oi.unit_price) AS order_total
FROM orders o
JOIN customers c  ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id, customer_name
HAVING SUM(oi.quantity * oi.unit_price) > 100
ORDER BY order_total DESC;

-- 5.4 Catégories avec chiffre d’affaires total associé
--      (on exclut les commandes CANCELLED)
SELECT
    c.name AS category_name,
    SUM(oi.quantity * oi.unit_price) AS category_revenue
FROM order_items oi
JOIN orders o     ON o.order_id = oi.order_id
JOIN products p   ON p.product_id = oi.product_id
JOIN categories c ON c.category_id = p.category_id
WHERE o.status <> 'CANCELLED'
GROUP BY c.name
ORDER BY category_revenue DESC;


-- ==========================================================
-- PARTIE 6 – SOUS-REQUÊTES
-- ==========================================================

-- 6.1 Produits vendus au moins une fois
SELECT
    p.product_id,
    p.name
FROM products p
WHERE p.product_id IN (
    SELECT DISTINCT product_id
    FROM order_items
);


-- 6.2 Produits jamais vendus
SELECT
    p.product_id,
    p.name
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.product_id
WHERE oi.product_id IS NULL;

-- 6.3 Client qui a dépensé le plus (TOP 1)
--     (on exclut les commandes CANCELLED)
SELECT
    c.customer_id,
    c.firstname,
    c.lastname,
    SUM(oi.quantity * oi.unit_price) AS total_spent
FROM customers c
JOIN orders o      ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status <> 'CANCELLED'
GROUP BY c.customer_id, c.firstname, c.lastname
ORDER BY total_spent DESC
LIMIT 1;


-- 6.4 Les 3 produits les plus vendus (en quantité)
SELECT
    p.product_id,
    p.name,
    SUM(oi.quantity) AS total_quantity
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY p.product_id, p.name
ORDER BY total_quantity DESC
LIMIT 3;

-- 6.5 Commandes dont le montant total est supérieur à la moyenne des commandes
WITH order_totals AS (
    SELECT
        o.order_id,
        SUM(oi.quantity * oi.unit_price) AS total
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.order_id
),
average_total AS (
    SELECT AVG(total) AS avg_total FROM order_totals
)
SELECT
    ot.order_id,
    ot.total
FROM order_totals ot, average_total a
WHERE ot.total > a.avg_total
ORDER BY ot.total DESC;

-- ==========================================================
-- PARTIE 7 – STATISTIQUES & AGRÉGATS
-- ==========================================================

-- 7.1 Chiffre d’affaires total (en excluant les commandes CANCELLED)
SELECT
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status <> 'CANCELLED';

-- 7.2 Panier moyen (montant moyen par commande, hors CANCELLED)
WITH order_totals AS (
    SELECT
        o.order_id,
        SUM(oi.quantity * oi.unit_price) AS total
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.status <> 'CANCELLED'
    GROUP BY o.order_id
)
SELECT
    AVG(total) AS average_order_value
FROM order_totals;


-- 7.3 Quantité totale vendue par catégorie
SELECT
    c.name AS category_name,
    SUM(oi.quantity) AS total_quantity
FROM order_items oi
JOIN orders o     ON o.order_id = oi.order_id
JOIN products p   ON p.product_id = oi.product_id
JOIN categories c ON c.category_id = p.category_id
WHERE o.status <> 'CANCELLED'
GROUP BY c.name
ORDER BY total_quantity DESC;

-- 7.4 Chiffre d’affaires par mois
--      (on tronque la date à la précision "mois")
SELECT
    date_trunc('month', o.order_date) AS month,
    SUM(oi.quantity * oi.unit_price) AS monthly_revenue
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status <> 'CANCELLED'
GROUP BY date_trunc('month', o.order_date)
ORDER BY month;


-- 7.5 Afficher les montants arrondis à deux décimales
--     (exemple : chiffre d’affaires total)
SELECT
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue_rounded
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status <> 'CANCELLED';

-- ==========================================================
-- PARTIE 8 – LOGIQUE CONDITIONNELLE (CASE)
-- ==========================================================


-- 8.1 Commandes avec statut "lisible" en français
SELECT
    o.order_id,
    o.order_date,
    c.firstname || ' ' || c.lastname AS customer_name,
    o.status,
    CASE o.status
        WHEN 'PAID'      THEN 'Payée'
        WHEN 'SHIPPED'   THEN 'Expédiée'
        WHEN 'PENDING'   THEN 'En attente'
        WHEN 'CANCELLED' THEN 'Annulée'
        ELSE 'Inconnu'
    END AS status_label
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_date;

-- 8.2 Segmentation des clients (Bronze/Argent/Or) selon le total dépensé
--     (on exclut les commandes CANCELLED)
WITH customer_totals AS (
    SELECT
        c.customer_id,
        c.firstname,
        c.lastname,
        SUM(oi.quantity * oi.unit_price) AS total_spent
    FROM customers c
    JOIN orders o      ON o.customer_id = c.customer_id
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.status <> 'CANCELLED'
    GROUP BY c.customer_id, c.firstname, c.lastname
)
SELECT
    customer_id,
    firstname,
    lastname,
    total_spent,
    CASE
        WHEN total_spent < 100 THEN 'Bronze'
        WHEN total_spent BETWEEN 100 AND 300 THEN 'Argent'
        ELSE 'Or'
    END AS segment
FROM customer_totals
ORDER BY total_spent DESC;

-- ==========================================================
-- PARTIE 9 – CHALLENGE FINAL (exemples de solutions)
-- ==========================================================

-- 9.1 Top 5 des clients les plus actifs (nombre de commandes)
SELECT
    c.customer_id,
    c.firstname,
    c.lastname,
    COUNT(o.order_id) AS orders_count
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.firstname, c.lastname
ORDER BY orders_count DESC
LIMIT 5;

-- 9.2 Top 5 des clients qui ont dépensé le plus (CA total, hors CANCELLED)
SELECT
    c.customer_id,
    c.firstname,
    c.lastname,
    SUM(oi.quantity * oi.unit_price) AS total_spent
FROM customers c
JOIN orders o      ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status <> 'CANCELLED'
GROUP BY c.customer_id, c.firstname, c.lastname
ORDER BY total_spent DESC
LIMIT 5;


-- 9.3 Les 3 catégories les plus rentables (CA total)
SELECT
    c.name AS category_name,
    SUM(oi.quantity * oi.unit_price) AS category_revenue
FROM order_items oi
JOIN orders o     ON o.order_id = oi.order_id
JOIN products p   ON p.product_id = oi.product_id
JOIN categories c ON c.category_id = p.category_id
WHERE o.status <> 'CANCELLED'
GROUP BY c.name
ORDER BY category_revenue DESC
LIMIT 3;



-- 9.4 Produits ayant généré moins de 10 € de CA au total
SELECT
    p.product_id,
    p.name,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_revenue
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.product_id
LEFT JOIN orders o       ON o.order_id = oi.order_id AND o.status <> 'CANCELLED'
GROUP BY p.product_id, p.name
HAVING COALESCE(SUM(oi.quantity * oi.unit_price), 0) < 10
ORDER BY total_revenue ASC;

-- 9.5 Clients n’ayant passé qu’une seule commande (tous statuts confondus)
SELECT
    c.customer_id,
    c.firstname,
    c.lastname,
    COUNT(o.order_id) AS orders_count
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.firstname, c.lastname
HAVING COUNT(o.order_id) = 1
ORDER BY c.lastname, c.firstname;