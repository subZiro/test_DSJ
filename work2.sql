USE test_DSJ;
GO
SELECT p.ProductName, SUM(pr.RequestedAmount) AS SumProduct, MONTH(pr.AppDate) AS month
FROM ProductRequest AS pr
INNER JOIN Product AS p ON p.ProductId = pr.ProductId 
WHERE pr.AppDate BETWEEN '2020-01-01' AND '2020-07-31'
GROUP BY month
HAVING SumProduct > 40000
GO
