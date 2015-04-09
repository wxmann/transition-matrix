from calc import validations
from calc.core import ProbabilityVector

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
    if first_period is None:
        first_period = transmatgroup.firstperiod()
    if last_period is None:
        last_period = transmatgroup.lastperiod()
    if first_period > last_period:
        raise ValueError('First period: {0} is > last period: {1}'.format(first_period, last_period))
    for matrix_assoc in transmatgroup:
        if matrix_assoc.period > last_period:
            break
        matrix = matrix_assoc.matrix
        validations.is_valid(matrix)
        validations.check_consistent_states(matrix, prob_vec_init)

    # now we're okay to do calculation
    probvec = prob_vec_init
    transmatgroup.set_period_marker(first_period)
    period = first_period
    while True:
        yield CalculationResult(period, probvec)
        if period > last_period:
            break
        periodmatassoc_next = next(transmatgroup)
        period_next, transmat_next = periodmatassoc_next.period + 1, periodmatassoc_next.matrix
        probvec = probvec if transmat_next is None else multiply(transmat_next, probvec)
        period = period_next


class CalculationResult:
    def __init__(self, period, probvector):
        self.period = period
        self.probabilities = probvector

    def __str__(self):
        return 'period: {0} | probabilities: {1}'.format(self.period, self.probabilities)
