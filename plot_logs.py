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


def _process_path(path):
    if path is None:
        # Try current_dir/logs
        pass
    else:
        # See if log files are present in path

        # See if log files are present in path/logs

        # Throw FileNotFoundError
        pass


def _get_log_files(path):
    # Extract list of log files from the path returned from _process_path
    pass


def plot_logs(path):
    path_to_log_files = _process_path(path)
    log_files = _get_log_files(path_to_log_files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot optimization from logs')
    parser.add_argument('path', type=str, default=None,
                        help='Path to log file or directory')
    name_space = parser.parse_args()
    plot_logs(name_space.path)
