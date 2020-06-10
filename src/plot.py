import matplotlib.pyplot as plt
import numpy as np
from src.compare import circa_single, circacompare
from src import constants


def predict_y(x, t):
    return x[0] + x[1] * np.cos(t - x[2])


def circa_single_plot(t0, y0, loss=constants.LOSS, f_scale=constants.F_SCALE, max_iterations=constants.MAX_ITERATIONS):
    optimised_result = circa_single(t0,y0, loss, f_scale, max_iterations)
    predictions = predict_y(optimised_result.x, t=t0)

    plt.plot(t0, y0, label="data", color='blue')
    plt.plot(t0, predictions, label="fit", color='red')
    plt.legend(loc="lower right")
    plt.show()


def circacompare_plot(t0, y0, g0, loss=constants.LOSS, f_scale=constants.F_SCALE, max_iterations=constants.MAX_ITERATIONS):
    optimised_result = circacompare(t0, y0, g0, loss, f_scale, max_iterations)

    x1 = optimised_result.x[np.array([0, 2, 4])]
    x2 = optimised_result.x[np.array([0, 2, 4])] + optimised_result.x[np.array([1, 3, 5])]
    time1 = t0[g0 == 0]
    time2 = t0[g0 == 1]
    prediction1 = predict_y(x1, time1)
    prediction2 = predict_y(x2, time2)

    plt.plot(time1, y0[g0 == 0], label="Group 0 data", color='red')
    plt.plot(time1, prediction1, label="Group 0 fit", color='maroon', linestyle='--')
    plt.plot(time2, y0[g0 == 1], label="Group 1 data", color='cornflowerblue')
    plt.plot(time2, prediction2, label="Group 1 fit", color='navy', linestyle='--')
    plt.legend(loc="lower right")

    plt.show()
