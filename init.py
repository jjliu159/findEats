#Import Flask Library
import json
from flask import Flask, Response, render_template, request, session, jsonify, url_for, redirect
# import pymysql.cursors
import psycopg2
import hashlib
import math
from geopy.distance import geodesic
from flask_login import LoginManager
import flask_login

login_manager = LoginManager()

from datetime import datetime
#Initialize the app from Flask
app = Flask(__name__, static_url_path ="", static_folder ="static")
# app.config['GOOGLEMAPS_KEY'] = "AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNGg"
app.secret_key = "random string"
app.config.update(TEMPLATES_AUTO_RELOAD = True)

# login_manager.init_app(app)

#Configure MySQL

# conn = psycopg2.connect(host='localhost',
#                        port=5431,
#                        user='alanlu',
#                        password='',
#                        database='test',)


#alan
# conn = psycopg2.connect(host='localhost',
#                        port=5432,
#                        user='postgres',
#                        password='password',
#                        database='findeats',)



# conn = psycopg2.connect(host='localhost',
#                        port=5431,
#                        user='alanlu',
#                        password='',
#                        database='test',)


# mandy
conn = psycopg2.connect(host='localhost',
                       port=5432,
                       user='postgres',
                       password='Basicscats168!',
                       database='findeats',)

# conn = psycopg2.connect(
#         host="localhost",
#         port = 5432,
#         database="postgres",
#         user="postgres",
#         password="")

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

# @login_manager.user_loader
# def load_user(user_id):
#     # return User.get(user_id)
#     cursor = conn.cursor()
#     query = 'SELECT * FROM person WHERE user_id = %s'
#     cursor.execute(query,user_id)
#     #stores the results in a variable
#     data = cursor.fetchone()
#     print(data)
#     return data


@app.route("/")
# @flask_login.login_required
def hello():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/edit")
def edit():
    curUser = session["username"]
    cursor = conn.cursor()
    query = 'SElECT * FROM person WHERE username = %s'
    cursor.execute(query,[curUser])
    error = None
    data = cursor.fetchall()[0]
    if data:
        userID,email,username,password,isOwner, restaurantName, latitude,longitude,description,address,reservationAmount = data
        if isOwner:
            return render_template("edit.html", username=username,password=password,email = email, isOwner=isOwner,restaurantName=restaurantName,description=description,address=address,reservationAmount=reservationAmount)
        else:
            return render_template("editUser.html",username=username,password=password,email=email)

#needed this specific function since JJ used flask's session storage earlier to pass on information from the map.html to the edit.html
@app.route("/logOut")
def logOut():
    session.clear()
    return render_template("index.html")


@app.route("/decrementCount",methods=['POST'])
def decrementCount():
    id = request.form['id']
    amount = request.form['count']
    amount = int(amount) - 1
    # "UPDATE person SET email = 'NEW_EMAIL', password = 'NEW_PW', description = 'NEW DESCRIPTION' WHERE user_id = id;"
    # query for owner
    # UPDATE person SET email = 'NEW_EMAIL', password = 'NEW_PW' WHERE user_id = id
    # query for customer
    # psycopg2 doesn't use %d for int updates
    query = "UPDATE person SET reservationamount = %s WHERE user_id = %s;"
    cursor = conn.cursor()
    cursor.execute(query, (amount, id))
    # need to commit the changes to SQL TABLE
    conn.commit()
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
    print('in loginauth',request.form,request.form['username'],len(request.form))
    username = request.form['username']
    password = request.form['password']

    #we have two incoming loginauth request, one from edit and one from regular sign in
    #regular sign in length is 2, therefore we need to encode it
    #if it's from edit, the password is already encoded and if it's already encoded it will be enconded once more
    #and this won't match up with the database
    if len(request.form) == 2:
        password = hashlib.md5(password.encode()).hexdigest()
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM person WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    # print(data)
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
            return render_template("map.html",username = username)
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
        print(password)
        password = hashlib.md5(password.encode()).hexdigest()
        print(password)
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

def findUser(username):
    print("WHERE IS THIS",username,type(username))
    cursor = conn.cursor()
    query = 'SELECT * FROM person WHERE username = %s'
    cursor.execute(query,[username])
    data = cursor.fetchall()
    if data:
        print(data)
    else:
        print("nonexistent")
    cursor.close()

@app.route('/editRestaurantAuth',methods =['GET', 'POST'])
def editRestaurantAuth():
    if request.method == 'POST':
        cursor = conn.cursor()
        username = request.form['username']
        password = request.form['password']
        password = hashlib.md5(password.encode()).hexdigest()
        email = request.form['email']
        print(request.form['isOwner'])
        if request.form['isOwner'] == 'true':
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            description = request.form['description']
            address = request.form['address']
            reservationAmount = request.form['reservationAmount']
            restaurantName = request.form['restaurantName']      
        
            update = "UPDATE person SET password = %s, email = %s, isOwner = %s, restaurantName = %s, latitude = %s, longitude = %s, address = %s, description = %s, reservationAmount = %s WHERE username = %s"
            cursor.execute(update,(password, email, True, restaurantName, latitude, longitude, address, description, reservationAmount, username))
        else:
            update = "UPDATE person SET password = %s, email = %s WHERE username = %s"
            cursor.execute(update,(password,email,username))
            print('did it go thru')
        conn.commit()
        cursor.close()
        return 'success'
    

def getDistance(x1,y1,x2,y2):
    return math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )


if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = False)