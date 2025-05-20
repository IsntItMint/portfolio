from pandas import read_csv
from src.plots.plotAIC import plotAIC


df = read_csv("./data/input/list/AICFigureList.csv")
outList = df["output file"].values.tolist()
AICList = df["AIC"].values.tolist()

for outFile, AICFile in zip(outList, AICList):
    print(outFile)
    df = read_csv(AICFile)
    AIC = df["AIC"].to_numpy()
    plotAIC(outFile, AIC)
    print("===")
