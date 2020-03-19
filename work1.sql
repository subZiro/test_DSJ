USE test_DSJ
GO
SELECT ProductName AS Product, count(*) AS count
FROM ProductRequest AS p
INNER JOIN Product c ON p.ProductId  = c.ProductId 
WHERE p.AppDate BETWEEN '2020-01-01' AND '2020-10-31'
GROUP BY p.ProductId
GO
