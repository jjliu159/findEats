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

ALTER TABLE Person (
ADD owner BIT ,
ADD latitude FLOAT,
ADD longitude FLOAT,
ADD message VARCHAR(200) ,
ADD user_id INT PRIMARY KEY IDENTITY (1, 1));

INSERT INTO person(userName,passWORD,owner, latitude, longitude) VALUES ('alan','loooo',True, 40.731619616175706,-73.99907986879239);

INSERT INTO person(userName, password, owner) VALUES ('alan','loooo',True);

