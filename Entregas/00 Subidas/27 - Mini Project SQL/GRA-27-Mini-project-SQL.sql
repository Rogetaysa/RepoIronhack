-- Inicio:
USE ironhackgambling;

-- Pregunta 1:
SELECT Title, FirstName, LastName, DateOfBirth
FROM Customer;

-- Pregunta 2:
SELECT CustomerGroup, COUNT(*) AS TotalCustomers
FROM Customer
GROUP BY CustomerGroup;

-- Pregunta 3:
SELECT c.*, a.CurrencyCode
FROM Customer c
JOIN Account a ON c.CustId = a.CustId;

-- Pregunta 4:
SELECT b.BetDate, p.product, SUM(b.Bet_Amt) AS TotalBet
FROM Betting b
JOIN Product p ON b.ClassId = p.CLASSID AND b.CategoryId = p.CATEGORYID
GROUP BY b.BetDate, p.product
ORDER BY b.BetDate, p.product;

-- Pregunta 5:
SELECT b.BetDate, p.product, SUM(b.Bet_Amt) AS TotalBet
FROM Betting b
JOIN Product p ON b.ClassId = p.CLASSID AND b.CategoryId = p.CATEGORYID
WHERE b.BetDate >= '2012-11-01' AND p.product = 'Sportsbook'
GROUP BY b.BetDate, p.product
ORDER BY b.BetDate;

-- Pregunta 6:
SELECT a.CurrencyCode, c.CustomerGroup, p.product, SUM(b.Bet_Amt) AS TotalBet
FROM Betting b
JOIN Account a ON b.AccountNo = a.AccountNo
JOIN Customer c ON a.CustId = c.CustId
JOIN Product p ON b.ClassId = p.CLASSID AND b.CategoryId = p.CATEGORYID
WHERE b.BetDate > '2012-12-01'
GROUP BY a.CurrencyCode, c.CustomerGroup, p.product
ORDER BY a.CurrencyCode, c.CustomerGroup, p.product;

-- Pregunta 7:
SELECT c.Title, c.FirstName, c.LastName, ROUND(COALESCE(SUM(b.Bet_Amt), 0),2) AS TotalBet
FROM Customer c
LEFT JOIN Account a ON c.CustId = a.CustId
LEFT JOIN Betting b ON a.AccountNo = b.AccountNo AND b.BetDate BETWEEN '2012-11-01' AND '2012-11-30'
GROUP BY c.Title, c.FirstName, c.LastName
ORDER BY c.LastName;

-- Pregunta 8:
-- Pregunta 8.1 Numero de productos por jugador:
SELECT a.AccountNo, c.Title, c.FirstName,c.LastName, COUNT(DISTINCT b.Product) AS ProductCount
FROM 
	Customer c
JOIN 
    Account a ON c.CustId = a.CustId
JOIN 
    Betting b ON a.AccountNo = b.AccountNo
GROUP BY 
    a.AccountNo, c.Title, c.FirstName, c.LastName
ORDER BY 
    ProductCount DESC, c.LastName;


-- Pregunta 8.2 Muestra de jugadores que juegan en Sportsbook y Vegas:
SELECT b.AccountNo
FROM Betting b
JOIN Product p ON b.ClassId = p.CLASSID AND b.CategoryId = p.CATEGORYID
WHERE p.product IN ('Sportsbook', 'Vegas')
GROUP BY b.AccountNo
HAVING COUNT(DISTINCT p.product) = 2;

SELECT a.AccountNo, c.Title, c.FirstName, c.LastName
FROM Customer c
JOIN 
    Account a ON c.CustId = a.CustId
JOIN 
    Betting b ON a.AccountNo = b.AccountNo
WHERE 
    b.Product IN ('Sportsbook', 'Vegas')
GROUP BY 
    a.AccountNo, c.Title, c.FirstName, c.LastName
HAVING 
    COUNT(DISTINCT b.Product) = 2
ORDER BY 
    c.LastName;

-- Pregunta 9:
SELECT a.AccountNo, c.Title, c.FirstName, c.LastName, ROUND(SUM(b.Bet_Amt), 2) AS TotalBetAmount
FROM 
    Betting b
JOIN 
    Product p ON b.ClassId = p.CLASSID AND b.CategoryId = p.CATEGORYID
JOIN 
    Account a ON b.AccountNo = a.AccountNo
JOIN 
    Customer c ON a.CustId = c.CustId
WHERE 
    b.Product = 'Sportsbook'  -- Sportsbook
    AND b.Bet_Amt > 0         -- iempre mayor que 0
GROUP BY 
    a.AccountNo, c.Title, c.FirstName, c.LastName
HAVING 
    COUNT(DISTINCT b.Product) = 1 -- 1 solo producto
ORDER BY 
    TotalBetAmount DESC, c.LastName;


-- Pregunta 10:
WITH RankedBets AS (
    SELECT c.Title, c.FirstName, c.LastName, p.product, ROUND(SUM(b.Bet_Amt), 2) AS TotalBet,
           ROW_NUMBER() OVER (PARTITION BY c.FirstName, c.LastName ORDER BY SUM(b.Bet_Amt) DESC) AS Ranking
    FROM Betting b
    JOIN Product p ON b.ClassId = p.CLASSID AND b.CategoryId = p.CATEGORYID
    JOIN Account a ON b.AccountNo = a.AccountNo
    JOIN Customer c ON a.CustId = c.CustId
    WHERE b.Bet_Amt > 0
    GROUP BY c.Title, c.FirstName, c.LastName, p.product
)
SELECT Title, FirstName, LastName, product, TotalBet
FROM RankedBets
WHERE Ranking = 1
ORDER BY LastName, TotalBet DESC;


-- Pregunta 11:
SELECT student_id, student_name, GPA
FROM Student_School
ORDER BY GPA DESC
LIMIT 5;

-- Pregunta 12:
SELECT sc.school_id, sc.school_name, COUNT(st.student_id) AS total_students
FROM School sc
LEFT JOIN Student st ON sc.school_id = st.school_id
GROUP BY school_id
HAVING sc.school_id <> '-----------';

SELECT 
    sc.school_id, 
    sc.school_name, 
    COUNT(st.student_id) AS total_students
FROM 
    School sc
LEFT JOIN 
    Student st ON sc.school_id = st.school_id
WHERE 
    sc.school_id <> '-----------'  -- Usar WHERE para excluir filas antes de contar
GROUP BY 
    sc.school_id, 
    sc.school_name  -- Incluir school_name en el GROUP BY
ORDER BY 
    total_students DESC, sc.school_id;  -- Ordenar el resultado



-- Pregunta 13:
SELECT sc.school_id, st.student_id, st.student_name,
ROW_NUMBER() OVER(PARTITION BY sc.school_id ORDER BY GPA DESC) AS 'Rank', gpa
FROM school sc
LEFT JOIN student st ON sc.school_id = st.school_id
WHERE st.gpa IS NOT NULL
HAVING sc.school_id <> '-----------' AND 'Rank' <= 3
ORDER BY school_id, 'Rank';

