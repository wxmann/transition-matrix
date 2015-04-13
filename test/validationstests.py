import unittest
from calc.core import TransitionMatrix, TransitionMatrixGroup
from calc import validations
from calc import exceptions
from test import testdata

__author__ = 'tangz'

class ValidationsTest(unittest.TestCase):

    def setUp(self):
        self.valid_trans_mat = testdata.valid_transition_mat()
        self.invalid_mat = testdata.inc_invalid_trans_mat()

    def test_should_take_valid_probs(self):
        validations.check_matrix_probs(self.valid_trans_mat)

    def test_should_take_normalized_probs(self):
        validations.check_normalized_probs(self.valid_trans_mat)

    def test_should_catch_invalid_probs(self):
        self.assertRaises(exceptions.InvalidProbabilityError, validations.check_matrix_probs, self.invalid_mat)

    def test_should_catch_nonnormal_probs(self):
        self.assertRaises(exceptions.UnnormalizedProbabilitiesError, validations.check_normalized_probs, self.invalid_mat)

    def test_should_catch_inconsistent_states_group(self):
        group = TransitionMatrixGroup()
        matrixp1 = TransitionMatrix('AAA', 'AA')
        matrixp2 = TransitionMatrix('AAA', 'AA')
        matrixp3 = TransitionMatrix('AA', 'A')
        group.add_matrix(1, matrixp1)
        group.add_matrix(2, matrixp2)
        group.add_matrix(3, matrixp3)
        self.assertRaises(exceptions.InconsistentStatesError, validations.check_consistent_group_states, group)

    def test_should_not_stop_consistent_states_group(self):
        group = TransitionMatrixGroup()
        matrixp1 = TransitionMatrix('AAA', 'AA')
        matrixp2 = TransitionMatrix('AAA', 'AA')
        matrixp3 = TransitionMatrix('AAA', 'AA')
        group.add_matrix(1, matrixp1)
        group.add_matrix(2, matrixp2)
        group.add_matrix(3, matrixp3)
        validations.check_consistent_group_states(group)


    def test_should_catch_inconsistent_states_group_with_null(self):
        group = TransitionMatrixGroup()
        matrixp1 = TransitionMatrix('AAA', 'AA')
        matrixp2 = TransitionMatrix('AAA', 'AA')
        matrixp4 = TransitionMatrix('AA', 'A')
        group.add_matrix(1, matrixp1)
        group.add_matrix(2, matrixp2)
        group.add_matrix(4, matrixp4)
        self.assertRaises(exceptions.InconsistentStatesError, validations.check_consistent_group_states, group)
