import pandas as pd


def get_inputs(csvfile):
    df = pd.read_csv(csvfile, delimiter=',', header=None)
    inputdir = df.iloc[0, :].values.tolist()
    label = df.iloc[1, :].values.tolist()
    return inputdir, label
