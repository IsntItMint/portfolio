from pandas import read_csv
from src.plots.plotConcLine import plotConcLine

df = read_csv("./data/input/list/concFigureList.csv")
outList = df["output folder"].values.tolist()
simList = df["simulation data"].values.tolist()

for outFile, simFile in zip(outList, simList):
    print(f"Output file : {outFile}")

    plotConcLine(outFile, simFile)
    print("===")
print("You can turn off the terminal now.")
