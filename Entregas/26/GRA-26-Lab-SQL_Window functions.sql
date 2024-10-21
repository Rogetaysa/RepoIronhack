-- Write SQL queries to perform the following tasks using the Sakila database:
-- Inicio
USE sakila;

-- Challenge 1:
-- 1. Rank films by their length and create an output table that includes the title, length, and rank columns only. Filter out any rows with null or zero values in the length column.
SELECT title, length,
	RANK() OVER (ORDER BY length DESC) AS 'rank'
FROM film
WHERE length IS NOT NULL AND length > 0;

-- 2. Rank films by length within the rating category and create an output table that includes the title, length, rating and rank columns only. Filter out any rows with null or zero values in the length column.
SELECT title, length, rating,
	RANK() OVER (PARTITION BY rating ORDER BY length DESC) AS 'rank'
FROM film
WHERE length IS NOT NULL AND length > 0;

-- 3. Produce a list that shows for each film in the Sakila database, the actor or actress who has acted in the greatest number of films, as well as the total number of films in which they have acted. Hint: Use temporary tables, CTEs, or Views when appropiate to simplify your queries.
WITH actor_film_count AS(
select actor_id, COUNT(film_id) AS total_films
FROM film_actor
GROUP BY actor_id
)
SELECT f.title, a.first_name, a.last_name, afc.total_films
FROM film f
JOIN film_actor fa ON f.film_id = fa.film_id
JOIN actor a ON fa.actor_id = a.actor_id
JOIN actor_film_count afc ON a.actor_id = afc.actor_id
ORDER BY afc.total_films DESC;

-- Challenge 2:
-- Step 1. Retrieve the number of monthly active customers, i.e., the number of unique customers who rented a movie in each month.
SELECT DATE_FORMAT(rental_date, '%Y-%m') AS month,
	COUNT(DISTINCT customer_id) AS active_customers
FROM rental
GROUP BY DATE_FORMAT(rental_date, '%Y-%m');
    
-- Step 2. Retrieve the number of active users in the previous month.
WITH monthly_activity AS (
	SELECT DATE_FORMAT(rental_date, '%Y-%m') AS month,
		COUNT(DISTINCT customer_id) AS active_customers
	FROM rental
    GROUP BY DATE_FORMAT(rental_date, '%Y-%m')
)
SELECT month,
	active_customers,
    LAG(active_customers, 1) OVER (ORDER BY month) AS previous_month_customers
FROM monthly_activity;
-- Este falla por que en 2006-02 debería dar 0, no el número de 2005-08

-- Step 3. Calculate the percentage change in the number of active customers between the current and previous month.
WITH monthly_activity AS (
    SELECT DATE_FORMAT(rental_date, '%Y-%m') AS month,
           COUNT(DISTINCT customer_id) AS active_customers
    FROM rental
    GROUP BY DATE_FORMAT(rental_date, '%Y-%m')
)
SELECT month,
       active_customers,
       LAG(active_customers, 1) OVER (ORDER BY month) AS previous_month_customers,
       ROUND(
           (active_customers - LAG(active_customers, 1) OVER (ORDER BY month)) * 100.0 /
           LAG(active_customers, 1) OVER (ORDER BY month), 2
       ) AS percentage_change
FROM monthly_activity;

-- Step 4. Calculate the number of retained customers every month, i.e., customers who rented movies in the current and previous months.
WITH customer_activity AS (
    SELECT customer_id, DATE_FORMAT(rental_date, '%Y-%m') AS month
    FROM rental
    GROUP BY customer_id, month
),
retained_customers AS (
    SELECT curr.month AS current_month, COUNT(DISTINCT curr.customer_id) AS retained_customers
    FROM customer_activity curr
    JOIN customer_activity prev
    ON curr.customer_id = prev.customer_id
    AND DATE_FORMAT(DATE_SUB(STR_TO_DATE(curr.month, '%Y-%m-01'), INTERVAL 1 MONTH), '%Y-%m') = prev.month
    GROUP BY curr.month
)
SELECT current_month, retained_customers
FROM retained_customers;

