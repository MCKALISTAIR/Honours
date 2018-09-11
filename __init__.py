from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_pymongo import PyMongo
import bcrypt
import random
import string
import pyperclip
import bcrypt
import os
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Users'
app.config['MONGO_URI'] = 'mongodb://MCKALISTAIR:Uacpad923!@ds145412.mlab.com:45412/users'
mongo = PyMongo(app)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('landing.html')
    else:
        return "Logged in"
@app.route('/login_page')
def login_page():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Logged in"
@app.route('/register_page')
def register_page():
    return render_template('register.html')
@app.route('/login', methods=['POST'])
def login():
    # Connect to DB
    users = mongo.db.users
    # Variable to store information of a logged in user.
    logged_user = users.find_one({'name' : request.form['username']})

    # If a user is loged in:
    if logged_user:
        # Compare inputted password with hashed password store in the DB
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), logged_user['password'].encode('utf-8')) == logged_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('login'))
    # If no user is logged in redirect them to the login page
    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Connect to the DB
        users = mongo.db.users
        # Variable for checking if a user is already registered
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            # Hash the inputted password
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            # Store the username and password in the DB
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            # Add user to session
            session['username'] = request.form['username']
            return redirect(url_for('login'))
	return render_template('register.html')

if __name__ == "__main__":
    app.secret_key = 'shhhhhhhh'
    app.run(ssl_context='adhoc', debug=True)
