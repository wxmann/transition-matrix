import unittest
from calc import create
from calc import validations
from calc import engine
from calc.core import ProbabilityVector

__author__ = 'tangz'

class CreateTests(unittest.TestCase):

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

    # TODO: this should not belong here.
    def test_should_create_random_group(self):
        periods = range(1, 10)
        group = create.random_group(('A', 'B', 'C', 'D', 'F'), periods)
        initvec = ProbabilityVector(A=0, B=1, C=0, D=0, F=0)
        for result in engine.calculator(group, initvec):
            print(result)