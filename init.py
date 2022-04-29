#Import Flask Library
import json
from flask import Flask, Response, render_template, request, session, jsonify, url_for, redirect
# import pymysql.cursors
import psycopg2
import hashlib
import psycopg2 
import math
from geopy.distance import geodesic



from datetime import datetime
#Initialize the app from Flask
app = Flask(__name__, static_url_path ="", static_folder ="static")
# app.config['GOOGLEMAPS_KEY'] = "AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNGg"
app.secret_key = "random string"
app.config.update(TEMPLATES_AUTO_RELOAD = True)

#Configure MySQL


# conn = psycopg2.connect(host='localhost',
#                        port=5432,
#                        user='postgres',
#                        password='',
#                        database='findeats',)


#alan
# conn = psycopg2.connect(host='localhost',
#                        port=5431,
#                        user='alanlu',
#                        password='chingchong',
#                        database='test',)

conn = psycopg2.connect(
        host="localhost",
        port = 5432,
        database="postgres",
        user="postgres",
        password="")

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

# @app.route("/confirmation")
# def confirmation():
#     return render_template("confirmation.html")

@app.route("/decrementCount",methods=['POST'])
def decrementCount():
    print('herererere')
    id = request.form['id']
    query = "UPDATE person SET reservationAmount = reservationAmount-1 WHERE user_id = %s;"
    cursor = conn.cursor()
    cursor.execute(query,id)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    


@app.route("/getPins",methods=['POST'])
def retrievePins():
    if request.method == 'POST':
        lat = request.form['Latitude']
        print("LATITUDE:", lat)
        lng = request.form['Longitude']
        print("LONGITUDE: ", lng)
    cursor = conn.cursor()
    query = 'SELECT * FROM person WHERE owner = True;'
    # cursor.execute(query)
    cursor.execute('SELECT * FROM person')
    #stores the results in a variable
    data = cursor.fetchall()
    counter = 0
    print('data',data)
    dest = (lat, lng)
    responseData = []
    
    for i in data:
        print(i)
        origin = (i[6] ,i[7])
        
        if geodesic(origin, dest).meters<5000:
            responseData.append({
                "longitude":i[7],
                "latitude":i[6],
                "description":i[8],
                "restName":i[5],
                "restAddress":i[9],
                "count":i[10],
                "id":i[0]
            })
    print("rendering Map2")
    print(responseData)
    return Response(json.dumps(responseData), mimetype='text/json') 
    


@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth(): #done
    #grabs information from the forms
    print('in loginauth')
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM person WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        try:
            session['username'] = username
            print("method: ",request.method)
            # return redirect(url_for('home'))
            return render_template("map.html")
        except Exception as e:
            print(e)
            
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
        isOwner = request.form['isOwner']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        description = request.form['description']
        address = request.form['address']
        reservationAmount = request.form['reservationAmount']
        restaurantName = request.form['restaurantName']


        #cursor used to send queries
        cursor = conn.cursor()
        #executes query
        query = 'SELECT * FROM person WHERE username = %s'
        cursor.execute(query,[username])
        #stores the results in a variable
        # data = cursor.fetchall()
        #use fetchall() if you are expecting more than 1 data row
        error = None
        data = cursor.fetchall()

        if data:
            error = "This user already exists"
            return "failure"
        else:
            if isOwner != "false":
                ins = 'INSERT INTO person (username, password, email, isOwner, latitude, longitude, description, address, reservationAmount, restaurantName) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(ins,(username, password, email, True, latitude, longitude, description, address, reservationAmount, restaurantName))
            else:
                print
                ins = 'INSERT INTO person (username, password, email, isOwner) VALUES(%s, %s, %s, %s)'
                cursor.execute(ins,(username,password, email, False))
            conn.commit()
            cursor.close()
            return "success"
    else:
        return render_template('register.html')

def getDistance(x1,y1,x2,y2):
    return math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )


if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = False)