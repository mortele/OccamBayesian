# /usr/local/bin/python3
import os
import subprocess
import matplotlib.pyplot as plt
from bayes_opt import BayesianOptimization
from file_read_backwards import FileReadBackwards
from visualize_progress import plot_gp


def _replace_in_file(file_name, key, value):
    """Create a new file with one change from the given file_name
    """
    tmp_name = file_name + '_tmp'
    old_name = file_name + '_old'
    with open(file_name, 'r') as in_file, open(tmp_name, 'w') as out_file:
        next = False
        for line in in_file:
            if next:
                out_file.write(str(value) + '\n')
                next = False
            else:
                if key in line:
                    next = True
                out_file.write(line)
    os.rename(file_name, old_name)
    os.rename(tmp_name, file_name)


def _read_total_pressure():
    with FileReadBackwards('fort.7') as in_file:
        for _ in range(50):
            line = in_file.readline()
            if line:
                line = line.split()
                if len(line) > 2:
                    if line[1] == 'total' and line[2] == 'press':
                        pressure = float(line[0])
            else:
                break
    return pressure


def occam_parameters(steps=None, kappa=None):
    """Search replace numbers in OCCAM fort.1 and fort.3 files to specify
    simulation details.
    """
    _replace_in_file('fort.1', 'number_of_steps', steps)
    _replace_in_file('fort.3', 'compressibility', kappa)


def occam_function(path, executable_name='occamcg'):
    """The 'black-box' function we optimize, w.r.t. the parameters adjusted in the
    occam_parameters function.
    """
    subprocess.call(os.path.join(path, executable_name),
                    stdout=subprocess.DEVNULL)
    return _read_total_pressure()


def occam_optimize(path, steps, kappa, init_points=10):
    """Wrapper function for performing the entire optimization procedure.
    """
    target_pressure = 26.1514

    def opt_target(x):
        """Input for the BayesianOptimization procedure from the bayes_opt
        package.

        The Bayesian optimization is a maximization procedure, so we have to
        define a cost function which takes a maximum where the difference
        between the target pressure and the measured pressure is smallest.
        """
        occam_parameters(steps=steps, kappa=x)
        pressure = occam_function(path)
        # cost = 1.0 / np.sqrt(np.abs(pressure - target_pressure) + 0.5)
        # cost = -abs(pressure - target_pressure)
        # cost = 1.0 / ((pressure - target_pressure)**2 + 0.5)
        cost = - (pressure - target_pressure)**2
        return cost

    p_bounds = {'x': (kappa[0], kappa[1])}
    opt = BayesianOptimization(f=opt_target,
                               pbounds=p_bounds,
                               verbose=2,
                               random_state=92898)
    opt.maximize(init_points=init_points, n_iter=0, kappa=5)

    """
    fit_param = np.array([-496.8262311718876,
                          2273.7122821175550,
                          -3724.1669657791103,
                          2747.1118106958093,
                          -764.3924710639956])
    fit_exponents = np.array([0.25, 0.5, 0.75, 1])
    x = np.linspace(kappa[0], kappa[1], 1000).reshape(-1, 1)
    y = (fit_param[0]
         + x**fit_exponents[0] * fit_param[1]
         + x**fit_exponents[1] * fit_param[2]
         + x**fit_exponents[2] * fit_param[3]
         + x**fit_exponents[3] * fit_param[4])
    y = 1.0 / ((y - target_pressure)**2 + 0.5)
    """

    for _ in range(20):
        opt.maximize(init_points=0, n_iter=5)
        # plot_gp(opt, x, y, set_xlim=(kappa[0], kappa[1]))
        plot_gp(opt,
                set_xlim=(kappa[0], kappa[1]))
        plt.show()
    print(opt.max)


if __name__ == '__main__':
    OCCAM_PATH = os.path.join('..', 'OCCAM', 'bin')
    occam_optimize(OCCAM_PATH, 1000, (0.01, 1.0), init_points=10)
