from calc import validations
from calc.core import ProbabilityVector

__author__ = 'tangz'

def multiply(transition_mat, prob_vec):
    validations.check_consistent_states(transition_mat, prob_vec)
    all_states = transition_mat.states
    future_vect = dict.fromkeys(all_states)
    for future_state in all_states:
        prob_sum = sum(transition_mat.get_probability(existing_state, future_state) * prob_vec.get(existing_state) for
                       existing_state in all_states)
        future_vect[future_state] = prob_sum
    return ProbabilityVector(**future_vect)


def calculator(transmatgroup, prob_vec_init):
    probvec = prob_vec_init
    while True:
        try:
            newprobvec = multiply(transmatgroup.next(), probvec)
            probvec = newprobvec
            yield probvec
        except StopIteration:
            # TODO: log end or something
            pass
