CREATE SCHEMA IF NOT EXISTS exercice6;

SET search_path TO 'exercice6', '$user', 'public'; 

-- SELECT FROM
-- Question1
SELECT * 
FROM users;

-- Question2
SELECT first_name, last_name, job 
FROM users;

-- SELECT WHERE
-- Question1
SELECT * 
FROM users 
WHERE job <> 'Developer';

-- Question2
SELECT * 
FROM users 
WHERE first_name = 'John';

-- Question3
SELECT * 
FROM users 
WHERE salary >= 3000;

-- SELECT OR AND
-- Question1
SELECT * 
FROM users 
WHERE age < 30 OR age >= 35;

-- Question2
SELECT * 
FROM users 
WHERE job = 'Teacher' AND salary > 2600;

-- SELECT NOT
SELECT * 
FROM users
WHERE "location" = 'New York'
AND salary BETWEEN 3000 AND 3500
AND job NOT IN ('Doctor', 'Lawyer');

-- SELECT BETWEEN IN
-- Question1
SELECT * 
FROM users 
WHERE job = 'Engineer';

-- Question2
SELECT first_name, last_name, "location"
FROM users 
WHERE "location" IN ('London', 'Paris', 'Berlin');

-- Question3
SELECT * 
FROM users 
WHERE age BETWEEN 25 AND 35;

-- Question4
SELECT * 
FROM users 
WHERE job = 'Developer' AND salary > 2500;

-- SELECT LIKE
-- Question1
SELECT * 
FROM users 
WHERE first_name ILIKE 'd%';

-- Question2
SELECT * 
FROM users 
WHERE last_name ILIKE '%son';

-- Question3
SELECT * 
FROM users 
WHERE first_name LIKE '_____';

-- Question4
SELECT * 
FROM users 
WHERE job ILIKE '%doctor%';

-- SELECT ORDER BY, LIMIT, OFFSET
-- Question1
SELECT * 
FROM users 
ORDER BY age DESC 
LIMIT 5;

-- Question2
SELECT * 
FROM users 
ORDER BY first_name 
OFFSET 5 
LIMIT 5;

-- Question3
SELECT * 
FROM users 
ORDER BY salary DESC 
LIMIT 3;

-- SELECT aggregation
-- Question1
SELECT MIN(salary) AS min_salary 
FROM users;

-- Question2
SELECT MAX(age) AS max_age 
FROM users
WHERE job = 'Engineer';

-- Question3
SELECT ROUND(AVG(salary)) AS avg_salary 
FROM users 
WHERE job = 'Teacher';

-- Question4
SELECT SUM(salary) AS sum_salary 
FROM users;

-- SELECT GROUP BY et HAVING
-- Question1
SELECT "location", COUNT(*) AS number_users 
FROM users 
GROUP BY "location" 
HAVING COUNT(*) > 1;

-- Question2
SELECT job, ROUND(AVG(salary)) AS avg_salary 
FROM users 
GROUP BY job 
HAVING ROUND(AVG(salary)) > 2500;

-- Question3
SELECT "location", SUM(salary) AS sum_salary 
FROM users 
GROUP BY "location" 
HAVING SUM(salary) > 5000;

-- Question4
SELECT birth_date, COUNT(*) AS number_users 
FROM users 
GROUP BY birth_date 
HAVING COUNT(*) > 1;

-- Question5
SELECT job, "location", MAX(salary) AS max_salary 
FROM users 
GROUP BY job, "location"
HAVING MAX(salary) > 3000;