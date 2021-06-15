-- SELECT persons.LastName,persons.FirstName,orders.OrderNo
-- FROM Persons
-- FULL JOIN Orders
-- ON persons.Id_P=orders.Id_p
-- ORDER BY Persons.LastName
-- 全连接，mysql不支持全连接
-- 以使用UNION ALL子句，将两个JOIN为如下
SELECT
	persons.LastName,
	persons.FirstName,
	orders.OrderNo 
FROM
	Persons
	LEFT JOIN Orders ON persons.Id_P = orders.Id_p UNION ALL
SELECT
	persons.LastName,
	persons.FirstName,
	orders.OrderNo 
FROM
	Persons
	RIGHT JOIN Orders ON persons.Id_P = orders.Id_p