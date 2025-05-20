import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from etch2DInterp import get_C, get_S
from Fileinfo import Fileinfo
# from cycler import cycler

xlabel = r'$y \ (\mathrm{mm})$ at $x = 50 \ \mathrm{mm}$'
# colors = ['0.0', '0.0', '0.0', '0.0', '0.4', '0.4', '0.4', '0.4']
# styles = ['-', '--', '-.', ':', '-', '--', '-.', ':']
# custom_cycler = (cycler(color=colors) +
#                  cycler(linestyle=styles))
# lines = len(colors)
lines = 10


def plotend(output):
    os.makedirs(os.path.dirname(output), exist_ok=True)
    plt.savefig(output, bbox_inches='tight')
    plt.close()


class Plot1D:
    def __init__(self, outputdir, ny):
        self.outputdir = outputdir
        self.set_y(ny)

    def set_y(self, ny):
        x = 50
        y = np.logspace(-3, 0, ny, base=10)
        self.X, self.Y = np.meshgrid(x, y)

    def plot_C_mid(self, myData):
        C = get_C(myData, self.X, self.Y)
        for i, iname in enumerate(myData.ionfilenames):
            output = f'{self.outputdir}/C/{iname}_mid.pdf'
            x = self.Y[:, 0]
            y = C[:, 0, i]
            ylabel = r'concentration ($\mathrm{mol/m^3}$)'

            with plt.style.context(Fileinfo.context):
                fig, ax = plt.subplots()
                ax.plot(x, y)
                ax.set_xscale('log')
                ax.set_xlim([1e-3, 1])
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)
                plotend(output)

    def plot_C_mid_all(self, myData):
        output = f'{self.outputdir}/All_mid.pdf'
        C = get_C(myData, self.X, self.Y)
        x = self.Y[:, 0]
        ylabel = r'concentration ($\mathrm{mol/m^3}$)'

        with plt.style.context(Fileinfo.context):
            fig, ax = plt.subplots()
            # ax.set_prop_cycle(custom_cycler)
            for i, iname in enumerate(myData.names):
                ilabel = rf'$\mathrm{{{iname}}}$'
                y = C[:, 0, i]
                line, = ax.plot(x, y)
                line.set_label(ilabel)
            ax.set_xscale('log')
            ax.set_xlim([1e-3, 1])
            ax.set_xlabel(xlabel)
            ax.set_yscale('log')
            ax.set_ylim(bottom=1e-7)
            ax.set_ylabel(ylabel)
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plotend(output)

    def plot_S_mid(self, myData):
        S = get_S(myData, self.X, self.Y)
        for i, iname in enumerate(myData.reaclabel):
            output = f'{self.outputdir}/S/S_{iname}_mid.pdf'
            x = self.Y[:, 0]
            y = S[:, 0, i]
            ylabel = r'reaction rate ($\mathrm{mol/m^3/s}$)'

            with plt.style.context(Fileinfo.context):
                fig, ax = plt.subplots()
                ax.plot(x, y)
                ax.set_xscale('log')
                ax.set_xlim([1e-3, 1])
                ax.set_ylabel(ylabel)
                plotend(output)

    def plot_middatas(self, ioutput, HFDatas, HNO3Datas, labels, index):
        output = f'{self.outputdir}/{ioutput}.pdf'
        colors = cm.rainbow(np.linspace(0, 1, len(labels)))
        x = self.Y[:, 0]
        ylabel = r"$C_{\mathrm{H^+}}$" + \
                 " on " + r"$x = 50$" + " mm " + \
                 r"$(\mathrm{mol}/\mathrm{m}^3)$"

        with plt.style.context(Fileinfo.context):
            fig, ax = plt.subplots()
            for (iHFdata, iHNO3data, ilabel, c) \
                    in zip(HFDatas, HNO3Datas, labels, colors):
                C = get_C(iHFdata, self.X, self.Y)
                line, = ax.plot(x, C[:, 0, index])
                line.set_color(c)
                line.set_label(ilabel)
                C = get_C(iHNO3data, self.X, self.Y)
                line, = ax.plot(x, C[:, 0, index])
                line.set_color(c)
                line.set_label(ilabel)
            handles, labels = ax.get_legend_handles_labels()
            labels, ids = np.unique(labels, return_index=True)
            handles = [handles[i] for i in ids]
            ax.legend(handles, labels, bbox_to_anchor=(1, 0),
                      loc="lower right", title=r"$v_{avg}$ (m/s)")
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            plt.text(1e-3, 9e-2, r"$\mathrm{HF}$")
            plt.text(1e-3, 9e-3, r"$\mathrm{HNO_3}$")
            plotend(output)

    def plot_NFe(self, ioutput, myDatas, labels):
        output = f'{self.outputdir}/{ioutput}.pdf'
        x = self.Y[:, 0]
        with plt.style.context(Fileinfo.context):
            fig, ax = plt.subplots()
            # ax.set_prop_cycle(custom_cycler)
            for (iData, ilabel) in zip(myDatas, labels):
                NFe, x = iData.get_NFe()
                line, = ax.plot(x, NFe * 1e+6)
                line.set_label(ilabel)
            ax.legend(bbox_to_anchor=(1, 1), loc="upper right")
            xlabel = r'$x \ (\mathrm{mm})$'
            ylabel = r'$N_{\mathrm{Fe}} (10^{-6} \mathrm{mol/m^2/s})$'
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            plotend(output)

    def plot_C_mid_select(self, ioutput, myDatas, labels, index):
        output = f'{self.outputdir}/{ioutput}.pdf'
        x = self.Y[:, 0]
        species = myDatas[0].names[index]
        ylabel = rf"$C_{{\mathrm{{{species}}}}} \ (\mathrm{{mol/L}})$"

        with plt.style.context(Fileinfo.context):
            fig, ax = plt.subplots()
            # ax.set_prop_cycle(custom_cycler)
            for (iData, ilabel) in zip(myDatas, labels):
                C = get_C(iData, self.X, self.Y)
                line, = ax.plot(x, C[:, 0, index])
                line.set_label(ilabel)
            ax.legend(loc='lower left', bbox_to_anchor=(0, 0))
            ax.set_xscale('log')
            ax.set_xlim([1e-3, 1])
            ax.set_xlabel(xlabel)
            ax.set_yscale('log')
            ax.set_ylabel(ylabel)
            plotend(output)
