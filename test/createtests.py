import unittest
from calc import create
from calc import validations
from calc import engine
from calc.core import ProbabilityVector

__author__ = 'tangz'

class CreateTests(unittest.TestCase):

    def test_should_create_valid_random_mat(self):
        matrices_to_create = 50
        for i in range(matrices_to_create):
            mat = create.random('A', 'B', 'C', 'D', 'F')
            validations.is_valid(mat)

    def test_should_create_random_group(self):
        periods = range(1, 10)
        group = create.random_group(('A', 'B', 'C', 'D', 'F'), periods)
        initvec = ProbabilityVector(A=0.9, B=0.05, C=0.01, D=0.02, F=0.01)
        for vec in engine.calculator(group, initvec):
            print(vec.vectordict)