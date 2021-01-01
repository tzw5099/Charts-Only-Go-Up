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
from flask import render_template_string,request, session, g, redirect, url_for, abort, render_template, flash, Blueprint
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



@charts.route('/<url_symbol>-stock/<url_name>/<url_fin_metric>', methods=['POST', 'GET']) # WORKS
def current_ratio(url_fin_metric,url_name,url_symbol): # WORKS
# def current_ratio(urilist,url_symbol_name):
    def magnitude_num(number, currency_symbol):
        if len(str(number)) > 9:
            magnitude = number/1000000000
            magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),"B")
        elif len(str(number)) > 6:
            magnitude = number/1000000
            magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),"M")
        elif len(str(number)) > 3:
            magnitude = number/1000
            magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),"K")
        else:
            magnitude = number
            magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),"K")
        return magnitude_str

    company_profiles = pd.read_csv("reference_data/Company_Profiles.csv")#, encoding='cp1252')
    fin_statements_matching = pd.read_csv("reference_data/Financial_Statements_Reference_Matching.csv")#, encoding='cp1252')
    currency_symbol = list(company_profiles[company_profiles['symbol']=="{}".format(url_symbol.upper())]['currency symbol'])[0]
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
    profiles_value = company_profiles[company_profiles['symbol']=="{}".format(url_symbol.upper())].values.tolist()[0]

    titles_bs = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Balance Sheet"]['Title'])
    titles_cf = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Cash Flow Statement"]['Title'])
    titles_is = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Income Statement"]['Title'])

    urls_bs = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Balance Sheet"]['URL'])
    urls_cf = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Cash Flow Statement"]['URL'])
    urls_is = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Income Statement"]['URL'])

    for n, profiles_col in enumerate(company_profiles_col):
        key = profiles_col
        value = profiles_value[n]
        profiles_dict[key] = value 

    if "{}".format(url_fin_metric) in urls_is:
        fin_statement_dir = "Income Statement"
    elif "{}".format(url_fin_metric) in urls_bs:
        fin_metric_pos = urls_bs.index("{}".format(url_fin_metric))
        fin_statement_dir = "Balance Sheet"
        fin_statement_cols = titles_bs
        cols = titles_bs
        fin_metric_title = fin_statement_cols[fin_metric_pos]

    elif "{}".format(url_fin_metric) in urls_cf:
        fin_statement_dir = "Cash Flow Statement"

    else:
        pass

    start_time = time.time()
    csv_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/{}/*~{}~*".format(fin_statement_dir, url_symbol.upper()))[-1]

    df = pd.read_csv(csv_file) #.format("NLOK"))[-1]
    # df = df[df['date'].notna()]#fillna(method='ffill')
    df = df[0:].iloc[::-1]#.dropna()
    df_fin_statement = df
    #region Pandas data manipulation
    matching_row = fin_statements_matching[fin_statements_matching['URL']=="{}".format(url_fin_metric)]
    fin_metric_title = list(matching_row['Title'])[0]
    fin_metric_name = list(matching_row['Name'])[0]
    print("fin metric name", fin_metric_name)
    sorted_metric = df["{}".format(fin_metric_name)].sort_values()
    # sorted_metric(int(len(sorted_metric)*(n/100)))
    quarters = round(len(sorted_metric)/4)
    bottom_25 = sorted_metric[len(sorted_metric)-1-quarters]
    top_25 = sorted_metric[quarters-1]
    max_num = sorted_metric.max()
    min_num = sorted_metric.min()
    mean = sorted_metric.mean()
    std_dev = sorted_metric.std()
    std_dev_str = "+/-{}{}%".format(currency_symbol,round(abs((std_dev-mean)/mean)*100,1))
    mean_str = magnitude_num(mean, currency_symbol)
    max_str = magnitude_num(max_num, currency_symbol)
    min_str = magnitude_num(min_num, currency_symbol)
    bottom_25_str = magnitude_num(bottom_25, currency_symbol)
    top_25_str = magnitude_num(top_25, currency_symbol)

    lifetime_sum_all_metric = df["{}".format(fin_metric_name)].sum()
    lifetime_sum_all_metric = magnitude_num(lifetime_sum_all_metric,currency_symbol)

    latest_num = df["{}".format(fin_metric_name)][0]
    first_num = list(df["{}".format(fin_metric_name)])[-1]
    pct_chg = (latest_num - first_num)/first_num
    historical_pct_chg = str(round(pct_chg*100, 1))

    if pct_chg>=0:
        pct_chg_str = "+{}%".format(pct_chg)
    elif pct_chg<0:
        pct_chg_str = "-{}%".format(pct_chg)
    else:
        pct_chg_str = ""
    # historical_pct_chg = str(round(pct_chg*100, 1))
    max_min_pct_diff = ((max_num-min_num)/min_num)
    if max_min_pct_diff>=0:
        max_min_pct_diff_str = "+{}%".format(round(max_min_pct_diff)*100,1)
    elif max_min_pct_diff<0:
        max_min_pct_diff_str = "-{}%".format(round(max_min_pct_diff)*100,1)
    else:
        max_min_pct_diff_str = ""
    df_fin_statement['Quarter & Year'] =(df_fin_statement['date'].astype(str).str[0:4]).astype(int)
    latest_year = list((df_fin_statement['date'].astype(str).str[0:4]))[0]
    earliest_year = list((df_fin_statement['date'].astype(str).str[0:4]))[-1]
    earliest_metric = (list(df["{}".format("cashAndCashEquivalents")])[-1])
    latest_metric = (list(df["{}".format("cashAndCashEquivalents")])[0])
    
    
    titles_list = ['Date','Symbol','Filing Date','Accepted Date','Period','SEC Filing Link']
    for x in titles_bs:
        if x in titles_list:
            titles_bs.remove(x)
    df_fin_statement = df_fin_statement.drop([ 'Unnamed: 0','date','symbol','fillingDate','acceptedDate','period','link'],axis=1)
    # bug (?) - Symbol & Accepted Date not removed
    titles_bs.remove('Symbol')
    titles_bs.remove('Accepted Date')
    titles_bs.append('Quarter & Year') 
    df_fin_statement.columns = titles_bs



    df_fin_statement = df_fin_statement[cols]

    df_fin_statement.index = df_fin_statement['Quarter & Year']
    
    million = 1000000
    billion = 1000000000
    fin_metric_history = df_fin_statement['{}'.format(fin_metric_title)]
    if list(fin_metric_history)[0]  > billion:
        df_fin_statement['{}'.format(fin_metric_title)] = (fin_metric_history/billion).round(decimals=2)
        

    elif fin_metric_history[0]  > million:
        pass
    else:
        pass

    df_pct_chg = df_fin_statement
    pct_chg_cols = (df_fin_statement.select_dtypes(include=['number']).pct_change(-1))
    df_pct_chg_str = df_pct_chg.drop(list(pct_chg_cols), axis=1)
    df_pct_chg = df_pct_chg_str.join(pct_chg_cols)[list(df_fin_statement)]

    pd.set_option('display.float_format', '{:.2f}'.format)
    df_pct_chg_t = df_pct_chg.transpose()
    df_pct_chg_t.columns = list(df_pct_chg['Quarter & Year'])
    df_pct_chg_t = df_pct_chg_t.iloc[1:]

    df_pct_chg_t = df_pct_chg.transpose()
    df_pct_chg_t.columns = list(df_pct_chg['Quarter & Year'])
    df_pct_chg_t = df_pct_chg_t.iloc[1:]
    df_pct_chg_t['']=df_pct_chg_t.index
    df_pct_chg_t.index = range(len(df_pct_chg_t))

    cols = list(df_pct_chg_t.columns)
    cols = [cols[-1]] + cols[:-1]
    df_pct_chg_t = df_pct_chg_t[cols]


    df_t = df_fin_statement.transpose()
    df_t.columns = list(df_fin_statement['Quarter & Year'])
    df_t = df_t.iloc[1:]
    df_t['']=df_t.index
    df_t.index = range(len(df_t))

    cols = list(df_t.columns)
    cols = [cols[-1]] + cols[:-1]
    df_t = df_t[cols]
    #endregion

    df_pct = df_pct_chg_t.to_html().replace('<table','<table class="df_tableBoot" id="df_myTable1"')# dt-responsive" id="df_myTable"')

    df_t = df_t[df_t.columns[::-1]]
    cols = list(df_t.columns)
    cols = [cols[-1]] + cols[:-1]
    df_t = df_t[cols]


    def isnumber(x):
        try:
            float(x)
            return True
        except:
            return False
    df_n = df_fin_statement[df_fin_statement.applymap(isnumber)]
    df_n[df_n < 2] = np.nan
    df_n_sum = pd.DataFrame(df_n.sum())
    df_n_sum[df_n_sum == 0] = ""
    new_header = df_n_sum.iloc[0] #grab the first row for the header
    df_n_sum = df_n_sum[1:] #take the data less the header row
    df_n_sum.columns = new_header #set the header row as the df header
    df_n_sum.index = range(len(df_n_sum))
    df_t = pd.merge(df_n_sum, df_t, left_index=True, right_index=True,suffixes=('Total: {} - {}'.format(latest_year,earliest_year), 'Line Items'))
    df_t = df_t[0:25]



    col_list = []
    n=0
    while n<len(list(df_t))-0:
        if n<6:
                col_item = '<col id="col_item_{}" class="col_item_class first_7_col">'.format(n)
        else:
            col_item = '<col id="col_item_{}" class="col_item_class">'.format(n)
        col_list.append(col_item)
        n+=1
    col_list_str = ''.join(map(str, col_list))
    df_html = df_t.to_html().replace('border="1" class="dataframe">','class="df_tableBoot" id="df_myTable" border="1" class="dataframe"><colgroup>{}</colgroup>'.format(col_list_str))

    df_table_html = df_fin_statement[['{}'.format(fin_metric_title)]].iloc[::-1].transpose().to_html().replace("\n","")

    df_tall = df
    df_tall.index = df['Quarter & Year'].iloc[::-1]
    # df_tall = df.index.shift(-1)
    df_tall = df_tall.reset_index()
    df_html_tall = df_tall[['{}'.format(fin_metric_name)]].to_html().replace("'","")
    # df_html_tall = df_html_tall.replace("\n","")
    df_html_tall = df_html_tall.replace("\n","")
    df_html_tall = df_html_tall.replace("{}".format("["),"")
    df_html_tall = df_html_tall #render_template_string(df_html_tall)
    df_html = df_html.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
    df_html = df_html.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
    df_html = df_html.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')
    #  df_html_tall = df_html_tall.replace("\n","")
    # df_html_tall.replace("\n",'">')
    df_html_tall = df_html_tall.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
    df_html_tall = df_html_tall.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
    df_html_tall = df_html_tall.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')
    df_html_tall = df_html_tall[0:]
    
    df = df[['date',"{}".format(fin_metric_name)]].dropna() #.fillna(0)#.fillna(method='bfill')
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

    values = list(df["{}".format(fin_metric_name)])#[0:19]

    colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

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
                            first_num = first_num,\
                            latest_num = latest_num,\
                            historical_pct_chg = historical_pct_chg,\
                            lifetime_sum_all_metric = lifetime_sum_all_metric,\
                            mean_str = mean_str,\
                            max_str = max_str,\
                            min_str = min_str,\
                            std_dev_str = std_dev_str,\
                            bottom_25_str = bottom_25_str,\
                            top_25_str = top_25_str,\
                            earliest_year = earliest_year,\
                            latest_year = latest_year,\
                            earliest_metric = earliest_metric,\
                            latest_metric = latest_metric,\
                            max_min_pct_diff_str = max_min_pct_diff_str, df_bs_table_html = [df_table_html],df_html_tall = [df_html_tall],fin_metric_name = fin_metric_title,\
                            df_date = df['date'].to_list(), df_rev = df["{}".format(fin_metric_name)].to_list(),\
                            df_json  =df.to_numpy().tolist(),\
                            table_pct = [df_pct],\
                            tables=[df_html],\
                            titles=df.columns.values,\
                            total_time=total_seconds,\
                            place_name=url_symbol,\
                            max=17000,\
                            labels=labels,\
                            values=values)


@charts.route('/test/<url_symbol>', methods=['POST', 'GET'])
# @cache.cached(timeout=5)
def fin_test(url_symbol):
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
     place_name=url_symbol, max=17000,
     )