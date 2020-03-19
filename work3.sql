
SELECT Product.ProductName, SUM(Payments.PayAmount) AS sumPayments, Debt.DebtAmount
FROM Payments
LEFT JOIN Debt ON Payments.DebtId = Debt.DebtId
LEFT JOIN ProductRequest ON Debt.AppId = ProductRequest.AppID 
LEFT JOIN Product ON ProductRequest.ProductId = Product.ProductID
WHERE Payments.PayDate BETWEEN '2020-01-01' AND '2020-07-31'
GROUP BY ProductRequest.ProductId, MONTH(Payments.PayDate)