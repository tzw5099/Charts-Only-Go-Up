import pandas as pd
import glob
import os

import pytest
pytest.skip("This provides 0 code coverage.". allow_module_level=True)

print(os.getcwd())
print("hello")
print(glob.glob("charts/annual_returns/annual_returns/KWK*")[-1])
#charts/annual_returns/data/NDSN*"))

# df = pd.read_csv("charts/annual_returns/data/")

df = pd.read_csv(glob.glob("charts/annual_returns/annual_returns/KWK*")[-1])

print(df)
test="KWK"


csv_file = glob.glob("charts/annual_returns/annual_returns/{}*".format(test))[-1]
# csv_file = glob.glob("charts/annual_returns/annual_returns/{}*".format(test))
print("csv file",csv_file)
df = pd.read_csv(csv_file)

full_path = csv_file.split(' ~ ')

import pathlib

path = pathlib.PurePath(full_path[0])



asset_ticker = path.name #full_path[0].split("/")
print(asset_ticker)

asset_type = full_path[1]
print(asset_type)

asset_name = full_path[-1]
print(asset_name)

import csv
print("csv file")
print(csv.DictReader(open(csv_file)))
