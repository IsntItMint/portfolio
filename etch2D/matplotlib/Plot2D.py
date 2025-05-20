import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from Fileinfo import Fileinfo
from etch2DInterp import get_C, get_Diffusion, get_Advection, \
                         get_Migration, get_zC, get_S, get_E


cmap = 'jet'
# cmap = 'gray_r'


def plotTemplate2D(output, cblabel, ax, cb):
    ax.set_yscale('log')
    ax.set_ylim([1e-3, 1])
    ax.set_xlabel(r'$x \ (\mathrm{mm})$')
    ax.set_ylabel(r'$y \ (\mathrm{mm})$')
    cb.set_label(cblabel)

    os.makedirs(os.path.dirname(output), exist_ok=True)
    plt.savefig(output, bbox_inches='tight')
    cb.remove()
    plt.clf()
    plt.close()


def plotMap2D(output, X, Y, U, cblabel, norm=None):
    with plt.style.context(Fileinfo.context):
        fig, ax = plt.subplots()
        pc = ax.pcolormesh(X, Y, U, cmap=cmap, shading='gouraud', norm=norm)
        cb = fig.colorbar(pc)
        plotTemplate2D(output, cblabel, ax, cb)


def plotQuiver2D(output, X, Y, U, V, M, cblabel):
    with plt.style.context(Fileinfo.context):
        fig, ax = plt.subplots()
        log_norm = colors.LogNorm(vmin=M.min(), vmax=M.max())
        Q = ax.quiver(
            X, Y, U, V, M, width=0.01,
            pivot='mid', cmap='GnBu', norm=log_norm)
        cb = fig.colorbar(Q)
        plotTemplate2D(output, cblabel, ax, cb)


class Plot2D:
    def __init__(self, outputdir, myData, nx, ny):
        self.outputdir = outputdir
        self.myData = myData
        self.set_xy(nx, ny)

    def __select_Normalize(self, U):
        Umax = U.max()
        Umin = U.min()
        norm = None
        if (Umax - Umin < 1e-4):
            mid = (U.max() + U.min()) / 2
            norm = colors.Normalize(vmin=mid - 1.0, vmax=mid + 1.0)
            return norm
        if (Umax > 0 and Umin < 0):
            threshold = 10 ** (np.floor(np.log10(max(Umax, -Umin))) - 2)
            norm = colors.SymLogNorm(threshold, base=10)
            return norm
        if (Umin >= 0):
            vmax = np.ceil(np.log10(Umax))
            if (Umin > 1e-7):
                vmin = np.floor(np.log10(Umin))
            else:
                vmin = vmax * 1e-3
            norm = colors.LogNorm(vmin=vmin, vmax=vmax)
            return norm
        return norm

    def set_xy(self, nx, ny):
        x = np.linspace(0, 100, nx)
        y = np.logspace(-3, 0, ny, base=10)
        self.X, self.Y = np.meshgrid(x, y)

    def plot_C(self):
        C = get_C(self.myData, self.X, self.Y)
        for i, iname in enumerate(self.myData.ionfilenames):
            output = f'{self.outputdir}/C/{iname}.pdf'
            cblabel = r'concentration ($\mathrm{mol/m^3}$)'
            plotMap2D(output, self.X, self.Y, C[:, :, i], cblabel)

    def plot_zC(self):
        zC = get_zC(self.myData, self.X, self.Y)
        output = f'{self.outputdir}/zC.pdf'
        cblabel = r'charge density ($\mathrm{mol/m^3}$)'
        plotMap2D(output, self.X, self.Y, zC, cblabel)

    def plot_S(self):
        S = get_S(self.myData, self.X, self.Y)
        if (len(self.myData.reaclabel) == 0):
            output = f'{self.outputdir}/S/S_HF.pdf'
            cblabel = r'reaction rate ($\mathrm{mol/m^3/s}$)'
            U = np.zeros((self.X.shape[0], self.X.shape[1]))
            plotMap2D(output, self.X, self.Y, U, cblabel)

        for i, ilabel in enumerate(self.myData.reaclabel):
            output = f'{self.outputdir}/S/S_{ilabel}.pdf'
            cblabel = r'reaction rate ($\mathrm{mol/m^3/s}$)'
            U = S[:, :, i]
            norm = self.__select_Normalize(U)
            plotMap2D(output, self.X, self.Y, U, cblabel, norm=norm)

    def plot_Diffusion(self):
        os.makedirs(os.path.dirname(self.outputdir + "/diffusion/"),
                    exist_ok=True)
        Fd = get_Diffusion(self.myData, self.X, self.Y)
        for i, iname in enumerate(self.myData.ionfilenames):
            output = f'{self.outputdir}/diffusion/{iname}.pdf'
            cblabel = r'Diffusion term ($\mathrm{mol/m^3/s}$)'
            U = Fd[:, :, i]
            norm = self.__select_Normalize(U)
            plotMap2D(output, self.X, self.Y, U, cblabel, norm=norm)

    def plot_Advection(self):
        os.makedirs(os.path.dirname(self.outputdir + "/advection/"),
                    exist_ok=True)
        Fa = get_Advection(self.myData, self.X, self.Y)
        for i, iname in enumerate(self.myData.ionfilenames):
            output = f'{self.outputdir}/advection/{iname}.pdf'
            cblabel = r'Advection term ($\mathrm{mol/m^3/s}$)'
            U = Fa[:, :, i]
            norm = self.__select_Normalize(U)
            plotMap2D(output, self.X, self.Y, U, cblabel, norm=norm)

    def plot_Migration(self):
        os.makedirs(os.path.dirname(self.outputdir + "/migration/"),
                    exist_ok=True)
        F = get_Migration(self.myData, self.X, self.Y)
        for i, iname in enumerate(self.myData.ionfilenames):
            output = f'{self.outputdir}/migration/{iname}.pdf'
            cblabel = r'Migration term ($\mathrm{mol/m^3/s}$)'
            U = F[:, :, i]
            norm = self.__select_Normalize(U)
            plotMap2D(output, self.X, self.Y, U, cblabel, norm=norm)

    def plot_E(self):
        def transform(u, v):
            luv = np.sqrt(u*u + v*v)
            return u/luv, v/luv, luv
        EX, EY = get_E(self.myData, self.X, self.Y)
        U, V, M = transform(EX, EY)
        cblabel = r'$\bm{E}$ (V/m)'
        output = f'{self.outputdir}/E.pdf'
        plotQuiver2D(output, self.X, self.Y, U, V, M, cblabel)
