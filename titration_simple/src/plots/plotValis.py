import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import re
import os
from src.plots.Fileinfo import Fileinfo

##########################################################################


def plotValis(outFile, simDir):
    with plt.style.context(Fileinfo.context):
        df1 = pd.read_csv(f"{simDir}/constr.csv")
        df2 = pd.read_csv(f"{simDir}/resi.csv")
        df3 = pd.read_csv(f"{simDir}/x0.csv")

        matplotlib.use("pdf")
        fig, axs = plt.subplots(3, 1)

        prog = re.compile(r"constr (.*)")
        if (df1.shape[1] > 2):
            for i in range(2, df1.shape[1]):
                ilabel = prog.match(df1.columns.values[i]).group(1)
                axs[0].plot(df1.iloc[:, 0], df1.iloc[:, i],
                            label=fr"$\mathrm{{{ilabel}}}$")
            axs[0].set_xlabel("V [mL]")
            axs[0].set_ylabel("constr")
            axs[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))

        prog = re.compile(r"resi (.*)")
        for i in range(2, df2.shape[1]):
            ilabel = prog.match(df2.columns.values[i]).group(1)
            axs[1].plot(df2.iloc[:, 0], df2.iloc[:, i],
                        label=fr"$\mathrm{{{ilabel}}}$")
        axs[1].set_xlabel("V [mL]")
        axs[1].set_ylabel("resi")
        axs[1].set_yscale("log")
        axs[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

        for i, ilabel in enumerate(df3.columns.values):
            axs[2].plot(df2.iloc[:, 0], df3.iloc[:, i],
                        label=fr"$\mathrm{{{ilabel}}}$")
        axs[2].set_xlabel("V [mL]")
        axs[2].set_ylabel("x0s")
        axs[2].legend(loc='center left', bbox_to_anchor=(1, 0.5))

        width = 3.25
        ratio = 16.0/6.0
        fig.set_size_inches(width, width*ratio)

        os.makedirs(os.path.dirname(outFile), exist_ok=True)
        plt.savefig(outFile, format="pdf", bbox_inches="tight")
        print("** vali graph is done")
        plt.close()
        return
