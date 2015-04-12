from calc import validations
from calc.core import TransitionMatrix, TransitionMatrixGroup, ProbabilityVector
from random import uniform
from util import logutil

__author__ = 'tangz'

def random_group(states, periods):
    group = TransitionMatrixGroup()
    for period in periods:
        matrix = random_matrix(*states)
        group.add_matrix(period, matrix)
    return group

def random_matrix(*states):
    transmat = TransitionMatrix(*states)
    statelist = list(states)
    last_state = statelist[-1]
    for current_state in states:
        for future_state in states:
            random_prob = _prob_helper(transmat, current_state, future_state, last_state)
            transmat.set_probability(current_state, future_state, random_prob)
    return transmat

def _prob_helper(transmat, current_state, future_state, last_state):
    probsto = transmat.probabilities_to(future_state)
    probsfrom = transmat.probabilities_from(current_state)
    lastprob_to = 1 - sum(probsto.values())
    lastprob_from = 1 - sum(probsfrom.values())
    validations.check_valid_probs(lastprob_to, lastprob_from)

    generated_prob = 0
    if current_state is last_state:
        generated_prob = lastprob_to
    elif future_state is last_state:
        generated_prob = lastprob_from
    else:
        upperbound = min(lastprob_from, lastprob_to)
        lowerbound = max(0.0, upperbound/2 - 0.1)
        generated_prob = uniform(lowerbound, upperbound)

    logutil.info('generated probability for current state: {0}, future state: {1}, is: {2}'.format(current_state, future_state, generated_prob))
    return generated_prob

def probability_exact(exact_state, possible_states):
    if not exact_state in possible_states:
        raise ValueError('Exact state provided is not in list of possible states!')
    mapping = {state: 1.0 if exact_state == state else 0.0 for state in possible_states}
    return ProbabilityVector(**mapping)


