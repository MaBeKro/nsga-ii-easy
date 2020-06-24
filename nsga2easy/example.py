import random
import copy
import time
import numpy as np
import matplotlib.pyplot as plt

from main import select_next_population, Individual
# replace this with from nsga2easy import select_next_population, Individual

def fit1(x):
    return -(x+50)**2

def fit2(x):
    return -(x-50)**2

def mutate(x, epsilon, bounds):
    lower, upper = bounds
    return max(lower, min(upper, x + (1 - 2*random.random()) * epsilon))

def evolve():
    random.seed(1)
    lower = -100
    upper = 100
    bounds = lower, upper
    epsilon = 1
    population_size = 200
    num_generations = 10

    previous_population = {}
    population = { Individual(None, random.random() * (upper - lower) + lower) for _ in range(population_size) }


    for generation in range(num_generations):
        before = time.time()
        print(f"generation {generation}")

        # Evaluation
        for p in population:
            p.fitness = fit1(p.value), fit2(p.value)

        previous_population = population

        # Selection
        population = { copy.deepcopy(p) for p in select_next_population(2, population, previous_population=previous_population) }
        
        for p in population:
            # Mutation
            p.value = mutate(p.value, epsilon, bounds)
        print(f" -> duration {time.time() - before}")
        
    points = np.array(sorted([ [*p.fitness, p.rank, p.value] for p in previous_population ], key=lambda pt: pt[3]))

    # you can do better
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.scatter(x=points[:,0], y=points[:, 1], c=points[:,2])
    plt.xlabel("-(x+50)**2")
    plt.ylabel("-(x-50)**2")
    plt.gca().set_aspect("equal")

    plt.subplot(2, 1, 2)
    l1, = plt.plot(points[:, 3], points[:,0], marker="|")
    l2, = plt.plot(points[:, 3], points[:,1], marker="|")
    plt.xlabel("x")
    plt.ylabel("fitness")
    plt.legend([l1, l2], ["-(x+50)**2", "-(x-50)**2"])

    plt.show()

if __name__ == "__main__":
    evolve()
