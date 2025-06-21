import csv
import numpy as np
from genSimData import gen_pendulum
from plotKalman import plotKalman
from scipy.integrate import solve_ivp

gen_pendulum()  # generate data/pendulum.csv

with open('data/pendulum.csv') as csvFile:
    # read data/pendulum.csv (t, z)
    myReader = csv.reader(csvFile)
    l = [row for row in myReader]
    t = [float(ti) for ti in l[0]]
    z = [float(xi) for xi in l[1]]  # measurement data
    del l

    n = len(t)
    dt = t[1] - t[0]

    x0 = np.array([0.0, 1.0])

    gdivl = 1

    def myfun(t, x):
        return np.array([x[1], -gdivl*np.sin(x[0])])
    sol = solve_ivp(myfun, [t[0], t[-1]], x0, t_eval=t)
    z_true = sol.y[0, :]  # true value of z

    z_hat = np.zeros(n)  # z estimated

    sigma = np.std(z_true - z, axis=0)  # standard deviation of z

    H = np.array([[1, 0]])

    Q = 0.001**2*np.eye(2)  # process noise covariance
    R = 0.1**2*np.eye(1)  # measurement noise covariance

    # u_hat = None

    # initial guess
    x_hat = x0.reshape((2, 1))
    P = sigma**2*np.eye(2)

    for i, (ti, zi) in enumerate(zip(t, z)):
        # predict
        sol = solve_ivp(myfun, [ti, ti+dt], x_hat.reshape((2)), t_eval=np.linspace(ti, ti+dt, 20))
        x_hat = sol.y[:, -1].reshape((2, 1))
        F = np.array([[0, 1], [-gdivl*np.cos(x_hat[0, 0]), 0]])
        P = F@P@F.T + Q

        # update
        K = P@H.T@np.linalg.inv(H@P@H.T + R)  # Kalman gain
        x_hat = x_hat + K@([[zi]] - H@x_hat)
        P = (np.eye(2)-K@H)@P
        z_hat[i] = (H@x_hat)[0, 0]

    plotKalman(t, z_true, z, z_hat, sigma, 'fig/pendulum.png')  # plot data
