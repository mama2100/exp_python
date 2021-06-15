-- 在 "Persons" 表创建时在 "Id_P" 列创建 PRIMARY KEY 约束：
-- CREATE TABLE persons2
-- (
-- id_p int not null,
-- LastName VARCHAR(255) not null,
-- FirstName VARCHAR(255),
-- Address VARCHAR(255),
-- city VARCHAR(255),
-- PRIMARY KEY (id_p)
-- )

-- 如果需要命名 PRIMARY KEY 约束，以及为多个列定义 PRIMARY KEY 约束，请使用下面的 SQL 语法：
-- CREATE TABLE Persons
-- (
-- Id_P int NOT NULL,
-- LastName varchar(255) NOT NULL,
-- FirstName varchar(255),
-- Address varchar(255),
-- City varchar(255),
-- CONSTRAINT pk_PersonID PRIMARY KEY (Id_P,LastName)
-- )

-- 如果在表已存在的情况下为 "Id_P" 列创建 PRIMARY KEY 约束，请使用下面的 SQL：
-- ALTER TABLE persons add PRIMARY key (id_p)


-- 如果需要命名 PRIMARY KEY 约束，以及为多个列定义 PRIMARY KEY 约束，请使用下面的 SQL 语法：
-- ALTER TABLE Persons ADD CONSTRAINT pk_PersonID PRIMARY KEY (Id_P,LastName)

-- 如需撤销 PRIMARY KEY 约束，请使用下面的 SQL：
-- ALTER TABLE Persons DROP PRIMARY KEY