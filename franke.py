import numpy as np
from numba import jit


@jit(nopython=True)
def franke(x, y):
    """Computes the Franke function

    The function was developed by Richard Franke as a test function for use in
    data interpolation testing [1]. "This surface consists of two Gaussian
    peaks and a sharper Gaussian dip superimposed on a surface sloping toward
    the first quadrant. The latter was included mainly to enhance the visual
    aspects of the surface (...)"
    The Franke function is usually computed on the grid [0,1] x [0,1] of x and
    y values.

    Parameters
    ----------
    x : numpy.array
        Meshgrid coordinate array for vectorized evaluations of the function
    y : numpy.array
        Meshgrid coordinate array for vectorized evaluations of the function

    Returns
    -------
    numpy.array
        The value of the Franke function at the vector points specified by the
        input parameters x and y

    [1] FRANKE, Richard. A critical comparison of some methods for
        interpolation of scattered data. Monterey, California: Naval
        Postgraduate School., 1979.
    """
    return (0.75 * np.exp(-((9*x - 2)**2) / 4 - ((9*y - 2)**2) / 4)
            + 0.75 * np.exp(-((9*x + 1)**2) / 49 - (9*y + 1) / 10)
            + 0.5 * np.exp(-((9*x - 7)**2) / 4 - ((9*y - 3)**2) / 4)
            - 0.2 * np.exp(-((9*x - 4)**2) - ((9*y - 7)**2)))
