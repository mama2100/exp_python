-- mysql 查询date时间
-- SELECT * FROM orders WHERE orderdate='2008-12-26'

-- SELECT now(),curdate(),curtime();
-- now()函数查看当前日期和时间
-- curdate()  查看当前日期
-- curtime() 查看当前时间

-- DATE() 函数返回日期或日期/时间表达式的日期部分。
-- select date('2008-12-29 16:25:46.635')
-- 返回为2008-12-29

-- EXTRACT() 函数用于返回日期/时间的单独部分，比如年、月、日、小时、分钟等等
-- 用法如下：EXTRACT(unit FROM date)
-- SELECT EXTRACT(year from orderdate) as orderyear,
-- EXTRACT(month from orderdate) as ordermoth,
-- EXTRACT(day from orderdate) as orderday
-- from orders
-- where orderid=1


-- MySQL DATE_ADD() 函数
-- DATE_ADD() 函数向日期添加指定的时间间隔。
-- 我们希望向 "OrderDate" 添加 2 天，这样就可以找到付款日期。
-- SELECT OrderID,date_add(orderdate,INTERVAL 2 DAY) as orderpaydate from orders


-- SQL Server DATEDIFF() 函数
-- DATEDIFF() 函数返回两个日期之间的时间。

SELECT DATEDIFF('2008-12-30','2008-12-29') AS DiffDate
