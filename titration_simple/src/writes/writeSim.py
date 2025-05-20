import os
import numpy as np
import pandas as pd


def writeCs(outFile, Vs, Cs, Ion):
    precMask = Ion.getIonPrecMask()
    ionMask = np.logical_not(precMask)

    speciesTeX = np.empty(len(Ion.species), dtype=object)
    speciesTeX[ionMask] = [f"[{value}] (mol/L)"
                           for value in Ion.species[ionMask]]
    speciesTeX[precMask] = [f"[{value}] v (mol/L)"
                            for value in Ion.prec]

    columns = ["V (mL)"] + speciesTeX.tolist()
    df = pd.DataFrame(np.c_[Vs, Cs], columns=columns)

    os.makedirs(os.path.dirname(outFile), exist_ok=True)
    df.to_csv(outFile, index=False, header=True)


def writeJs(outFile, Vs, pHs, Js, labels):
    columns = ["V (mL)", "pH"] + labels.tolist()
    df = pd.DataFrame(np.c_[Vs, pHs, Js], columns=columns)
    os.makedirs(os.path.dirname(outFile), exist_ok=True)
    df.to_csv(outFile, index=False, header=True)


def writeValiResi(outFile, Vs, pHs, resis):
    columns = ["V (mL)", "pH"] + [f"{i}" for i in range(resis.shape[1])]
    df = pd.DataFrame(np.c_[Vs, pHs, resis], columns=columns)
    os.makedirs(os.path.dirname(outFile), exist_ok=True)
    df.to_csv(outFile, index=False, header=True)


def writeValiConstr(outFile, Vs, pHs, constrs):
    columns = ["V (mL)", "pH"] + [f"{i}" for i in range(constrs.shape[1])]
    df = pd.DataFrame(np.c_[Vs, pHs, constrs], columns=columns)
    os.makedirs(os.path.dirname(outFile), exist_ok=True)
    df.to_csv(outFile, index=False, header=True)


def writeValix0(outFile, x0s):
    df = pd.DataFrame(x0s)
    os.makedirs(os.path.dirname(outFile), exist_ok=True)
    df.to_csv(outFile, index=False, header=True)
