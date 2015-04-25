import unittest
from calc import create
from calc import validations
from calc import engine
from calc import io
from calc.core import ProbabilityVector

__author__ = 'tangz'

class CreateTests(unittest.TestCase):

    def test_prob_exact(self):
        expected_vect = ProbabilityVector(AAA=0.0, AA=0.0, A=1.0)
        actual_vect = create.probability_exact('A', ('AAA', 'AA', 'A'))
        self.assertEqual(expected_vect, actual_vect)

    def test_should_create_valid_random_mat(self):
        matrices_to_create = 20
        for i in range(matrices_to_create):
            mat = create.random_matrix('A', 'B', 'C', 'D', 'F')
            validations.is_valid(mat)

    def test_should_create_random_group(self):
        terminate_period = 10
        periods = range(1, terminate_period)
        group = create.random_group(('A', 'B', 'C', 'F'), periods)
        for matrix_assoc in group:
            if matrix_assoc.period >= terminate_period:
                break
            validations.is_valid(matrix_assoc.matrix)

    # TODO: move into integration test
    def test_should_calculate_random_group(self):
        terminate_period = 10
        periods = range(1, terminate_period)
        group = create.random_group(('A', 'B', 'C', 'D', 'F'), periods)
        results = engine.results(group, 'B')
        io.results_to_file(results, 'test_calc_random_group.csv')