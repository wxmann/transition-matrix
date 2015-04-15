import unittest
from test import testdata
from calc import io, create

__author__ = 'tangz'

class IOTest(unittest.TestCase):
    def test_output(self):
        file = "export_test.csv"
        matrix = testdata.valid_transition_mat()
        io.matrix_to_csv(file, matrix, 'FirstMatrixOutput')

    def test_output_group(self):
        file = "export_test_group.csv"
        matrix_group = create.random_group(('AAA', 'AA', 'A', 'B', 'C'), [1, 2, 3, 4, 5, 7, 9, 10])
        io.matrixgroup_to_csv(file, matrix_group)

    def test_input(self):
        file = "import_test.csv"
        matrix = io.matrix_from_csv(file, ('AAA', 'AA', 'A'))
        self.assertEqual(matrix, testdata.valid_transition_mat())
