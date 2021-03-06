-- 列出所有在中国和美国的不同的雇员名
SELECT e_name FROM employees_china 
union all
SELECT e_name FROM employees_usa
-- UNION 操作符用于合并两个或多个 SELECT 语句的结果集。
-- 请注意，UNION 内部的 SELECT 语句必须拥有相同数量的列。列也必须拥有相似的数据类型。同时，每条 SELECT 语句中的列的顺序必须相同。
-- 默认地，UNION 操作符选取不同的值。如果允许重复的值，请使用 UNION ALL。