from calc import validations
from calc import create
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
    if last_period is not None and first_period > last_period:
        raise ValueError('First period: {0} is > last period: {1}'.format(first_period, last_period))
    validations.check_consistent_group_states(transmatgroup)
    probvec = prob_vec_init
    if last_period is not None:
        last_period += 1
    for matrix_assoc in matrixrange(transmatgroup, first_period, last_period):
        # TODO: check if probability vector sums to 1?
        matrix = matrix_assoc.matrix
        non_null_matrix = matrix is not None
        if non_null_matrix:
            validations.is_valid(matrix)
            validations.check_consistent_states(matrix, probvec)
        period = matrix_assoc.period
        yield CalculationResult(period, probvec)
        if non_null_matrix:
            probvec = multiply(matrix, probvec)


def results(transmatgroup, initial_state, states, first_period=None, last_period=None):
    init_vec = create.probability_exact(initial_state, states)
    return (result for result in calculator(transmatgroup, init_vec, first_period, last_period))


class CalculationResult:
    def __init__(self, period, probvector):
        self.period = period
        self.probabilities = probvector

    def __str__(self):
        return 'period: {0} | probabilities: {1}'.format(self.period, self.probabilities)
