-- 在 "Persons" 表创建时为 "Id_P" 列创建 CHECK 约束。CHECK 约束规定 "Id_P" 列必须只包含大于 0 的整数。
-- CREATE TABLE Persons1
-- (
-- Id_P int NOT NULL,
-- LastName varchar(255) NOT NULL,
-- FirstName varchar(255),
-- Address varchar(255),
-- City varchar(255),
-- CHECK (Id_P>0)
-- )


-- 如果在表已存在的情况下为 "Id_P" 列创建 CHECK 约束，请使用下面的 SQL：
-- alter TABLE persons1 add check(id_p >0)

-- 如果需要命名 CHECK 约束，以及为多个列定义 CHECK 约束，请使用下面的 SQL 语法：

-- ALTER table persons add CONSTRAINT chk_Person CHECK (Id_P>0 AND City='Sandnes')
-- constraint是约束关键字


-- 需撤销 CHECK 约束，请使用下面的 SQL：
-- ALTER TABLE Persons DROP CHECK chk_Person
