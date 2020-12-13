
# mark: top

# https://github.com/ptmcg/littletable
    # https://github.com/sunary/flask-optimize
    # https://github.com/h2oai/datatable
    # https://github.com/derekeder/csv-to-html-table
    # https://github.com/vividvilla/csvtotable
    # https://medium.com/casual-inference/the-most-time-efficient-ways-to-import-csv-data-in-python-cc159b44063d
    # https://blog.esciencecenter.nl/irregular-data-in-pandas-using-c-88ce311cb9ef
    # all the imports - https://flask.palletsprojects.com/en/0.12.x/tutorial/setup/#tutorial-setup
    # https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
    # https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
    # https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table
    # https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe
    # https://stackoverflow.com/questions/17134942/pandas-dataframe-output-end-of-csv
    # http://www.compjour.org/lessons/flask-single-page/multiple-dynamic-routes-in-flask/

# Flask-DebugToolbar
import os
import sqlite3
import pandas as pd
import glob
import pathlib
import time
import sys


sys.path.append(os.path.join(os.path.dirname(__file__)))

# from financial_statements.functions.pandas_extraction import FS
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
# app = Flask(__name__)
from string import Template

# https://stackoverflow.com/questions/17309889/how-to-debug-a-flask-app
# from flask_debugtoolbar import DebugToolbarExtension
# app.debug = True
# toolbar = DebugToolbarExtension(app)


# app.config['CACHE_TYPE'] = 'simple'
# cache.init_app(app)
# blueprint = Blueprint('stock', __name__, static_url_path='', static_folder='stock')
charts = Blueprint('charts', __name__)
# app.register_blueprint(blueprint)




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
# @cache.cached(timeout=5)

def html_table(some_place):
    start_time = time.time()
    # test="KWK"
    # df = pd.read_csv(glob.glob("charts/annual_returns/annual_returns/{}*".format(test))[-1])
    csv_file = glob.glob("Charts_TenDollarData/financial_statements/charts/annual_returns/annual_returns/{}*".format(some_place))[-1]
    csv_file = glob.glob("Charts_TenDollarData/financial_statements/charts/annual_returns/annual_returns/{}*".format(some_place))[-1]
    df = pd.read_csv(csv_file)
    df_html = df.to_html().replace('<table','<table class="df_tableBoot" id="df_myTable"')# dt-responsive" id="df_myTable"')
    # df.to_html(classes='annual-returns-data')
    # 0.009995698928833008
    # 0.013002872467041016
    full_path = csv_file.split(' ~ ')
    path = pathlib.PurePath(full_path[0])
    asset_ticker = path.name #full_path[0].split("/")
    asset_type = full_path[1]
    asset_name = full_path[-1]
    # df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
    #                    'B': [5, 6, 7, 8, 9],
    #                    'C': ['a', 'b', 'c--', 'd', 'e']})
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
# @cache.cached(timeout=5)
def financial_statements(some_place):

    start_time = time.time()
    csv_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/Income Statement/*~{}~*".format(some_place))[-1] #.format("NLOK"))[-1]
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


    return render_template('fin_statements_bootstrapped.html',    
     df_date = df['date'].to_list(), df_rev = df['revenue'].to_list(),
     df_json =df.to_numpy().tolist(), table_pct = [df_pct], tables=[df_html], titles=df.columns.values,





     total_time=total_seconds, place_name=some_place, max=17000, labels=labels, values=values)

# mark: WIP - dynamic

company_profiles = pd.read_csv("reference_Data/Company_Profiles.csv")#, encoding='cp1252')
company_profiles['lower symbol'] = company_profiles['symbol'].apply(lambda x: x.lower())
company_profiles['lower short name'] = company_profiles['short name'].apply(lambda x: x.lower())
short_symbol = list(company_profiles['lower symbol'])
short_name = list(company_profiles['lower short name'])
profiles_dict = {}
url_symbol_name = list(company_profiles['lower symbol']+"/"+company_profiles['lower short name'])
short_name = ["log", "cash_and_cash_equivalents","current_ratio_not_gonna_work", "loginexample"]
print("yesss")
print("BOO HOOf",url_symbol_name[1],url_symbol_name[1].split("/")[0].upper())
print("ok lets try /{}/{}/dzs".format(url_symbol_name,"cash_and_cash_equivalents"))
urilist = ["log", "cash_and_cash_equivalents","current_ratio_not_gonna_work", "loginexample"]
# @charts.route('/<some_place>-stock/<urilist>/dzs', methods=['POST', 'GET'])
@charts.route('/<url_symbol_name>/<urilist>/dzs', methods=['POST', 'GET'])
# @charts.route('/<some_place>-stock/<short_name>/dzs', methods=['POST', 'GET'])

# company_name_url = company_profiles[company_profiles['symbol']=="{}".format(some_place)]
# @cache.cached(timeout=5)
# def current_ratio(urilist,url_symbol_name):
def current_ratio(urilist,some_place):
    print(url_symbol_name," yee haw")
    some_place = url_symbol_name.split("/")[0].upper()
    print(some_place," yee haw")
    # short_name = short_name
    url_is_list = [ 'revenue_sales',
                'cost_of_sales_cost_of_revenue_cost_of_goods_sold',
                'gross_profit_gross_income',
                'gross_income_ratio_gross_profit_ratio',
                'r%26d_research_and_development_expenses',
                'sg%26a_sga_sales_general_and_administrative_expenses',
                'other_expenses',
                'operating_expenses',
                '',
                'interest_expense',
                'd%26a_depreciation_and_amortization',
                'ebitda',
                'ebitda_ratio',
                'operating_income',
                'operating_income_ratio',
                'other_income_other_expenses_net',
                'income_before_tax_provisions',
                'income_before_tax_ratio',
                'income_tax_expense_provisions',
                'net_income',
                'net_income_ratio',
                'eps_earnings_per_share',
                'eps_earnings_per_share_diluted',
                'shares_outstanding_for_eps',
                'shares_outstanding_weighted_for_eps',]
    url_bs_list = ['quarter_and_year','cash_and_cash_equivalents',
                'short_term_investments',
                'cash_and_short_term_investments',
                'net_receivables',
                'inventory',
                'other_current_assets',
                'total_current_assets',
                'pp_and_e',
                'goodwill',
                'intangible_assets',
                'goodwill_and_intangible_assets',
                'long_term_investments',
                'tax_assets',
                'other_non_current_assets',
                'total_non_current_assets',
                'other_assets',
                'total_assets',
                'accounts_payables',
                'short_term_debt',
                'tax_payables',
                'deferred_revenue',
                'other_current_liabilities',
                'total_current_liabilities',
                'long_term_debt',
                'deferred_revenue_non_current',
                'deferred_tax_liabilities_non_current',
                'other_non_current_liabilities',
                'total_non_current_liabilities',
                'other_liabilities',
                'total_liabilities',
                'common_stock',
                'retained_earnings',
                'accumulated_other_comprehensive_income_loss',
                'other_total_stockholders_equity',
                'total_stockholders_equity',
                'total_liabilities_and_stockholders_equity',
                'total_investments',
                'total_debt',
                'net_debt','final_link']
    url_cf_list = ['net_income',
                    'depreciation_and_amortization',
                    'deferred_income_tax',
                    'stock_based_compensation',
                    'change_in_working_capital',
                    'accounts_receivable',
                    'inventory',
                    'accounts_payables',
                    'other_working_capital',
                    'other_non_cash_items',
                    'net_cash_provided_by_operating_activities',
                    'investments_in_property_plant_and_equipment',
                    'acquisitions_net',
                    'purchases_of_investments',
                    'sales_maturities_of_investments',
                    'other_investing_activities',
                    'net_cash_used_for_investing_activities',
                    'debt_repayment',
                    'common_stock_issued',
                    'common_stock_repurchased',
                    'dividends_paid',
                    'other_financing_activities',
                    'net_cash_used_provided_by_financing_activities',
                    'effect_of_forex_changes_on_cash',
                    'net_change_in_cash',
                    'cash_at_end_of_period',
                    'cash_at_beginning_of_period',
                    'operating_cash_flow',
                    'capital_expenditure',
                    'free_cash_flow']

    company_profiles = pd.read_csv("reference_Data/Company_Profiles.csv")#, encoding='cp1252')
    company_profiles_col = ['symbol',
                            'long name',
                            'currency',
                            'exchange',
                            'industry',
                            'description',
                            'sector',
                            'country',
                            'ipo date',
                            'short name']
    company_profiles = company_profiles[company_profiles_col]    
    profiles_dict = {}
    profiles_value = company_profiles[company_profiles['symbol']=="{}".format(some_place.upper())].values.tolist()[0]
    for n, profiles_col in enumerate(company_profiles_col):
        key = profiles_col
        value = profiles_value[n]
        profiles_dict[key] = value 
    
    if "{}".format(urilist) in url_is_list:
        fin_statement_dir = "Income Statement"
    elif "{}".format(urilist) in url_bs_list:
        fin_metric_pos = url_bs_list.index("{}".format(urilist))
        fin_statement_dir = "Balance Sheet"
        fin_statement_cols = ['Cash and Cash Equivalents',
                            'Short Term Investments',
                            'Cash And Short-Term Investments',
                            'Net Receivables',
                            'Inventory',
                            'Other Current Assets',
                            'Total Current Assets',
                            'PP&E',
                            'Goodwill',
                            'Intangible Assets',
                            'Goodwill and Intangible Assets',
                            'Long-term Investments',
                            'Tax Assets',
                            'Other Non-Current Assets',
                            'Total Non-Current Assets',
                            'Other Assets',
                            'TotalAssets',
                            'Accounts Payables',
                            'Short-term Debt',
                            'Tax Payables',
                            'Deferred Revenue',
                            'Other Current Liabilities',
                            'Total Current Liabilities',
                            'Long-term Debt',
                            'Deferred Revenue Non-Current',
                            'Deferred Tax Liabilities Non-Current',
                            'Other Non-Current Liabilities',
                            'Total Non-Current Liabilities',
                            'Other Liabilities',
                            'Total Liabilities',
                            'Common Stock',
                            'Retained Earnings',
                            'Accumulated Other Comprehensive Income Loss',
                            'Other Total Stockholders Equity',
                            'Total Stockholders Equity',
                            'Total Liabilities & Stockholders Equity',
                            'Total Investments',
                            'Total Debt',
                            'Net Debt',
                            'finalLink','Quarter & Year']
        cols = ['Quarter & Year',
                'Cash and Cash Equivalents',
                'Short Term Investments',
                'Cash And Short-Term Investments',
                'Net Receivables',
                'Inventory',
                'Other Current Assets',
                'Total Current Assets',
                'PP&E',
                'Goodwill',
                'Intangible Assets',
                'Goodwill and Intangible Assets',
                'Long-term Investments',
                'Tax Assets',
                'Other Non-Current Assets',
                'Total Non-Current Assets',
                'Other Assets',
                'TotalAssets',
                'Accounts Payables',
                'Short-term Debt',
                'Tax Payables',
                'Deferred Revenue',
                'Other Current Liabilities',
                'Total Current Liabilities',
                'Long-term Debt',
                'Deferred Revenue Non-Current',
                'Deferred Tax Liabilities Non-Current',
                'Other Non-Current Liabilities',
                'Total Non-Current Liabilities',
                'Other Liabilities',
                'Total Liabilities',
                'Common Stock',
                'Retained Earnings',
                'Accumulated Other Comprehensive Income Loss',
                'Other Total Stockholders Equity',
                'Total Stockholders Equity',
                'Total Liabilities & Stockholders Equity',
                'Total Investments',
                'Total Debt',
                'Net Debt',
                'finalLink']        
        fin_metric_name = fin_statement_cols[fin_metric_pos-1]
        
    elif "{}".format(urilist) in url_cf_list:
        fin_statement_dir = "Cash Flow Statement"
        
    else:
        pass
    # pragma adasdadsd
    # MARK: asdas
    start_time = time.time()
    csv_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/{}/*~{}~*".format(fin_statement_dir, some_place.upper()))[-1]
    # csv_file = glob.glob("../Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/*/*~{}~*".format(some_place))[-1]
    df = pd.read_csv(csv_file) #.format("NLOK"))[-1]
    # df = df[df['date'].notna()]#fillna(method='ffill')
    df = df[0:].iloc[::-1]#.dropna()
    df_bs = df
    #region Pandas data manipulation
    # df_bs['Quarter & Year'] = df_bs['period']+" "+(df_bs['date'].astype(str).str[0:4])#((df_bs['date'].astype(str).str[0:4].astype(int))-1).astype(str)
    df_bs['Quarter & Year'] =(df_bs['date'].astype(str).str[0:4]).astype(int)#((df_bs['date'].astype(str).str[0:4].astype(int))-1)
    latest_year = list((df_bs['date'].astype(str).str[0:4]))[0]
    earliest_year = list((df_bs['date'].astype(str).str[0:4]))[-1]

    df_bs = df_bs.drop([ 'Unnamed: 0','date',
    'symbol',
    'fillingDate','period','link','acceptedDate'],axis=1)
    
    df_bs.columns = fin_statement_cols
    # for col in df_bs.columns:
    #     if len(df_bs[col].unique()) == 1:
    #         df_bs.drop(col,inplace=True,axis=1)


    df_bs = df_bs[cols]

    df_bs.index = df_bs['Quarter & Year']
    
    million = 1000000
    billion = 1000000000
    fin_metric_history = df_bs['{}'.format(fin_metric_name)]
    if list(fin_metric_history)[0]  > billion:
        print()
        df_bs['{}'.format(fin_metric_name)] = (fin_metric_history/billion).round(decimals=2)
        df_bs_table_html = df_bs[['{}'.format(fin_metric_name)]].iloc[::-1].transpose().to_html().replace("'","")
        
    elif fin_metric_history[0]  > million:
        pass
    else:
        pass

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
    df = df[['date','cashAndCashEquivalents']].dropna() #.fillna(0)#.fillna(method='bfill')

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

    values = list(df['cashAndCashEquivalents'])#[0:19]

    colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    df_html
    # return render_template('D:\\Cloud\\rclone\\OneDrive\\Web\\TenDollarData\\Charts_TenDollarData\\financial_statements\\templates\\fin_statements_bootstrapped.html',
    return render_template('current_ratio.html', company_symbol = profiles_dict['symbol'],\
                            company_long_name = profiles_dict['long name'],\
                            company_currency = profiles_dict['currency'],\
                            company_exchange = profiles_dict['exchange'],\
                            company_industry = profiles_dict['industry'],\
                            company_description = profiles_dict['description'],\
                            company_sector = profiles_dict['sector'],\
                            company_country = profiles_dict['country'],\
                            company_ipo_date = profiles_dict['ipo date'],\
                            company_short_name = profiles_dict['short name'],\
    df_bs_table_html = [df_bs_table_html], fin_metric_name = fin_metric_name,
     df_date = df['date'].to_list(), df_rev = df['cashAndCashEquivalents'].to_list(),
     df_json  =df.to_numpy().tolist(), table_pct = [df_pct], tables=[df_html], titles=df.columns.values,





     total_time=total_seconds, place_name=some_place, max=17000, labels=labels, values=values)


@charts.route('/test/<some_place>', methods=['POST', 'GET'])
# @cache.cached(timeout=5)
def fin_test(some_place):
    # values = list(FS("IS","AAPL")['Beginning Price'])[0:19]


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

