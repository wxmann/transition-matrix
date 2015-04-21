import argparse

from calc import create, engine, io


__author__ = 'tangz'


def run_random(initial_state, states, periods, matrixgroup_file, results_file):
    transmatgroup = create.random_group(states, periods)
    results = engine.results(transmatgroup, initial_state, states=states)
    io.matrixgroup_to_csv(matrixgroup_file, transmatgroup)
    io.results_to_file(results, results_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transition matrix calculation script')
    parser.add_argument('-s', '--states', help='Transition states. Required.', nargs='+', required=True)
    parser.add_argument('-i', '--initial',
                        help='Initial transition state. Required. Must be one of the states provided in -s arguments.',
                        required=True)
    parser.add_argument('-p', '--periods',
                        help='Periods to generate transition matrices, must be positive integer [default: 1; overriden by -r argument]',
                        default=[1], type=int, nargs='*')
    parser.add_argument('-r', '--range',
                        help='Period range from two arguments (inclusive) to generate transition matrix, must both be positive integers [overrides -p if present]',
                        type=int, nargs=2)
    parser.add_argument('-o', '--results',
                        help='Output file for calculated forecasted probabilities [default: results.csv]',
                        default='results.csv')
    parser.add_argument('-m', '--matrices',
                        help='Output file for generated transition matrices [default: matrices.csv]',
                        default='matrices.csv')
    args = parser.parse_args()

    initial_state = args.initial
    states = args.states
    if args.range:
        periods = range(args.range[0], args.range[1] + 1)
    else:
        periods = args.periods
    matrixgroup_file = args.matrices
    results_file = args.results

    run_random(initial_state, states, periods, matrixgroup_file, results_file)