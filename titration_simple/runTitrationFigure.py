from csv import reader
from src.plots.plotTitration import plotTitration


def readTitrationFigureList():
    with open("./data/input/list/titrationFigureList.csv") as f:
        outList = list()
        rangeList = list()
        simList = list()
        simLabelList = list()
        simColorList = list()
        simStyleList = list()
        simWidthList = list()
        expList = list()
        expSheetList = list()
        expIdxList = list()
        expLabelList = list()
        expColorList = list()

        myReader = reader(f, delimiter=",", quotechar="\"")
        while True:
            try:
                outList.append(next(myReader)[1])
                rangeList.append(next(myReader)[1])
                simList.append(next(myReader)[1:])
                simLabelList.append(next(myReader)[1:])
                simColorList.append(next(myReader)[1:])
                simStyleList.append(next(myReader)[1:])
                simWidthList.append(next(myReader)[1:])
                expList.append(next(myReader)[1:])
                expSheetList.append(next(myReader)[1:])
                expIdxList.append(next(myReader)[1:])
                expLabelList.append(next(myReader)[1:])
                expColorList.append(next(myReader)[1:])
                next(myReader)
            except StopIteration:
                break

    return outList, rangeList, \
        simList, simLabelList, simColorList, simStyleList, simWidthList, \
        expList, expSheetList, expIdxList, expLabelList, expColorList


outList, rangeList, \
    simList, simLabelList, simColorList, simStyleList, simWidthList, \
    expList, expSheetList, expIdxList, expLabelList, expColorList \
    = readTitrationFigureList()
outListUnique = list(set(outList))
for iout, irange, \
        isims, isimLabels, isimColors, isimStyles, isimWidths, \
        iexps, iexpSheets, iexpIdxs, iexpLabels, iexpColors in \
        zip(outList, rangeList,
            simList, simLabelList, simColorList, simStyleList, simWidthList,
            expList, expSheetList, expIdxList, expLabelList, expColorList):
    print(f"Output file : {iout}")

    plotTitration(iout, rangeTxt=irange,
                  simFiles=isims, simLabels=isimLabels,
                  simColors=isimColors, simStyles=isimStyles,
                  simWidths=isimWidths, expFiles=iexps,
                  expSheets=iexpSheets, expIdxs=iexpIdxs,
                  expLabels=iexpLabels, expColors=iexpColors)
    print("===")
print("You can turn off the terminal now.")
