# findEats

instructions
download from https://sourceforge.net/projects/wampserver/
install and then run it

instructions are in this video on how to set up:
https://streamable.com/bt6biz


SQL code is below:
CREATE TABLE Person(
user_id serial PRIMARY KEY,
userName VARCHAR(50) NOT NULL,
password VARCHAR(50) NOT NULL,
owner BOOLEAN NOT NULL,
latitude FLOAT,
longitude FLOAT,
message VARCHAR(200) 
);

ALTER TABLE Person (
ADD owner BIT ,
ADD latitude FLOAT,
ADD longitude FLOAT,
ADD message VARCHAR(200) ,
ADD user_id INT PRIMARY KEY IDENTITY (1, 1));

INSERT INTO person(userName,password,owner, latitude, longitude) 
VALUES ('alan','loooo',True, 10.1,10.2);