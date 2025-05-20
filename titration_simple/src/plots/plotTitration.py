import matplotlib.pyplot as plt
from src.reads.readResult import readSim_Cs, readExp
import numpy as np
import os
from src.plots.Fileinfo import Fileinfo


sigma_pH = 0.30


def plotTitration(outFile, rangeTxt=None,
                  simFiles=None, simLabels=None,
                  simColors=None, simStyles=None,
                  simWidths=None, expFiles=None,
                  expSheets=None, expIdxs=None,
                  expLabels=None, expColors=None):
    with plt.style.context(Fileinfo.context):
        fig, ax = plt.subplots()
        for expFile, expSheet, expIdx, expLabel, expColor \
                in zip(expFiles, expSheets, expIdxs, expLabels, expColors):
            _, expVs, exppHs, _ = readExp(
                expFile, expSheet, expIdx, rangeTxt=rangeTxt)
            ax.scatter(expVs, exppHs, label=expLabel, color=expColor, zorder=1)
            ax.fill_between(expVs, (exppHs - sigma_pH), (exppHs + sigma_pH),
                            color=(expColor, 0.3), edgecolor=expColor,
                            label=f'pH {sigma_pH} error', zorder=0)

        Vmax = np.max(expVs)
        for simFile, simLabel, simColor, simStyle, simWidth in zip(
                simFiles, simLabels, simColors, simStyles, simWidths):
            simData = readSim_Cs(simFile)
            mask = simData.iloc[:, 0] <= Vmax
            simVs = simData.iloc[:, 0][mask]
            simpHs = -np.log10(simData.iloc[:, 1])[mask]
            ax.plot(simVs, simpHs, label=simLabel, color=simColor,
                    linestyle=simStyle, linewidth=simWidth, zorder=10)

        ax.set_xlabel("V [mL]")
        ax.set_ylabel("pH")
        ax.legend(loc='lower center')
        handle, label = ax.get_legend_handles_labels()
        reorder = lambda label, nc: sum((label[i::nc] for i in range(nc)), [])
        ax.legend(reorder(handle, 2), reorder(label, 2), ncol=2,
                  loc='lower center', bbox_to_anchor=(0.5, 1.0))

        # mmtoin = 0.0393701
        # width = 120 * mmtoin
        width = 3.25
        ratio = 5.0/6.0
        fig.set_size_inches(width, width*ratio)
        fig.tight_layout()

        os.makedirs(os.path.dirname(outFile), exist_ok=True)
        plt.savefig(outFile, format="pdf", bbox_inches="tight")
        plt.close('all')
        print("V-pH Graph is done")
