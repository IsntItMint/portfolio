import csv
import numpy as np
from genSimData import gen_accel
from plotKalman import plotKalman

gen_accel()  # generate data/accel.csv

with open('data/accel.csv') as csvFile:
    # read data/accel.csv (t, z)
    myReader = csv.reader(csvFile)
    l = [row for row in myReader]
    t = [float(ti) for ti in l[0]]
    z = [float(xi) for xi in l[1]]  # measurement data
    del l

    n = len(t)

    x0 = 10.0
    v0 = 0.0
    a = 0.01
    z_true = np.array([x0 + v0*ti + a*0.5*ti**2 for ti in t])  # true value of z
    z_hat = np.zeros(n)  # z estimated

    dt = 1
    F = np.array([[1, dt], [0, 1]])
    G = np.array([[dt**2/2], [dt]])
    H = np.array([[1, 0]])

    sigma = np.std(z_true - z, axis=0)  # standard deviation of z
    Q = 0.01**2*np.eye(2)  # process noise covariance
    R = 0.5**2*np.eye(1)  # measurement noise covariance

    u_hat = [[a]]
    # initial guess
    x_hat = np.array([[10], [0]])
    P = sigma**2*np.eye(2)

    for i, (ti, zi) in enumerate(zip(t, z)):
        # predict
        x_hat = F@x_hat + G@u_hat
        P = F@P@F.T + Q

        # update
        K = P@H.T@np.linalg.inv(H@P@H.T + R)  # Kalman gain
        x_hat = x_hat + K@([[zi]] - H@x_hat)
        P = (np.eye(2)-K@H)@P

        z_hat[i] = (H@x_hat)[0, 0]

    plotKalman(t, z_true, z, z_hat, sigma, 'fig/accel.png')  # plot data
