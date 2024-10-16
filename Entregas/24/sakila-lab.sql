
-- Inicio
USE sakila;
-- 1. Show tables
SHOW TABLES;
-- 2. Recuperar taules
SELECT * FROM actor;
SELECT * FROM film;
SELECT * FROM customer;

-- 3.1 titols
SELECT title FROM film;
-- 3.2 Idiomas
SELECT name AS language FROM language;
-- 3.3 empleados
SELECT first_name FROM staff;

-- 4. Años
SELECT DISTINCT release_year FROM film;

-- 5.1 numero de tiendas
SELECT COUNT(*) AS store_count FROM store;
-- 5.2 numero de empleados
SELECT COUNT(*) AS employee_count FROM staff;

-- 5.3 para alquilar y alquiladas
SELECT 
    (SELECT COUNT(*) FROM inventory) AS films_available,
    (SELECT COUNT(*) FROM rental) AS films_rented;

-- 5.3 para alquilar
SELECT COUNT(*) AS films_available FROM inventory;

-- 5.3 alquiladas
SELECT COUNT(*) AS films_rented FROM rental;

-- 5.4 apellidos distintos de actores
SELECT COUNT(DISTINCT last_name) AS distinct_actor_last_names FROM actor;

-- 6. 10 peliculas más largas
SELECT title, length 
FROM film 
ORDER BY length DESC 
LIMIT 10;

-- 7.1 actores con nombre scarlett
SELECT * 
FROM actor 
WHERE first_name = 'SCARLETT';


-- BONUS
-- 7.2 Armageddon y +100 minuts
SELECT * 
FROM film 
WHERE title LIKE '%ARMAGEDDON%' 
AND length > 100;

-- 7.3 Behind the scenes
SELECT COUNT(*) AS films_with_behind_scenes 
FROM film 
WHERE special_features LIKE '%Behind the Scenes%';

