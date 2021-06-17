-- SQL COUNT() 语法
-- 我们希望计算客户 "Carter" 的订单数
-- SELECT Count(Customer) as kehu FROM orders1 where Customer='Carter'

-- 我们希望计算 "Orders" 表中不同客户的数目。
-- SELECT Count(DISTINCT Customer) as kehu FROM orders1 


-- 我们希望查找 "OrderPrice" 列的第一个值。
-- SELECT first(OrderPrice) FROM Orders1  mysql不支持这种写法
-- SELECT last(OrderPrice) FROM Orders1

-- MAX 函数返回一列中的最大值。
-- SELECT max(OrderPrice) FROM Orders1

-- MIN 函数返回一列中的最小值。NULL 值不包括在计算中。
-- SELECT min(OrderPrice) FROM orders1

-- SUM 函数返回数值列的总数（总额）。
-- 我们希望查找 "OrderPrice" 字段的总数。
-- SELECT sum(OrderPrice) as ordertotal FROM orders1

-- 现在，我们希望查找每个客户的总金额（总订单）。
-- 我们想要使用 GROUP BY 语句对客户进行组合。
-- SELECT customer,sum(OrderPrice) FROM  orders1 GROUP BY(Customer) 

-- SQL HAVING 子句
-- 现在，我们希望查找订单总金额少于 2000 的客户。
-- SELECT Customer,sum(OrderPrice) as sumprice FROM orders1 GROUP BY Customer HAVING sumprice < 2000
-- 在 SQL 中增加 HAVING 子句原因是，WHERE无法使用  


-- SQL UCASE() 语法
-- 我们希望选取 "LastName" 和 "FirstName" 列的内容，然后把 "LastName" 列转换为大写
-- SELECT ucase(LastName),FirstName FROM persons


-- LCASE() 函数
-- LCASE 函数把字段的值转换为小写。
-- SELECT lcase(LastName),FirstName FROM persons


-- MID() 函数
-- MID 函数用于从文本字段中提取字符。
-- 现在，我们希望从 "City" 列中提取前 3 个字符。
-- SELECT mid(city,1,3) as smailcity FROM persons


-- SQL LEN() 函数
-- LEN 函数返回文本字段中值的长度。
-- SELECT LENGTH(City) as lengthcity FROM persons
-- mysql里只有length

-- ROUND() 函数
-- ROUND 函数用于把数值字段舍入为指定的小数位数。
-- 现在，我们希望把名称和价格舍入为最接近的整数。
-- SELECT ProductName,round(unitprice) from products
-- SELECT ProductName, ROUND(UnitPrice,0) as UnitPrice FROM Products
-- SELECT ProductName,UnitPrice,NOW() as perdate FROM products

-- SQL FORMAT() 函数
-- FORMAT 函数用于对字段的显示进行格式化。
-- SELECT ProductName,UnitPrice,format(Now(),'YYYY-MM-DD') as perdate FROM products
