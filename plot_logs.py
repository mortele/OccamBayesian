import os
import json
import warnings
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, gridspec
from matplotlib.widgets import Slider
from bayes_opt import BayesianOptimization
from bayes_opt.util import load_logs


def _log_files_present(files):
    for f in files:
        if ('log' in f) and ('.json' in f):
            return True
    return False


def _process_path(path):
    working_dir = os.getcwd()
    if path is None:
        files = os.listdir(working_dir)
        if _log_files_present(files):
            return working_dir

        working_dir_logs = os.path.join(working_dir, 'logs')
        if (os.path.exists(working_dir_logs)
                and os.path.isdir(working_dir_logs)):
            files = os.listdir(working_dir_logs)
            if _log_files_present(files):
                return working_dir_logs

        error_string = ('No log files found in current_directory ('
                        + working_dir + ') or current_directory/logs.')
        raise FileNotFoundError(error_string)
    else:
        if os.path.exists(path) and os.path.isdir(path):
            files = os.listdir(path)
            if _log_files_present(files):
                return path
        else:
            error_string = ('Given path (' + path + ') [abs path: '
                            + os.path.abspath(path) + '] is not a directory.')
            raise FileNotFoundError(error_string)

        path_logs = os.path.join(path, 'logs')
        if (os.path.exists(path_logs)
                and os.path.isdir(path_logs)):
            files = os.listdir(path_logs)
            if _log_files_present(files):
                return path_logs

        error_string = ('No log files found in ' + path
                        + ' [abs path: ' + os.path.abspath(path) + '] or '
                        + os.path.join(path, 'logs') + '.')
        raise FileNotFoundError(error_string)


def _get_log_files(path):
    all_files = os.listdir(path)
    log_files = []
    for f in all_files:
        if ('log' in f) and ('.json' in f):
            log_files.append(f)
    assert len(log_files) != 0
    return [os.path.abspath(os.path.join(path, f)) for f in log_files]


def _load_bounds_file(path_to_log_files):
    bounds_file = os.path.join(path_to_log_files, 'bounds.json')
    with open(bounds_file, 'r') as in_file:
        bounds = json.load(in_file)
    return bounds


def _plot_iteration(iteration, opt, x, y, X, ax0, ax1, obs_points, obs_targets,
                    gridsize, x_name, y_name):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        opt._gp.fit(obs_points[:][:int(iteration)],
                    obs_targets[:int(iteration)])
        mu, s = opt._gp.predict(X, return_std=True)
    ax0.clear()
    im0 = ax0.hexbin(x, y, C=mu, gridsize=gridsize, cmap=cm.jet, bins=None)
    ax0.axis([x.min(), x.max(), y.min(), y.max()])
    ax0.plot(obs_points[:int(iteration), 0], obs_points[:int(iteration), 1],
             'o', markersize=4, c='k')
    ax0.set_title('Gaussian process mean')

    ax1.clear()
    im1 = ax1.hexbin(x, y, C=s, gridsize=gridsize, cmap=cm.jet, bins=None)
    ax1.axis([x.min(), x.max(), y.min(), y.max()])
    ax1.plot(obs_points[:int(iteration), 0], obs_points[:int(iteration), 1],
             'o', markersize=4, c='k')
    ax1.set_title('Standard deviation')

    for a in (ax0, ax1):
        a.set_xlabel(x_name)
        a.set_ylabel(y_name)
    return im0, im1


def plot_logs(path):
    path_to_log_files = _process_path(path)
    log_files = _get_log_files(path_to_log_files)
    bounds = _load_bounds_file(path_to_log_files)
    opt = BayesianOptimization(f=lambda x, y: None,
                               pbounds=bounds,
                               verbose=2)
    print('Loading optimizer runs from logfile(s):')
    for f in log_files:
        print(f)
    load_logs(opt, logs=log_files)

    keys = list(bounds.keys())
    x_bounds = bounds[keys[0]]
    x_bound_name = keys[0]
    y_bounds = bounds[keys[1]]
    y_bound_name = keys[1]

    gridsize = 50
    x = np.linspace(x_bounds[0], x_bounds[1], 100)
    y = np.linspace(y_bounds[0], y_bounds[1], 100)
    X, Y = np.meshgrid(x, y)
    x = X.ravel()
    y = Y.ravel()
    X = np.vstack([x, y]).T[:, [1, 0]]
    observed_points = np.array([[res['params'][keys[0]],
                                 res['params'][keys[1]]] for res in opt.res])
    observed_targets = np.array([res['target'] for res in opt.res])

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        opt._gp.fit(observed_points, observed_targets)
        mu, s = opt._gp.predict(X, return_std=True)

    fig = plt.figure()
    gs = gridspec.GridSpec(3, 1, height_ratios=[5, 5, 1])
    ax0 = plt.subplot(gs[0, 0])
    ax1 = plt.subplot(gs[1, 0])

    def update(val):
        _plot_iteration(iter_slider.val, opt, x, y, X, ax0, ax1,
                        observed_points, observed_targets, gridsize,
                        x_bound_name, y_bound_name)
        fig.canvas.draw_idle()

    n_iterations = len(observed_targets)
    ax_slider = plt.subplot(gs[2, 0])
    iter_slider = Slider(ax_slider, 'Iteration', 1, n_iterations,
                         valinit=n_iterations, valstep=1)
    iter_slider.on_changed(update)
    im0, im1 = _plot_iteration(n_iterations, opt, x, y, X, ax0, ax1,
                               observed_points, observed_targets, gridsize,
                               x_bound_name, y_bound_name)
    fig.colorbar(im0, ax=ax0)
    fig.colorbar(im1, ax=ax1)

    for a in (ax0, ax1):
        a.set_xlabel(x_bound_name)
        a.set_ylabel(y_bound_name)

    gs.update(hspace=0.5)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot optimization from logs')
    parser.add_argument('path', type=str, nargs='?', default=None,
                        help='Path to log file or directory')
    name_space = parser.parse_args()
    plot_logs(name_space.path)
