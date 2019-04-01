import numpy as np
import skopt
import matplotlib.pyplot as plt


def target(x, noise_variance=0.0):
    y = (np.sin(5 * x) * (1 - np.tanh(x**2)
         + np.random.randn(*np.array(x).shape) * noise_variance))
    return y


def setup_example():
    noise_variance = 0.1
    x = np.linspace(-2, 2, 400)
    f_exact = target(x, noise_variance=0.0)
    plt.figure(1)
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
    plt.plot(x[::skip], f_sampled, 'b^', label='random sampled')
    plt.xlim(-2, 2)
    plt.grid()
    plt.pause(1e-5)
    return x, f_exact, noise_variance


def opt_example():
    x, f_exact, noise_variance = setup_example()
    plt.figure(2)
    plt.plot(x, f_exact, 'k-', label='true target')
    plt.fill_between(x,
                     f_exact - 1.96 * noise_variance,
                     f_exact + 1.96 * noise_variance,
                     color='r', alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('target')

    opt = skopt.Optimizer([(-2, 2)], 'GP', acq_func='EI',
                          n_initial_points=0)
    for _ in range(5):
        x_next = np.random.uniform(-2, 2)
        opt.tell([x_next], target(x_next, noise_variance=noise_variance))

    for i in range(10):
        for j in range(5):
            x_next = opt.ask()
            opt.tell(x_next, target(x_next[0], noise_variance=noise_variance))

        # mu, s = opt.models[-1].predict(x.reshape(-1, 1), return_std=True)
        plt.plot(opt.Xi, opt.yi, 'bv')
        plt.pause(1e-5)
    plt.legend()
    plt.xlim(-2, 2)
    plt.grid()


if __name__ == '__main__':
    opt_example()
    plt.show()
