from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from wtforms import Form, StringField, SelectField
from bottle import route, run, template
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
import bcrypt
import random
import string
import pyperclip
import bcrypt
import os
import json
try:
    conn = MongoClient()
    #print("Connected to MongoDB")
except:
    print("Could not connect to MongoDB")
db = conn.database
# Created or Switched to collection names:
collection = db.users
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'Users'
app.config['MONGO_URI'] = 'mongodb://MCKALISTAIR:Uacpad923!@ds145412.mlab.com:45412/users'
mongo = PyMongo(app)
client = MongoClient('mongodb://MCKALISTAIR:Uacpad923!@ds145412.mlab.com:45412/users')
db = client.users
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
@app.route('/landing')
def landing():
    return render_template('landing.html')
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    logged_user = users.find_one({'username' : request.form['username']})

    if logged_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), logged_user['password'].encode('utf-8')) == logged_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            usern = session['username']
            name = users.find_one({'username' : usern})['name']
            session['user'] = "User"
            session['status'] = "user"  ###NEED TO GET THIS BIT DIFFERING BETWEEN MANAGER AND USER, PROBS HAVE THE SYSTEM CHECK ACCOUNT PERMS
            type = users.find_one({'username' : usern})['Type']
            return redirect(url_for('userlanding'))
    return redirect(url_for('login'))
@app.route("/managerlanding", methods=['POST','GET'])
def managerlanding():
    if session.get('status', None) == "manager":
        abort(403)
    else:
        return render_template('managerlanding.html')
@app.route("/permissions", methods=['POST','GET'])
def permissions():
    users = mongo.db.users
    userss = users.find_one({'Type' : 'User'})
    utype = ""
    if session.get('status', None) == "manager":
        abort(403)
    else:
        return render_template('permissions.html', utype = utype)
@app.route('/updateavailability/', methods=['POST', 'GET'])
def updateavailability():
        users = mongo.db.users
        usern = session['username']
        name = users.find_one({'username' : usern})['name']
        #user = request.form['username']
        #current_usern = users.find_one({'username' : user})
        if users.find_one({'username' : usern})['Sunday-Early'] == "Available":
            sune = "true"
        else:
            sune = "false"
            flash(sune)
        if users.find_one({'username' : usern})['Sunday-Late'] == "Available":
            sunl = "true"
        else:
            sunl = "false"
        if users.find_one({'username' : usern})['Monday-Early'] == "Available":
            mone = "true"
        else:
            mone = "false"
        if users.find_one({'username' : usern})['Monday-Late'] == "Available":
            monl = "true"
        else:
            monl = "false"
        if users.find_one({'username' : usern})['Tuesday-Early'] == "Available":
            tuee = "true"
        else:
            tuee = "false"
        if users.find_one({'username' : usern})['Tuesday-Late'] == "Available":
            tuel = "true"
        else:
            tuel = "false"
        if users.find_one({'username' : usern})['Wednesday-Early'] == "Available":
            wede = "true"
        else:
            wede = "false"
        if users.find_one({'username' : usern})['Wednesday-Late'] == "Available":
            wedl = "true"
            flash(wedl)
        else:
            wedl = "false"
        if users.find_one({'username' : usern})['Thursday-Early'] == "Available":
            thure = "true"
        else:
            thure = "false"
        if users.find_one({'username' : usern})['Thursday-Late'] == "Available":
            thul = "true"
        else:
            thul = "false"
        if users.find_one({'username' : usern})['Friday-Early'] == "Available":
            frie = "true"
        else:
            frie = "false"
        if users.find_one({'username' : usern})['Friday-Late'] == "Available":
            fril = "true"
        else:
            fril = "false"
        if users.find_one({'username' : usern})['Saturday-Early'] == "Available":
            sate = "true"
        else:
            sate = "false"
        if users.find_one({'username' : usern})['Saturday-Late'] == "Available":
            satl = "true"
        else:
            satl = "false"

            #request.form.getlist('sun_early')
            #flash(request.form.getlist('sun_early'))
        #return render_template('availability.html', sune = sune, name = name)
        #return render_template('availability.html', current_usern=current_usern)
@app.route("/workeravailability", methods=['POST','GET'])
def workeravailability():
    #if request.method == 'POST':
    users = mongo.db.users
    usern = session['username']
    name = users.find_one({'username' : usern})['name']
    existing_user = users.find_one({'username' : usern})
    #updateavailability()
    if users.find_one({'username' : usern})['Sunday-Early'] == "Available":
        sune = "true"
    else:
        sune = "false"
    if users.find_one({'username' : usern})['Sunday-Late'] == "Available":
        sunl = "true"
    else:
        sunl = "false"
    if users.find_one({'username' : usern})['Monday-Early'] == "Available":
        mone = "true"
    else:
        mone = "false"
    if users.find_one({'username' : usern})['Monday-Late'] == "Available":
        monl = "true"
    else:
        monl = "false"
    if users.find_one({'username' : usern})['Tuesday-Early'] == "Available":
        tuee = "true"
    else:
        tuee = "false"
    if users.find_one({'username' : usern})['Tuesday-Late'] == "Available":
        tuel = "true"
    else:
        tuel = "false"
    if users.find_one({'username' : usern})['Wednesday-Early'] == "Available":
        wede = "true"
    else:
        wede = "false"
    if users.find_one({'username' : usern})['Wednesday-Late'] == "Available":
        wedl = "true"
    else:
        wedl = "false"
    if users.find_one({'username' : usern})['Thursday-Early'] == "Available":
        thure = "true"
    else:
        thure = "false"
    if users.find_one({'username' : usern})['Thursday-Late'] == "Available":
        thul = "true"
    else:
        thul = "false"
    if users.find_one({'username' : usern})['Friday-Early'] == "Available":
        frie = "true"
    else:
        frie = "false"
    if users.find_one({'username' : usern})['Friday-Late'] == "Available":
        fril = "true"
    else:
        fril = "false"
    if users.find_one({'username' : usern})['Saturday-Early'] == "Available":
        sate = "true"
    else:
        sate = "false"
    if users.find_one({'username' : usern})['Saturday-Late'] == "Available":
        satl = "true"
    else:
        satl = "false"
    #test = mongo.db.users.find( { "Monday-Early": "Available" }  )

    #if users({existing_user},{'Monday-Early':'Available'}) return render_template('availability.html', name=name)  fuck this line, this line is a dick
    #if session.get('status', None) == "manager":
        #abort(403)
    #else:
    return render_template('availability.html', mone = mone, monl = monl, tuee = tuee, tuel = tuel, wedl=wedl, wede=wede, thure = thure, thul = thul, frie = frie, fril = fril, sate = sate, satl = satl, name = name)

@app.route("/userlanding", methods=['POST','GET'])
def userlanding():
    users = mongo.db.users
    usern = session['username']
    name = users.find_one({'username' : usern})['name']
    if users.find_one({'username' : usern})['Type'] != "User":
        abort(403)
    else:
        return render_template('userlanding.html', name = name)
        #return render_template('userlanding.html', name=name)
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords did not match. Please enter passwords again.")
            return redirect(url_for('register_page'))
        if existing_user is None:
            hashdpw = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username' : request.form['username'], 'name' : request.form['name'], 'password' : hashdpw,  'Type' : 'User', 'Monday-Early' : 'Not set', 'Monday-Late' : 'Not set', 'Tuesday-Early' : 'Not set', 'Tuesday-Late' : 'Not set', 'Wednesday-Early' : 'Not set', 'Wednesday-Late' : 'Not set', 'Thursday-Early' : 'Not set', 'Thursday-Late' : 'Not set', 'Friday-Early' : 'Not set', 'Friday-Late' : 'Not set', 'Saturday-Early' : 'Not set', 'Saturday-Late' : 'Not set', 'Sunday-Early' : 'Not set', 'Sunday-Late' : 'Not set' })
            session['username'] = request.form['username']
            session['name'] = request.form['name']
            return redirect(url_for('landing'))
	return render_template('landing.html')
@app.route('/searchforuser/', methods=['POST', 'GET'])
def searchforuser():
        users = mongo.db.users
        user = request.form['username']
        current_usern = users.find_one({'username' : user})
        utype = users.find_one({'username' : user})['Type']
        usernam = users.find_one({'username' : user})['name']
        #return redirect(url_for('permissions'))
        return render_template('permissions.html', current_usern=current_usern, usernam = usernam, utype = utype)
@app.route('/upgradeuser/', methods=['POST', 'GET'])
def upgradeuser():
        users = mongo.db.users
        user = request.form['username']
        current_usern = users.find_one({'username' : user})
        #utype = users.find_one({'username' : user})['Type']
        usernam = users.find_one({'username' : user})['name']
        users.update({'username':usernam},{"$set":{'Type':'Manager'}})
        #return redirect(url_for('permissions'))
        return render_template('permissions.html', current_usern=current_usern, usernam = usernam, utype = utype)
@app.route('/submit/', methods=['POST', 'GET'])
def sendavailability():
    if request.method == 'POST':
        users = mongo.db.users
        usern = session['username']
        #name = session['name']
        existing_user = users.find_one({'username' : usern})

        if request.form.getlist('mon_early') == [u'mon_early']:
            users.update({'username':usern},{"$set":{'Monday-Early':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Monday-Early':'Not Available'}})
        if request.form.getlist('mon_late') == [u'mon_late']:
            users.update({'username':usern},{"$set":{'Monday-Late':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Monday-Late':'Not Available'}})
        if request.form.getlist('tue_early') == [u'tue_early']:
            users.update({'username':usern},{"$set":{'Tuesday-Early':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Tuesday-Early':'Not Available'}})
        if request.form.getlist('tue_late') == [u'tue_late']:
            users.update({'username':usern},{"$set":{'Tuesday-Late':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Tuesday-Late':'Not Available'}})
        if request.form.getlist('wed_early') == [u'wed_early']:
            users.update({'username':usern},{"$set":{'Wednesday-Early':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Wednesday-Early':'Not Available'}})
        if request.form.getlist('wed_late') == [u'wed_late']:
            users.update({'username':usern},{"$set":{'Wednesday-Late':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Wednesday-Late':'Not Available'}})
        if request.form.getlist('thur_early') == [u'thur_early']:
            users.update({'username':usern},{"$set":{'Thursday-Early':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Thursday-Early':'Not Available'}})
        if request.form.getlist('thur_late') == [u'thur_late']:
            users.update({'username':usern},{"$set":{'Thursday-Late':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Thursday-Late':'Not Available'}})
        if request.form.getlist('fri_early') == [u'fri_early']:
            users.update({'username':usern},{"$set":{'Friday-Early':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Friday-Early':'Not Available'}})
        if request.form.getlist('fri_late') == [u'fri_late']:
            users.update({'username':usern},{"$set":{'Friday-Late':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Friday-Late':'Not Available'}})
        if request.form.getlist('sat_early') == [u'sat_early']:
            users.update({'username':usern},{"$set":{'Saturday-Early':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Saturday-Early':'Not Available'}})
        if request.form.getlist('sat_late') == [u'sat_late']:
            users.update({'username':usern},{"$set":{'Saturday-Late':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Saturday-Late':'Not Available'}})
        if request.form.getlist('sun_early') == [u'sun_early']:
            users.update({'username':usern},{"$set":{'Sunday-Early':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Sunday-Early':'Not Available'}})
        if request.form.getlist('sun_late') == [u'sun_late']:
            users.update({'username':usern},{"$set":{'Sunday-Late':'Available'}})
        else:
            users.update({'username':usern},{"$set":{'Sunday-Late':'Not Available'}})
        return redirect(url_for('landing'))
	return render_template('landing.html')
@app.route('/logout/')
def logout():
    session['user'] = ""
    session['status'] = ""
    flash('You have been logged out')
    return redirect(url_for('landing'))

@app.errorhandler(403)
def page_not_found(error4):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.secret_key = 'shhhhhhhh'
    app.run(ssl_context='adhoc', debug=True)
