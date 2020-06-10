import numpy as np


def generate_data(t, k, a, p, noise=0, n_outliers=0, random_state=0):
    y = k + a * np.sin(t - p)
    rnd = np.random.RandomState(random_state)
    error = noise * rnd.randn(t.size)
    outliers = rnd.randint(0, t.size, n_outliers)
    error[outliers] *= 10
    return y + error
