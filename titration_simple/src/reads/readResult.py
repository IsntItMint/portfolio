import pandas as pd
# import numpy as np
# import re


def readSim_Cs(filename):
    simData = pd.read_csv(filename)
    return simData


def readSim_Js(filename):
    simData = pd.read_csv(filename)
    return simData


def readExp(expFile, expSheet, expIdx, rangeTxt=None):
    # df = pd.read_excel(expFile, sheet_name=expSheet,
    #                   skiprows=7, nrows=1, usecols=expIdx)
    # d0 = np.reshape(df.iloc[0, 0:3], (3, 1))
    # d1 = float(re.search(
    #     r'NaOH\s?((?:[0]|[1-9]\d*)(?:.\d*)?)M', df.iloc[0, 4])[1])

    expData = pd.read_excel(
        expFile, sheet_name=expSheet,
        skiprows=10, usecols=expIdx).dropna(
        how='all').dropna(
            axis=1, how='all').reset_index(drop=True)
    V_0 = 100.0
    expLen = expData.shape[0]
    expVs = (expData.iloc[:, 0].values).flatten()
    exppHs = (expData.iloc[:, 2].values).flatten()
    return expLen, expVs, exppHs, V_0
