from __future__ import print_function
from __future__ import division
from ortools.sat.python import cp_model
import random

from deap import base
from deap import creator
from deap import tools
""""
def generaterota():
    shifts_per_day = 2
    Days = 5
    Population = 100
    Generations = 10
    Crossover_prob = 0.2
    Mutation_prob = 0.1
    total_shifts = Days * shifts_per_day
    duplicate_shift = 1
    shift_assigned_on_non_available = 2
    less_than_5 = 3
    7_consecutive_shifts = 4
    shift_count = 5
    full_day

def calculate_fitness():
    breaches = 0
    duplicate_shift = 0
    shift_assigned_on_non_available = 0
    less_than_2_days_off = 0

    for employee_shifts in chain(*shift.values());
        if (shifts_per_week > 5):
            less_than_2_days_off = less_than_2_days_off +1
        else if (shifts_per_week < 5):
            less_than_5 = less_than_5 + 1
        if (consecutive_days == 7):
            7_consecutive_shifts = 7_consecutive_shifts + 5
        if(shifts_assinged_per_day > 1):
            full_day = full_day +1
    breaches = breaches + less_than_2_days_off
    breaches = breaches + full_day

"""
def geneticalgorithm(pop_count, generations_number,
       cx_prob, mut_prob, mut_change_shifts_prob,
       evaluate_func, total_shifts, shifts,
       shiftslot_to_day, shiftslot_to_dayslot,
       print_best_result, select_method=None):

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("random_shift", random.randint, 0, total_shifts - 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.random_shift, n=len(shifts))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # mate/crossover function
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=total_shifts - 1, indpb=mut_change_shifts_prob)
    toolbox.register("evaluate", evaluate_func)

    if select_method:
        select_func, select_kwargs = select_method
    else:
        select_func, select_kwargs = tools.selTournament, {'tournsize': 3}

    toolbox.register("select", select_func, **select_kwargs)

    pop = toolbox.population(n=pop_count)

    best_result = pop[0]

    # Calculate fitness for first generation
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)
        if ind.fitness.values > best_result.fitness.values:
            best_result = toolbox.clone(ind)

    print("Begining work")
    for gen in range(generation):
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = map(toolbox.clone, offspring)

        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_prob:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < mut_prob:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        current_best = tools.selBest(pop, k=1)[0]
        if current_best.fitness.values > best_result.fitness.values:
            best_result = toolbox.clone(ind)
    print("Generation finished")

    # Printing result
    def print_individual(ind):
        print("Fitness of schedule:", ind.fitness.values)

        print(toolbox.evaluate(ind, inverse=False))

        for index, shift in enumerate(shifts):
            shifttype = ind[index]
            day = timeslot_to_day(shifttype)
            slot = timeslot_to_dayslot(shifttype)
            print("Emmployee {} is on the {} shfit on {}".format(employee, shift, day))

    if print_best_result:
        print_individual(best_result)

    return best_result.fitness.values[0]
