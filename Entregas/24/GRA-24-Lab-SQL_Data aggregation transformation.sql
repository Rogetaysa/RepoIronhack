-- Inicio
USE sakila;
-- Show tables
SHOW TABLES;

-- Challenge 1:
-- 1.1 Determine the shortest and longest movie durations and name the values as max_duration and min_duration.
SELECT 
    MIN(length) AS min_duration,
    MAX(length) AS max_duration
FROM film;

-- 1.2. Express the average movie duration in hours and minutes. Don't use decimals.
SELECT 
    FLOOR(AVG(length) / 60) AS avg_hours,
    FLOOR(AVG(length) % 60) AS avg_minutes
FROM film;

-- 2.1 Calculate the number of days that the company has been operating.
SELECT 
    DATEDIFF(MAX(rental_date), MIN(rental_date)) AS days_of_operation
FROM rental;

-- 2.2 Retrieve rental information and add two additional columns to show the month and weekday of the rental. Return 20 rows of results.
SELECT 
    rental_id, rental_date,
    DATE_FORMAT(rental_date, '%M') AS rental_month,
    DATE_FORMAT(rental_date, '%W') AS rental_weekday
FROM rental
LIMIT 20;

-- 2.3 Bonus: Retrieve rental information and add an additional column called DAY_TYPE with values 'weekend' or 'workday', depending on the day of the week.
SELECT 
    rental_id, rental_date,
    CASE 
        WHEN DAYOFWEEK(rental_date) IN (1, 7) THEN 'weekend'
        ELSE 'workday'
    END AS day_type
FROM rental
LIMIT 20;

-- 3. You need to ensure that customers can easily access information about the movie collection. To achieve this, retrieve the film titles and their rental duration. If any rental duration value is NULL, replace it with the string 'Not Available'. Sort the results of the film title in ascending order.
SELECT 
    title,
    IFNULL(rental_duration, 'Not Available') AS rental_duration
FROM film
ORDER BY title ASC;

-- 4. Bonus
SELECT 
    CONCAT(first_name, ' ', last_name) AS full_name,
    LEFT(email, 3) AS email_prefix
FROM customer
ORDER BY last_name ASC;


-- Challenge 2:

-- 1.1 The total number of films that have been released.
SELECT 
    COUNT(*) AS total_films
FROM film;

-- 1.2 The number of films for each rating.
SELECT 
    rating,
    COUNT(*) AS number_of_films
FROM film
GROUP BY rating;

-- 1.3 The number of films for each rating, sorting 
SELECT 
    rating,
    COUNT(*) AS number_of_films
FROM film
GROUP BY rating
ORDER BY number_of_films DESC;

-- 2.1 The mean film duration for each rating
SELECT 
    rating,
    ROUND(AVG(length), 2) AS avg_duration
FROM film
GROUP BY rating
ORDER BY avg_duration DESC;

-- 2.2 Identify which ratings have a mean duration of over two hours
SELECT 
    rating
FROM film
GROUP BY rating
HAVING AVG(length) > 120;

-- 3. Bonus: determine which last names are not repeated in the table actor.
SELECT 
    last_name
FROM actor
GROUP BY last_name
HAVING COUNT(*) = 1;
