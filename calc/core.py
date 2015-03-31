from calc.exceptions import InvalidTransitionStateError
from calc.validations import check_state_valid
from collections import defaultdict

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

# TODO: make iterable (generator?)
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
        return self.group.keys()

    def firstperiod(self):
        sortedperiods = sorted(self.periods())
        if not sortedperiods:
            return None
        return sortedperiods[0]

    def lastperiod(self):
        reversesortedperiods = sorted(self.periods(), reverse=True)
        if not reversesortedperiods:
            return None
        return reversesortedperiods[0]

    # def __bool__(self):
    #     return not self.group


class TransitionMatrix:
    def __init__(self, *states):
        self.data = defaultdict(dict)
        self.reset_states(states)

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
        check_state_valid(self, current_state, future_state)
        self.data[current_state][future_state] = probability

    def get_probability(self, current_state, future_state):
        check_state_valid(self, current_state, future_state)
        return self.data[current_state][future_state]

    def probabilities_from(self, current_state):
        check_state_valid(self, current_state)
        return self.data[current_state].copy()

    def probabilities_to(self, future_state):
        check_state_valid(self, future_state)
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