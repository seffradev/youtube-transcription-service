CREATE TABLE account (  
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    auth_token VARCHAR(255),
    tokens INT NOT NULL DEFAULT 30,
    name VARCHAR(255),
    email VARCHAR (255) UNIQUE,
    password VARCHAR(255)
);