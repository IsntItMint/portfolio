from src.plots.plotValis import plotValis
import os

valiset = {"constr.csv", "resi.csv", "x0.csv"}

for root, dirs, files in os.walk("./data/simulation"):
    if (not dirs and valiset <= set(files)):
        outDir = root.replace("data/", "fig/")
        outFile = f"{outDir}/valis.pdf"
        plotValis(outFile, root)
