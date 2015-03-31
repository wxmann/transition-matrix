import unittest
from calc import engine
from calc.core import ProbabilityVector
from test import testdata

__author__ = 'tangz'

class EngineTest(unittest.TestCase):

    def setUp(self):
        self.matrix = testdata.valid_transition_mat()
        self.probvec = testdata.valid_prob_vec()

    def test_multiply(self):
        actualprobvec = engine.multiply(self.matrix, self.probvec)
        self.assertAlmostEqual(actualprobvec.get('AAA'), 0.29)
        self.assertAlmostEqual(actualprobvec.get('AA'), 0.35)
        self.assertAlmostEqual(actualprobvec.get('A'), 0.36)


