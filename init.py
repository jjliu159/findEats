#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import hashlib

from datetime import datetime
#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                    #    port=8889,
                       user='root',
                    #    password='root',
                       db='findEats',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route("/")

def index():
    return render_template("index.html")

def login():
    return render_template("login.html")

def register():
    return render_template("register.html")

def home():
    return render_template("home.html")

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth(): #done
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return redirect(url_for('home'))
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
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']

        #cursor used to send queries
        cursor = conn.cursor()
        #executes query
        query = 'SELECT * FROM Person WHERE username = %s'
        cursor.execute(query, (username))
        #stores the results in a variable
        data = cursor.fetchall()
        #use fetchall() if you are expecting more than 1 data row
        error = None
        if(data):
            #If the previous query returns data, then user exists
            error = "This user already exists"
            return render_template('register.html', error = error)
        else:
            ins = 'INSERT INTO Person VALUES(%s, %s, %s, %s, %s)'
            cursor.execute(ins, (username, password, firstName, lastName, email))
            conn.commit()
            cursor.close()
            return render_template('index.html')
    else:
        return render_template('register.html')