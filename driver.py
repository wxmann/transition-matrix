from calc import create, engine, io

__author__ = 'tangz'

def execute_random(initial_state, states, periods, matrixgroup_file, results_file, calc_range=None):
    transmatgroup = create.random_group(states, periods)
    if calc_range:
        results = engine.results(transmatgroup, initial_state, states=states, first_period=calc_range[0], last_period=calc_range[1])
    else:
        results = engine.results(transmatgroup, initial_state, states=states)
    io.matrixgroup_to_csv(matrixgroup_file, transmatgroup)
    io.results_to_file(results, results_file)


def execute_load(initial_state, matrixgroup_file, results_file, calc_range=None):
    transmatgroup = io.matrixgroup_from_csv(matrixgroup_file)
    if calc_range:
        results = engine.results(transmatgroup, initial_state, first_period=calc_range[0], last_period=calc_range[1])
    else:
        results = engine.results(transmatgroup, initial_state)
    io.results_to_file(results, results_file)