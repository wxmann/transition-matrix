import unittest
from calc.core import TransitionMatrix
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
