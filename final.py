#!/usr/bin/env python3

__author__ = "nicoroble"
__version__ = "0.1.0"
__license__ = "MIT"

import threading
import sys, getopt
import algorithms as optimizer
import pandas as pd
import os

class_slot_size = 3

RUNS = 1000

# (classname, student slots)
classes = ['Optimization_Theory',
           'Machine_Learning',
           'Quantum_Computing',
           'Computer_Architecture',
           'Operating_Systems',
           'Security',
           'International_Relations',
           'Business_Management',
           'Web_Design'
           ]

students = [('Nikko', ('Optimization_Theory', 'Machine_Learning', 'Quantum_Computing')),
            ('Hideo', ('Optimization_Theory', 'Machine_Learning', 'Quantum_Computing')),
            ('Mioto', ('Optimization_Theory', 'Machine_Learning', 'Quantum_Computing')),
            ('Bradley', ('Computer_Architecture', 'Operating_Systems', 'Security')),
            ('Leojojo', ('Computer_Architecture', 'Operating_Systems', 'Security')),
            ('Korry', ('Computer_Architecture', 'Operating_Systems', 'Security')),
            ('Erika', ('International_Relations', 'Business_Management', 'Web_Design')),
            ('Leonard', ('International_Relations', 'Business_Management', 'Web_Design')),
            ('Aimi', ('International_Relations', 'Business_Management', 'Web_Design'))
            ]


def print_solution(vector):
    slots = []

    for i in range(len(classes)):
        slots += [i] * 3

    i = 0

    while i < len(vector):
        x1 = int(vector[i])
        x2 = int(vector[i + 1])
        x3 = int(vector[i + 2])
        to_be_removed = [x1, x2, x3]

        class_1 = classes[slots[x1]]
        class_2 = classes[slots[x2]]
        class_3 = classes[slots[x3]]
        chosen_classes = [class_1, class_2, class_3]

        student = students[i][0] if i == 0 else students[int(i / 3)][0]

        print("Student: {}\nChosen Classes:{}, {}, {}".format(student, class_1, class_2, class_3))

        slots = [i for j, i in enumerate(slots) if j not in to_be_removed]
        i += 3
    print("\n")


def classes_cost(vector):
    cost = 0
    slots = []

    for i in range(len(classes)):
        slots += [i] * 3

    i = 0

    while i < len(vector):
        x1 = int(vector[i])
        x2 = int(vector[i + 1])
        x3 = int(vector[i + 2])
        to_be_removed = [x1, x2, x3]

        class_1 = classes[slots[x1]]
        class_2 = classes[slots[x2]]
        class_3 = classes[slots[x3]]
        chosen_classes = [class_1, class_2, class_3]

        preferences = students[i][1] if i == 0 else students[int(i / 3)][1]

        #  punishments for invalid solutions
        if class_1 == class_2:
            cost += 100
        if class_2 == class_3:
            cost += 100
        if class_1 == class_3:
            cost += 100

        for chosen_class in chosen_classes:
            if chosen_class in preferences:
                cost += 0
            else:
                cost += 5
        slots = [i for j, i in enumerate(slots) if j not in to_be_removed]
        i += 3

    return cost


def usage():
    print('-t = bool\tused to run multiple threads and store results if true')
    print('-r = bool\tused to read resulting csv files')
    print('-n = int\tspecify number of threads for each optimization algorithm')
    print('-f = string\tspecify which csv file to read')


def str2bool(v):
    return v.lower() in ("true")


def main(opts):
    num = 10
    csv_file = 'results'
    thread_test = False
    read_results = False

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-t', '--threading'):
            thread_test = str2bool(arg)
        elif opt in ('-n', '--num'):
            num = int(arg)
        elif opt in ('-r', '--results'):
            read_results = str2bool(arg)
            print(read_results)
        elif opt in ('-f', '--file'):
            read_results = arg
        else:
            usage()
            sys.exit(2)

    classes_domain = []

    s_optimal = [6, 3, 0,
                 4, 2, 0,
                 2, 1, 0,
                 6, 3, 0,
                 4, 2, 0,
                 2, 1, 0,
                 6, 3, 0,
                 4, 2, 0,
                 2, 1, 0]

    for i in range(0, len(students) * 3):
        classes_domain += [(0, (len(students) * 3) - i - 1)]

    if thread_test == False and read_results == False:

        random = optimizer.RandomOptimizeWorker('Random', classes_domain, classes_cost)
        hillclimbing = optimizer.HillClimbOptimizeWorker('Hill_Climber', classes_domain, classes_cost)
        annealing = optimizer.AnnealingOptimizeWorker('Annealer', classes_domain, classes_cost)
        genetic = optimizer.GeneticOptimizeWorker('Genetic', classes_domain, classes_cost)

        print("Optimal Solution Cost: {}\n".format(classes_cost(s_optimal)))
        random.run()
        hillclimbing.run()
        annealing.run(T=100000000000000.0, cool=.999)
        genetic.run(population_size=10000, maxiter=100)

        print("Optimal Solution:\n")
        print_solution(s_optimal)
        print("Final Solution for Random:\n")
        print_solution(random.final_solution)
        print("Final Solution for Hill Climbing:\n")
        print_solution(hillclimbing.final_solution)
        print("Final Solution for Annealing:\n")
        print_solution(annealing.final_solution)
        print("Final Solution for Genetic:\n")
        print_solution(genetic.final_solution)

    elif thread_test:

        random_optimizers = []
        hillclimbing_optimizers = []
        annealing_optimizers = []
        genetic_optimizers = []

        random_threads = []
        hillclimbing_threads = []
        annealing_threads = []
        genetic_threads = []

        for i in range(0, num):
            random_optimizers.append(
                optimizer.RandomOptimizeWorker('random_optimizer_' + str(i), classes_domain, classes_cost))
            random_threads.append(threading.Thread(target=random_optimizers[i].run))

            hillclimbing_optimizers.append(
                optimizer.HillClimbOptimizeWorker('hillclimbing_optimizer_' + str(i), classes_domain, classes_cost))
            hillclimbing_threads.append(threading.Thread(target=hillclimbing_optimizers[i].run))

            annealing_optimizers.append(
                optimizer.AnnealingOptimizeWorker('annealing_optimizer_' + str(i), classes_domain, classes_cost))
            annealing_threads.append(
                threading.Thread(target=annealing_optimizers[i].run, kwargs={'T': 100000000000000.0, 'cool': .999}))

            genetic_optimizers.append(
                optimizer.GeneticOptimizeWorker('genetic_optimizer_' + str(i), classes_domain, classes_cost))
            genetic_threads.append(
                threading.Thread(target=genetic_optimizers[i].run, kwargs={'population_size': 100, 'maxiter': 1000}))

        for t in range(0, num):
            random_threads[t].start()
            hillclimbing_threads[t].start()
            annealing_threads[t].start()
            genetic_threads[t].start()

        for t in range(0, num):
            random_threads[t].join()
            hillclimbing_threads[t].join()
            annealing_threads[t].join()
            genetic_threads[t].join()

        results_df = pd.DataFrame({'Random_Total_Cost': [x.total_cost for x in random_optimizers],
                                   'Random_Solution': [x.final_solution for x in random_optimizers],
                                   'Hill_Climbing_Total_Cost': [x.total_cost for x in hillclimbing_optimizers],
                                   'Hill_Climbing_Solution': [x.final_solution for x in hillclimbing_optimizers],
                                   'Annealing_Total_Cost': [x.total_cost for x in annealing_optimizers],
                                   'Annealing_Solution': [x.final_solution for x in annealing_optimizers],
                                   'Genetic_Total_Cost': [x.total_cost for x in genetic_optimizers],
                                   'Genetic_Solution': [x.final_solution for x in genetic_optimizers]}
                                  )
        print(results_df.head(10))
        print(results_df.describe())
        results_df.to_csv('results_{}_{}'.format(num, os.getpid()), index=False)

    elif read_results:
        results_df = pd.read_csv(csv_file)
        print(results_df.head(10))
        print(results_df.describe())


if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], 't:n:r:f:h', ['threading=', 'num=', 'results=', 'file=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    main(opts)
