from calc.exceptions import InvalidTransitionStateError
import calc.validations
from collections import defaultdict
from util import mathutil

__author__ = 'tangz'


class ProbabilityVector:
    def __init__(self, **initprobs):
        self.vectordict = {}
        for state in initprobs.keys():
            self.vectordict[state] = initprobs[state]

    def set(self, state, prob):
        self.vectordict[state] = prob

    def states(self):
        return self.vectordict.keys()

    def get(self, state):
        if not state in self.states():
            raise InvalidTransitionStateError('Invalid state: ' + state)
        return self.vectordict[state]

    def __str__(self):
        return str(self.vectordict)

    def __eq__(self, other):
        if not isinstance(other, ProbabilityVector):
            return False
        return self is other or self.vectordict == other.vectordict

    def __hash__(self):
        return hash(self.vectordict)

# def matrixrange(matrix_group):
#     matrixrange(matrix_group, 1, matrix_group.lastperiod() + 1)
#
#
# def matrixrange(matrix_group, period_stop):
#     matrix_group.reset_period_marker()
#     for per_matrix in matrix_group:
#         if per_matrix.period >= period_stop:
#             break
#         yield per_matrix


def matrixrange(matrix_group, period_start=1, period_stop=None):
    if period_stop is None:
        period_stop = matrix_group.lastperiod() + 1
    matrix_group.set_period_marker(period_start)
    for per_matrix in matrix_group:
        if per_matrix.period >= period_stop:
            break
        yield per_matrix


class TransitionMatrixGroup:
    def __init__(self):
        self.group = {}
        self.reset_period_marker()

    def __iter__(self):
        return self

    def _pmarker_incrementer(self):
        if not self.group:
            self.reset_period_marker()
        self.pmarker += 1

    def __next__(self):
        nextval = self.PeriodMatrixAssociation(self.pmarker, self.get_matrix(self.pmarker))
        self._pmarker_incrementer()
        return nextval

    def add_matrix(self, period, transition_mat):
        self.group[period] = transition_mat

    def has_matrix(self, period):
        return period in self.group.keys()

    def get_matrix(self, period):
        return self.group.get(period)

    def periods(self):
        return list(sorted(self.group.keys()))

    def firstperiod(self):
        return self.periods()[0]

    def lastperiod(self):
        return self.periods()[-1]

    def reset_period_marker(self):
        self.set_period_marker(1)

    def set_period_marker(self, period):
        if period <= 0:
            raise ValueError('Period must be a positive integer!')
        self.pmarker = period

    class PeriodMatrixAssociation:
        def __init__(self, period, matrix):
            self.period = period
            self.matrix = matrix


# TODO: str
class TransitionMatrix:
    def __init__(self, *states):
        self.data = defaultdict(dict)
        self.reset_states(states)

    def __eq__(self, other):
        if not isinstance(other, TransitionMatrix):
            return False
        else:
            return self is other or (self._states_eq(other) and self._probs_eq(other))

    def _states_eq(self, other):
        return sorted(self.states) == sorted(other.states)

    def _probs_eq(self, other):
        for current_state in self.states:
            for future_state in self.states:
                if not mathutil.eq(self.get_probability(current_state, future_state),
                                   other.get_probability(current_state, future_state)):
                    return False
        return True

    def __hash__(self):
        return hash(self.data)

    # def __str__(self):
    # firstrow =


    def reset_states(self, states):
        self.states = states
        for s_out in states:
            temp = dict()
            for s_in in states:
                temp[s_in] = 0
            self.data[s_out] = temp

    def state_exists(self, state):
        return state in self.states

    def set_probability(self, current_state, future_state, probability):
        calc.validations.check_state_valid(self, current_state, future_state)
        self.data[current_state][future_state] = probability

    def get_probability(self, current_state, future_state):
        calc.validations.check_state_valid(self, current_state, future_state)
        return self.data[current_state][future_state]

    def probabilities_from(self, current_state):
        calc.validations.check_state_valid(self, current_state)
        return self.data[current_state].copy()

    def probabilities_to(self, future_state):
        calc.validations.check_state_valid(self, future_state)
        states = self.states
        current_prob_dict = dict()
        for current_state in states:
            current_prob_dict[current_state] = self.get_probability(current_state, future_state)
        return current_prob_dict

    def values(self):
        values = []
        for state in self.states:
            probs = self.probabilities_from(state)
            values.extend(probs.values())
        return values