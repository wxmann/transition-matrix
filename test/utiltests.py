import unittest
from util import commandlineutil

__author__ = 'tangz'

class UtilTests(unittest.TestCase):

    def test_parse_states_str(self):
        teststr = "[A,B,C]"
        states = commandlineutil.parse_state_str(teststr)
        self.assertCountEqual(states, ['A', 'B', 'C'])

    def test_parse_states_str_with_whitespace(self):
        teststr = "[A, B, C]"
        states = commandlineutil.parse_state_str(teststr)
        self.assertCountEqual(states, ['A', 'B', 'C'])

    def test_parse_state_str_without_brackets(self):
        teststr = "A, B, C"
        states = commandlineutil.parse_state_str(teststr)
        self.assertCountEqual(states, ['A', 'B', 'C'])

    def test_parse_period_range(self):
        teststr = "1:15"
        self.assertEqual(commandlineutil.parse_periods(teststr), range(1, 16))

    def test_parse_period_enumeration(self):
        teststr = "1, 2, 4, 8"
        self.assertCountEqual(commandlineutil.parse_periods(teststr), [1, 2, 4, 8])
