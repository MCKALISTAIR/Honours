from __future__ import print_function
from __future__ import division
from itertools import chain
from geneticalgorithm import geneticalgorithm
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from wtforms import Form, StringField, SelectField
from bottle import route, run, template

from ortools.sat.python import cp_model
import random
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
import bcrypt
import pymongo
import random
import string
import pyperclip
import bcrypt
import os
import re
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
population = 10
crossover = 0.5
mutation = 0.5
ghg = 0
mutationc = 0.5
generation= 10
no_days = 7
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
            session['name']  = users.find_one({'username' : usern})['name']
            #session['user'] = "User"
            #session['status'] = "user"  ###NEED TO GET THIS BIT DIFFERING BETWEEN MANAGER AND USER, PROBS HAVE THE SYSTEM CHECK ACCOUNT PERMS
            session['type'] = users.find_one({'username' : usern})['Type']
            if session['type'] == 'Manager':
                flash(session['type'])
                return redirect(url_for('managerlanding'))
            else:
                flash(session['type'])
                return redirect(url_for('userlanding'))
    return redirect(url_for('login'))
@app.route("/managerlanding", methods=['POST','GET'])
def managerlanding():
    this_user = session['name']
    if session['type'] != 'Manager':
        abort(403)
    else:
        return render_template('managerlanding.html', this_user=this_user)
@app.route("/permissions", methods=['POST','GET'])
def permissions():
    users = mongo.db.users
    this_user = session['name']
    userss = users.find_one({'Type' : 'User'})
    utype = ""
    if session['type'] != 'Manager':
        abort(403)
    else:
        return render_template('permissions.html', utype = utype, this_user=this_user)
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

    #if users({existing_user},{'Monday-Early':'Available'}) return render_template('availability.html', name=name)
    if session['type'] == 'User' or session['type'] == 'Manager':
        return render_template('availability.html', mone = mone, monl = monl, tuee = tuee, tuel = tuel, wedl=wedl, wede=wede, thure = thure, thul = thul, frie = frie, fril = fril, sate = sate, satl = satl, sune=sune, sunl=sunl, name = name)
    else:
        abort(403)
@app.route("/rota", methods=['POST','GET'])
def generaterota():
    users = mongo.db.users
    myclient = pymongo.MongoClient("mongodb://MCKALISTAIR:Uacpad923!@ds145412.mlab.com:45412/users")
    accounts = db.users
    mydb = myclient["users"]
    mycol = mydb["users"]
    usern = session['username']
    name = users.find_one({'username' : usern})['name']

    class ShiftPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
        """Print intermediate solutions."""
        def __init__(self, shifts, number_of_employees, number_of_days, number_of_shifts, sols):

            cp_model.CpSolverSolutionCallback.__init__(self)
            self._shifts = shifts
            self._number_of_employees = number_of_employees
            self._number_of_days = number_of_days
            self._number_of_shifts = number_of_shifts
            self._solutions = set(sols)
            self._solution_count = 0

        def on_solution_callback(self):
            self._solution_count += 1
            if self._solution_count in self._solutions:
                print('Solution %i' % self._solution_count)
                for d in range(self._number_of_days):
                    #print('Day %i' % d)
                    if(d == 0):
                        print('Monday')
                    if(d == 1):
                        print('Tuesday')
                    if(d == 2):
                        print('Wednesday')
                    if(d == 3):
                        print('Thursday')
                    if(d == 4):
                        print('Friday')
                    if(d == 5):
                        print('Saturday')
                    if(d == 6):
                        print('Sunday')

                    for e in range(self._number_of_employees):
                        is_working = False
                        for s in range(self._number_of_shifts):
                            if self.Value(self._shifts[(e, d, s)]):
                                is_working = True
                                print('  Employee %i works shift %i' % (e, s))
                        if not is_working:
                            print('  Employee {} does not work'.format(e))
                print()

        def solution_count(self):
            return self._solution_count


    def mains():
        # Data.
        noofuser = 0
        usercounter = 0
        listofemps = []
        holdingpen = []
        shiftlist = []
        masterlist = []
        finallist = []
        for x in mycol.find({'Type' : "User"}):
            noofuser = noofuser + 1
        for record in mycol.find({'Type' : "User"}):
            listofemps.append(record)
            names = record['username']
            #finder = users.find_one({'username' : name})
            if users.find_one({'username' : names})['Sunday-Early'] == "Available":
                sune = 1
            else:
                sune = 0
            if users.find_one({'username' : names})['Sunday-Late'] == "Available":
                sunl = 1
            else:
                sunl = 0
            if users.find_one({'username' : names})['Monday-Early'] == "Available":
                mone = 1
            else:
                mone = 0
            if users.find_one({'username' : names})['Monday-Late'] == "Available":
                monl = 1
            else:
                monl = 0
            if users.find_one({'username' : names})['Tuesday-Early'] == "Available":
                tuee = 1
            else:
                tuee = 0
            if users.find_one({'username' : names})['Tuesday-Late'] == "Available":
                tuel = 1
            else:
                tuel = 0
            if users.find_one({'username' : names})['Wednesday-Early'] == "Available":
                wede = 1
            else:
                wede = 0
            if users.find_one({'username' : names})['Wednesday-Late'] == "Available":
                wedl = 1
            else:
                wedl = 0
            if users.find_one({'username' : names})['Thursday-Early'] == "Available":
                thure = 1
            else:
                thure = 0
            if users.find_one({'username' : names})['Thursday-Late'] == "Available":
                thul = 1
            else:
                thul = 0
            if users.find_one({'username' : names})['Friday-Early'] == "Available":
                frie = 1
            else:
                frie = 0
            if users.find_one({'username' : names})['Friday-Late'] == "Available":
                fril = 1
            else:
                fril = 0
            if users.find_one({'username' : names})['Saturday-Early'] == "Available":
                sate = 1
            else:
                sate = 0
            if users.find_one({'username' : names})['Saturday-Late'] == "Available":
                satl = 1
            else:
                satl = 0
            holdingpen1 = [users.find_one({'username' : names})['Employee Number'],sune,sunl]
            holdingpen2 = [users.find_one({'username' : names})['Employee Number'],mone,monl]
            holdingpen3 = [users.find_one({'username' : names})['Employee Number'],tuee,tuel]
            holdingpen4 = [users.find_one({'username' : names})['Employee Number'],wede,wedl]
            holdingpen5 = [users.find_one({'username' : names})['Employee Number'],thure,thul]
            holdingpen6 = [users.find_one({'username' : names})['Employee Number'],frie,fril]
            holdingpen7 = [users.find_one({'username' : names})['Employee Number'],sate,satl]
            shiftlist.append(holdingpen1)
            shiftlist.append(holdingpen2)
            shiftlist.append(holdingpen3)
            shiftlist.append(holdingpen4)
            shiftlist.append(holdingpen5)
            shiftlist.append(holdingpen6)
            shiftlist.append(holdingpen7)
            holdingpen1 = []
            holdingpen2 = []
            holdingpen3 = []
            holdingpen4 = []
            holdingpen5 = []
            holdingpen6 = []
            holdingpen7 = []
            masterlist.append(shiftlist)
            shiftlist = []
        #flash(masterlist[0][1])
        number_of_employees = noofuser
        number_of_shifts = 2
        number_of_days = 7
        all_employees = range(number_of_employees)
        all_shifts = range(number_of_shifts)
        all_days = range(number_of_days)
        availability_list = masterlist
        flash(availability_list)
        # Creates the model.
        model = cp_model.CpModel()

        # Creates shift variables.
        # shifts[(n, d, s)]: employee 'n' works shift 's' on day 'd'.
        shifts = {}
        for e in all_employees:
            for d in all_days:
                for s in all_shifts:
                    shifts[(e, d, s)] = model.NewBoolVar('shift_e%id%is%i' % (e, d,
                                                                              s))

        # Each shift is assigned to exactly one employee in the schedule period.
        for d in all_days:
            for s in all_shifts:
                model.Add(sum(shifts[(e, d, s)] for e in all_employees) == 1)

        # Each employee works at most one shift per day.
        for e in all_employees:
            for d in all_days:
                model.Add(sum(shifts[(e, d, s)] for s in all_shifts) <= 1)

        # min_shifts_per_employee is the largest integer such that every employee
        # can be assigned at least that many shifts. If the number of employees doesn't
        # divide the total number of shifts over the schedule period,
        # some employees have to work one more shift, for a total of
        # min_shifts_per_employee + 1.
        min_shifts_per_employee = (number_of_shifts * number_of_days) // number_of_employees
        max_shifts_per_employee = min_shifts_per_employee + 1
        for n in all_employees:
            num_shifts_worked = sum(
                shifts[(e, d, s)] for d in all_days for s in all_shifts)
            model.Add(min_shifts_per_employee <= num_shifts_worked)
            model.Add(num_shifts_worked <= max_shifts_per_employee)
        solver = cp_model.CpSolver()
        a_few_solutions = range(5)
        solution_printer = ShiftPartialSolutionPrinter(
        shifts, number_of_employees, number_of_days, number_of_shifts, a_few_solutions)
        solver.SearchForAllSolutions(model, solution_printer)

        model.Maximize(
            sum(availability_list[e][d][s] * shifts[(e, d, s)] for e in all_employees
                for d in all_days for s in all_shifts))
        flash(model)

        solver = cp_model.CpSolver()
        solver.Solve(model)
        for d in all_days:
            if(d == 0):
                print('Monday')
            if(d == 1):
                print('Tuesday')
            if(d == 2):
                print('Wednesday')
            if(d == 3):
                print('Thursday')
            if(d == 4):
                print('Friday')
            if(d == 5):
                print('Saturday')
            if(d == 6):
                print('Sunday')
            for e in all_employees:
                for s in all_shifts:
                    flash(solver.Value(shifts[(e, d, s)]))
                    if solver.Value(shifts[(e, d, s)]) == 1:
                        if availability_list[e][d][s] == 1:
                            print('Employee', e, 'works shift', s, '(Available).')
                        else:
                            print('Employee', e, 'works shift', s, '(Not Available).')
            print()
        print()
        flash(shifts)
        flash(solver.ObjectiveValue())
             # '(out of', number_of_employees * min_shifts_per_employee, ')')
        print()
        print('Stats')
        print('  - Number of shift requests met = %i' % solver.ObjectiveValue(), '(out of', number_of_employees * 7, ')')
        print('  - conflicts       : %i' % solver.NumConflicts())
        print('  - branches        : %i' % solver.NumBranches())
        print('  - wall time       : %f ms' % solver.WallTime())
        print('  - solutions found : %i' % solution_printer.solution_count())
        conflicts = solver.NumConflicts()
        shiftsmet = solver.ObjectiveValue()
        outof = number_of_employees * min_shifts_per_employee
        shiftfitness = shiftsmet/outof
        fitness(outof, conflicts, shiftsmet)

    mains()

    if session['type'] == 'Manager':
        abort(403)
    else:
        return render_template('rota.html', name = name)

def fitness(outof, conflicts, shiftsmet):
    fitness = 0
    flash(outof)
    flash(conflicts)
    fitness = fitness - conflicts
    print("Fitness: ")
    print(fitness)
    return fitness

@app.route("/userlanding", methods=['POST','GET'])
def userlanding():
    users = mongo.db.users
    usern = session['username']
    name = users.find_one({'username' : usern})['name']
    if session['type'] != 'User':
        abort(403)
    else:
        return render_template('userlanding.html', name = name)
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
        number_counter = users.find_one({'username' : "Counter"})['Employee Number Main']
        number_counter = number_counter + 1
        users.update({'username':"Counter"},{"$set":{'Employee Number Main':number_counter}})
        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords did not match. Please enter passwords again.")
            return redirect(url_for('register_page'))
        if existing_user is None:
            hashdpw = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username' : request.form['username'], "Employee Number": number_counter, 'name' : request.form['name'], 'password' : hashdpw,  'Type' : 'User', 'Monday-Early' : 'Not set', 'Monday-Late' : 'Not set', 'Tuesday-Early' : 'Not set', 'Tuesday-Late' : 'Not set', 'Wednesday-Early' : 'Not set', 'Wednesday-Late' : 'Not set', 'Thursday-Early' : 'Not set', 'Thursday-Late' : 'Not set', 'Friday-Early' : 'Not set', 'Friday-Late' : 'Not set', 'Saturday-Early' : 'Not set', 'Saturday-Late' : 'Not set', 'Sunday-Early' : 'Not set', 'Sunday-Late' : 'Not set' })
            session['username'] = request.form['username']
            session['name'] = request.form['name']
            return redirect(url_for('landing'))
	return render_template('landing.html')
@app.route('/searchforuser/', methods=['POST', 'GET'])
def searchforuser():
        users = mongo.db.users
        user = request.form['username']
        session['user'] = user
        this_user = session['name']
        current_usern = users.find_one({'username' : user})
        utype = users.find_one({'username' : user})['Type']
        usernam = users.find_one({'username' : user})['name']
        return render_template('permissions.html', current_usern=current_usern, usernam = usernam, utype = utype, user=user, this_user=this_user)
@app.route('/upgradeuser/', methods=['POST', 'GET'])
def upgradeuser():
        users = mongo.db.users
        #user = user
        user = session.get('user', None)
        current_usern = users.find_one({'username' : user})
        utype = users.find_one({'username' : user})['Type']
        usernam = users.find_one({'username' : user})['name']

        utype2 = users.find_one({'username' : user})['Type']
        users.update({'username':usernam},{"$set":{'Type':'Manager'}})
        flash("Account upgrade succesfull")
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
