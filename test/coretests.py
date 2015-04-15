import unittest

from calc.core import *
from calc import exceptions
from test import testdata


__author__ = 'tangz'


class ProbabilityVectorTest(unittest.TestCase):
    def setUp(self):
        self.probvector = ProbabilityVector(AAA=1, AA=2, A=3)

    def test_should_get_states(self):
        self.assertCountEqual(self.probvector.states(), ['AAA', 'AA', 'A'])

    def test_should_get_probs(self):
        self.assertAlmostEqual(self.probvector.get('AA'), 2)

    def test_should_set_prob(self):
        self.probvector.set('AAA', 5)
        self.assertAlmostEqual(self.probvector.get('AAA'), 5)

    def test_should_set_nonexisting_state(self):
        self.probvector.set('BB', 5)
        self.assertAlmostEqual(self.probvector.get('BB'), 5)

    def test_should_raise_if_get_nonexisting_state(self):
        self.assertRaises(exceptions.InvalidTransitionStateError, self.probvector.get, 'XX')

    def test_should_eq(self):
        probvector2 = ProbabilityVector(AAA=1, AA=2, A=3)
        self.assertEqual(self.probvector, probvector2)

    def test_should_not_eq(self):
        probvector2 = ProbabilityVector(AAA=2, AA=2, A=3)
        self.assertNotEqual(self.probvector, probvector2)


class TransitionMatrixGroupTest(unittest.TestCase):
    def setUp(self):
        self.sample_trans_mat1 = TransitionMatrix('A', 'AA')
        self.sample_trans_mat2 = TransitionMatrix('A', 'AAA')
        self.trans_mat_group = TransitionMatrixGroup()
        self.trans_mat_group.add_matrix(1, self.sample_trans_mat1)
        self.trans_mat_group.add_matrix(3, self.sample_trans_mat2)

    def tearDown(self):
        self.trans_mat_group.reset_period_marker()

    def test_should_have_matrix(self):
        self.assertTrue(self.trans_mat_group.has_matrix(1))
        self.assertTrue(self.trans_mat_group.has_matrix(3))
        self.assertFalse(self.trans_mat_group.has_matrix(2))

    def test_should_get_matrix(self):
        matrixp1 = self.trans_mat_group.get_matrix(1)
        matrixp2 = self.trans_mat_group.get_matrix(2)
        matrixp3 = self.trans_mat_group.get_matrix(3)
        self.assertIsNotNone(matrixp1)
        self.assertIsNone(matrixp2)
        self.assertIsNotNone(matrixp3)
        self.assertEqual(self.sample_trans_mat1, matrixp1)
        self.assertEqual(self.sample_trans_mat2, matrixp3)

    def test_should_return_periods(self):
        # has to be ordered
        self.assertEqual(self.trans_mat_group.periods(), [1, 3])

    def test_should_iterate(self):
        p1 = next(self.trans_mat_group)
        p2 = next(self.trans_mat_group)
        p3 = next(self.trans_mat_group)
        p4 = next(self.trans_mat_group)
        expectedp1mat = self.sample_trans_mat1
        expectedp2mat = None
        expectedp3mat = self.sample_trans_mat2
        expectedp4mat = None

        self.assertEqual(p1.period, 1)
        self.assertEqual(p1.matrix, expectedp1mat)
        self.assertEqual(p2.period, 2)
        self.assertEqual(p2.matrix, expectedp2mat)
        self.assertEqual(p3.period, 3)
        self.assertEqual(p3.matrix, expectedp3mat)
        self.assertEqual(p4.period, 4)
        self.assertEqual(p4.matrix, expectedp4mat)

    def test_should_return_first_period(self):
        self.assertEqual(self.trans_mat_group.firstperiod(), 1)

    def test_should_return_last_period(self):
        self.assertEqual(self.trans_mat_group.lastperiod(), 3)

    def test_matrix_range(self):
        mrange = matrixrange(self.trans_mat_group, 1, 5)
        matrixp1 = self.trans_mat_group.get_matrix(1)
        matrixp2 = self.trans_mat_group.get_matrix(2)
        matrixp3 = self.trans_mat_group.get_matrix(3)
        matrixp4 = self.trans_mat_group.get_matrix(4)
        expected_mats = {1: matrixp1, 2: matrixp2, 3: matrixp3, 4: matrixp4}
        for period, matrix in mrange:
            self.assertEqual(matrix, expected_mats[period])

    def test_matrix_range_with_diff_start_period(self):
        mrange = matrixrange(self.trans_mat_group, 3, 5)
        matrixp3 = self.trans_mat_group.get_matrix(3)
        matrixp4 = self.trans_mat_group.get_matrix(4)
        expected_mats = {3: matrixp3, 4: matrixp4}
        for period, matrix in mrange:
            self.assertEqual(matrix, expected_mats[period])




class TransitionMatrixTest(unittest.TestCase):
    def setUp(self):
        self.states = ['AAA', 'AA', 'A']
        self.matrix = TransitionMatrix('AAA', 'AA', 'A')

    def test_init_matrix(self):
        self.assertCountEqual(self.matrix.states, self.states, "matrix should have states AAA, AA, A")
        self.assertIsNotNone(self.matrix.data['AAA']['AAA'], "matrix should not have null element at AAA, AAA")
        self.assertIsNotNone(self.matrix.data['AA']['A'], "matrix should not have null element at AA, A")

    def test_set_get_probability(self):
        self.matrix.set_probability('AAA', 'AA', 0.01)
        self.assertIs(self.matrix.get_probability('AAA', 'AA'), 0.01,
                      "matrix element AAA, AA should have correct value")

    def test_set_all_probabilities(self):
        self.matrix = testdata.inc_invalid_trans_mat()

        self.assertAlmostEqual(self.matrix.get_probability('AAA', 'AAA'), 1)
        self.assertAlmostEqual(self.matrix.get_probability('AAA', 'AA'), 2)
        self.assertAlmostEqual(self.matrix.get_probability('AAA', 'A'), 3)

        self.assertAlmostEqual(self.matrix.get_probability('AA', 'AAA'), 4)
        self.assertAlmostEqual(self.matrix.get_probability('AA', 'AA'), 5)
        self.assertAlmostEqual(self.matrix.get_probability('AA', 'A'), 6)

        self.assertAlmostEqual(self.matrix.get_probability('A', 'AAA'), 7)
        self.assertAlmostEqual(self.matrix.get_probability('A', 'AA'), 8)
        self.assertAlmostEqual(self.matrix.get_probability('A', 'A'), 9)

    def test_set_using_invalid_state(self):
        self.assertRaises(exceptions.InvalidTransitionStateError, self.matrix.set_probability, 'AAA', 'Incorrect, man!',
                          0.03)

    def test_get_using_invalid_state(self):
        self.assertRaises(exceptions.InvalidTransitionStateError, self.matrix.get_probability, 'AAA', 'Incorrect, man!')

    def test_get_all_future_probs(self):
        self.matrix = testdata.inc_invalid_trans_mat()
        probs = self.matrix.probabilities_from('AAA')
        self.assertDictEqual(probs, {'AAA': 1, 'AA': 2, 'A': 3})

    def test_get_all_current_probs(self):
        self.matrix = testdata.inc_invalid_trans_mat()
        probs = self.matrix.probabilities_to('AAA')
        self.assertDictEqual(probs, {'AAA': 1, 'AA': 4, 'A': 7})

    def test_values(self):
        self.matrix = testdata.inc_invalid_trans_mat()
        self.assertCountEqual(self.matrix.values(), range(1, 10))

    def test_get_all_future_invalid_state(self):
        self.assertRaises(exceptions.InvalidTransitionStateError, self.matrix.probabilities_from, 'AAAAAA')

    def test_get_all_current_invalid_state(self):
        self.assertRaises(exceptions.InvalidTransitionStateError, self.matrix.probabilities_to, 'AAAAAA')

    def test_eq_same_probs(self):
        matrix1 = testdata.inc_invalid_trans_mat()
        matrix2 = testdata.inc_invalid_trans_mat()
        self.assertEqual(matrix1, matrix2)

    def test_eq_same_matrix(self):
        matrix1 = testdata.inc_invalid_trans_mat()
        self.assertEqual(matrix1, matrix1)

    def test_not_eq_not_same_probs(self):
        matrix1 = testdata.inc_invalid_trans_mat()
        matrix2 = testdata.valid_transition_mat()
        self.assertNotEqual(matrix1, matrix2)

    def test_not_eq_not_same_states(self):
        matrix1 = testdata.inc_invalid_trans_mat()
        matrix2 = TransitionMatrix('Q', 'R')
        self.assertNotEqual(matrix1, matrix2)




