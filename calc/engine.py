import logging
from calc import validations
from calc import create
from calc.core import ProbabilityVector, matrixrange

__author__ = 'tangz'


def multiply(transition_mat, prob_vec):
    validations.check_consistent_states(transition_mat, prob_vec)
    all_states = transition_mat.states
    future_vect = {}
    for future_state in all_states:
        prob_sum = sum(_calc_and_log_path(transition_mat, prob_vec, current_state, future_state) for current_state in all_states)
        future_vect[future_state] = prob_sum
    return ProbabilityVector(**future_vect)

def _calc_and_log_path(transition_mat, prob_vec, current_state, future_state):
    next_prob = transition_mat.get_probability(current_state, future_state) * prob_vec.get(current_state)
    logging.info('Probability of transitioning to state: {0} from state: {1} is: {2}'.format(future_state, current_state, next_prob))
    return next_prob


def calculator(transmatgroup, prob_vec_init, first_period=1, last_period=None):
    # validations:
    # 1. First period <= last period
    # 2. transition matrix group and initial probability vector have to have same states.
    # 3. all transition matrices must be valid.
    # 4. transition matrix group states must be consistent (but if validation (2) passes, this follows)

    if last_period is not None and first_period > last_period:
        raise ValueError('First period: {0} is > last period: {1}'.format(first_period, last_period))

    probvec = prob_vec_init
    validations.is_valid_prob_vector(probvec)
    calcrange = matrixrange(transmatgroup) if last_period is None else matrixrange(transmatgroup, first_period, last_period + 1)
    for period, matrix in calcrange:
        logging.info('=== Calculating transition matrix paths for period: {0} ==='.format(period))
        if matrix is not None:
            validations.is_valid(matrix)
            validations.check_consistent_states(matrix, probvec)
            probvec = multiply(matrix, probvec)
            validations.is_valid_prob_vector(probvec)
        else:
            logging.info('No transition matrix provided in time period, probabilities remain same.')
        logging.info('Probabilities for period: {0} are {1}'.format(period, probvec))
        yield period, probvec



def results(transmatgroup, initial_state, states=None, first_period=None, last_period=None):
    logging.info('Begin a new calculation for initial state: {0}'.format(initial_state))
    if states is None:
        states = transmatgroup.states()
    init_vec = create.probability_exact(initial_state, states)
    result = {period: vec for period, vec in calculator(transmatgroup, init_vec, first_period, last_period)}
    logging.info('Finish calculating transition matrix probabilities')
    return result
