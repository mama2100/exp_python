-- 把 "Persons" 表中的 "P_Id" 列定义为 auto-increment 主键：
-- create TABLE persons2
-- (
-- p_id int not null auto_increment,
-- LastName VARCHAR(255) not null,
-- FirstName VARCHAR(255),
-- Address VARCHAR(255),
-- city VARCHAR(255),
-- PRIMARY key (p_id)
-- )
-- 

-- 要让 AUTO_INCREMENT 序列以其他的值起始，请使用下列 SQL 语法：
-- ALTER TABLE persons auto_increment=100
-- INSERT into persons2(FirstName,LastName) VALUES('Bill','Gates')
-- 
