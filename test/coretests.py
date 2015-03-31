import unittest

from calc.core import TransitionMatrix, TransitionMatrixGroup, ProbabilityVector
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


class TransitionMatrixGroupTest(unittest.TestCase):
    def setUp(self):
        self.sample_trans_mat = TransitionMatrix('A', 'AA')
        self.trans_mat_group = TransitionMatrixGroup()
        self.trans_mat_group.add_matrix(1, self.sample_trans_mat)
        self.trans_mat_group.add_matrix(3, self.sample_trans_mat)

    def test_should_have_matrix(self):
        self.assertTrue(self.trans_mat_group.has_matrix(1))
        self.assertTrue(self.trans_mat_group.has_matrix(3))
        self.assertFalse(self.trans_mat_group.has_matrix(2))

    def test_should_get_matrix(self):
        self.assertIsNotNone(self.trans_mat_group.get_matrix(1))
        self.assertIsNone(self.trans_mat_group.get_matrix(2))
        self.assertIsNotNone(self.trans_mat_group.get_matrix(3))

    def test_should_return_periods(self):
        self.assertCountEqual(self.trans_mat_group.periods(), [1, 3])

    def test_should_return_first_period(self):
        self.assertEqual(self.trans_mat_group.firstperiod(), 1)

    def test_should_return_last_period(self):
        self.assertEqual(self.trans_mat_group.lastperiod(), 3)


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



