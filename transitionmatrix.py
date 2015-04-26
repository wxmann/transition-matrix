import argparse
import datetime
import logging
import driver

__author__ = 'tangz'


def run_generate(args):
    initial_state = args.initial_state
    states = args.all_states
    if args.range:
        periods = range(args.range[0], args.range[1] + 1)
    else:
        periods = args.periods
    matrixgroup_file = args.matrix_output
    results_file = args.results
    calc_range = args.calc_range
    driver.execute_random(initial_state, states, periods, matrixgroup_file, results_file, calc_range)


def run_load(args):
    initial_state = args.initial_state
    matrixgroup_file = args.matrix_input
    result_file = args.results
    calc_range = args.calc_range
    driver.execute_load(initial_state, matrixgroup_file, result_file, calc_range)


def main():
    timestr = datetime.datetime.now().strftime("%y%m%d%H%M%S")
    timestampedfile = 'TransitionMatrix-{0}.log'.format(timestr)
    logging.basicConfig(filename=timestampedfile, level=logging.INFO)

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('-i', '--initial-state',
                               help='Initial transition state. Required. Must be one of the states provided in -s arguments.',
                               required=True)
    common_parser.add_argument('-o', '--results',
                               help='Output file for calculated forecasted probabilities [default: results.csv]',
                               default='results.csv')
    common_parser.add_argument('-R', '--calc-range',
                               help='''Period range from two arguments (inclusive) to calculate results, both must be positive integers.
                               By default, calculation starts on first period and goes to the last period
                               that transition matrix exists.''',
                               nargs=2, type=int)

    main_parser = argparse.ArgumentParser(description='Transition matrix calculation script')
    subparsers = main_parser.add_subparsers(description='Calculation Options', dest='mode')

    generator_parser = subparsers.add_parser('generate', help='Generate transition matrices randomly',
                                             parents=[common_parser])
    generator_parser.add_argument('-s', '--all-states', help='Transition states. Required.', nargs='+', required=True)
    generator_parser.add_argument('-p', '--periods',
                                  help='''Periods to generate transition matrices, must be positive integer
                                  [default: 1; overriden by -r argument]''',
                                  default=[1], type=int, nargs='*')
    generator_parser.add_argument('-r', '--range',
                                  help='''Period range from two arguments (inclusive) to generate transition matrix, must
                                  both be positive integers [overrides -p if present]''''',
                                  type=int, nargs=2)
    generator_parser.add_argument('-m', '--matrix-output',
                                  help='Output file for generated transition matrices [default: output_matrices.csv]',
                                  default='output_matrices.csv')

    load_parser = subparsers.add_parser('load', help='Load transition matrices from file', parents=[common_parser])
    load_parser.add_argument('-f', '--matrix-input',
                             help='Input file for transition matrices. Required.',
                             required=True, default='input_matrices.csv')

    args = main_parser.parse_args()
    if args.mode == 'load':
        run_load(args)
    elif args.mode == 'generate':
        run_generate(args)
    else:
        main_parser.print_usage()


if __name__ == "__main__":
    main()