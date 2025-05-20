import os
from gets import get_inputs
from Etch2DData import Etch2DData
from Plot1D import Plot1D
from Plot2D import Plot2D


mapdir = "./input/map.csv"
inputdir, label = get_inputs(mapdir)
myDatas = [Etch2DData(iinput) for iinput in inputdir]

outputdir = "../fig/simulation/1D"
os.makedirs(os.path.dirname(outputdir + "/"), exist_ok=True)
myPlot1D = Plot1D(outputdir, 50)
myPlot1D.plot_NFe("NFe", myDatas, label)
# myPlot1D.plot_C_mid_select("ZrOH4", myDatas, label, 6)

for iinput, myData in zip(inputdir, myDatas):
    print(iinput)

    outputdir = f"../fig/simulation/2D/{iinput}"
    os.makedirs(os.path.dirname(outputdir + "/"), exist_ok=True)
    myPlot2D = Plot2D(outputdir, myData, 50, 50)
    myPlot2D.plot_C()
    myPlot2D.plot_Diffusion()
    myPlot2D.plot_Advection()
    myPlot2D.plot_Migration()
    myPlot2D.plot_zC()
    myPlot2D.plot_S()
    myPlot2D.set_xy(20, 20)
    myPlot2D.plot_E()

    outputdir = f"../fig/simulation/1D/{iinput}"
    os.makedirs(os.path.dirname(outputdir + "/"), exist_ok=True)
    myPlot1D = Plot1D(outputdir, 50)
    # myPlot1D.plot_C_mid(myData)
    myPlot1D.plot_C_mid_all(myData)
    myPlot1D.plot_S_mid(myData)
