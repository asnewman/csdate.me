CREATE TABLE Users (
   id INT AUTO_INCREMENT PRIMARY KEY, 
   username VARCHAR(16),
   password VARCHAR(16),
   email VARCHAR(64),
   firstName VARCHAR(55),
   middleName VARCHAR(55) default NULL,
   lastName VARCHAR(55),
   gender VARCHAR(20),
   state VARCHAR(20),
   city VARCHAR(256),
   birthday DATE,
   favoriteOS VARCHAR(20)
); 
