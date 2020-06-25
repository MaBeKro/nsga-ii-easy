import unittest
import random
import itertools

from nsga2easy.main import fast_non_dominated_sort, sort_crowding_distance, Individual

class TestFastNonDominatedSort(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        random.seed(1)

    def test_basic(self):
        ind = Individual([1], str(1))
        pop = next(fast_non_dominated_sort([ind]))
        new_ind = pop.pop()
        self.assertEqual(str(1), new_ind.value)
        self.assertEqual([1], new_ind.fitness)

    def test_single_objective(self):
        pop = [ Individual([i], str(i)) for i in range(10) ]
        random.shuffle(pop)
        pop = list(itertools.chain(*fast_non_dominated_sort(pop)))
        self.assertTrue(all((
            i1.fitness[0] <= i2.fitness[0] for i1, i2 in zip(pop, pop[1:]))))

    def test_multi_objective_pyramid(self):
        pyramid_pop = []
        for i in range(0,6):
            current_layer = ( Individual(f, i)
                for f in itertools.permutations(range(i+1), r=2) if sum(f) == i )
            pyramid_pop.extend(current_layer)
        pop = itertools.chain(*fast_non_dominated_sort(pyramid_pop))
        self.assertTrue(all(( p.value == p.rank for p in pop)))

    def test_mult_objective_grid(self):
        grid_pop = [ Individual((f1,f2), None) for f1 in range(10) for f2 in range(10) ]
        pop = list(fast_non_dominated_sort(grid_pop))
        maxima = [ max(( sum(p.fitness) for p in front )) for front in pop if front ]
        self.assertTrue(all(( m1 <= m2 for m1, m2 in zip(maxima, maxima[1:]))))

class TestSortCrowdingDistance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        random.seed(1)

    def test_basic(self):
        ind = Individual([1], str(1))
        ind.rank = 0
        srt = list(sort_crowding_distance([ind], [1], same_rank=True))
        new_ind = srt[0]
        self.assertEqual(str(1), new_ind.value)
        self.assertEqual([1], new_ind.fitness)
        self.assertEqual(new_ind.crowding_distance, float('inf'))

    def test_single_objective(self):
        pop = [ Individual([i], str(i)) for i in range(10) ]
        random.shuffle(pop)
        pop = list(sort_crowding_distance(pop, [10], same_rank=True))
        self.assertTrue(
            all(( p1.crowding_distance == p2.crowding_distance
                for p1, p2 in zip(pop, pop[1:])
                if p1.crowding_distance != float('inf') and p2.crowding_distance != float('inf'))))
        self.assertEqual(2, len([ p for p in pop if p.crowding_distance == float('inf')]))

    def test_ranking(self):
        pop = [ Individual([i], str(i)) for i in range(10) ]
        for idx, p in enumerate(pop):
            p.rank = idx
        random.shuffle(pop)
        pop = list(sort_crowding_distance(pop, [1], same_rank=False))
        self.assertTrue(all(( p1.rank <= p2.rank for p1, p2 in zip(pop, pop[1:]))))

if __name__ == "__main__":
    unittest.main()