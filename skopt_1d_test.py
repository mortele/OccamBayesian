import numpy as np
import skopt
import matplotlib.pyplot as plt


def target(x, noise_variance=0.0):
    return (np.sin(5 * x) * (1 - np.tanh(x**2))
            + np.random.randn(*x.shape) * noise_variance)


def main():
    noise_variance = 0.1
    x = np.linspace(-2, 2, 400)
    f_exact = target(x, noise_variance=0.0)
    plt.plot(x, f_exact, 'k-', label='true target')
    plt.fill_between(x,
                     f_exact - 1.96 * noise_variance,
                     f_exact + 1.96 * noise_variance,
                     color='r', alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('target')
    plt.legend()

    skip = 5
    f_sampled = target(x[::skip], noise_variance=noise_variance)
    plt.plot(x[::skip], f_sampled, 'b^', label='sampled')
    plt.xlim(-2, 2)
    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()
