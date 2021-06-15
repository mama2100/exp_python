-- SELECT * INTO Persons_backup FROM Persons
-- MySQL 数据库不支持 SELECT ... INTO 语句，但支持 INSERT INTO ... SELECT 。
-- 当然你可以使用以下语句来拷贝表结构及数据：
-- CREATE TABLE 新表
-- AS
-- SELECT * FROM 旧表 
CREATE table persons_backup
as 
SELECT * FROM persons