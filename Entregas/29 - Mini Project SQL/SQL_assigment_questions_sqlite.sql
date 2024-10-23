-- LEVEL 1
USE sql_test;
-- Question 1: Number of users with sessions
SELECT COUNT(DISTINCT user_id) AS number_of_users
FROM sessions;

-- Question 2: Number of chargers used by user with id 1
SELECT COUNT(DISTINCT charger_id) AS number_of_chargers
FROM sessions
WHERE user_id = 1;



-- LEVEL 2

-- Question 3: Number of sessions per charger type (AC/DC):
SELECT c.type, COUNT(s.id) AS number_of_sessions
FROM sessions s
JOIN chargers c ON s.charger_id = c.id
GROUP BY c.type;

-- Question 4: Chargers being used by more than one user
SELECT charger_id, COUNT(DISTINCT user_id)
FROM sessions
GROUP BY charger_id
HAVING COUNT(DISTINCT user_id) >1
ORDER BY COUNT(DISTINCT user_id) DESC;

-- Question 5: Average session time per charger
SELECT charger_id, start_time, end_time, (julianday(end_time) - julianday(start_time))*24
FROM sessions;

SELECT charger_id, ROUND(AVG(julianday(end_time) - julianday(start_time))*24,2) AS AVG_Charging_Time
FROM sessions
GROUP BY charger_id
ORDER BY AVG_Charging_Time DESC;


-- LEVEL 3

-- Question 6: Full username of users that have used more than one charger in one day (NOTE: for date only consider start_time)
-- Version 1:
SELECT COUNT(DISTINCT s.charger_id) AS total_count_chargers, u.name || ' ' || u.surname AS full_name
FROM users u
JOIN sessions s ON u.id = s.user_id
GROUP BY DATE(s.start_time)
HAVING COUNT(DISTINCT s.charger_id) >1;

-- Version 2:
SELECT COUNT(DISTINCT s.charger_id) AS total_count_chargers, u.name, u.surname
FROM users u
JOIN sessions s ON u.id = s.user_id
GROUP BY DATE(s.start_time)
HAVING COUNT(DISTINCT s.charger_id) >1;

-- Version 3 Gabi:
WITH MultiChargerDays AS (
    SELECT u.id, u.name || ' ' || u.surname AS full_name,
        DATE(s.start_time) AS session_date,
        COUNT(DISTINCT s.charger_id) AS charger_count
    FROM users u
    JOIN sessions s ON u.id = s.user_id
    GROUP BY u.id, session_date
    HAVING charger_count >1
    )
SELECT full_name, COUNT(session_date) AS days_with_multiple_chargers
FROM MultiChargerDays
GROUP BY full_name
ORDER BY days_with_multiple_chargers DESC;

-- Version Flor:
SELECT DISTINCT u.name || ' ' || u.surname AS full_name
FROM users u
JOIN sessions s ON u.id = s.user_id
GROUP BY DATE(s.start_time), u.id
HAVING COUNT(DISTINCT s.charger_id) > 1;



-- Question 7: Top 3 chargers with longer sessions
SELECT charger_id, ROUND(MAX(julianday(end_time) - julianday(start_time))*24, 2) AS longest_session_hours,  start_time, end_time
FROM sessions
GROUP BY charger_id
ORDER BY longest_session_hours DESC
LIMIT 3;

SELECT charger_id, ROUND((julianday(end_time) - julianday(start_time))*24, 2) AS longest_session_hours
FROM sessions
-- GROUP BY charger_id
ORDER BY longest_session_hours DESC
LIMIT 3;

-- FLOR V1:
SELECT charger_id, ROUND(MAX((julianday(end_time) - julianday(start_time)) * 24), 2) AS max_session_duration_hours
FROM sessions
GROUP BY charger_id
ORDER BY max_session_duration_hours DESC
LIMIT 3;

-- Question 8: Average number of users per charger (per charger in general, not per charger_id specifically)
SELECT AVG(user_count) AS avg_user_per_charger
FROM (
    SELECT charger_id, COUNT(DISTINCT user_id) AS user_count
    FROM sessions
    GROUP BY charger_id
);

-- Question 9: Top 3 users with more chargers being used
SELECT user_id, COUNT(DISTINCT charger_id) AS chargers_used
FROM Sessions
GROUP BY user_id
ORDER BY chargers_used DESC
LIMIT 3;



-- LEVEL 4
-- Question 10: Number of users that have used only AC chargers, DC chargers or both
WITH UserChargerTypes AS (
    SELECT user_id,
            COUNT(DISTINCT CASE WHEN
                c.type = 'AC'
                THEN 1
                END)
                AS ac_count,
            COUNT(DISTINCT CASE WHEN
                c.type = 'DC'
                THEN 1
                END)
                AS dc_count
    FROM sessions s
    JOIN chargers c ON s.charger_id = c.id
    GROUP BY user_id
)
SELECT
    SUM(CASE WHEN
        ac_count > 0 AND dc_count = 0
        THEN 1
        ELSE 0
        END)
        AS only_ac,
    SUM(CASE WHEN
        dc_count > 0 AND ac_count = 0
        THEN 1
        ELSE 0
        END)
        AS only_dc,
    SUM(CASE WHEN
        ac_count > 0 AND dc_count > 0
        THEN 1
        ELSE 0
        END)
        AS both
FROM UserChargerTypes;

-- Question 11: Monthly average number of users per charger
-- Correcta:
SELECT strftime('%Y-%m', s.start_time) AS month,
    s.charger_id,
    -- COUNT(DISTINCT s.user_id) AS num_users,
    AVG(COUNT(DISTINCT s.user_id)) OVER (PARTITION BY s. charger_id) AS avg_users_per_month
FROM sessions s
GROUP BY month, s.charger_id;
    
-- Test
SELECT strftime('%Y-%m', s.start_time) AS month,
    AVG(user_count) AS avg_users_per_charger
FROM (
    SELECT s.charger_id,
        strftime('%Y-%m', s.start_time) AS month,
        COUNT(DISTINCT s.user_id) AS user_count
    FROM sessions s
    GROUP BY charger_id, month
)
GROUP BY month;

-- test 2:
WITH UserCountPerMonth AS (
    SELECT strftime('%Y-%m', s.start_time) AS month, 
           s.charger_id,
           COUNT(DISTINCT s.user_id) AS num_users
    FROM sessions s
    GROUP BY month, s.charger_id
)
SELECT charger_id,
       AVG(num_users) AS avg_users_per_month
FROM UserCountPerMonth
GROUP BY charger_id;

-- para comprobar:
SELECT start_time
FROM sessions;

-- Flor:
SELECT AVG(user_count), mes
FROM (SELECT STRFTIME('%Y-%m',s.start_time) AS mes, s.charger_id, COUNT(DISTINCT u.id) AS user_count
FROM sessions s
JOIN users u ON s.user_id = u.id
GROUP BY mes, s.charger_id)
GROUP BY charger_id;

-- Question 12: Top 3 users per charger (for each charger, number of sessions)
SELECT charger_id, user_id, session_count
FROM (
    SELECT charger_id, user_id, COUNT(*) AS session_count,
        ROW_NUMBER() OVER (
        -- Row number asigna un numero secuencial (rank) a cada sesión de usuario, ordenada por las session_count
            PARTITION BY charger_id
            -- partition by es usa en row_number() para dividir los resultados en grupos independientes antes de la función
            ORDER BY COUNT (*) DESC
            )
            AS rank
    FROM sessions
    GROUP BY charger_id, user_id
)
WHERE rank <=3;



-- LEVEL 5

-- Question 13: Top 3 users with longest sessions per month (consider the month of start_time)
SELECT month, user_id, max_session_duration_hours
FROM (
    SELECT strftime ('%Y-%m', start_time) as month,
        user_id,
        ROUND(MAX(julianday(end_time) - julianday(start_time)) * 24, 2) AS max_session_duration_hours,
        ROW_NUMBER() OVER (
        -- Row number asigna un numero secuencial (rank) a cada sesión de usuario, ordenada por las max_session_duration_hours
            PARTITION BY strftime('%Y-%m', start_time)
            -- partition by es usa en row_number() para dividir los resultados en grupos independientes antes de la función
            ORDER BY ROUND(MAX(julianday(end_time) - julianday(start_time)) * 24, 2)  DESC
            )
        AS rank
    FROM sessions
    GROUP BY month, user_id
)
WHERE rank <=3;    

    
-- Question 14. Average time between sessions for each charger for each month (consider the month of start_time)

WITH SessionIntervals AS (
    SELECT charger_id, strftime('%Y-%m', start_time) AS month,
           round(julianday(LEAD(start_time) OVER (PARTITION BY charger_id ORDER BY start_time)) - julianday(start_time),2) AS time_between_sessions
    FROM sessions
)
SELECT charger_id, month, round(AVG(time_between_sessions) * 24,2) AS avg_time_between_sessions_hours
FROM SessionIntervals
GROUP BY charger_id, month;

WITH
diferencias AS (
    SELECT
        charger_id,
        start_time,
        LAG(start_time) OVER (PARTITION BY charger_id ORDER BY start_time) AS carga_previa
    FROM sessions
)
SELECT
    charger_id,
    STRFTIME('%Y-%m', start_time) AS mes,
    ROUND(AVG((julianday(start_time) - julianday(carga_previa)) * 24), 2) AS 'Average time between sessions'
FROM diferencias
WHERE carga_previa IS NOT NULL
GROUP BY mes, charger_id
ORDER BY mes, charger_id;
