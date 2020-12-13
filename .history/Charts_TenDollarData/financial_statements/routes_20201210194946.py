

import os
import sqlite3
import pandas as pd
import glob
import pathlib
import time
import sys


sys.path.append(os.path.join(os.path.dirname(__file__)))

from functions.pandas_extraction import FS


import numpy as np
import functools
from datetime import datetime
from string import Template
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import logging
from flask import request, session, g, redirect, url_for, abort, render_template, flash, Blueprint
cache = Cache()
from string import Template

charts = Blueprint('charts', __name__)

@charts.route('/', methods=['POST', 'GET'])
@charts.route("/home")
def index():

    return render_template('index.html')


@charts.route('/portfolios', methods=['POST', 'GET'])
def portfolio_details():
    return render_template('portfolio.html')



@charts.route('/<toms_file_name>', methods=['POST', 'GET'])
def toms_file_name_function(toms_file_name):
    return render_template('{}'.format(toms_file_name))



@charts.route('/annual_returns/<some_place>', methods=['POST', 'GET'])

def html_table(some_place):
    start_time = time.time()

    csv_file = glob.glob("charts/annual_returns/annual_returns/{}*".format(some_place))[-1]
    csv_file = glob.glob("charts/annual_returns/annual_returns/{}*".format(some_place))[-1]
    df = pd.read_csv(csv_file)
    df_html = df.to_html().replace('<table','<table class="df_tableBoot" id="df_myTable"')# dt-responsive" id="df_myTable"')

    full_path = csv_file.split(' ~ ')
    path = pathlib.PurePath(full_path[0])
    asset_ticker = path.name #full_path[0].split("/")
    asset_type = full_path[1]
    asset_name = full_path[-1]

    print("Nothing took {} seconds".format(time.time() - start_time))
    total_seconds = ((time.time() - start_time))

    labels = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
    ]
    labels = list(df['Year'])[0:19]

    values = [
        967.67, 1190.89, 1079.75, 1349.19,
        2328.91, 2504.28, 2873.83, 4764.87,
        4349.29, 6458.30, 9907, 16297
    ]

    values = list(df['Beginning Price'])[0:19]

    colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

    return render_template('annual_returns.html',  tables=[df_html], titles=df.columns.values, total_time=total_seconds, place_name=some_place, max=17000, labels=labels, values=values)

@charts.route('/financial_statements/<some_place>', methods=['POST', 'GET'])


def financial_statements(some_place):

    start_time = time.time()
    csv_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/Income Statement/*_{}_*".format(some_place))[-1] #.format("NLOK"))[-1]
    df = pd.read_csv(csv_file)
    # df = df[df['date'].notna()]#fillna(method='ffill')
    df = df[0:].iloc[::-1]#.dropna()
    df_bs = df
    #region Pandas data manipulation
    df_bs['Quarter & Year'] = df_bs['period']+" "+(df_bs['date'].astype(str).str[0:4])#((df_bs['date'].astype(str).str[0:4].astype(int))-1).astype(str)

    latest_year = list((df_bs['date'].astype(str).str[0:4]))[0]
    earliest_year = list((df_bs['date'].astype(str).str[0:4]))[-1]

    df_bs = df_bs.drop([ 'Unnamed: 0','date',
     'symbol',
     'fillingDate','period','link'],axis=1)

    df_bs.columns = [
     'Date & Time Filing Accepted',
     'Revenue (Sales)',
     'Cost of Revenue (Sales)',
     'Gross Profit (Income)',
     'Gross Profit (Income) Ratio',
     'Research and Development (R&D) Expenses',
     'Sales, General and Administrative (SG&A) Expenses',
     'Selling and Marketing (S&M) Expenses',
     'Other Expenses',
     'Operating Expenses',
     'Cost and Expenses',
     'Interest Expense',
     'Depreciation and Amortization (D&A)',
     'EBITDA',
     'EBITDA Ratio',
     'Operating Income',
     'Operating Income Ratio',
     'Total Other Income Expenses (Net)',
     'Income Before Tax',
     'Income Before Tax Ratio',
     'Income Tax Expense',
     'Net Income',
     'Net Income Ratio',
     'EPS',
     'EPS Diluted',
     'Weighted Average Shares Outstanding',
     'Weighted Average Shares Outstanding (Diluted)',
     'SEC Filing', 'Quarter & Year'
                    ]
    # for col in df_bs.columns:
    #     if len(df_bs[col].unique()) == 1:
    #         df_bs.drop(col,inplace=True,axis=1)

    cols = [ 'Quarter & Year', 'Revenue (Sales)',
     'Cost of Revenue (Sales)',
     'Gross Profit (Income)',
     'Gross Profit (Income) Ratio',
     'Research and Development (R&D) Expenses',
     'Sales, General and Administrative (SG&A) Expenses',
     'Other Expenses',
     'Operating Expenses',
     'Cost and Expenses',
     'Interest Expense',
     'Depreciation and Amortization (D&A)',
     'EBITDA',
     'EBITDA Ratio',
     'Operating Income',
     'Operating Income Ratio',
     'Total Other Income Expenses (Net)',
     'Income Before Tax',
     'Income Before Tax Ratio',
     'Income Tax Expense',
     'Net Income',
     'Net Income Ratio',
     'EPS',
     'EPS Diluted',
     'Weighted Average Shares Outstanding',
     'Weighted Average Shares Outstanding (Diluted)',
     'SEC Filing','Date & Time Filing Accepted']

    df_bs = df_bs[cols]

    df_bs_pct_chg = df_bs
    pct_chg_cols = (df_bs.select_dtypes(include=['number']).pct_change(-1))
    df_bs_str = df_bs_pct_chg.drop(list(pct_chg_cols), axis=1)
    df_bs_pct_chg = df_bs_str.join(pct_chg_cols)[list(df_bs)]

    pd.set_option('display.float_format', '{:.2f}'.format)
    df_bs_pct_chg_t = df_bs_pct_chg.transpose()
    df_bs_pct_chg_t.columns = list(df_bs_pct_chg['Quarter & Year'])
    df_bs_pct_chg_t = df_bs_pct_chg_t.iloc[1:]

    df_bs_pct_chg_t = df_bs_pct_chg.transpose()
    df_bs_pct_chg_t.columns = list(df_bs_pct_chg['Quarter & Year'])
    df_bs_pct_chg_t = df_bs_pct_chg_t.iloc[1:]
    df_bs_pct_chg_t['']=df_bs_pct_chg_t.index
    df_bs_pct_chg_t.index = range(len(df_bs_pct_chg_t))

    cols = list(df_bs_pct_chg_t.columns)
    cols = [cols[-1]] + cols[:-1]
    df_bs_pct_chg_t = df_bs_pct_chg_t[cols]


    df_bs_t = df_bs.transpose()
    df_bs_t.columns = list(df_bs['Quarter & Year'])
    df_bs_t = df_bs_t.iloc[1:]
    df_bs_t['']=df_bs_t.index
    df_bs_t.index = range(len(df_bs_t))

    cols = list(df_bs_t.columns)
    cols = [cols[-1]] + cols[:-1]
    df_bs_t = df_bs_t[cols]
    #endregion

    df_pct = df_bs_pct_chg_t.to_html().replace('<table','<table class="df_tableBoot" id="df_myTable1"')# dt-responsive" id="df_myTable"')

    df_bs_t = df_bs_t[df_bs_t.columns[::-1]]
    cols = list(df_bs_t.columns)
    cols = [cols[-1]] + cols[:-1]
    df_bs_t = df_bs_t[cols]
    # df_html = df_bs_t.to_html().replace('<table','<table class="df_tableBoot" id="df_myTable2"')# dt-responsive" id="df_myTable"')



    def isnumber(x):
        try:
            float(x)
            return True
        except:
            return False
    df_bs_n = df_bs[df_bs.applymap(isnumber)]
    df_bs_n[df_bs_n < 2] = np.nan
    # pd.DataFrame(df_bs_n.sum())#axis=0))
    df_bs_n_sum = pd.DataFrame(df_bs_n.sum())
    df_bs_n_sum[df_bs_n_sum == 0] = ""
    new_header = df_bs_n_sum.iloc[0] #grab the first row for the header
    df_bs_n_sum = df_bs_n_sum[1:] #take the data less the header row
    df_bs_n_sum.columns = new_header #set the header row as the df header
    df_bs_n_sum.index = range(len(df_bs_n_sum))
    df_bs_t = pd.merge(df_bs_n_sum, df_bs_t, left_index=True, right_index=True,suffixes=('Total: {} - {}'.format(latest_year,earliest_year), 'Line Items'))
    df_bs_t = df_bs_t[0:25]



    col_list = []
    n=0
    while n<len(list(df_bs_t))-0:
        if n<6:
                col_item = '<col id="col_item_{}" class="col_item_class first_7_col">'.format(n)
        else:
            col_item = '<col id="col_item_{}" class="col_item_class">'.format(n)
        col_list.append(col_item)
        n+=1
    col_list_str = ''.join(map(str, col_list))
    df_html = df_bs_t.to_html().replace('border="1" class="dataframe">','class="df_tableBoot" id="df_myTable" border="1" class="dataframe"><colgroup>{}</colgroup>'.format(col_list_str))


    df_html = df_html.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
    df_html = df_html.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
    df_html = df_html.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')

    df_html=df_html[0:]
    df = df[['date','revenue']].dropna() #.fillna(0)#.fillna(method='bfill')

    df['date'] = pd.to_datetime(df['date']).values.astype(np.int64) // 10 ** 6

    full_path = csv_file.split(' ~ ')

    path = pathlib.PurePath(full_path[0])
    # asset_ticker = path.name #full_path[0].split("/")
    # asset_type = full_path[1]
    # asset_name = full_path[-1]
    print("Nothing took {} seconds".format(time.time() - start_time))
    total_seconds = ((time.time() - start_time))

    labels = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
    ]
    labels = list(df['date'])#[0:19]

    values = [
        967.67, 1190.89, 1079.75, 1349.19,
        2328.91, 2504.28, 2873.83, 4764.87,
        4349.29, 6458.30, 9907, 16297
    ]

    values = list(df['revenue'])#[0:19]

    colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


    df_html


    # return render_template('D:\\Cloud\\rclone\\OneDrive\\Web\\TenDollarData\\Charts_TenDollarData\\financial_statements\\templates\\fin_statements_bootstrapped.html',
    return render_template('fin_statements_bootstrapped.html',    
     df_date = df['date'].to_list(), df_rev = df['revenue'].to_list(),
     df_json =df.to_numpy().tolist(), table_pct = [df_pct], tables=[df_html], titles=df.columns.values,





     total_time=total_seconds, place_name=some_place, max=17000, labels=labels, values=values)


@charts.route('/current_ratio/<some_place>', methods=['POST', 'GET'])

def current_ratio(some_place):

    start_time = time.time()
    csv_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/Income Statement/*_{}_*".format(some_place))[-1] #.format("NLOK"))[-1]
    df = pd.read_csv(csv_file)
    # df = df[df['date'].notna()]#fillna(method='ffill')
    df = df[0:].iloc[::-1]#.dropna()
    df_bs = df
    #region Pandas data manipulation
    df_bs['Quarter & Year'] = df_bs['period']+" "+(df_bs['date'].astype(str).str[0:4])#((df_bs['date'].astype(str).str[0:4].astype(int))-1).astype(str)

    latest_year = list((df_bs['date'].astype(str).str[0:4]))[0]
    earliest_year = list((df_bs['date'].astype(str).str[0:4]))[-1]

    df_bs = df_bs.drop([ 'Unnamed: 0','date',
     'symbol',
     'fillingDate','period','link'],axis=1)

    df_bs.columns = [
     'Date & Time Filing Accepted',
     'Revenue (Sales)',
     'Cost of Revenue (Sales)',
     'Gross Profit (Income)',
     'Gross Profit (Income) Ratio',
     'Research and Development (R&D) Expenses',
     'Sales, General and Administrative (SG&A) Expenses',
     'Selling and Marketing (S&M) Expenses',
     'Other Expenses',
     'Operating Expenses',
     'Cost and Expenses',
     'Interest Expense',
     'Depreciation and Amortization (D&A)',
     'EBITDA',
     'EBITDA Ratio',
     'Operating Income',
     'Operating Income Ratio',
     'Total Other Income Expenses (Net)',
     'Income Before Tax',
     'Income Before Tax Ratio',
     'Income Tax Expense',
     'Net Income',
     'Net Income Ratio',
     'EPS',
     'EPS Diluted',
     'Weighted Average Shares Outstanding',
     'Weighted Average Shares Outstanding (Diluted)',
     'SEC Filing', 'Quarter & Year'
                    ]
    cols = [ 'Quarter & Year', 'Revenue (Sales)',
     'Cost of Revenue (Sales)',
     'Gross Profit (Income)',
     'Gross Profit (Income) Ratio',
     'Research and Development (R&D) Expenses',
     'Sales, General and Administrative (SG&A) Expenses',
     'Other Expenses',
     'Operating Expenses',
     'Cost and Expenses',
     'Interest Expense',
     'Depreciation and Amortization (D&A)',
     'EBITDA',
     'EBITDA Ratio',
     'Operating Income',
     'Operating Income Ratio',
     'Total Other Income Expenses (Net)',
     'Income Before Tax',
     'Income Before Tax Ratio',
     'Income Tax Expense',
     'Net Income',
     'Net Income Ratio',
     'EPS',
     'EPS Diluted',
     'Weighted Average Shares Outstanding',
     'Weighted Average Shares Outstanding (Diluted)',
     'SEC Filing','Date & Time Filing Accepted']

    df_bs = df_bs[cols]

    df_bs_pct_chg = df_bs
    pct_chg_cols = (df_bs.select_dtypes(include=['number']).pct_change(-1))
    df_bs_str = df_bs_pct_chg.drop(list(pct_chg_cols), axis=1)
    df_bs_pct_chg = df_bs_str.join(pct_chg_cols)[list(df_bs)]

    pd.set_option('display.float_format', '{:.2f}'.format)
    df_bs_pct_chg_t = df_bs_pct_chg.transpose()
    df_bs_pct_chg_t.columns = list(df_bs_pct_chg['Quarter & Year'])
    df_bs_pct_chg_t = df_bs_pct_chg_t.iloc[1:]

    df_bs_pct_chg_t = df_bs_pct_chg.transpose()
    df_bs_pct_chg_t.columns = list(df_bs_pct_chg['Quarter & Year'])
    df_bs_pct_chg_t = df_bs_pct_chg_t.iloc[1:]
    df_bs_pct_chg_t['']=df_bs_pct_chg_t.index
    df_bs_pct_chg_t.index = range(len(df_bs_pct_chg_t))

    cols = list(df_bs_pct_chg_t.columns)
    cols = [cols[-1]] + cols[:-1]
    df_bs_pct_chg_t = df_bs_pct_chg_t[cols]


    df_bs_t = df_bs.transpose()
    df_bs_t.columns = list(df_bs['Quarter & Year'])
    df_bs_t = df_bs_t.iloc[1:]
    df_bs_t['']=df_bs_t.index
    df_bs_t.index = range(len(df_bs_t))

    cols = list(df_bs_t.columns)
    cols = [cols[-1]] + cols[:-1]
    df_bs_t = df_bs_t[cols]
    #endregion

    df_pct = df_bs_pct_chg_t.to_html().replace('<table','<table class="df_tableBoot" id="df_myTable1"')# dt-responsive" id="df_myTable"')

    df_bs_t = df_bs_t[df_bs_t.columns[::-1]]
    cols = list(df_bs_t.columns)
    cols = [cols[-1]] + cols[:-1]
    df_bs_t = df_bs_t[cols]



    def isnumber(x):
        try:
            float(x)
            return True
        except:
            return False
    df_bs_n = df_bs[df_bs.applymap(isnumber)]
    df_bs_n[df_bs_n < 2] = np.nan
    # pd.DataFrame(df_bs_n.sum())#axis=0))
    df_bs_n_sum = pd.DataFrame(df_bs_n.sum())
    df_bs_n_sum[df_bs_n_sum == 0] = ""
    new_header = df_bs_n_sum.iloc[0] #grab the first row for the header
    df_bs_n_sum = df_bs_n_sum[1:] #take the data less the header row
    df_bs_n_sum.columns = new_header #set the header row as the df header
    df_bs_n_sum.index = range(len(df_bs_n_sum))
    df_bs_t = pd.merge(df_bs_n_sum, df_bs_t, left_index=True, right_index=True,suffixes=('Total: {} - {}'.format(latest_year,earliest_year), 'Line Items'))
    df_bs_t = df_bs_t[0:25]



    col_list = []
    n=0
    while n<len(list(df_bs_t))-0:
        if n<6:
                col_item = '<col id="col_item_{}" class="col_item_class first_7_col">'.format(n)
        else:
            col_item = '<col id="col_item_{}" class="col_item_class">'.format(n)
        col_list.append(col_item)
        n+=1
    col_list_str = ''.join(map(str, col_list))
    df_html = df_bs_t.to_html().replace('border="1" class="dataframe">','class="df_tableBoot" id="df_myTable" border="1" class="dataframe"><colgroup>{}</colgroup>'.format(col_list_str))


    df_html = df_html.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
    df_html = df_html.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
    df_html = df_html.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')

    df_html=df_html[0:]
    df = df[['date','revenue']].dropna() #.fillna(0)#.fillna(method='bfill')

    df['date'] = pd.to_datetime(df['date']).values.astype(np.int64) // 10 ** 6

    full_path = csv_file.split(' ~ ')

    path = pathlib.PurePath(full_path[0])

    print("Nothing took {} seconds".format(time.time() - start_time))
    total_seconds = ((time.time() - start_time))

    labels = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
    ]
    labels = list(df['date'])#[0:19]

    values = [
        967.67, 1190.89, 1079.75, 1349.19,
        2328.91, 2504.28, 2873.83, 4764.87,
        4349.29, 6458.30, 9907, 16297
    ]

    values = list(df['revenue'])#[0:19]

    colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


    return render_template('fin_statements_bootstrapped.html',    
     df_date = df['date'].to_list(), df_rev = df['revenue'].to_list(),
     df_json =df.to_numpy().tolist(), table_pct = [df_pct], tables=[df_html], titles=df.columns.values,





     total_time=total_seconds, place_name=some_place, max=17000, labels=labels, values=values)

@charts.route('/test/<some_place>', methods=['POST', 'GET'])
def fin_test(some_place):


    return render_template('financial_statements.html',

     df_html=FS("IS","AAPL").df_html(), 
     tables=FS("IS","AAPL").df_values()['df_table'], 
     table_pct = FS("IS","AAPL").df_values()['df_table_pct'], 
     df_date = FS("IS","AAPL").df_values()['chart_x_dates'], 
     df_rev = FS("IS","AAPL").df_values()['chart_y_revenue'],
     df_json = FS("IS","AAPL").df_values()['df_json'],
     titles=FS("IS","AAPL").df_values()['df_titles'],
     labels = FS("IS","AAPL").df_labels(),
     values=FS("IS","AAPL").df_price(),
     place_name=some_place, max=17000, 
     )

