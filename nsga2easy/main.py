from collections import defaultdict
from itertools import chain
from itertools import groupby

# for maximizing use negative mask [ ..., -1, ...]
def mask_fitness(fitness, min_max_mask):
    return [ v * m for v, m in zip (fitness, min_max_mask) ]

# we minimize, so an individual that is all smaller is definetily better
def dominates(fitness1, fitness2):
    """

    """
    # any is so individuals cannot dominate themselves
    return all(( f1 <= f2 for f1, f2 in zip(fitness1, fitness2 )))\
        and any(( f1 < f2 for f1, f2 in zip(fitness1, fitness2 )))

class Individual:
    def __init__(self, fitness, value):
        self.fitness = fitness
        self.value = value

def fast_non_dominated_sort(population):
    # population = [ _Individual(f, v) for f, v in zip(fitnesses, values) ]

    # initialize variables
    for p in population:
        p.dominated_set = set()
        p.dominated_by_counter = 0

    current_front = set()
    # first phase, find the first front
    for p in population:
        for q in population:
            if dominates(p.fitness, q.fitness):
                p.dominated_set.add(q)
            elif dominates(q.fitness, p.fitness): 
                p.dominated_by_counter += 1

        if p.dominated_by_counter == 0:
            p.rank = 1
            current_front.add(p)
    yield current_front
    
    # second phase, find all the other fronts
    previous_front = current_front
    front_idx = 1
    while previous_front:
        current_front = set()
        for p in previous_front:
            for q in p.dominated_set:
                q.dominated_by_counter -= 1
                if q.dominated_by_counter == 0:
                    q.rank = front_idx + 1
                    current_front.add(q)
        front_idx += 1
        previous_front = current_front
        yield current_front


def sort_crowding_distance(population, range_objectives_lst, same_rank=False):
    l = len(population)
    for p in population:
        p.crowding_distance = 0
    for objective, current_range in enumerate(range_objectives_lst):
        population = sorted(population, key=lambda p: p.fitness[objective])
        population[0].crowding_distance, population[-1].crowding_distance = float('inf'), float('inf')
        for i in range(1, l - 1):
            population[i].crowding_distance +=\
            abs(population[i + 1].fitness[objective] - population[i - 1].fitness[objective]) / current_range
    
    # a bit ugly because we do not have custom compare sorting in python3
    # so we separate first by rank, then sort using crowding distance, then join
    # note that this is not necessary if they are all from the same rank
    # which is actually the case in the selection outlined in the paper,
    # although their crowding compare does not care
    if same_rank:
        return sorted(population, key=lambda p: p.crowding_distance, reverse=True)
    else:
        return chain(*(
            # sort subgroups by crowding distance in descending order
            sorted(values, key=lambda p: p.crowding_distance, reverse=True)
            for _, values in
                sorted(
                    # find all groups of individuals with the same rank
                    groupby(population, key=lambda p: p.rank),
                    # sort them according to rank in ascending order
                    key=lambda tp: tp[0])))

def range_objectives(population):
    return [ max(af) - min(af) for af in zip(*(p.fitness for p in population)) ]


def select_next_population(population, previous_population=set(), k=None, range_objectives_lst=None):
    if k is None:
        k = len(population)
    population.update(previous_population)

    if not range_objectives_lst:
        range_objectives_lst = range_objectives(population)

    new_population = []
    for front in fast_non_dominated_sort(population):
        # add fronts until one does not fit completely into the new generation
        sorted_front = sort_crowding_distance(front, range_objectives_lst, same_rank=True)
        if len(front) + len(new_population) <= k:
            # TODO: we could also sort these fronts with crowding distance
            new_population.extend(sorted_front)
        else:
            new_population.extend(sorted_front[:k - len(new_population)])
            break
    
    return new_population
    
def select_next_population_wrapped(population_fitness, population_values=None, k=None, mask=None, range_objectives_lst=None):
    if population_values is None:
        population_values = list(range(len(population_fitness)))
    if mask is None:
        population = [ Individual(f, v) for f, v in zip(population_fitness, population_values)]
    else:
        population = [ Individual(mask_fitness(f, mask), v) for f, v in zip(population_fitness, population_values)]
    new_population = select_next_population(population, k=k, range_objectives_lst=range_objectives_lst)

    return\
        [ p.fitness for p in new_population],\
        [ p.value for p in new_population],\
        [ p.rank for p in new_population],
    
    


