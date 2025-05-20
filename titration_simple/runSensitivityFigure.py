from pandas import read_csv
from src.plots.plotSensitivity import plotSensitivity, plotSensitivity2

df = read_csv("./data/input/list/sensitivityFigureList.csv")
outList = df["output file"].values.tolist()
simList = df["simulation data"].values.tolist()
ylabelList = df["y axis label"].values.tolist()
yscaleList = df["y axis scale"].values.tolist()
AICList = df["AIC"].values.tolist()

for outFile, simFile, ylabel, yscale, AICFile in zip(
        outList, simList, ylabelList, yscaleList, AICList):
    print(f"Output folder : {outFile}")

    df = read_csv(AICFile)
    ranking = df["ranking"].to_numpy()
    extractflag = df["extractflag"].to_numpy()

    plotSensitivity(outFile, simFile, ylabel, yscale, ranking, extractflag)

    outFile2 = outFile.replace(".pdf", "_titration.pdf")
    plotSensitivity2(outFile2, simFile, ylabel, yscale)

    print("===")
print("You can turn off the terminal now.")
