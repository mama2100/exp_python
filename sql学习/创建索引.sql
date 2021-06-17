-- 创建一个简单的索引，名为 "PersonIndex"，在 Person 表的 LastName 列：
-- CREATE INDEX personinex on persons1(LastName)

-- 如果您希望以降序索引某个列中的值，您可以在列名称之后添加保留字 DESC：
-- CREATE INDEX PersonIndex ON Person (LastName DESC)

-- 假如您希望索引不止一个列，您可以在括号中列出这些列的名称，用逗号隔开：
-- CREATE INDEX personindex on persons1 (LastName,FirstName)
