import unittest
from calc import engine, create
from calc.core import ProbabilityVector, TransitionMatrixGroup, TransitionMatrix
from test import testdata

__author__ = 'tangz'

class EngineTest(unittest.TestCase):

    def setUp(self):
        self.matrix = testdata.valid_transition_mat()
        self.probvec = testdata.valid_prob_vec()

        self.calculationgroup = TransitionMatrixGroup()

        matrix_p1 = TransitionMatrix('A', 'B', 'C')
        matrix_p1.set_probability('A', 'A', 0.8)
        matrix_p1.set_probability('A', 'B', 0.2)
        matrix_p1.set_probability('A', 'C', 0.0)
        matrix_p1.set_probability('B', 'A', 0.25)
        matrix_p1.set_probability('B', 'B', 0.6)
        matrix_p1.set_probability('B', 'C', 0.15)
        matrix_p1.set_probability('C', 'A', 0.05)
        matrix_p1.set_probability('C', 'B', 0.25)
        matrix_p1.set_probability('C', 'C', 0.7)
        self.calculationgroup.add_matrix(1, matrix_p1)

        matrix_p2 = TransitionMatrix('A', 'B', 'C')
        matrix_p2.set_probability('A', 'A', 0.9)
        matrix_p2.set_probability('A', 'B', 0.05)
        matrix_p2.set_probability('A', 'C', 0.05)
        matrix_p2.set_probability('B', 'A', 0.1)
        matrix_p2.set_probability('B', 'B', 0.8)
        matrix_p2.set_probability('B', 'C', 0.1)
        matrix_p2.set_probability('C', 'A', 0.0)
        matrix_p2.set_probability('C', 'B', 0.1)
        matrix_p2.set_probability('C', 'C', 0.9)
        self.calculationgroup.add_matrix(2, matrix_p2)


    def test_multiply(self):
        actualprobvec = engine.multiply(self.matrix, self.probvec)
        self.assertAlmostEqual(actualprobvec.get('AAA'), 0.29)
        self.assertAlmostEqual(actualprobvec.get('AA'), 0.35)
        self.assertAlmostEqual(actualprobvec.get('A'), 0.36)


    def test_calculation(self):
        resultsA = engine.results(self.calculationgroup, 'A')
        # self.assertEqual(resultsA[1], ProbabilityVector(A=1.0, B=0.0, C=0.0))
        self.assertEqual(resultsA[1], ProbabilityVector(A=0.8, B=0.2, C=0.0))
        self.assertEqual(resultsA[2], ProbabilityVector(A=0.74, B=0.2, C=0.06))

        resultsB = engine.results(self.calculationgroup, 'B')
        # self.assertEqual(resultsB[1], ProbabilityVector(A=0.0, B=1.0, C=0.0))
        self.assertEqual(resultsB[1], ProbabilityVector(A=0.25, B=0.6, C=0.15))
        self.assertEqual(resultsB[2], ProbabilityVector(A=0.285, B=0.5075, C=0.2075))

        resultsC = engine.results(self.calculationgroup, 'C')
        # self.assertEqual(resultsC[1], ProbabilityVector(A=0.0, B=0.0, C=1.0))
        self.assertEqual(resultsC[1], ProbabilityVector(A=0.05, B=0.25, C=0.7))
        self.assertEqual(resultsC[2], ProbabilityVector(A=0.07, B=0.2725, C=0.6575))
