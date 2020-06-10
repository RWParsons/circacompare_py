import numpy as np
from scipy.optimize import least_squares
from src import constants


# find a more descriptive name for this
def fun_circa_single(x, t, y):
    return x[0] + x[1] * np.cos(t - x[2]) - y


# find more descriptive names for some of the variables in this function
def param_standard_errors(optimised_result, y):
    ssr = np.nansum(optimised_result.fun ** 2)
    dof = y.size - 2
    mse = ssr / dof
    rmse = np.sqrt(mse)
    # get parameter standard error estimates
    neg_hess = np.dot(optimised_result.jac.T, optimised_result.jac)
    inv_neg_hess = np.linalg.inv(neg_hess)
    res_lsq_params_se = np.sqrt(np.diagonal(inv_neg_hess)) * rmse
    return res_lsq_params_se


def circa_single(t0, y0, loss=constants.LOSS, f_scale=constants.F_SCALE, max_iterations=constants.MAX_ITERATIONS):
    counter = 0
    while counter < max_iterations:
        start_args = np.random.rand(1, 3)[0] * np.array([2 * np.median(y0), y0.max() - y0.min(), 2 * np.pi])
        result_least_squares = least_squares(fun_circa_single,
                                start_args,
                                loss=loss,
                                f_scale=f_scale,
                                args=(t0, y0))
        if result_least_squares.x[1] > 0 and 0 < result_least_squares.x[2] < 2 * np.pi:
            break
        counter += 1

    if counter == max_iterations:
        return None, None

    param_standard_errors(result_least_squares, y0) * 1.96
    confidence_intervals = ([result_least_squares.x + param_standard_errors(result_least_squares, y0) * 1.96],
          [result_least_squares.x - param_standard_errors(result_least_squares, y0) * 1.96])
    result_least_squares.confidence_intervals = confidence_intervals

    return result_least_squares


# find a more descriptive name for this -- what are we comparing? compare_etc
def fun_circacompare(x, t, y, g):
    return (x[0] + x[1] * g) + (x[2] + x[3] * g) * np.cos(t - (x[4] + x[5] * g)) - y


def circacompare(t0, y0, g0, loss=constants.LOSS, f_scale=constants.F_SCALE, max_iterations=constants.MAX_ITERATIONS):
    counter = 0
    while counter < max_iterations:
        random_array = np.concatenate((np.random.rand(1, 5)[0], (np.random.rand(1,1)[0] - 0.5) * 2))
        start_args = random_array * np.array([2 * np.median(y0[g0 == 0]),
                                              2 * np.median(y0[g0 == 1]),
                                              y0[g0 == 0].max() - y0[g0 == 0].min(),
                                              (y0[g0 == 0].max() - y0[g0 == 0].min()) -
                                              (y0[g0 == 1].max() - y0[g0 == 1].min()),
                                              2 * np.pi,
                                              np.pi])
        result_least_squares = least_squares(fun_circacompare,
                                start_args,
                                loss=loss,
                                f_scale=f_scale,
                                args=(t0, y0, g0))
        if result_least_squares.x[2] > 0 and (result_least_squares.x[2] + result_least_squares.x[3]) > 0 and \
                0 < result_least_squares.x[4] < 2 * np.pi and -np.pi < result_least_squares.x[5] < np.pi:
            break
        counter += 1

    if counter == max_iterations:
        return None, None

    param_standard_errors(result_least_squares, y0) * 1.96
    confidence_internals = ([result_least_squares.x + param_standard_errors(result_least_squares, y0) * 1.96],
          [result_least_squares.x - param_standard_errors(result_least_squares, y0) * 1.96])

    result_least_squares.confidence_intervals = confidence_internals

    return result_least_squares
