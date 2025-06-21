import csv
import numpy as np
from scipy.integrate import solve_ivp


def gen_constant():
    with open('data/constant.csv', 'w', newline='') as csvFile:
        n = 50
        t = [i for i in range(n)]
        sigp = 0.1
        sigq = 0.01
        x0 = 10
        z = np.random.normal(loc=x0, scale=sigp, size=n) + np.random.normal(loc=0.0, scale=sigq, size=n)

        # plotSim(t,z)
        myWriter = csv.writer(csvFile)
        myWriter.writerows([t, z])

    return


def gen_accel():
    with open('data/accel.csv', 'w', newline='') as csvFile:
        n = 100
        t = [i for i in range(n)]

        x0 = 10.0
        v0 = 0.0
        a = 0.01
        sigma = 0.5
        z = np.array([x0 + v0*ti + a*0.5*ti**2 for ti in t]) + np.random.normal(loc=0.0, scale=sigma, size=n)

        # plotSim(t,z)
        myWriter = csv.writer(csvFile)
        myWriter.writerows([t, z])

    return


def gen_pendulum():
    with open('data/pendulum.csv', 'w', newline='') as csvFile:
        n = 201
        t0 = 0
        tfinal = 10
        t = np.linspace(t0, tfinal, n)

        theta0 = 0
        thetadot0 = 1
        gdivl = 1
        sigma = 0.05

        def myfun(t, x):
            return np.array([x[1], -gdivl*np.sin(x[0])])

        sol = solve_ivp(myfun, [t0, tfinal], np.array([theta0, thetadot0]), t_eval=t)
        x = sol.y
        z = x[0, :].reshape((n)) + np.random.normal(loc=0.0, scale=sigma, size=n)

        # plotSim(t,z)
        myWriter = csv.writer(csvFile)
        myWriter.writerows([t, z])

    return
