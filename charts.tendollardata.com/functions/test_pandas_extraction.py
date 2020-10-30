# create pytest textexpander w/ default arguments & plugins

# https://github.com/pytest-dev/pytest-flask

## %%
# %pylab inline
# plot([1,2,3],[2,3,4])
# https://stackoverflow.com/questions/2349991/how-to-import-other-python-files
# https://stackoverflow.com/questions/61605/is-it-pythonic-for-a-function-to-return-multiple-values
# https://github.com/pytest-dev/pytest-cov
# https://github.com/ionelmc/pytest-benchmark

# https://plugincompat.herokuapp.com/
# https://pypi.org/project/pytest-aggreport/
# 

# https://github.com/anapaulagomes/pytest-picked - git related

# pytest --cov ../    https://www.youtube.com/watch?v=4R0dcsNrrAI
# pytest --cov ../ --cov-report html
# pytest --durations 10


# https://github.com/pytest-dev/pytest-repeat
# pytest --count=10 test_file.py
# @pytest.mark.repeat(3)
# def test_repeat_decorator():
    # pass
# https://github.com/hdw868/pytest-aggreport
# pytest --count=5 --html

# https://github.com/wolever/parameterized
# @pytest.mark.parametrize !! alternative

# https://github.com/ionelmc/pytest-benchmark
# https://github.com/Teemu/pytest-sugar
# https://github.com/pytest-dev/pytest-html
# pytest --html=report.html

# 

# pytest -s !!! can print

from parameterized import parameterized, parameterized_class

import unittest

# @parameterized([
#     ("Income Statement","AAPL"),
# ])

from pandas_extraction import FS_csv, FS_first_year,FS_latest_year
import pytest
import glob
import pandas as pd

# @pytest.mark.filterwarnings("ignore:DeprecationWarning: invalid escape sequence \d")

# @pytest.fixture

subject = "Income Statement"
symbol  = "AAPL"

@pytest.mark.parametrize("subject,symbol", [("Income Statement", "AAPL"), ("Income Statement", "ZM")])

# @pytest.fixture
def FS_csv(subject, symbol):
    csv_file = glob.glob("..\\data\\Historical Financial Statements\\*\\year\\{}\\*_{}_*".format(subject,symbol))[-1] #.format("NLOK"))[-1]
    df = pd.read_csv(csv_file)
    # df = list((df['date'].astype(str).str[0:4]))[-1]
    return(df)

df = FS_csv(subject, symbol)

@pytest.mark.wip #pytest -m wip
def FS_first_year(df):
    earliest_year = list((df['date'].astype(str).str[0:4]))[-1]
    return(earliest_year)

@pytest.mark.wip #py.test -v -m pandastest
def FS_latest_year(df):
    latest_year = list((df['date'].astype(str).str[0:4]))[0]
    return(latest_year)


def test_FS_first_year():
    print(FS_first_year(df))
    assert FS_first_year(df) == '1983'

def test_FS_latest_year():
    print(FS_latest_year(df))
    assert 998 <= int(FS_latest_year(df)) <= 3000



# assert (998 <= int(FS_latest_year(df)) <= 3000)FS_latest_year(df) == '1983'



# def test_FS_first_year():
#     assert FS_csv("Income Statement","AAPL") == '1983'
