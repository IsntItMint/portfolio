from csv import reader
from src.fitting.fitting import fitting

with open("./data/input/list/fittingList.csv") as f:
    reacList = list()
    speciesList = list()
    outSimList = list()
    inSimList = list()
    expList = list()
    sheetList = list()
    columnList = list()

    myReader = reader(f, delimiter=",", quotechar="\"")
    while (True):
        try:
            reacList.append(next(myReader)[1])
            speciesList.append(next(myReader)[1])
            outSimList.append(next(myReader)[1:])
            inSimList.append(next(myReader)[1:])
            expList.append(next(myReader)[1:])
            sheetList.append(next(myReader)[1:])
            columnList.append(next(myReader)[1:])
        except StopIteration:
            break

for ireac, ispecies, ioutSim, iinSim, \
        iexp, isheet, icolumn \
        in zip(
            reacList, speciesList, outSimList, inSimList,
            expList, sheetList, columnList):
    print("Reaction : " + ispecies)
    fitting(ireac, ispecies, ioutSim, iinSim,
            iexp, isheet, icolumn)
    # print("Input file : " + inList[i])
    # runTitrationSim(inList[i], outList[i],vali=True)
    print("===")

print("You can turn off the terminal now.")
