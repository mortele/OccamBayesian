# /usr/local/bin/python3
import os
import numpy as np
from math import isnan
from bayes_opt import BayesianOptimization
from bayes_opt.observer import JSONLogger
from bayes_opt.event import Events
from bayes_opt.util import load_logs
from franke import franke
from visualize_2d import PlotProgress_2D
from save_optimizer import new_log_file_name, find_log_files


param_file_name = 'param.dat'
result_file_name = 'res.dat'


def _check_steps_finite(steps):
    if isnan(steps) or np.isnan(steps):
        return False
    elif steps < 0:
        return False
    else:
        return True


def change_parameters(*params):
    """Sets the parameters for the current simulation run"""
    with open(param_file_name, 'w') as out_file:
        for p in params:
            out_file.write(str(p) + '\n')


def run_simulation():
    """Start the actual simulation run"""
    params = []
    with open(param_file_name, 'r') as in_file:
        for line in in_file:
            params.append(float(line))

    with open(result_file_name, 'w') as out_file:
        f = franke(*tuple(params))
        out_file.write(str(f))


def extract_results():
    """Extracts the results from the last simulation run"""
    res = []
    with open(result_file_name, 'r') as in_file:
        for line in in_file:
            res.append(float(line))
    return res


def cost(result):
    """Cost function to maximize"""
    target = 1.5
    return - (result - target)**2


def optimize_2d(path=None, steps=None, init_points=None, bounds=None,
                true_function=None, plot=False, load=False):

    def wrapper(x, y):
        change_parameters(x, y)
        run_simulation()
        res = extract_results()
        return cost(res[0])

    opt = BayesianOptimization(f=wrapper,
                               pbounds=bounds,
                               verbose=2,
                               random_state=92898)
    log_file = new_log_file_name()
    logger = JSONLogger(path=log_file)
    opt.subscribe(Events.OPTMIZATION_STEP, logger)
    print('Logging to logfile: ', log_file)

    if load:
        files = find_log_files()
        load_logs(opt, logs=files)

        print('Loading previous runs form logfile(s):')
        for f in files:
            print(f)
    else:
        opt.maximize(init_points=init_points, n_iter=0)

    if _check_steps_finite(steps):
        for _ in range(steps):
            opt.maximize(init_points=0, n_iter=1)
    else:
        while True:
            opt.maximize(init_points=0, n_iter=1)
    print("MAX: ", opt.max)
    return opt


if __name__ == '__main__':
    opt = optimize_2d(steps=1, init_points=1,
                      bounds={'x': (0, 1), 'y': (-0.2, 1)}, load=True)
