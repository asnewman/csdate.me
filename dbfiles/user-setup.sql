DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
   id INT AUTO_INCREMENT PRIMARY KEY, 
   username VARCHAR(16) NOT NULL,
   password VARCHAR(256) NOT NULL,
   email VARCHAR(64) NOT NULL,
   token VARCHAR(256) DEFAULT NULL,
   tokenTime TIMESTAMP NULL,
   firstName VARCHAR(32),
   middleName VARCHAR(32) DEFAULT NULL,
   lastName VARCHAR(32),
   gender VARCHAR(1),
   state VARCHAR(32),
   city VARCHAR(32),
   birthday DATE,
   favoriteOS VARCHAR(16)
); 
