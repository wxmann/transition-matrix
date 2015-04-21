import unittest
from calc.core import ProbabilityVector
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
        matrix = io.matrix_from_csv(file)
        self.assertEqual(matrix, testdata.valid_transition_mat())

    def test_output_results(self):
        filename = "results.csv"
        vecp1 = ProbabilityVector(AAA=0.1, AA=0, A=0.5)
        vecp2 = ProbabilityVector(AAA=0.2, AA=0.3, A=0.4)
        results = {1:vecp1, 2:vecp2}
        io.results_to_file(results, filename)

    def test_import_group(self):
        filename_group = "import_matrix_group_sample.csv"
        filename_p1 = "import_group_expected_p1.csv"
        filename_p2 = "import_group_expected_p2.csv"
        filename_p3 = "import_group_expected_p3.csv"
        matrixgroup = io.matrixgroup_from_csv(filename_group)
        matrixp1 = io.matrix_from_csv(filename_p1)
        matrixp2 = io.matrix_from_csv(filename_p2)
        matrixp3 = io.matrix_from_csv(filename_p3)

        self.assertEqual(matrixgroup.get_matrix(1), matrixp1)
        self.assertEqual(matrixgroup.get_matrix(2), matrixp2)
        self.assertEqual(matrixgroup.get_matrix(3), matrixp3)

