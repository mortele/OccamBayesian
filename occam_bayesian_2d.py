# /usr/local/bin/python3
import numpy as np
from math import isnan
from bayes_opt import BayesianOptimization
from franke import franke
from visualize_2d import PlotProgress_2D


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


def cost(result, target):
    """Cost function to maximize"""
    return - (result - target)**2


def optimize_2d(path=None, steps=None, init_points=None, bounds=None,
                true_function=None, plot=False):
    target = 1.5

    def wrapper(x, y):
        change_parameters(x, y)
        run_simulation()
        res = extract_results()
        return cost(res[0], target)

    opt = BayesianOptimization(f=wrapper,
                               pbounds=bounds,
                               verbose=2,
                               random_state=92898)
    if plot:
        pp2 = PlotProgress_2D(opt, true_function=true_function,
                              cost=lambda x: cost(x, target))
    opt.maximize(init_points=init_points, n_iter=0)

    if plot:
        pp2.plot()

    if _check_steps_finite(steps):
        for _ in range(steps):
            opt.maximize(init_points=0, n_iter=1)
            if plot:
                pp2.plot()
    else:
        while True:
            opt.maximize(init_points=0, n_iter=1)
            if plot:
                pp2.plot()


if __name__ == '__main__':
    optimize_2d(steps=10, init_points=10,
                bounds={'x': (0, 1), 'y': (-0.2, 1)},
                true_function=franke, plot=False)
