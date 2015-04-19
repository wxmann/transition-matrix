from calc import validations
from calc.core import TransitionMatrix, TransitionMatrixGroup, ProbabilityVector
import random
from util import logutil

__author__ = 'tangz'

_DIFFERENTIATOR = 0.7


def random_group(states, periods):
    group = TransitionMatrixGroup()
    for period in periods:
        matrix = random_matrix(*states)
        group.add_matrix(period, matrix)
    return group


def random_matrix(*states):
    if len(states) <= 1:
        raise ValueError('Must have at least two states to create random matrix successfully')
    transmat = TransitionMatrix(*states)
    _diagonal_prob_helper(transmat)
    for current_state in states:
        future_nonequiv_states = _future_states_helper(states, current_state)
        _nondiagonal_prob_helper(transmat, current_state, future_nonequiv_states)
    return transmat


def _future_states_helper(all_states, current_state):
    future_states_in_order = []
    i_0 = all_states.index(current_state)
    num_states = len(all_states)
    for j in range(1, num_states):
        i_pj = i_0 + j
        i_nj = i_0 - j
        if i_pj < num_states:
            future_states_in_order.append(all_states[i_pj])
        if i_nj >= 0:
            future_states_in_order.append(all_states[i_nj])
    return future_states_in_order


def _diagonal_prob_helper(transmat, lowerbound=_DIFFERENTIATOR):
    upperbound = 1.0
    for state in transmat.states:
        prob = random.uniform(lowerbound, upperbound)
        logutil.info(
            'generated probability for current state: {0}, future state: {1}, is: {2}'.format(state, state, prob))
        validations.check_valid_probs(prob)
        transmat.set_probability(state, state, prob)


def _nondiagonal_prob_helper(transmat, current_state, future_states):
    last_state = future_states[-1]
    for future_state in future_states:
        probsfrom = transmat.probabilities_from(current_state)
        sum1m = 1 - sum(probsfrom.values())
        generated_prob = sum1m if future_state is last_state else random.uniform(0.0, sum1m)
        validations.check_valid_probs(generated_prob)
        logutil.info('generated probability for current state: {0}, future state: {1}, is: {2}'.format(current_state,
                                                                                                       future_state,
                                                                                                       generated_prob))
        transmat.set_probability(current_state, future_state, generated_prob)


def probability_exact(exact_state, possible_states):
    if not exact_state in possible_states:
        raise ValueError('Exact state provided is not in list of possible states!')
    mapping = {state: 1.0 if exact_state == state else 0.0 for state in possible_states}
    return ProbabilityVector(**mapping)


