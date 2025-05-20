import re
import numpy as np
import pandas as pd


def get_input(inputfile):
    df = pd.read_csv(inputfile, delimiter=',', header=None)
    speciesfile = "../input/species/" + df.iloc[0, 1]
    reactionsfile = "../input/reactions/" + df.iloc[1, 1]
    discretefile = "../input/discrete/" + df.iloc[2, 1]

    return speciesfile, reactionsfile, discretefile


def get_species(file):
    def get_ionfilename(name):
        newname = name.replace('+', 'plus')
        newname = newname.replace('-', 'plus')
        newname = newname.replace('^', 'sup_')

        # Remove parentheses, and curly brackets
        # The regex pattern matches: (, ), {, and }
        newname = re.sub(r'[\(\)\{\}]', '', newname)
        return newname

    df = pd.read_csv(file)
    names = df["name"].tolist()
    # originalnames = df["name"].tolist()
    z = df["z"].to_numpy()
    # D = df["D"].to_numpy()
    # C0 = df["C0[mol/L]"].to_numpy()
    # names = [rf"$\mathrm{{{iname}}}$" for iname in originalnames]
    ionfilenames = [get_ionfilename(iname) for iname in names]

    return names, z, ionfilenames


def get_reactions(file):
    df = pd.read_csv(file)
    label = df["label"]
    k0 = df["k0"].to_numpy()
    nu = df.iloc[:, 3:].to_numpy()
    K = np.pow(10, df["logK"].to_numpy() + 3*np.sum(nu, axis=1))

    return label, K, k0, nu


def get_discrete(file):
    df = pd.read_csv(file)
    # return df["nx"][0], df["ny"][0], df["ks"][0], df["vavg"][0]

    return df["ks"][0], df["vavg"][0]


def get_points(inputdir, nelem):
    x = 1e+3 * pd.read_csv(inputdir + "x.csv",
                           delimiter=',', header=None).to_numpy().flatten()
    y = 1e+3 * pd.read_csv(inputdir + "y.csv",
                           delimiter=',', header=None).to_numpy().flatten()
    nx = len(x)
    ny = len(y)
    points = np.c_[(np.tile(x, ny).T, np.repeat(y, nx).T)]

    return points


class Etch2DData:
    def __init__(self, iinput):
        inputfile = "../input/input/" + iinput + ".csv"

        speciesfile, reactionsfile, discretefile = get_input(inputfile)
        self.names, self.z, self.ionfilenames = get_species(speciesfile)
        # self.reaclabel, self.K, self.k0, self.nu
        self.reaclabel, _, _, _ = get_reactions(reactionsfile)
        self.ks, self.vavg = get_discrete(discretefile)

        self.inputdir = "../data/simulation/" + iinput + "/"

        self.points = get_points(self.inputdir, len(self.names))

    def __get_points_elems(self, file):
        df = pd.read_csv(file, delimiter=",", header=None)
        nelem = len(self.names)
        npoints = len(self.points)
        u = df.to_numpy().reshape((npoints, nelem), order='F')

        return u

    def get_conc(self):
        file = self.inputdir + "C.csv"
        u = self.__get_points_elems(file)

        return u

    def get_diffusion(self):
        file = self.inputdir + "diffusion.csv"
        f = self.__get_points_elems(file)

        return f

    def get_advection(self):
        file = self.inputdir + "advection.csv"
        f = self.__get_points_elems(file)

        return f

    def get_migration(self):
        file = self.inputdir + "migration.csv"
        f = self.__get_points_elems(file)

        return f

    def get_e(self):
        F = 96485
        R = 8.3144598
        T = 293.19
        const = -R*T/F

        file = self.inputdir + "p.csv"
        e = pd.read_csv(file, delimiter=",", header=None).to_numpy().T
        e *= const

        return e

    def get_zc(self):
        u = self.get_conc()
        npoints = len(self.points)
        zu = np.zeros(npoints)
        for i, iz in enumerate(self.z):
            zu += iz*u[:, i]

        return zu

    def get_s(self):
        file = self.inputdir + "s.csv"
        npoints = len(self.points)
        nreac = len(self.reaclabel)
        if (nreac == 0):
            return np.zeros((npoints, nreac))
        df = pd.read_csv(file, delimiter=",", header=None)
        s = df.to_numpy().reshape((npoints, nreac), order='F')

        return s

    def get_NFe(self):
        ymask = [y == 0 for y in self.points[:, 1]]
        x = self.points[ymask, 0].flatten()
        u = self.get_conc()[ymask, 0]
        NFe = 0.5 * self.ks * u

        return NFe, x

    def get_NFeavg(self):
        NFe, x = self.get_NFe()
        dxi = np.log(x[2] - x[1]) - np.log(x[1] - x[0])
        A = (x[1] - x[0]) / (np.exp(dxi) - 1)
        b = x[0] - A
        dx = x - b
        NFeavg = sum(np.multiply(NFe, dx)) / sum(dx)

        return NFeavg
