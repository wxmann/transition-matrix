from functools import reduce
from calc.exceptions import *
from util.mathutil import eq

__author__ = 'tangz'

# TODO: check consistent states between probability vector and transition matrix

# TODO: unit test
def check_consistent_states(transition_mat_group):
    states = None
    for period in transition_mat_group.periods():
        mat = transition_mat_group.get_matrix(period)
        if mat is not None:
            if states is None:
                states = mat.states
            elif set(states) != set(mat.states):
                raise InconsistentStatesError("Found inconsistent states in transition matrix group.")


### General methods ###

def check_valid_probs(*probs):
    if any(prob > 1.0 or prob < 0.0 for prob in probs):
        raise InvalidProbabilityError(
            'Invalid probability found (> 1 or < 0)! Check the probabilities again: {}'.format(probs))


def check_probs_sum_to_one(*probs):
    if not eq(sum(probs), 1.0):
        raise UnnormalizedProbabilitiesError(
            "Sum of probabilities: {} is not equal to 1.0 where it is expected to.".format(probs))


### Methods specific to transition matrix ###

def is_valid(transition_mat):
    check_probs_valid(transition_mat)
    check_normalized_probs(transition_mat)


def check_probs_valid(transition_mat):
    check_valid_probs(*transition_mat.values())


def check_normalized_probs(transition_mat):
    states = transition_mat.states
    [check_probs_sum_to_one(*transition_mat.probabilities_from(current_state).values()) for current_state in states]
    [check_probs_sum_to_one(*transition_mat.probabilities_to(future_state).values()) for future_state in states]


def check_state_valid(transition_mat, *states):
    if any(not transition_mat.state_exists(state) for state in states):
        raise InvalidTransitionStateError(
            'Invalid transition state provided! Check the states again: (provided) {} | (in matrix) {}'.format(states,
                                                                                                               transition_mat.states))


def check_consistent_states(transition_mat, prob_vec):
    if not set(transition_mat.states) == set(prob_vec.states()):
        raise InconsistentStatesError(
            'Inconsistent states between transition matrix: {} and probability vector: {}!'.format(
                transition_mat.states(), prob_vec.states()))