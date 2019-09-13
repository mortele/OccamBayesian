from skopt.acquisition import gaussian_ei
from skopt import Optimizer
import numpy as np
import matplotlib.pyplot as plt


#         Noise scaling function
#       ╭─────────────────────────────────────────────────────────────────────
#   1.0 ┼                             ╭─────────╮
#   0.9 ┤                         ╭───╯         ╰───╮
#   0.8 ┤                      ╭──╯                 ╰──╮
#   0.8 ┤                   ╭──╯                       ╰──╮
#   0.7 ┤                 ╭─╯                             ╰─╮
#   0.6 ┤              ╭──╯                                 ╰──╮
#   0.5 ┤            ╭─╯                                       ╰─╮
#   0.4 ┤         ╭──╯                                           ╰──╮
#   0.3 ┤      ╭──╯                                                 ╰──╮
#   0.3 ┤  ╭───╯                                                       ╰───╮
#   0.2 ┤──╯                                                               ╰──
#   0.1 ┼
#   0.0 ╰─────────────────┼────────────────┼─────────────────┼───────────────┼
#     -2.0              -1.0              0.0               1.0             2.0
def noise_scaling(x, noise_var):
    return noise_var * (np.sin(0.5 * (x + np.pi)))**4


#         Objective function without added noise
#       ╭─────────────────────────────────────────────────────────────────────
#   1.0 ┼
#   0.9 ┤                                     ╭───╮
#   0.7 ┤                                    ╭╯   ╰╮
#   0.6 ┤                                    │     ╰╮
#   0.4 ┤                 ╭───╮             ╭╯      │
#   0.2 ┤               ╭─╯   ╰─╮          ╭╯       ╰╮
#   0.1 ┼───────────────╯       ╰╮         │         ╰╮       ╭───────────────
#  -0.1 ┼                        ╰╮       ╭╯          ╰─╮   ╭─╯
#  -0.2 ┤                         │      ╭╯             ╰───╯
#  -0.4 ┤                         ╰╮     │
#  -0.6 ┤                          ╰╮   ╭╯
#  -0.7 ┤                           ╰───╯
#  -0.9 ┤
#  -1.0 ╰─────────────────┼────────────────┼─────────────────┼───────────────┼
#     -2.0              -1.0              0.0               1.0             2.0
def objective(x, noise_var, single=False):
    if single:
        x = x[0]
        noise = noise_scaling(x, noise_var) * np.random.randn()
    else:
        noise = (noise_scaling(x, noise_var)
                 * np.random.randn(np.squeeze(x.shape)))
    return np.sin(5 * x) * (1 - np.tanh(x ** 2)) + noise


def plot_optimizer(opt, x, fx, noise_var):
    model = opt.models[-1]
    x_model = opt.space.transform(x.tolist())
    plt.plot(x, fx, "r--", label="True objective")

    fn = objective(x, noise_var)
    noise = noise_scaling(x, noise_var) * 1.96
    plt.fill_between(x, fx - noise, fx + noise, alpha=0.2)
    plt.plot(x, fn, 'k.', label="Noisy samples")

    y_pred, sigma = model.predict(x_model, return_std=True)
    plt.plot(x, y_pred, "g--", label=r"$\mu(x)$")
    plt.fill(np.concatenate([x, x[::-1]]),
             np.concatenate([y_pred - 1.9600 * sigma,
                             (y_pred + 1.9600 * sigma)[::-1]]),
             alpha=.2, fc="g", ec="None")

    # Plot sampled points
    plt.plot(opt.Xi, opt.yi,
             "r.", markersize=8, label="Observations")

    acq = gaussian_ei(x_model, model, y_opt=np.min(opt.yi))
    # shift down to make a better plot
    acq = 4*acq - 2
    plt.plot(x, acq, "b", label="EI(x)")
    plt.fill_between(x.ravel(), -2.0, acq.ravel(), alpha=0.3, color='blue')

    # Adjust plot layout
    plt.grid()
    plt.legend(loc='best')


def optimize_objective(func=None, noise=0.1, initial_iters=10, iters=10):
    pass


if __name__ == '__main__':
    plt.set_cmap("viridis")
    np.random.seed(1234)
    noise_variance = 0.1
    N = 100
    x = np.linspace(-2, 2, N)
    fx = objective(x, noise_variance)
    res = optimize_objective(func=objective, noise=noise_variance,
                             initial_iters=10, iters=10)

    opt = Optimizer([(-2.0, 2.0)], "ET", acq_optimizer="sampling")
    for i in range(10):
        next_x = opt.ask()
        f_val = objective(next_x, noise_variance, single=True)
        opt.tell(next_x, f_val)
    plot_optimizer(opt, x, fx, noise_variance)
    plt.show()


"""
# Plot f(x) + contours
x = np.linspace(-2, 2, 400).reshape(-1, 1)
fx = np.array([objective(x_i, noise_level=0.0) for x_i in x])
fxn = np.array([objective(x_i, noise_level=noise_level) for x_i in x])
noise_fill = np.array([noise_scaling(xi) for xi in x])
plt.plot(x, fx, "r--", label="True (unknown)")
plt.fill(np.concatenate([x, x[::-1]]),
         np.concatenate((fx - 1.9600 * noise_fill,
                         fx[::-1] + 1.9600 * noise_fill[::-1])),
         alpha=.2, fc="r", ec="None")
plt.plot(x, fxn, 'k.', label="Sampled true f(x)")
plt.legend()
plt.grid()
plt.pause(1.0)

opt = Optimizer([(-2.0, 2.0)], "ET", acq_optimizer="sampling")
next_x = opt.ask()
print(next_x)

f_val = objective(next_x, noise_level=noise_level)
opt.tell(next_x, f_val)

for i in range(9):
    next_x = opt.ask()
    f_val = objective(next_x)
    opt.tell(next_x, f_val)


def plot_optimizer(opt, x, fx):
    fig = plt.gca()
    fig.clear()
    model = opt.models[-1]
    x_model = opt.space.transform(x.tolist())

    # Plot true function.
    plt.plot(x, fx, "r--", label="True (unknown)")
    plt.fill(np.concatenate([x, x[::-1]]),
             np.concatenate([fx - 1.9600 * noise_level,
                             fx[::-1] + 1.9600 * noise_level]),
             alpha=.2, fc="r", ec="None")

    # Plot Model(x) + contours
    y_pred, sigma = model.predict(x_model, return_std=True)
    plt.plot(x, y_pred, "g--", label=r"$\mu(x)$")
    plt.fill(np.concatenate([x, x[::-1]]),
             np.concatenate([y_pred - 1.9600 * sigma,
                             (y_pred + 1.9600 * sigma)[::-1]]),
             alpha=.2, fc="g", ec="None")

    # Plot sampled points
    plt.plot(opt.Xi, opt.yi,
             "r.", markersize=8, label="Observations")

    acq = gaussian_ei(x_model, model, y_opt=np.min(opt.yi))
    # shift down to make a better plot
    acq = 4*acq - 2
    plt.plot(x, acq, "b", label="EI(x)")
    plt.fill_between(x.ravel(), -2.0, acq.ravel(), alpha=0.3, color='blue')

    # Adjust plot layout
    plt.grid()
    plt.legend(loc='best')


plot_optimizer(opt, x, fx)
plt.pause(0.1)
for i in range(10000):
    next_x = opt.ask()
    f_val = objective(next_x)
    opt.tell(next_x, f_val)

    plot_optimizer(opt, x, fx)
    plt.pause(0.1)
plt.show()
# ==============================================================================
"""
"""
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
                     color='r', alpha=0.05)
    plt.xlabel('x')
    plt.ylabel('target')

    opt = skopt.Optimizer([(-2, 2)], 'GP', acq_func='EI',
                          n_initial_points=0)
    for _ in range(5):
        x_next = np.random.uniform(-2, 2)
        opt.tell([x_next], target(x_next))

    for i in range(10):
        for j in range(5):
            x_next = opt.ask()
            opt.tell(x_next, target(x_next[0], noise_variance=noise_variance))

            mu, s = opt.models[-1].predict(x.reshape(-1, 1), return_std=True)
            plt.plot(np.linspace(-2, 2, len(mu)), mu, 'g-')
            plt.fill_between(np.linspace(-2, 2, len(mu)),
                             mu - s,
                             mu + s,
                             color='g', alpha=0.1)
            plt.plot(opt.Xi, opt.yi, 'bv')
            plt.pause(1.0)
    plt.legend()
    plt.xlim(-2, 2)
    plt.grid()


if __name__ == '__main__':
    opt_example()
    plt.show()
"""
