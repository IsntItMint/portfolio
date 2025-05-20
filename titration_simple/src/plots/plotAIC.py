import matplotlib.pyplot as plt
import os
from matplotlib.ticker import MaxNLocator
from src.plots.Fileinfo import Fileinfo


def plotAIC(outFile, AIC, texOption=False):
    with plt.style.context(Fileinfo.context):
        # plt.rc('font', size=16)
        fig, ax = plt.subplots()

        xint = list(range(1, len(AIC) + 1))
        plt.plot(xint, AIC, marker='o')
        # plt.plot(xint, AIC, marker='o', color='black')

        plt.xlabel("reactions selected")
        plt.ylabel("AIC")
        plt.yscale("log")

        # ax.set_xticks(xint)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        width = 3.25
        # mmtoin = 0.0393701
        # width = 120 * mmtoin
        ratio = 4.0/6.0
        fig.set_size_inches(width, width*ratio)

        os.makedirs(os.path.dirname(outFile), exist_ok=True)
        plt.savefig(outFile, format="pdf", bbox_inches="tight")
        plt.close('all')
