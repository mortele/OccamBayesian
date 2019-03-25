import os
import sys
import argparse
import numpy as np
from math import isnan
from bayes_opt import BayesianOptimization
from bayes_opt.observer import JSONLogger
from bayes_opt.event import Events
from bayes_opt.util import load_logs
from franke import franke
from visualize_2d import PlotProgress_2D
from save_optimizer import new_log_file_name, find_log_files


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
    # Extract list of log files from the path returned from _process_path
    all_files = os.listdir(path)
    log_files = []
    for f in all_files:
        if ('log' in f) and ('.json' in f):
            log_files.append(f)
    assert len(log_files) != 0
    return log_files


def plot_logs(path):
    path_to_log_files = _process_path(path)
    print(path_to_log_files)
    log_files = _get_log_files(path_to_log_files)
    print(log_files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot optimization from logs')
    parser.add_argument('path', type=str, nargs='?', default=None,
                        help='Path to log file or directory')
    name_space = parser.parse_args()
    plot_logs(name_space.path)
