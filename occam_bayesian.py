import os
import re
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import bayes_opt as opt
from file_read_backwards import FileReadBackwards


def occam_parameters(steps=1000, kappa=1.0):
    """
    Search replace numbers in OCCAM fort.1 and fort.3 files to specify
    simulation details.
    """
    with open('fort.1', 'r') as in_file:
        with open('fort.1_tmp', 'w') as out_file:
            i = -1
            while True:
                line = in_file.readline()
                i += 1
                if line:
                    if line.strip() == 'number_of_steps:':
                        in_file.readline()
                        out_file.write('number_of_steps:\n')
                        out_file.write('{n_steps}\n'.format(n_steps=steps))
                    else:
                        out_file.write(line)
                else:
                    break
    os.rename('fort.1', 'fort.1_old')
    os.rename('fort.1_tmp', 'fort.1')

    with open('fort.3', 'r') as in_file:
        with open('fort.3_tmp', 'w') as out_file:
            i = -1
            while True:
                line = in_file.readline()
                i += 1
                if line:
                    if line.strip() == '* compressibility':
                        in_file.readline()
                        out_file.write('* compressibility\n')
                        out_file.write('{kappa}\n'.format(kappa=kappa))
                    else:
                        out_file.write(line)
                else:
                    break
    os.rename('fort.3', 'fort.3_old')
    os.rename('fort.3_tmp', 'fort.3')


def occam_function(path, executable_name='occamcg'):
    """
    The 'black-box' function we optimize, w.r.t. the parameters adjusted in the
    occam_parameters function.
    """
    subprocess.call(os.path.join(path, executable_name))

    # Extract the total pressure from the fort.7 file.
    pressure = None
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


def occam_optimize(path, steps=100, kappa=np.linspace(0.1, 1.0, 10)):
    """
    Wrapper function for performing the entire optimization procedure.
    """
    occam_parameters(steps=steps, kappa=kappa[0])
    occam_function(path)


if __name__ == '__main__':
    OCCAM_PATH = os.path.join('..', 'OCCAM', 'bin')
    occam_optimize(OCCAM_PATH)
