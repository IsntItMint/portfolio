import csv
from numpy import full, zeros, std
from genSimData import gen_constant
from plotKalman import plotKalman

gen_constant()  # generate data/constant.csv

with open('data/constant.csv') as csvFile:
    # read data/constant.csv (t, z)
    myReader = csv.reader(csvFile)
    l = [row for row in myReader]
    t = [float(ti) for ti in l[0]]
    z = [float(zi) for zi in l[1]]  # measure
    del l

    n = len(t)

    z_true = full(n, 10)  # true value of x
    z_hat = zeros(n)  # z estimated

    sigma = std(z, axis=0)  # standard deviation of x
    q = 0.01**2  # process noise
    r = sigma  # measurement noise

    # initial guess
    x_hat = 10
    p_hat = sigma**2

    for i, (ti, zi) in enumerate(zip(t, z)):
        # predict
        # x_hat = x_hat
        p_hat = p_hat + q

        # update
        K = p_hat/(p_hat+r)  # Kalman gain
        x_hat = x_hat + K*(zi - x_hat)
        p_hat = (1-K)*p_hat

        z_hat[i] = x_hat

    plotKalman(t, z_true, z, z_hat, sigma, 'fig/constant.png')  # plot data
