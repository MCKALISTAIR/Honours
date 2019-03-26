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
import time
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
import copy
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
def fillshiftlist():
    users = mongo.db.users
    myclient = pymongo.MongoClient("mongodb://MCKALISTAIR:Uacpad923!@ds145412.mlab.com:45412/users")
    accounts = db.users
    mydb = myclient["users"]
    mycol = mydb["users"]
    usern = session['username']
    name = users.find_one({'username' : usern})['name']
    listofemps = []
    holdingpen = []
    shiftlist = []
    masterlist = []
    finallist = []
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
    return masterlist
@app.route("/generate", methods=['POST','GET'])
def generate():

    if session['type'] == 'Manager':
        abort(403)
    else:
        return render_template('generate.html')

def inversemutation(subject):
    print("INVERSE")
    mutation_values = random.sample(set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]), 2)
    shift_extraction = []
    for x in subject:
        shift_extraction.append(x[1])
    choices = random.sample(set([2,4,6,8,10,12,14,16,18,20]), 2)
    if choices[0]>choices[1]:
        first_choice = choices[0]
        second_choice = choices[1]
    else:
        first_choice = choices[1]
        second_choice = choices[0]
    section_to_remove = shift_extraction[second_choice:first_choice]
    first_part = shift_extraction[0:second_choice]
    second_part = shift_extraction[first_choice:]
    section_to_remove.reverse()
    mutated_section = section_to_remove
    for i in mutated_section:
        first_part.append(i)
    for i in second_part:
        first_part.append(i)
    i = 0
    for x in subject:
        x[1] = first_part[i]
        i+=1
    return subject
mutated_subject = None
@app.route("/rota", methods=['POST','GET'])
def generaterota():

    selection = request.form.get('Selection')
    crossover = request.form.get('Crossover')
    mutation = request.form.get('Mutation')
    users = mongo.db.users
    myclient = pymongo.MongoClient("mongodb://MCKALISTAIR:Uacpad923!@ds145412.mlab.com:45412/users")
    accounts = db.users
    mydb = myclient["users"]
    mycol = mydb["users"]
    usern = session['username']
    name = users.find_one({'username' : usern})['name']
    conflicts = 0
    bestfitness = 0
    generation = 0
    thisrota = []
    holdingcell = []
    population = []
    #availability_fitness = 0
    solutionsfound = 0
    namelist = []
    #ename = users.find_one({'Employee Number' : e})['name']
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
            #self.availability_fitness = 0

        def on_solution_callback(self):
            self._solution_count += 1
            availability_fitness = function()
            shiftsmet = smfunction()
            if self._solution_count in self._solutions:
                print('Solution %i' % self._solution_count)
                i=0
                print(i)
                print("i")
                for d in range(self._number_of_days):
                    if(d == 0):
                        day = 'Monday'
                        print()
                        print('Monday')
                    if(d == 1):
                        day = 'Tuesday'
                        print()
                        print('Tuesday')
                    if(d == 2):
                        day = 'Wednesday'
                        print()
                        print('Wednesday')
                    if(d == 3):
                        day = 'Thursday'
                        print()
                        print('Thursday')
                    if(d == 4):
                        day = 'Friday'
                        print()
                        print('Friday')
                    if(d == 5):
                        day = 'Saturday'
                        print()
                        print('Saturday')
                    if(d == 6):
                        day = 'Sunday'
                        print()
                        print('Sunday')
                    for x in nolist:
                        enames = users.find_one({'Employee Number' : x})['name']
                        namelist.append(enames)
                    for e in range(self._number_of_employees):
                            ename = namelist[e]
                            is_working = False
                            for s in range(self._number_of_shifts):
                                if self.Value(self._shifts[(e, d, s)]):
                                    is_working = True
                                    if s == 0:
                                        s = "early shift"
                                        shift = "-Early"
                                    else:
                                        s = "late shift"
                                        shift = "-Late"
                                    combined = day + shift
                                    print(ename + ' works the ' + s)
                                    if users.find_one({'username' : ename})[combined] == "Not Available":
                                        print("a")
                                        availability_fitness -= 10
                                    else:
                                        print("aa")
                                        availability_fitness += 10
                                        print("aaa")
                                        shiftsmet +=1
                                        print("aaaa")
                                    print(availability_fitness)
                                    print("avup")
                                    thisrota.append([ename,d,s])
                            if not is_working:
                                print('{} does not work'.format(ename))
                                s = "Off"
                                thisrota.append([ename,d,s])
                            if i == 20:
                                fit = availability_fitness + shiftsmet
                                thisrota.append(fit)
                                holdingcell.append(thisrota[:])
                                thisrota[:] = []
                                i = 0
                            i+=1


            thisfitness = availability_fitness
            #if self._solution_count in self._solutions:
                #print('Solution %i' % self._solution_count)
                #print("calling fitness")
            #function()
                    #avf = self.availability_fitness ADD 22

        def solution_count(self):
            return self._solution_count, thisrota, shiftsmet


    #def mains(conflicts, solutionsfound):
        # Data
    noofuser = 0
    n = 5
    sol = 1
    solution_lists = [[] for i in range(0, n)]
    usercounter = 0
    for x in mycol.find({'Type' : "User"}):
        noofuser = noofuser + 1
    fillshiftlist()
    nolist = []
    namelist = []
    mycol2 = mydb["users"]
    for record in mycol2.find({'Type' : "Manager"}):
	       mycol2.delete_one(record)
    for record in mycol2.find({'Type' : "User"}):
	       nolist.append(record["Employee Number"])
    number_of_employees = len(nolist)
    number_of_shifts = 2
    number_of_days = 7
    all_employees = range(number_of_employees)
    all_shifts = range(number_of_shifts)
    all_days = range(number_of_days)
    masterlist = fillshiftlist()
    availability_list = masterlist
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


    shiftsmet = solver.ObjectiveValue()
    print()
    print('Stats')
    print('  - Number of shift requests met = %i' % shiftsmet, '(out of', number_of_employees * 7, ')')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f ms' % solver.WallTime())


    #print('  - solutions found : %i' % solution_printer.solution_count())
    conflicts = solver.NumConflicts()

    timet = solver.WallTime()
    #solutionsfound = solution_printer.solution_count()
    outof = number_of_employees * min_shifts_per_employee
    shiftfitness = shiftsmet/outof
    #fitness(outof, conflicts, shiftsmet)

    population.append(holdingcell)
    print(population)
    thisrota[:] = []
    solution_count = 0
    list_of_solutions = []
    '''
    if selection == "Tournament":
        tournamentselection(population, crossover, mutation)
    elif selection == "Random":
        randomselection(population, crossover, mutation)
    '''
    while solution_count !=5:
        start = time.time()
        if selection == "Tournament":
            print("Tournament")
            tournamentselection(population, crossover, mutation)
        elif selection == "Random":
            print("Random")
            randomselection(population, crossover, mutation)
        end = time.time()
        solution_count += 1
        print("Solution")
        print(solution_count)
        print("time")
        print(end - start)
        global mutated_subject
        print(mutated_subject)
        '''
        if mutation == "Swap":
            mutated_subject = swapmutation(subject)
        elif mutation == "Inverse":
            subject = inversemutation(subject)
        '''



        fitlist = []
        i = 0
        for x in population:
            print(x)
            fitlist.append(x[i][21])
            i+=1
        min_fit_index = fitlist.index(min(fitlist))
        min_fit = min(fitlist)
        if fit > min_fit:
            population[0][min_fit_index] = mutated_subject



    print("DONE")
    #fitness(outof, conflicts, shiftsmet,generation, time, thisrota)
    #thisfitness = fitness(outof, conflicts, shiftsmet, generation, time, thisrota)
    #if thisfitness > 0:
    #    bestfitness = thisfitness
    if session['type'] == 'Manager':
        abort(403)
    else:
        return render_template('rota.html', name = name, conflicts=conflicts, shiftsmet=shiftsmet, solutionsfound=solutionsfound, thisrota = thisrota, population=population, crossover = crossover, mutation = mutation)
def fitness(shiftsmet, availability_fitness):
    fitness = shiftsmet + availability_fitness
    return fitness
def advanced_fitness():
    employee_extraction = [x[2] for x in this_rota[0]]
    shift_extraction = [x[1] for x in this_rota[0]]
    day_extraction = [x[0] for x in this_rota[0]]
    for x in employee_extraction:
        num = users.find_one({'Employee Number' : x})
        for y in day_extraction:
            if(d == 0):
                day = 'Monday'
            if(d == 1):
                day = 'Tuesday'
            if(d == 2):
                day = 'Wednesday'
            if(d == 3):
                day = 'Thursday'
            if(d == 4):
                day = 'Friday'
            if(d == 5):
                day = 'Saturday'
            if(d == 6):
                day = 'Sunday'
            for z in shift_extraction:
                if z == 0:
                    shift = "Off"
                elif z == 1:
                    shift = "-early"
                elif z == 2:
                    shift = "-late"
        combined = day + shift
        if users.find_one({'Employee Number' : num})[combined] == "Available":
            availability_fitness += 10
        else:
            availability_fitness += 10

def function():
    availability_fitness = 0
    return availability_fitness
def smfunction():
    shiftsmet = 0
    return shiftsmet

def tournamentselection(population, crossover, mutation):
    print("TOURNAMENT")
    firstwinner = None
    secondwinner = None
    loop = 0
    while loop != 2:
        choices = random.sample(set([0, 1, 2, 3]), 4)
        one = choices[0]
        two = choices[1]
        three = choices[2]
        four = choices[3]
        print(population[0][1])
        contenderone = population[0][one]
        contendertwo = population[0][two]
        contenderthree = population[0][three]
        contenderfour = population[0][four]
        print("3")
        print(contenderone)
        print(contenderone[20])
        contenderone_fitness = contenderone[21]
        contendertwo_fitness = contendertwo[21]
        contenderthree_fitness = contenderthree[21]
        contenderfour_fitness = contenderfour[21]
        if contenderone_fitness == contendertwo_fitness:
            firstwinner = contenderone
            loop += 1
        elif contendertwo_fitness > contenderone_fitness:
            firstwinner = contendertwo
            loop += 1
        else:
            loop = 0
        if contenderthree_fitness == contenderfour_fitness:
            secondwinner = contenderthree
            loop += 1
        elif contenderfour_fitness > contenderthree_fitness:
            secondwinner = contenderfour
            loop += 1
        else:
            loop = 0
    if crossover == "Two point":
        twopointcrossover(firstwinner, secondwinner, mutation)
    elif crossover == "Partially mapped":
        partiallymappedcrossover(firstwinner, secondwinner, mutation)
    return firstwinner, secondwinner
def randomselection(population, crossover, mutation):
    print("RANDOM")
    choices = random.sample(set([0, 1, 2, 3]), 2)
    one = choices[0]
    two = choices[1]
    firstwinner = population[0][one]
    secondwinner = population[0][two]
    if crossover == "Two point":
        twopointcrossover(firstwinner, secondwinner, mutation)
    elif crossover == "Partially mapped":
        partiallymappedcrossover(firstwinner, secondwinner, mutation)
    return firstwinner, secondwinner

def partiallymappedcrossover(firstwinner, secondwinner, mutation):
    print("PARTIALY MAPPED")
    firstwinner.pop(21)
    secondwinner.pop(21)
    first_shift_extraction = []
    second_shift_extraction = []
    for x in firstwinner:
        first_shift_extraction.append(x[1])
    for x in secondwinner:
        second_shift_extraction.append(x[1])
    choices = random.sample(set([1,6,11,16,20]), 2)
    if choices[0]>choices[1]:
        second_point = choices[0]
        first_point = choices[1]
    else:
        second_point = choices[1]
        first_point = choices[0]
    swath = []
    swath = first_shift_extraction[second_point:first_point]

    i=0
    r=0
    value = 0
    while terminate == 0:
        if r != 0:
            p1_value = swath[p2_index]
            if p1_value in second_shift_extraction:
                if p1_value in swath:
                    value = p1_value
                else:
                    found_you = second_shift_extraction.index(p1_value)
                    child.insert(found_you, value_to_insert)
        else:
            while found == 0:
                for v in swath:
                    swath_value = swath[i]
                    for x in second_shift_extraction[second_point:first_point]:
                        if swath_value != x:
                            related_value = x #to insert
                            related_index = second_shift_extraction.index(related_value)
                            found = 1
                        else:
                            found = 0
                            i+=1
                print("Not found")
            p1_index_value = first_shift_extraction[related_index]
            value_to_insert = x


        if p1_index_value in second_shift_extraction[second_point:first_point]:
            p2_index = second_shift_extraction[second_point:first_point].index(p1_index_value)
            if p2_index in swath:
                value = p2_index
                r = 1






    index = first_shift_extraction.index(swath[i])
    value = first_shift_extraction[index]

    parent2_index = second_shift_extraction.index()
    #parent2_value = second_shift_extraction[]
    if mutation == "Swap":
        swapmutation(subject)
    elif mutation == "Inverse":
        inversemutation(subject)
    return first_child

def onepointcrossover(firstwinner, secondwinner):
    first_shift_extraction = []
    first_shift_extraction = [item[0] for item in firstwinner]
    print(first_shift_extraction)
    second_shift_extraction = [x[1] for x in secondwinner[0]]
    crossover_value = random.randint(1,19)
    firsthalf = first_shift_extraction[0:crossover_value]
    thirdhalf = first_shift_extraction[:crossover_value]
    secondhalf = second_shift_extraction[:crossover_value]
    fourthhalf = second_shift_extraction[:crossover_value]
    thirdhalf.append(secondhalf)
    firsthalf.append(secondhalf)
    first_child = firsthalf
    secondchild = thirdhalf
    return first_child
def twopointcrossover(firstwinner, secondwinner, mutation):
    print("TWO POINT")
    firstwinner.pop(21)
    secondwinner.pop(21)
    first_shift_extraction = []
    second_shift_extraction = []
    for x in firstwinner:
        first_shift_extraction.append(x[1])
    for x in secondwinner:
        second_shift_extraction.append(x[1])
    choices = random.sample(set([2, 4, 6, 8, 10, 12, 14, 16, 18, 20]), 2)
    if choices[0]>choices[1]:
        first_choice = choices[0]
        second_choice = choices[1]
    else:
        first_choice = choices[1]
        second_choice = choices[0]
    holdingcell = []
    holdingcell2 = []
    first_child = []
    first_section_to_remove = first_shift_extraction[second_choice:first_choice]
    second_section_to_remove = second_shift_extraction[second_choice:first_choice]
    first_section = first_shift_extraction[0:second_choice]
    second_section = first_shift_extraction[first_choice:]
    for i in second_section_to_remove:
        first_section.append(i)
    for i in second_section:
        first_section.append(i)
    first_child = first_section
    i = 0
    for x in firstwinner:
        print(x)
        x[1] = first_child[i]
        i+=1
    subject = firstwinner
    if mutation == "Swap":
        swapmutation(subject)
    elif mutation == "Inverse":
        inversemutation(subject)
    return first_child
def swapmutation(subject):
    print("SWAP")
    print(subject)
    mutation_values = random.sample(set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]), 2)
    value_one = mutation_values[0]
    value_two = mutation_values[1]
    first_to_swap = subject[value_one][1]
    second_to_swap = subject[value_two][1]
    subject[value_one][1] = second_to_swap
    subject[value_two][1] = first_to_swap
    global mutated_subject
    mutated_subject = subject
    return subject

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
