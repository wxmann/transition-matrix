from calc import validations
from calc.core import ProbabilityVector, matrixrange

__author__ = 'tangz'


def multiply(transition_mat, prob_vec):
    validations.check_consistent_states(transition_mat, prob_vec)
    all_states = transition_mat.states
    future_vect = {}
    for future_state in all_states:
        prob_sum = sum(transition_mat.get_probability(existing_state, future_state) * prob_vec.get(existing_state) for
                       existing_state in all_states)
        future_vect[future_state] = prob_sum
    return ProbabilityVector(**future_vect)


def calculator(transmatgroup, prob_vec_init, first_period=None, last_period=None):
    # validations:
    # 1. First period <= last period
    # 2. transition matrix group and initial probability vector have to have same states.
    # 3. all transition matrices must be valid.
    # 4. transition matrix group states must be consistent
    if first_period is None:
        first_period = transmatgroup.firstperiod()
    if last_period is None:
        last_period = transmatgroup.lastperiod()
    if first_period > last_period:
        raise ValueError('First period: {0} is > last period: {1}'.format(first_period, last_period))
    validations.check_consistent_group_states(transmatgroup)
    for matrix_assoc in matrixrange(transmatgroup, first_period, last_period + 1):
        matrix = matrix_assoc.matrix
        if matrix is not None:
            validations.is_valid(matrix)
            validations.check_consistent_states(matrix, prob_vec_init)

    # now we're okay to do calculation
    probvec = prob_vec_init
    for periodmatassoc in matrixrange(transmatgroup, first_period, last_period+1):
        period = periodmatassoc.period
        yield CalculationResult(period, probvec)
        matrix = periodmatassoc.matrix
        probvec = probvec if matrix is None else multiply(matrix, probvec)


class CalculationResult:
    def __init__(self, period, probvector):
        self.period = period
        self.probabilities = probvector

    def __str__(self):
        return 'period: {0} | probabilities: {1}'.format(self.period, self.probabilities)
