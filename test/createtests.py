import unittest
from calc import create
from calc import validations
from calc import engine
from calc.core import ProbabilityVector

__author__ = 'tangz'

## Done: rewrote create random matrix to not have sum(col)==1.0 restriction
## TODO: round to certain decimal places.
## Done: include states method in TransitionMatrixGroup
## TODO: add unit test for bigger matrix in Mayank's spreadsheet.
## TODO: add Transition matrix constructor to include keyvaluemappings from start.
## Done: validate that probability vector result has unit total probability. => values method in ProbabilityVector
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

    def test_should_calculate_random_group(self):
        terminate_period = 10
        periods = range(1, terminate_period)
        group = create.random_group(('A', 'B', 'C', 'D', 'F'), periods)
        results = engine.results(group, 'B')