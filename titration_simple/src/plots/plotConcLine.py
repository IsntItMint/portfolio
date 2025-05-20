import matplotlib.pyplot as plt
import math
import os
import re
import numpy as np
# from cycler import cycler
from src.reads.readResult import readSim_Cs
from src.plots.Fileinfo import Fileinfo


def plotConcLine(outDir, simFile):
    with plt.style.context(Fileinfo.context):
        fig, ax = plt.subplots()

        simData = readSim_Cs(simFile)
        V = simData.iloc[:, 0]
        simData = simData.iloc[:, 1:]
        simData.replace(0, np.nan, inplace=True)

        prog = re.compile(r"\[(.*?)]")
        label = [rf"$\mathrm{{{prog.match(name).group(1)}}}$"
                 for name in simData.columns]

        lines = 10
        figcount = int(math.ceil((simData.shape[1]) / lines))

        # colors = ['0.0', '0.0', '0.0', '0.0', '0.4', '0.4', '0.4', '0.4']
        # styles = ['-', '--', '-.', ':', '-', '--', '-.', ':']
        # custom_cycler = (cycler(color=colors) +
        #                  cycler(linestyle=styles))

        fig, axs = plt.subplots(figcount, 1)
        if figcount == 1:
            axs = [axs]
        for i, ax in enumerate(axs):
            ax.clear()
            st = i * lines
            ed = min(simData.shape[1], (i+1) * lines)
            # ax.plot(V, simData.iloc[:, st:ed],
            #         label=label[st:ed])
            # ax.set_prop_cycle(custom_cycler)
            ax.plot(V[1:], simData.iloc[1:, st:ed],
                    label=label[st:ed])

            ax.set_ylabel("concentration [mol/L]")
            ax.set_yscale('log')
            ax.set_ylim([1e-14, 1e+0])
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        axs[-1].set_xlabel("V [mL]")
        # mmtoin = 0.0393701
        # width = 120 * mmtoin
        width = 3.25
        ratio = (4.0 * figcount)/6.0
        fig.set_size_inches(width, width*ratio)
        fig.align_ylabels(axs)
        fig.tight_layout()

        outFile = f"{outDir}/conc.pdf"
        os.makedirs(os.path.dirname(outFile), exist_ok=True)
        plt.savefig(outFile, format="pdf", bbox_inches="tight")

        print("Conc Line graph pdf is done")
        plt.close('all')
        return 0
