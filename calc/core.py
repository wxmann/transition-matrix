from calc.exceptions import InvalidTransitionStateError, InconsistentStatesError
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

    def values(self):
        return self.vectordict.values()

    def __str__(self):
        return str(self.vectordict)

    def __eq__(self, other):
        if not isinstance(other, ProbabilityVector):
            return False
        return self is other or self._num_eq(self.vectordict, other.vectordict)

    def _num_eq(self, vectordict1, vectordict2):
        if not vectordict1.keys() == vectordict2.keys():
            return False
        for key in vectordict1:
            if not mathutil.eq(vectordict1[key], vectordict2[key]):
                return False
        return True

    def __hash__(self):
        return hash(self.vectordict)


def matrixrange(matrix_group, period_start=1, period_stop=None):
    if period_stop is None:
        period_stop = matrix_group.lastperiod() + 1
    for period in range(period_start, period_stop):
        yield period, matrix_group.get_matrix(period)


class TransitionMatrixGroup:
    def __init__(self):
        self.group = {}

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

    def states(self):
        states = ()
        for period, matrix in matrixrange(self):
            if matrix is None:
                continue
            if not states:
                states = matrix.states
            elif not sorted(matrix.states) == sorted(states):
                raise InconsistentStatesError('Transition matrix group does not have consisted states!')
        return states


# TODO: str
class TransitionMatrix:

    @classmethod
    def from_values(cls, values):
        # honestly, this is not the best way to do it. But I don't see any other choice.
        states = tuple(values.keys())
        matrix = TransitionMatrix(*states)
        for current_state in states:
            for future_state in states:
                matrix.set_probability(current_state, future_state, values[current_state][future_state])
        return matrix

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
                temp[s_in] = 0.0
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