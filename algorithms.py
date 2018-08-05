#!/usr/bin/env python3

__author__ = "nicoroble"
__version__ = "0.1.0"
__license__ = "MIT"

import random, math


class OptimizationWorker:
    total_cost = 0
    valid_arguments = []
    final_solution = []

    def __init__(self, name, domain, costfunction, **kwargs):

        self.name = name

        if isinstance(domain, list):
            self.domain = domain
        else:
            print(type(domain))
            raise ValueError

        if hasattr(costfunction, '__call__'):
            self.costfunction = costfunction
        else:
            raise ValueError

        for key, value in kwargs.items():
            if key not in self.valid_arguments:
                raise AttributeError
            else:
                setattr(self, key, value)


class RandomOptimizeWorker(OptimizationWorker):

    def __init__(self, name, domain, costfunction, **kwargs):
        super().__init__(name, domain, costfunction, **kwargs)

    def run(self):
        best = 999999999
        bestsolution = None

        for i in range(1000):
            # Create a random solution
            vector = [int(random.randint(self.domain[i][0], self.domain[i][1])) for i in range(len(self.domain))]

            cost = self.costfunction(vector)

            if cost < best:
                best = cost
                bestsolution = vector

        self.total_cost = self.costfunction(vector)
        self.final_solution = vector
        print('{} of class RandomOptimizeWorker has a total cost of {}'.format(self.name, self.total_cost))
        return vector


class HillClimbOptimizeWorker(OptimizationWorker):

    def __init__(self, name, domain, costfunction, **kwargs):
        super().__init__(name, domain, costfunction, **kwargs)

    def run(self):
        # Create a random solution
        domain = self.domain
        costfunction = self.costfunction

        solution = [int(random.randint(domain[i][0], domain[i][1])) for i in range(len(domain))]
        # Main loop
        while 1:
            # Create list of neighboring solutions
            neighbors = []

            for j in range(len(domain)):
                if solution[j] > domain[j][0]:
                    # adds 1 to the first element, copies the rest
                    if solution[j] < domain[j][1]:
                        neighbors.append(solution[0:j] + [solution[j] + 1] + solution[j + 1:])

                if solution[j] < domain[j][1]:
                    # subtracts one to the first element, copies the rest
                    if solution[j] > domain[j][0]:
                        neighbors.append(solution[0:j] + [solution[j] - 1] + solution[j + 1:])

            # Find the best solution among the neighbors
            current = costfunction(solution)
            best = current

            for j in range(len(neighbors)):
                cost = costfunction(neighbors[j])
                if cost < best:
                    best = cost
                    solution = neighbors[j]

            # If there's no improvement, then we've reached the top
            if best == current:
                break
        self.total_cost = costfunction(solution)
        self.final_solution = solution
        print('{} of class HillClimbOptimizeWorker has a total cost of {}'.format(self.name, self.total_cost))
        return solution


class AnnealingOptimizeWorker(OptimizationWorker):

    def __init__(self, name, domain, costfunction, **kwargs):
        super().__init__(name, domain, costfunction, **kwargs)

    def run(self, T=10000.0, cool=0.95, step=1):
        domain = self.domain
        costfunction = self.costfunction
        # Initialize the values randomly
        vector = [int(random.randint(domain[i][0], domain[i][1])) for i in range(len(domain))]

        while T > 0.1:
            # Choose one of the indices
            i = random.randint(0, len(domain) - 1)

            # Choose a direction to change it
            direction = random.randint(-step, step)

            # Create a new list with one of the values changed
            vectorb = vector[:]
            vectorb[i] += direction
            if vectorb[i] < domain[i][0]:
                vectorb[i] = domain[i][0]
            elif vectorb[i] > domain[i][1]:
                vectorb[i] = domain[i][1]

            # Calculate the current cost and the new cost
            ea = costfunction(vector)
            eb = costfunction(vectorb)
            p = pow(math.e, (-eb - ea) / T)

            # Is it better, or does it make the probability
            # cutoff?
            if (eb < ea or random.random() < p):
                vector = vectorb

                # Decrease the temperature
            T = T * cool

        self.total_cost = costfunction(vector)
        self.final_solution = vector
        print('{} of class AnnealingOptimizeWorker has a total cost of {}'.format(self.name, self.total_cost))
        return vector


class GeneticOptimizeWorker(OptimizationWorker):

    def __init__(self, name, domain, costfunction, **kwargs):
        super().__init__(name, domain, costfunction, **kwargs)

    def run(self, population_size=50, steps=1, mutationprobability=0.2, elite=0.2, maxiter=100):
        domain = self.domain
        costfunction = self.costfunction

        # Mutation Operation
        def mutate(vec):
            i = random.randint(0, len(domain) - 1)
            if random.random() < 0.5 and vec[i] > domain[i][0]:
                return vec[0:i] + [vec[i] - steps] + vec[i + 1:]
            elif vec[i] < domain[i][1]:
                return vec[0:i] + [vec[i] + steps] + vec[i + 1:]

        # Crossover Operation
        def crossover(r1, r2):
            i = random.randint(1, len(domain) - 2)
            return r1[0:i] + r2[i:]

        # Build the initial population
        pop = []
        for i in range(population_size):
            vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
            pop.append(vec)

        # How many winners from each generation?
        topelite = int(elite * population_size)

        # Main loop
        for i in range(maxiter):
            scores = [(costfunction(v), v) for v in pop if v is not None]

            scores.sort(key=lambda x: x[0])
            ranked = [v for (s, v) in scores]

            # Start with the pure winners
            pop = ranked[0:topelite]

            # Add mutated and bred forms of the winners
            while len(pop) < population_size:
                if random.random() < mutationprobability:

                    # Mutation
                    c = random.randint(0, topelite)
                    pop.append(mutate(ranked[c]))
                else:

                    # Crossover
                    c1 = random.randint(0, topelite)
                    c2 = random.randint(0, topelite)
                    pop.append(crossover(ranked[c1], ranked[c2]))

        self.total_cost = costfunction(scores[0][1])
        self.final_solution = scores[0][1]
        print('{} of class GeneticOptimizeWorker has a total cost of {}'.format(self.name, self.total_cost))
        return scores[0][1]
