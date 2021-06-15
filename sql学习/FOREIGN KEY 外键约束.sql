-- 在 "Orders" 表创建时为 "Id_P" 列创建 FOREIGN KEY：
-- CREATE TABLE ORDERs1 
-- (
-- id_o int not null,
-- orderno int not null,
-- id_p int,
-- PRIMARY key (id_o),
-- FOREIGN key (id_p) REFERENCES persons(id_p)
-- )

-- 如果需要命名 FOREIGN KEY 约束，以及为多个列定义 FOREIGN KEY 约束，请使用下面的 SQL 语法：

-- CREATE TABLE ORDERs1 
-- (
-- id_o int not null,
-- orderno int not null,
-- id_p int,
-- PRIMARY key (id_o),
-- CONSTRAINT fk_perorders FOREIGN key (id_p) 
-- REFERENCES persons(id_p)
-- )

-- 在 "Orders" 表已存在的情况下为 "Id_P" 列创建 FOREIGN KEY 约束，请使用下面的 SQL：
-- ALTER TABLE orders1 add FOREIGN key (id_p) REFERENCES persons(id_p)


-- 如果需要命名 FOREIGN KEY 约束，以及为多个列定义 FOREIGN KEY 约束，请使用下面的 SQL 语法：
-- ALTER TABLE orders 
-- add CONSTRAINT fk_perorders
-- FOREIGN key (id_p)
-- REFERENCES persons(id_P)


-- 如需撤销 FOREIGN KEY 约束，请使用下面的 SQL：
ALTER TABLE Orders
DROP FOREIGN KEY fk_PerOrders