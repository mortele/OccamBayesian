import os
import re
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import bayes_opt as opt


def occam_parameters(path, steps=1000, kappa=1.0):
    """
    Search replace numbers in OCCAM fort.1 and fort.3 files to specify
    simulation details.
    """
    with open(os.path.join(path, 'fort.1'), 'r') as in_file:
        with open(os.path.join(path, 'fort.1_tmp'), 'w') as out_file:
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
    os.rename(os.path.join(path, 'fort.1'), os.path.join(path, 'fort.1_old'))
    os.rename(os.path.join(path, 'fort.1_tmp'), os.path.join(path, 'fort.1'))

    with open(os.path.join(path, 'fort.3'), 'r') as in_file:
        with open(os.path.join(path, 'fort.3_tmp'), 'w') as out_file:
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
    os.rename(os.path.join(path, 'fort.3'), os.path.join(path, 'fort.3_old'))
    os.rename(os.path.join(path, 'fort.3_tmp'), os.path.join(path, 'fort.3'))


def occam_function(path, executable_name='occamcg'):
    pass


def occam_optimize(path, steps=500, kappa=np.linspace(0.1, 1.0, 10)):
    pass


if __name__ == '__main__':
    OCCAM_PATH = os.path.join('..', 'OCCAM', 'bin')
    occam_optimize(OCCAM_PATH)
