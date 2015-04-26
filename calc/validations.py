import calc.core
from calc.exceptions import *
from util.mathutil import eq

__author__ = 'tangz'

# TODO: we can probably get rid of this, it's built into transmatgroup.states()
def check_consistent_group_states(transition_mat_group):
    states = ()
    for period, matrix in calc.core.matrixrange(transition_mat_group):
        if matrix is None:
            continue
        if not states:
            states = matrix.states
        elif not sorted(matrix.states) == sorted(states):
            raise InconsistentStatesError('Transition matrix group does not have consisted states!')


### General methods ###

def check_valid_probs(*probs):
    if any(prob > 1.0 or prob < 0.0 for prob in probs):
        raise InvalidProbabilityError(
            'Invalid probability found (> 1 or < 0)! Check the probabilities again: {0}'.format(probs))


def check_probs_sum_to_one(*probs):
    if not eq(sum(probs), 1.0):
        raise UnnormalizedProbabilitiesError(
            "Sum of probabilities: {0} is not equal to 1.0 where it is expected to.".format(probs))


### Specific to transition matrix ###

def is_valid(transition_mat):
    if len(transition_mat.states) <= 1:
        raise ValueError("Transition matrix must have at least two states!")
    check_matrix_probs(transition_mat)
    check_normalized_probs(transition_mat)


def check_matrix_probs(transition_mat):
    check_valid_probs(*transition_mat.values())


def check_normalized_probs(transition_mat):
    states = transition_mat.states
    for state in states:
        check_probs_sum_to_one(*transition_mat.probabilities_from(state).values())


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

### Specific to probability vector ###

def is_valid_prob_vector(probvector):
    check_probs_sum_to_one(*probvector.values())