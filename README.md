# findEats

instructions
download from https://sourceforge.net/projects/wampserver/
install and then run it

instructions are in this video on how to set up:
https://streamable.com/bt6biz


SQL code is below:
CREATE TABLE Person(
user_id serial PRIMARY KEY,
email VARCHAR(50) NOT NULL,
userName VARCHAR(50) NOT NULL,
password VARCHAR(50) NOT NULL,
isOwner BOOLEAN NOT NULL,
restaurantName VARCHAR(20),
latitude FLOAT,
longitude FLOAT,
description VARCHAR(200),
address VARCHAR(100),
reservationAmount INT
);

ALTER TABLE Person(
user_id serial PRIMARY KEY,
email VARCHAR(50) NOT NULL,
userName VARCHAR(50) NOT NULL,
password VARCHAR(50) NOT NULL,
isOwner BOOLEAN NOT NULL,
restaurantName VARCHAR(20),
latitude FLOAT,
longitude FLOAT,
description VARCHAR(200),
address VARCHAR(100),
reservationAmount INT
);

INSERT INTO person(email,userName,password,isOwner, restaurantName, latitude, longitude, description, address, reservationAmount) VALUES ('alanlu1999@gmail.com','alan','loooo',True, 'McDonalds' ,40.731619616175706,-73.99907986879239, 'Best burgers','White House 69',100);


INSERT INTO person(email,userName,password,isOwner, restaurantName, latitude, longitude, description, address, reservationAmount) VALUES ('alanlu1999@gmail.com','alan','loooo',True, 'BurgerKing' ,40.731719616175706,-73.99207986879239, 'Best burgers','The address',100);

INSERT INTO person(userName, password, owner) VALUES ('alan','loooo',True);

