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
    # 4. transition matrix group states must be consistent (but if validation (2) passes, this follows)

    if first_period is None:
        first_period = transmatgroup.firstperiod()
    elif last_period is not None and first_period > last_period:
        raise ValueError('First period: {0} is > last period: {1}'.format(first_period, last_period))

    probvec = prob_vec_init
    validations.is_valid_prob_vector(probvec)
    yield first_period, probvec
    for period, matrix in matrixrange(transmatgroup, first_period, last_period):
        if matrix is not None:
            validations.is_valid(matrix)
            validations.check_consistent_states(matrix, probvec)
            probvec = multiply(matrix, probvec)
            validations.is_valid_prob_vector(probvec)
        yield period + 1, probvec



def results(transmatgroup, initial_state, first_period=None, last_period=None):
    states = transmatgroup.states()
    init_vec = create.probability_exact(initial_state, states)
    return {period: vec for period, vec in calculator(transmatgroup, init_vec, first_period, last_period)}
