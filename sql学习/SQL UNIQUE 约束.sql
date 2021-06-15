-- 在 "Persons" 表创建时在 "Id_P" 列创建 UNIQUE 约束：

-- CREATE TABLE Persons1
-- (
-- Id_P int NOT NULL,
-- LastName varchar(255) NOT NULL,
-- FirstName varchar(255),
-- Address varchar(255),
-- City varchar(255),
-- UNIQUE (Id_P)
-- )

-- 如果需要命名 UNIQUE 约束，以及为多个列定义 UNIQUE 约束，请使用下面的 SQL 语法：
/* CREATE TABLE Persons !
(
Id_P int NOT NULL,
LastName varchar(255) NOT NULL,
FirstName varchar(255),
Address varchar(255),
City varchar(255),
CONSTRAINT uc_PersonID UNIQUE (Id_P,LastName)
)
*/


-- 当表已被创建时，如需在 "Id_P" 列创建 UNIQUE 约束，请使用下列 SQL：
-- ALTER TABLE Persons ADD UNIQUE (Id_P)
-- ALTER TABLE persons add CONSTRAINT uc_personid UNIQUE(id_p,lastname)

-- 如需撤销 UNIQUE 约束，请使用下面的 SQL：
-- ALTER TABLE Persons DROP INDEX uc_personid

