-- a) INNER JOIN -- 
SELECT c.nom, c.prenom, a.produit, a.montant
FROM exercice7.achats AS a
INNER JOIN exercice7.clients AS c ON a.client_id = c.id;  

-- b) LEFT JOIN -- 
SELECT c.nom, c.prenom, a.produit, a.montant
FROM exercice7.achats AS a
LEFT JOIN exercice7.clients AS c ON a.client_id = c.id;  

-- c) RIGHT JOIN -- 
SELECT c.nom, c.prenom, a.produit, a.montant
FROM exercice7.achats a
RIGHT JOIN exercice7.clients AS c ON a.client_id = c.id;  

-- d) FULL JOIN -- 
SELECT c.nom, c.prenom, a.produit, a.montant
FROM exercice7.achats AS a
FULL JOIN exercice7.clients AS c ON a.client_id = c.id;  

-- Bonus, uniquement les clients sans achats -- 
SELECT c.nom, c.prenom, a.produit, a.montant
FROM exercice7.achats AS a
RIGHT JOIN exercice7.clients AS c ON a.client_id = c.id
WHERE a.client_id IS NULL; 

-- Bonus, uniquement les achats sans clients -- 
SELECT c.nom, c.prenom, a.produit, a.montant
FROM exercice7.achats AS a
LEFT JOIN exercice7.clients AS c ON a.client_id = c.id
WHERE c.id IS NULL;