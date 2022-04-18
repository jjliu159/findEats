#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
from flask_googlemaps import GoogleMaps
import pymysql.cursors
import hashlib
import psycopg2 


from datetime import datetime
#Initialize the app from Flask
app = Flask(__name__, static_url_path ="", static_folder ="static")
# app.config['GOOGLEMAPS_KEY'] = "AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNGg"


#Configure PostgreSQL
conn = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        password = '',
                        dbname = 'findeats',
                        )
#Configure MySQL
# conn = pymysql.connect(host='localhost',
#                        port=5432,
#                        user='root',
#                        password='',
#                        db='findeats',
#                        charset='utf8mb4',
#                        cursorclass=pymysql.cursors.DictCursor)


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth(): #done
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Users WHERE username = %s and pass = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        print('here')
        # return redirect(url_fo   r('home'))
        return render_template('map.html')
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST']) 
def registerAuth(): #done
    if request.method == 'POST':
        #grabs information from the forms
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        checkUser = request.form['checkUser']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        #cursor used to send queries
        cursor = conn.cursor()
        #executes query
        # query = 'SELECT * FROM Users WHERE username = %s'
        # cursor.execute(query, (username))
        #stores the results in a variable
        # data = cursor.fetchall()
        #use fetchall() if you are expecting more than 1 data row
        error = None
        if checkUser == "true":
            query = 'SELECT * FROM Owners WHERE username = %s'
            cursor.execute(query,(username))
            data = cursor.fetchall()
            if data:
                error = "This user already exists"
                return render_template('register.html', error = error)
            else:
                ins = 'INSERT INTO Owners VALUES(%s, %s, %s)'
                cursor.execute(ins,(username,password,email))
                conn.commit()
                cursor.close()
                return redner_template('index.html')
        else:
            query = 'SELECT * FROM Users WHERE username = %s'
            cursor.execute(query,(username))
            data = cursor.fetchall()
            if(data):
                #If the previous query returns data, then user exists
                error = "This user already exists"
                return render_template('register.html', error = error)
            else:
                ins = 'INSERT INTO Users VALUES(%s, %s, %s,%s,%s)'
                cursor.execute(ins, (username, password,latitude,longitude,email))
                conn.commit()
                cursor.close()
                return render_template('index.html')
    else:
        return render_template('register.html')

# @app.route("/map")
# def mapview():
#     # creating a map in the view
#     mymap = Map(
#         identifier="view-side",
#         lat=37.4419,
#         lng=-122.1419,
#         markers=[(37.4419, -122.1419)]
#     )
#     sndmap = Map(
#         identifier="sndmap",
#         lat=37.4419,
#         lng=-122.1419,
#         markers=[
#           {
#              'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
#              'lat': 37.4419,
#              'lng': -122.1419,
#              'infobox': "<b>Hello World</b>"
#           },
#           {
#              'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
#              'lat': 37.4300,
#              'lng': -122.1400,
#              'infobox': "<b>Hello World from other place</b>"
#           }
#         ]
#     )
#     return render_template('example.html', mymap=mymap, sndmap=sndmap)

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = False)