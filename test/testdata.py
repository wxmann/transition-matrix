from calc.core import TransitionMatrix, ProbabilityVector

__author__ = 'tangz'


def valid_prob_vec():
    return ProbabilityVector(AAA=0.2, AA=0.5, A=0.3)


def valid_transition_mat():
    valid_trans_mat = TransitionMatrix('AAA', 'AA', 'A')

    valid_trans_mat.set_probability('AAA', 'AAA', 0.3)
    valid_trans_mat.set_probability('AAA', 'AA', 0.5)
    valid_trans_mat.set_probability('AAA', 'A', 0.2)

    valid_trans_mat.set_probability('AA', 'AAA', 0.1)
    valid_trans_mat.set_probability('AA', 'AA', 0.5)
    valid_trans_mat.set_probability('AA', 'A', 0.4)

    valid_trans_mat.set_probability('A', 'AAA', 0.6)
    valid_trans_mat.set_probability('A', 'AA', 0.0)
    valid_trans_mat.set_probability('A', 'A', 0.4)

    return valid_trans_mat


def inc_invalid_trans_mat():
    invalid_mat = TransitionMatrix('AAA', 'AA', 'A')
    count = 1
    for state_outer in invalid_mat.states:
        for state_inner in invalid_mat.states:
            invalid_mat.set_probability(state_outer, state_inner, count)
            count += 1
    return invalid_mat