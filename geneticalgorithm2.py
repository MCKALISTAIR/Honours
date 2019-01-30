from __future__ import print_function
from __future__ import division
from ortools.sat.python import cp_model
import random

class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions.

@app.route("/rota", methods=['POST','GET'])
def generaterota():
    users = mongo.db.users
    myclient = pymongo.MongoClient("mongodb://MCKALISTAIR:Uacpad923!@ds145412.mlab.com:45412/users")
    accounts = db.users
    mydb = myclient["users"]
    mycol = mydb["users"]
    usern = session['username']
    name = users.find_one({'username' : usern})['name']
#lists for available shifts
    sune = []
    sunl = []
    mone = []
    monl = []
    tuee = []
    tuel = []
    wede = []
    wedl = []
    thure = []
    thurl = []
    frie = []
    fril = []
    sate = []
    satl = []
#lists for not available shifts
    sunen = []
    sunln = []
    monen = []
    monln = []
    tueen = []
    tueln = []
    weden = []
    wedln = []
    thuren = []
    thurln = []
    frien = []
    friln = []
    saten = []
    satln = []
    listofusers = []
    for x in mycol.find({'Type' : "User"}):
        listofusers.append(x)
    liste = []
    cursor = accounts.find()
    for x in mycol.find({'Sunday-Early': 'Available'}):
        sune.append(x["username"])
    for x in mycol.find({'Sunday-Late': 'Available'}):
        sunl.append(x["username"])
    for x in mycol.find({'Monday-Early': 'Available'}):
        mone.append(x["username"])
    for x in mycol.find({'Monday-Late': 'Available'}):
        monl.append(x["username"])
    for x in mycol.find({'Tuesday-Early': 'Available'}):
        tuee.append(x["username"])
    for x in mycol.find({'Tuesday-Late': 'Available'}):
        tuel.append(x["username"])
    for x in mycol.find({'Wednesday-Early': 'Available'}):
        wede.append(x["username"])
    for x in mycol.find({'Wednesday-Late': 'Available'}):
        wedl.append(x["username"])
    for x in mycol.find({'Thursday-Early': 'Available'}):
        thure.append(x["username"])
    for x in mycol.find({'Thursday-Late': 'Available'}):
        thurl.append(x["username"])
    for x in mycol.find({'Friday-Early': 'Available'}):
        frie.append(x["username"])
    for x in mycol.find({'Friday-Late': 'Available'}):
        fril.append(x["username"])
    for x in mycol.find({'Saturday-Early': 'Available'}):
        sate.append(x["username"])
    for x in mycol.find({'Saturday-Late': 'Available'}):
        satl.append(x["username"])

    for x in mycol.find({'Sunday-Early': 'Not Available'}):
        sunen.append(x["username"])
    for x in mycol.find({'Sunday-Late': 'Not Available'}):
        sunln.append(x["username"])
    for x in mycol.find({'Monday-Early': 'Not Available'}):
        monen.append(x["username"])
    for x in mycol.find({'Monday-Late': 'Not Available'}):
        monln.append(x["username"])
    for x in mycol.find({'Tuesday-Early': 'Not Available'}):
        tueen.append(x["username"])
    for x in mycol.find({'Tuesday-Late': 'Not Available'}):
        tueln.append(x["username"])
    for x in mycol.find({'Wednesday-Early': 'Not Available'}):
        weden.append(x["username"])
    for x in mycol.find({'Wednesday-Late': 'Not Available'}):
        wedln.append(x["username"])
    for x in mycol.find({'Thursday-Early': 'Not Available'}):
        thuren.append(x["username"])
    for x in mycol.find({'Thursday-Late': 'Not Available'}):
        thurln.append(x["username"])
    for x in mycol.find({'Friday-Early': 'Not Available'}):
        frien.append(x["username"])
    for x in mycol.find({'Friday-Late': 'Not Available'}):
        friln.append(x["username"])
    for x in mycol.find({'Saturday-Early': 'Not Available'}):
        saten.append(x["username"])
    for x in mycol.find({'Saturday-Late': 'Not Available'}):
        satln.append(x["username"])
    existing_user = users.find_one({'username' : usern})
    shifts_per_day = 2
    total_shifts = 14
    shifts=10
    #updateavailability()
    if users.find_one({'username' : usern})['Sunday-Early'] == "Available":
        sune = 1
    else:
        sune = 0
    if users.find_one({'username' : usern})['Sunday-Late'] == "Available":
        sunl = 1
    else:
        sunl = 0
    if users.find_one({'username' : usern})['Monday-Early'] == "Available":
        mone = 1
    else:
        mone = 0
    if users.find_one({'username' : usern})['Monday-Late'] == "Available":
        monl = 1
    else:
        monl = 0
    if users.find_one({'username' : usern})['Tuesday-Early'] == "Available":
        tuee = 1
    else:
        tuee = 0
    if users.find_one({'username' : usern})['Tuesday-Late'] == "Available":
        tuel = 1
    else:
        tuel = 0
    if users.find_one({'username' : usern})['Wednesday-Early'] == "Available":
        wede = 1
    else:
        wede = 0
    if users.find_one({'username' : usern})['Wednesday-Late'] == "Available":
        wedl = 1
    else:
        wedl = 0
    if users.find_one({'username' : usern})['Thursday-Early'] == "Available":
        thure = 1
    else:
        thure = 0
    if users.find_one({'username' : usern})['Thursday-Late'] == "Available":
        thul = 1
    else:
        thul = 0
    if users.find_one({'username' : usern})['Friday-Early'] == "Available":
        frie = 1
    else:
        frie = 0
    if users.find_one({'username' : usern})['Friday-Late'] == "Available":
        fril = 1
    else:
        fril = 0
    if users.find_one({'username' : usern})['Saturday-Early'] == "Available":
        sate = 1
    else:
        sate = 0
    if users.find_one({'username' : usern})['Saturday-Late'] == "Available":
        satl = 1
    else:
        satl = 0

    '''
    geneticalgorithm(population=population,
       generation=generation,
       crossover=crossover,
       mutation=mutation,
       mutationc=mutationc,
       geneticalgorithm=geneticalgorithm,
       shifts_per_day=shifts_per_day,
       total_shifts = total_shifts,
       shifts=shifts,
       #timeslot_to_day=timeslot_to_day,
       #timeslot_to_dayslot=timeslot_to_dayslot,
       best_result=True)
       '''

    if session['type'] == 'Manager':
        abort(403)
    else:
        return render_template('rota.html', name = name)

    """

    def __init__(self, shifts, num_nurses, num_days, num_shifts, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_nurses = num_nurses
        self._num_days = num_days
        self._num_shifts = num_shifts
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        self._solution_count += 1
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            for d in range(self._num_days):
                print('Day %i' % d)
                for n in range(self._num_nurses):
                    is_working = False
                    for s in range(self._num_shifts):
                        if self.Value(self._shifts[(n, d, s)]):
                            is_working = True
                            print('  Nurse %i works shift %i' % (n, s))
                    if not is_working:
                        print('  Nurse {} does not work'.format(n))
            print()

    def solution_count(self):
        return self._solution_count




def main():
    # Data.
    num_nurses = 4
    num_shifts = 3
    num_days = 3
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)
    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d,
                                                                          s))

    # Each shift is assigned to exactly one nurse in the schedule period.
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_nurses) == 1)

    # Each nurse works at most one shift per day.
    for n in all_nurses:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)

    # min_shifts_per_nurse is the largest integer such that every nurse
    # can be assigned at least that many shifts. If the number of nurses doesn't
    # divide the total number of shifts over the schedule period,
    # some nurses have to work one more shift, for a total of
    # min_shifts_per_nurse + 1.
    min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
    max_shifts_per_nurse = min_shifts_per_nurse + 1
    for n in all_nurses:
        num_shifts_worked = sum(
            shifts[(n, d, s)] for d in all_days for s in all_shifts)
        model.Add(min_shifts_per_nurse <= num_shifts_worked)
        model.Add(num_shifts_worked <= max_shifts_per_nurse)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    # Display the first five solutions.
    a_few_solutions = range(5)
    solution_printer = NursesPartialSolutionPrinter(
        shifts, num_nurses, num_days, num_shifts, a_few_solutions)
    solver.SearchForAllSolutions(model, solution_printer)

    # Statistics.
    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f ms' % solver.WallTime())
    print('  - solutions found : %i' % solution_printer.solution_count())
