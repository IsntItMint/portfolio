import numpy as np
from scipy.interpolate import griddata


def interp(points, v, X, Y):
    V = griddata(
        points=points, values=v,
        xi=(X, Y), method='cubic')
    return V


def __get_X_Y_elem(myData, X, Y, u):
    ny = X.shape[0]
    nx = X.shape[1]
    nelem = len(myData.names)
    U = np.zeros((ny, nx, nelem))

    for i in range(nelem):
        U[:, :, i] = interp(myData.points, u[:, i], X, Y)

    return U


def get_C(myData, X, Y):
    u = myData.get_conc()
    C = __get_X_Y_elem(myData, X, Y, u)

    return C


def get_Diffusion(myData, X, Y):
    u = myData.get_diffusion()
    Fd = __get_X_Y_elem(myData, X, Y, u)

    return Fd


def get_Advection(myData, X, Y):
    u = myData.get_advection()
    Fa = __get_X_Y_elem(myData, X, Y, u)

    return Fa


def get_Migration(myData, X, Y):
    u = myData.get_migration()
    Fa = __get_X_Y_elem(myData, X, Y, u)

    return Fa


def get_zC(myData, X, Y):
    zc = myData.get_zc()
    zC = interp(myData.points, zc, X, Y)

    return zC


def get_S(myData, X, Y):
    ny = X.shape[0]
    nx = X.shape[1]
    s = myData.get_s()
    nreac = s.shape[1]
    S = np.zeros((ny, nx, nreac))
    if (nreac == 0):
        return S

    for i in range(nreac):
        S[:, :, i] = interp(myData.points, s[:, i], X, Y)

    return S


def get_E(myData, X, Y):
    e = myData.get_e()
    EX = interp(myData.points, e[:, 0], X, Y)
    EY = interp(myData.points, e[:, 1], X, Y)

    return EX, EY
