from pandas import read_csv
from src.titration.genMogi import genMogi
from src.titration.Ion import Ion
from src.titration.Conc import Conc
from src.titration.Reac import Reac
from src.titration.CalcComplex import CalcComplex


df = read_csv("./data/input/list/simulationList.csv")
outList = df["output folder"].values.tolist()
initList = df["initial file"].values.tolist()
convertList = df["convert file"].values.tolist()
speciesList = df["species file"].values.tolist()
reacList = df["reactions file"].values.tolist()

for outDir, initFile, convertFile, speciesFile, reacFile \
        in zip(outList, initList, convertList, speciesList, reacList):
    print(f"Output file will be : {outDir}")
    myIon = Ion(speciesFile=speciesFile)
    myReac = Reac(reacFile=reacFile)
    myConc = Conc(initFile=initFile, convertFile=convertFile)

    epsilon = 1e-3
    weight1 = 1
    weight2 = 100

    prob = CalcComplex(
        myIon, myReac, myConc,
        epsilon, weight1, weight2)

    genMogi(prob)

    print("===")
