import sys
from calc import create, engine, io
from util import commandlineutil

__author__ = 'tangz'

def run_random(initial_state, states, periods, matrixgroup_file="matrices.csv", results_file="results.csv"):
    transmatgroup = create.random_group(states, periods)
    results = engine.results(transmatgroup, initial_state, states=states)
    io.matrixgroup_to_csv(matrixgroup_file, transmatgroup)
    io.results_to_file(results, results_file)


if __name__ == "__main__":
    args = sys.argv
    initial_state = args[1]
    states = commandlineutil.parse_state_str(args[2])
    periods = commandlineutil.parse_periods(args[3])
    run_random(initial_state, states, periods)