-- CREATE TABLE persons1 
-- (
-- id_p int null,
-- LastName VARCHAR(255) not null,
-- FirstName VARCHAR(255),
-- Address VARCHAR(255),
-- city VARCHAR(255) DEFAULT 'sandnes'
-- )
-- 


-- 如果在表已存在的情况下为 "City" 列创建 DEFAULT 约束，请使用下面的 SQL：
-- ALTER TABLE persons1 ALTER city set DEFAULT 'sandnes'

-- 如需撤销 DEFAULT 约束，请使用下面的 SQL：
-- ALTER TABLE Persons ALTER City DROP DEFAULT