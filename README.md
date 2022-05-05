# findEats

instructions:

NEED: Python, HTML, CSS, JavaScript

1) Download PostgresSQL/pgAdmin 4 and insert the SQL below:


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
reservationAmount INT,
code VARCHAR(10)
);

2) open terminal and pip install: flask, psycopg2, geopy

3) set conn = psycopg2.connect in init.py to your PostgresSQL authentication

4) in terminal: 
    a) go to folder directory
    b) type in "set FLASK_APP = init.py"
    c) type in "flask run"
    d) will give you the link to run on local host