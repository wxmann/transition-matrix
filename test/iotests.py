import unittest
from test import testdata
from calc import io

__author__ = 'tangz'

class IOTest(unittest.TestCase):
    def test_output(self):
        file = "export_test.csv"
        matrix = testdata.valid_transition_mat()
        io.matrix_to_csv(file, matrix, 'FirstMatrixOutput')

    def test_input(self):
        file = "import_test.csv"
        matrix = io.matrix_from_csv(file, ('AAA', 'AA', 'A'))
        self.assertEqual(matrix, testdata.valid_transition_mat())
