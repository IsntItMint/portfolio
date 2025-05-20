import os
import matplotlib.pyplot as plt
import numpy as np
# from cycler import cycler
from src.reads.readResult import readSim_Js
from src.plots.Fileinfo import Fileinfo

maxsubplots = 8


def plotSensitivityExtract(V, J, Jlabel, Jmin, Jmax,
                           idx, axs, ylabel, yscale):
    with plt.style.context(Fileinfo.context):
        for i, ax in enumerate(axs):
            ax.plot(V, J[:, idx[i]],
                    label=Jlabel[idx[i]])
            ax.axhline(y=0, linestyle="dotted", color="gray")
            ax.set_ylabel(fr"${ylabel}$")
            ax.set_yscale('linear')
            ax.set_ylim(Jmin, Jmax)
            # ax.yaxis.offsetText.set_x(-0.12)
            # ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),
                      handlelength=0, handletextpad=0)

    return


def plotSensitivityExclude(V, J, Jmin, Jmax,
                           idx, ax, ylabel, yscale):
    # colors = ['0.0', '0.0', '0.0', '0.0', '0.4', '0.4', '0.4', '0.4']
    # styles = ['-', '--', '-.', ':', '-', '--', '-.', ':']
    # custom_cycler = (cycler(color=colors) +
    #                  cycler(linestyle=styles))
    count = J.shape[1]
    Jlabel = ["unselected"] + ["_"] * (count - 1)

    with plt.style.context(Fileinfo.context):
        # ax.set_prop_cycle(custom_cycler)
        ax.axhline(y=0, linestyle=":", color="0.9", linewidth=0.5)
        ax.plot(V, J[:, idx], label=Jlabel)
        ax.set_ylabel(fr"${ylabel}$")
        ax.set_yscale('linear')
        ax.set_ylim(Jmin, Jmax)
        ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5),
                  handlelength=0, handletextpad=0)

    return


def plotSensitivity(outFile, simFile, ylabel, yscale, ranking, extractflag):
    df = readSim_Js(simFile)
    V = df.iloc[:, 0].to_numpy()
    # pH = df.iloc[:, 1].to_numpy()
    Vlabel = df.columns.values[0]

    J = df.iloc[:, 2:].to_numpy()

    Jlabel = df.columns.values[2:]
    Jlabel = np.array([rf"$\mathrm{{{name}}}$" for name in Jlabel])

    Jmax = max(J.flatten())
    Jmin = min(J.flatten())
    Jmargin = (Jmax - Jmin) / 10.0
    Jmax += Jmargin
    Jmin -= Jmargin

    Jextract = J[:, extractflag]
    extractlabel = Jlabel[extractflag]
    extractidx = np.argsort(ranking[extractflag])
    extractcount = len(extractlabel)

    excludeflag = np.logical_not(extractflag)
    Jexclude = J[:, excludeflag]
    excludeidx = np.argsort(ranking[excludeflag])
    excludecount = len(excludeidx)
    excludefigcount = 0
    if excludecount > 0:
        excludefigcount = 1

    with plt.style.context(Fileinfo.context):
        fig, axs = plt.subplots(extractcount + excludefigcount, 1)
        if extractcount > 0:
            plotSensitivityExtract(V, Jextract, extractlabel, Jmin, Jmax,
                                   extractidx, axs[:extractcount],
                                   ylabel, yscale)
        if excludecount > 0:
            plotSensitivityExclude(V, Jexclude, Jmin, Jmax,
                                   excludeidx, axs[-1],
                                   ylabel, yscale)

        axs[-1].set_xlabel(Vlabel)
        # mmtoin = 0.0393701
        # width = 120 * mmtoin
        width = 3.25
        ratio = (1.25 * (extractcount + excludefigcount)) / 6.0
        fig.set_size_inches(width, width*ratio)
        fig.align_ylabels(axs)
        fig.tight_layout()

        os.makedirs(os.path.dirname(outFile), exist_ok=True)
        plt.savefig(outFile, format="pdf", bbox_inches="tight")
        plt.close('all')

    print("Sensitivity Graph is done")
    return


def plotSensitivity2(outFile, simFile, ylabel, yscale):
    with plt.style.context(Fileinfo.context):
        fig, ax1 = plt.subplots()

        df = readSim_Js(simFile)

        sqsum = np.abs(df.iloc[:, 2:]).mean(axis=0)
        idxrank = np.argsort(sqsum)[::-1]
        idxrank = idxrank[:] + 2

        for i in idxrank:
            ax1.plot(df.iloc[:, 0], df.iloc[:, i],
                     label=fr"$\mathrm{{{df.columns.values[i]}}}$")
        ax1.set_xlabel(df.columns.values[0])
        ax1.set_ylabel(fr"${ylabel}$")
        ax1.set_yscale(yscale)

        ax2 = ax1.twinx()
        ax2.set_ylabel(df.columns.values[1], color='lime')
        ax2.tick_params(axis='y', labelcolor='lime')
        ax2.plot(df.iloc[:, 0], df.iloc[:, 1], color='lime')
        ax1.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))

        width = 3.25
        ratio = 4.0/6.0
        fig.set_size_inches(width, width*ratio)

        os.makedirs(os.path.dirname(outFile), exist_ok=True)
        plt.savefig(outFile, format="pdf", bbox_inches="tight")
        plt.close()

        print("Sensitivity Graph is done")
        return
