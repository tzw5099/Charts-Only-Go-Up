## %%
# %pylab inline
# plot([1,2,3],[2,3,4])
# https://stackoverflow.com/questions/20309456/call-a-function-from-another-file

import pandas as pd
import numpy as np
import glob
import time
import datetime
import pathlib


def FS_csv(subject, symbol):
    csv_file = glob.glob("..\data\Historical Financial Statements\*\year\{}\*_{}_*".format(subject,symbol))[-1] #.format("NLOK"))[-1]
    df = pd.read_csv(csv_file)
    return(df)

def FS_first_year(df):
    earliest_year = list((df['date'].astype(str).str[0:4]))[-1]
    return(earliest_year)

def FS_latest_year(df):
    latest_year = list((df_bs['date'].astype(str).str[0:4]))[0]
    return(latest_year)

print(FS_first_year(FS_csv("Income Statement","AAPL")))