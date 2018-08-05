# Optimization Theory Final
## Submitted by: Nikko Mizutani(s16574nm)

## Problem being solved
I created this project with the goal of solving the random selection for classes at SFC. Although the number of classes
on the list is nothing compared to what is on the syllabus, the same principle applies.

#### There are N classes. To simplify the problem, only 3 students can register to each class.
```python
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
```

#### Each student has can have 3 preferred classes.
```python
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
```

#### Each student should not be registered to the same class however!

#### Problem
I treated this problem to be a travelling salesman problem? I'm not sure.

#### Algorithms used
I used the hill climbing algorithm, the simulated annealing algorithm, and the genetic algorithm. I fed each algorithm a cost function and the domain for which it will use to create a vector. The solution will be a vector representing which class each student is registered to.

### Cost Function
If a student will be registered to 2 same classes, there will be a cost penalty of 100 for each same class. For each class a student is registered to but is not his or her class of choice, there will be a cost penalty of 5. If the student gets his or her class, there will be no penalty.

```python
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
```

#### Optimal Solution
```python
s_optimal = [6, 3, 0,
             4, 2, 0,
             2, 1, 0,
             6, 3, 0,
             4, 2, 0,
             2, 1, 0,
             6, 3, 0,
             4, 2, 0,
             2, 1, 0]
```
total cost for the optimal solution is 0.

#### Best Results

Best results so far was from the genetic algorithm, with only a cost of 0. Meaning it got the optimal solution. However it took a very long time to compute, since I tweaked the parameters:

```python
    annealing = optimizer.AnnealingOptimizeWorker('Annealer', classes_domain, classes_cost)
    genetic.run(population_size=10000, maxiter=10000)
```

It took about 40 minutes to get the results. 

#### Usage
```bash
python final.py
```
Will do a regular one time run and print the results of each algorithm. It will show the optimal solution. The optimal solution will be printed first followed by each algorithm, their respective total cost, and their solutions.

Additional arguments:

-t [boolean]
> True will create multiple threads and will run each algorithm n number of times. After the run, the data will be saved to a csv file. false will do the defaul run.

-n [int]
> Specify the number of threads to spawn for each algorithm. Default is 10.

-r [boolean]
> Reads the resulting csv file and describes the results.

-f [string]
> Specify which csv file to read and describe. Defaul it result.

-h
> Prints out the usage


