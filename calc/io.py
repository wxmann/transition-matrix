from collections import defaultdict, OrderedDict
import csv
from calc import core

__author__ = 'tangz'

DEFAULT_MATRIX_ID_COL = 'NAME'
DEFAULT_CURRENT_STATE_HEADER = 'START_STATE'
DEFAULT_FUTURE_STATE_HEADER = 'END_STATE'
DEFAULT_PROBABILITY_HEADER = 'PROBABILITY'
DEFAULT_PERIOD_ID_COL = 'PERIOD'


def results_to_file(results_map, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = None
        for period, probvec in results_map.items():
            states = list(probvec.states())
            states.sort()
            if writer is None:
                writer = csv.DictWriter(csvfile, ['PERIOD'] + states)
                writer.writeheader()
            row = {'PERIOD': period}
            row.update(probvec.vectordict)
            writer.writerow(row)


# TODO: add flag to write into separate files
def matrixgroup_to_csv(file, transmatgroup, matrix_id_col=DEFAULT_MATRIX_ID_COL,
                       current_state_col=DEFAULT_CURRENT_STATE_HEADER,
                       future_state_col=DEFAULT_FUTURE_STATE_HEADER, prob_col=DEFAULT_PROBABILITY_HEADER):
    csvfile = open(file, 'w', newline='')
    try:
        writer = csv.DictWriter(csvfile, (matrix_id_col, current_state_col, future_state_col, prob_col))
        writer.writeheader()
        for period, matrix in core.matrixrange(transmatgroup):
            if matrix is not None:
                matrixid = 'Matrix_Period_' + str(period)
                _write_matrix(writer, matrix, matrixid, matrix_id_col, current_state_col, future_state_col, prob_col)
    finally:
        csvfile.close()


# TODO: test
# def matrixgroup_from_csv(period_file_map, current_state_col=DEFAULT_CURRENT_STATE_HEADER,
#                          future_state_col=DEFAULT_FUTURE_STATE_HEADER, prob_col=DEFAULT_PROBABILITY_HEADER):
#     group = core.TransitionMatrixGroup()
#     for period, file in period_file_map.items():
#         matrix = matrix_from_csv(file, current_state_col, future_state_col, prob_col)
#         group.add_matrix(period, matrix)

def matrixgroup_from_csv(file, period_id_col=DEFAULT_PERIOD_ID_COL, current_state_col=DEFAULT_CURRENT_STATE_HEADER,
                          future_state_col=DEFAULT_FUTURE_STATE_HEADER, prob_col=DEFAULT_PROBABILITY_HEADER):
    rawdata_map = {}
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            period = int(line[period_id_col])
            if period not in rawdata_map:
                matrix_dict = defaultdict(dict)
                rawdata_map[period] = matrix_dict
            else:
                matrix_dict = rawdata_map[period]
            current_state = line[current_state_col]
            future_state = line[future_state_col]
            prob = float(line[prob_col])
            matrix_dict[current_state][future_state] = prob

    matrixgroup = core.TransitionMatrixGroup()
    for period in rawdata_map:
        matrix = core.TransitionMatrix.from_values(rawdata_map[period])
        matrixgroup.add_matrix(period, matrix)
    return matrixgroup


def matrix_to_csv(file, matrix, matrixid, matrix_id_col=DEFAULT_MATRIX_ID_COL,
                  current_state_col=DEFAULT_CURRENT_STATE_HEADER,
                  future_state_col=DEFAULT_FUTURE_STATE_HEADER, prob_col=DEFAULT_PROBABILITY_HEADER):
    with open(file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, (matrix_id_col, current_state_col, future_state_col, prob_col))
        writer.writeheader()
        _write_matrix(writer, matrix, matrixid, matrix_id_col, current_state_col, future_state_col, prob_col)


def _write_matrix(dictwriter, matrix, matrixid, matrix_id_col, current_state_col, future_state_col, prob_col):
    for future_state in matrix.states:
        for current_state in matrix.states:
            row = {matrix_id_col: matrixid, current_state_col: current_state, future_state_col: future_state,
                   prob_col: matrix.get_probability(current_state, future_state)}
            dictwriter.writerow(row)


def matrix_from_csv(file, current_state_col=DEFAULT_CURRENT_STATE_HEADER,
                    future_state_col=DEFAULT_FUTURE_STATE_HEADER, prob_col=DEFAULT_PROBABILITY_HEADER):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        return _read_matrix(reader, current_state_col, future_state_col, prob_col)


def _read_matrix(dictreader, current_state_col, future_state_col, prob_col):
    matrix_dict = defaultdict(dict)
    for line in dictreader:
        current_state = line[current_state_col]
        future_state = line[future_state_col]
        prob = float(line[prob_col])
        matrix_dict[current_state][future_state] = prob
    return core.TransitionMatrix.from_values(matrix_dict)


