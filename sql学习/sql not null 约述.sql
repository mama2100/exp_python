-- sql not null 约述
-- not null 约束强制列始终包含值
CREATE table persons1(
id_p int not NULL,
LastName VARCHAR(255) not null,
FirstName VARCHAR(255),
Address VARCHAR(255),
city VARCHAR(255)
)
