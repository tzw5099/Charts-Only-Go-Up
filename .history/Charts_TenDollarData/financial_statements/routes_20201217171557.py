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



@charts.route('/<url_symbol>-<stock_or_etf>/<url_name>/<statement_or_ratio>/<url_fin_metric>', methods=['POST', 'GET']) # WORKS
def current_ratio(url_fin_metric,stock_or_etf,url_name,statement_or_ratio,url_symbol): # WORKS
    from route_imports.ratio_map import metric_to_url_map # as ratios
    from route_imports.ratio_map import url_to_var_name_map
    from route_imports.ratio_map import url_to_name_map
    from route_imports.ratio_map import fin_statement_raw_names
    from route_imports.ratio_map import fin_statement_renamed_cols
    from route_imports.ratio_map import metric_to_formula_map
    from route_imports.ratio_map import url_to_metric_map
    start_time = time.time()
    url_symbol="aapl"
    titles_list = ['Date','Symbol','Filing Date','Accepted Date','Period','SEC Filing Link']
    def magnitude_num(number, currency_symbol):
        if len(str(number)) > 9 and number > 0:
            magnitude = number/1000000000
            magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),"B")
        elif len(str(number)) > 6 and number > 0:
            magnitude = number/1000000
            magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),"M")
        elif len(str(number)) > 3 and number > 0:
            magnitude = number/1000
            magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),"K")

        elif len(str(number)) > 9 and number < 0:
            magnitude = abs(number/1000000000)
            magnitude_str = "-{}{}{}".format(currency_symbol,round(magnitude,1),"B")
        elif len(str(number)) > 6 and number < 0:
            magnitude = abs(number/1000000)
            magnitude_str = "-{}{}{}".format(currency_symbol,round(magnitude,1),"M")
        elif len(str(number)) > 3 and number < 0:
            magnitude = abs(number/1000)
            magnitude_str = "-{}{}{}".format(currency_symbol,round(magnitude,1),"K")
        else:
            magnitude = number
            magnitude_str = "{}{}{}".format("",round(magnitude,1),"K")
        return magnitude_str
    fin_statements_list = ["balance-sheet","income-statement","cash-flow-statement"]
    if "{}".format(statement_or_ratio) in fin_statements_list:
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
                                'short name',
                                'Industries',
                                'Similar Companies']
        company_profiles = company_profiles[company_profiles_col]
        profiles_dict = {}
        profiles_value = company_profiles[company_profiles['symbol']=="{}".format(url_symbol.upper())].values.tolist()[0]

        # http://127.0.0.1:5000/aapl-stock/apple/balance-sheet/cash-and-cash-equivalents

        titles_cf = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Cash Flow Statement"]['Title'])
        titles_is = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Income Statement"]['Title'])

        urls_bs = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Balance Sheet"]['URL'])
        urls_cf = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Cash Flow Statement"]['URL'])
        urls_is = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Income Statement"]['URL'])

        for n, profiles_col in enumerate(company_profiles_col):
            key = profiles_col
            value = profiles_value[n]
            profiles_dict[key] = value 



        chars_to_remove = ["'","[","]"]

        for character in chars_to_remove:
            profiles_dict['Industries'] = profiles_dict['Industries'].replace(character, "")
            profiles_dict['Similar Companies'] = profiles_dict['Similar Companies'].replace(character, "")

        if "{}".format(statement_or_ratio) == "income-statement":
            titles_bs = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Income Statement"]['Title'])
            fin_metric_pos = urls_is.index("{}".format(url_fin_metric))
            fin_statement_dir = "Income Statement"
        elif "{}".format(statement_or_ratio) == "balance-sheet":
            titles_bs = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Balance Sheet"]['Title'])
            fin_metric_pos = urls_bs.index("{}".format(url_fin_metric))
            fin_statement_dir = "Balance Sheet"

        elif "{}".format(statement_or_ratio) == "cash-flow-statement":
            titles_bs = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Cash Flow Statement"]['Title'])
            fin_metric_pos = urls_cf.index("{}".format(url_fin_metric))

            fin_statement_dir = "Cash Flow Statement"
        else:
            pass
        fin_statement_cols = titles_bs
        cols = titles_bs
        fin_metric_title = fin_statement_cols[fin_metric_pos]

        csv_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/quarter/{}/*~{}~*".format(fin_statement_dir, url_symbol.upper()))[-1]

        df = pd.read_csv(csv_file) #.format("NLOK"))[-1]
        # df = df[df['date'].notna()]#fillna(method='ffill')
        df = df[0:].iloc[::-1]#.dropna()
        #region Pandas data manipulation
        df = df
        matching_row = fin_statements_matching[fin_statements_matching['URL']=="{}".format(url_fin_metric)]
        fin_metric_title = list(matching_row['Title'])[0]
        fin_metric_name = list(matching_row['Name'])[0]
        print("fin_metric_name", fin_metric_name)
        print("fin metric name", fin_metric_name)
        df = df.dropna(subset=["{}".format(fin_metric_name)]) #.fillna(0)#.fillna(method='bfill')
        df = df[df["{}".format(fin_metric_name)] != 0]
        print("goodwill")
        print(df)
        sorted_metric = df["{}".format(fin_metric_name)].sort_values()
        lifetime_sum_all_metric = df["{}".format(fin_metric_name)].sum()
        lifetime_sum_all_metric = magnitude_num(lifetime_sum_all_metric,currency_symbol)
        print("lifetime passed")


    else:
        currency_symbol = ""
        fin_dir = ["Income Statement","Balance Sheet","Cash Flow Statement"]
        fin_df_list = []
        for x in fin_dir:
            fin_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/{}/*~{}~*".format(x, url_symbol.upper()))[-1]
            fin_df = pd.read_csv(fin_file)
            fin_df_list.append(fin_df)
        df_merge_is_bs = pd.merge(fin_df_list[0],fin_df_list[1],how="inner", on="date")
        # df
        # df_merge cols
        df_merge = pd.merge(df_merge_is_bs,fin_df_list[2],how="inner", on="date")
        df_merge = df_merge[fin_statement_raw_names]
        
        df_merge.columns = fin_statement_renamed_cols
        df = df_merge

        df['ffo_math']=df['net_income'] + df['d_n_a'] + df['sales_maturities_of_investments'] + df['purchase_of_investments'] + df['investments_in_pp_n_e'] + df['acquisitions_net']
        df['book_value_math']=df['total_assets'].dropna()-df['total_liabilities'].dropna()
        df['ebit_math']=df['ebitda_non'] - df['d_n_a']
        df['working_capital_math']= df['total_current_assets'] - df['total_current_liabilities']

        df['quick_assets_math']=df['cash_non']+df['short_term_investments']+df['accounts_receivable']
        df['quick_ratio_math']=df['total_current_assets'] - df['inventory']
        metric_name = url_to_metric_map['net-working-capital-ratio']

        # url_fin_metric = 'net-working-capital-ratio'

        fin_metric_title = url_to_name_map[url_fin_metric]
        fin_metric_name = url_to_var_name_map[url_fin_metric]
        metric_history = metric_to_formula_map(df,metric_name)
        sorted_metric = metric_history.sort_values(ascending=True)
        # sorted_metric(int(len(sorted_metric)*(n/100)))
        lifetime_sum_all_metric = ""
        lifetime_sum_all_metric = ""
        df = df
        df["{}".format(fin_metric_name)] = metric_history
    
    quarters = round(len(sorted_metric)/4)
    bottom_25 = sorted_metric[len(sorted_metric)-1-quarters]
    top_25 = sorted_metric[quarters-1]
    max_metric = sorted_metric.max()
    min_metric = sorted_metric.min()
    mean = sorted_metric.mean()
    std_dev = sorted_metric.std()
    
    std_dev_pct = abs((std_dev-mean)/mean)*100
    
    std_dev_abs = std_dev_pct * mean/100
    std_dev_abs = magnitude_num(std_dev_abs, currency_symbol)
    
    std_dev_str = "+/-{}%".format(round(std_dev_pct,1))
    std_dev_abs_str = "+/-{}".format(std_dev_abs)
    
    mean_str = magnitude_num(mean, currency_symbol)
    max_str = magnitude_num(max_metric, currency_symbol)
    min_str = magnitude_num(min_metric, currency_symbol)
    bottom_25_str = magnitude_num(bottom_25, currency_symbol)
    top_25_str = magnitude_num(top_25, currency_symbol)
    
    num_years = len(sorted_metric)
    earliest_year = list((df['date'].astype(str).str[0:4]))[0]    
    latest_year = list((df['date'].astype(str).str[0:4]))[-1]    # average_abs_chg = latest_metric-earliest_metric
    earliest_metric = list(df["{}".format(fin_metric_name)])[0]
    latest_metric = list(df["{}".format(fin_metric_name)])[-1]
    print("latest num", latest_metric)
    pct_chg = (latest_metric - earliest_metric)/earliest_metric
    historical_pct_chg = str(round(pct_chg*100, 1))
    annual_pct_chg = str(round((10*(pct_chg*100)**(1/num_years)), 1))

    if pct_chg>=0:
        hist_pct_chg_str = "+{}%".format(historical_pct_chg)
        annual_pct_chg_str = "+{}%".format(annual_pct_chg)
    elif pct_chg<0:
        hist_pct_chg_str = "-{}%".format(historical_pct_chg)
        annual_pct_chg_str = "-{}%".format(annual_pct_chg)
    else:
        hist_pct_chg_str = ""
        annual_pct_chg_str = ""
    historical_pct_chg = hist_pct_chg_str
    annual_pct_chg = annual_pct_chg_str
    max_min_pct_diff = ((max_metric-min_metric)/min_metric)

    if max_min_pct_diff>=0:
        max_min_pct_diff_str = "+{}%".format(round(max_min_pct_diff)*100,1)
    elif max_min_pct_diff<0:
        max_min_pct_diff_str = "-{}%".format(round(max_min_pct_diff)*100,1)
    else:
        max_min_pct_diff_str = ""
    
    df = df.drop(['Quarter & Year', 'Unnamed: 0','symbol','fillingDate','acceptedDate','period','link'],axis=1, errors='ignore')

    
    print("list 5 ", df)
    for x in reversed(titles_bs):
        if x in titles_list:
            titles_bs.remove(x)                
    titles_bs.append('Quarter & Year') 
    df['Quarter & Year'] =(df['date'].astype(str).str[0:4]).astype(int)
    # df = df.drop(['date'],axis=1, errors='ignore')
    print("titles_bs",titles_bs)
    print("list_fin_statement",list(df))
    titles_bs.insert(0,"date")
    df.columns = titles_bs
    df = df



    df = df[cols]

    df.index = df['Quarter & Year']
    print("1st title",fin_metric_title)
    million = 1000000
    billion = 1000000000
    fin_metric_history = df['{}'.format(fin_metric_title)]
    print("list 6 ", df)
    if list(fin_metric_history)[0]  > billion:
        # df['{}'.format(fin_metric_title)] = (fin_metric_history/billion).round(decimals=2)
        pass
    elif list(fin_metric_history)[0]  > million:
        # df['{}'.format(fin_metric_title)] = (fin_metric_history/million).round(decimals=2)

        pass
    else:
        # df['{}'.format(fin_metric_title)] = (fin_metric_history).round(decimals=2)
        pass

    df_pct_chg = df
    pct_chg_cols = (df.select_dtypes(include=['number']).pct_change(-1))
    df_pct_chg_str = df_pct_chg.drop(list(pct_chg_cols), axis=1)
    df_pct_chg = df_pct_chg_str.join(pct_chg_cols)[list(df)]

    pd.set_option('display.float_format', '{:.2f}'.format)
    df_pct_chg_t = df_pct_chg.transpose()
    df_pct_chg_t.columns = list(df_pct_chg['Quarter & Year'])
    df_pct_chg_t = df_pct_chg_t.iloc[1:]
    print("list 69")
    df_pct_chg_t = df_pct_chg.transpose()
    df_pct_chg_t.columns = list(df_pct_chg['Quarter & Year'])
    df_pct_chg_t = df_pct_chg_t.iloc[1:]
    df_pct_chg_t['']=df_pct_chg_t.index
    df_pct_chg_t.index = range(len(df_pct_chg_t))

    cols = list(df_pct_chg_t.columns)
    cols = [cols[-1]] + cols[:-1]
    df_pct_chg_t = df_pct_chg_t[cols]


    df_t = df.transpose()
    df_t.columns = list(df['Quarter & Year'])
    df_t = df_t.iloc[1:]
    df_t['']=df_t.index
    df_t.index = range(len(df_t))

    cols = list(df_t.columns)
    cols = [cols[-1]] + cols[:-1]
    df_t = df_t[cols]
    #endregion
    print("list pct chg")
    print(df_pct_chg_t)
    df_pct = df_pct_chg_t.to_html().replace('<table','<table class="df_tableBoot" id="df_myTable1"')# dt-responsive" id="df_myTable"')
    print("kk 34d3")
    df_t = df_t[df_t.columns[::-1]]
    cols = list(df_t.columns)
    print("kk 34321111")
    cols = [cols[-1]] + cols[:-1]
    df_t = df_t[cols]
    print("kk 3433")

    def isnumber(x):
        try:
            float(x)
            return True
        except:
            return False
    df_n = df[df.applymap(isnumber)]
    print("kk 343")
    df_n[df_n < 2] = np.nan
    df_n_sum = pd.DataFrame(df_n.sum())
    df_n_sum[df_n_sum == 0] = ""
    new_header = df_n_sum.iloc[0] #grab the first row for the header
    df_n_sum = df_n_sum[1:] #take the data less the header row
    df_n_sum.columns = new_header #set the header row as the df header
    df_n_sum.index = range(len(df_n_sum))
    df_t = pd.merge(df_n_sum, df_t, left_index=True, right_index=True,suffixes=('Total: {} - {}'.format(latest_year,earliest_year), 'Line Items'))
    df_t = df_t[0:25]

    print("asdasd 22")

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
    # df_table_html = df_fin_statement[['{}'.format(fin_metric_title)]].iloc[::-1].transpose().to_html()#.replace("\n","")
    df_tall = df.iloc[::-1]
    # df_tall.index = df['Quarter & Year']
    # df_tall = df.index.shift(-1)
    # df_tall = df_tall.reset_index()
    print("list 7 ", fin_metric_title)
    df_html_tall = df_tall[['{}'.format('Quarter & Year'),'{}'.format(fin_metric_title)]].to_html(index=False)
    df_html_tall = df_html_tall.replace('border="1" class="dataframe">','class="abc" id="df_myTable" border="1" class="dataframe">')#.replace("'","")
    # df_html_tall = df_html_tall.replace("\n","")
    df_html_tall = df_html_tall.replace("\n","")
    df_html_tall = df_html_tall.replace("{}".format("["),"")
    df_html_tall = df_html_tall #render_template_string(df_html_tall)
    #  df_html_tall = df_html_tall.replace("\n","")
    # df_html_tall.replace("\n",'">')
    # https://stackoverflow.com/questions/39599802/python-conditionally-add-class-to-td-tags-in-html-table
    df_html_tall = df_html_tall.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
    df_html_tall = df_html_tall.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
    df_html_tall = df_html_tall.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')
    df_html_tall = df_html_tall[0:]
    print("list 8 ", fin_metric_title)
    df_html = df_html.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
    df_html = df_html.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
    df_html = df_html.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')
    
    # df = df[["{}".format(fin_metric_title)]].dropna() #.fillna(0)#.fillna(method='bfill')
    df['date'] = pd.to_datetime(df['date']).values.astype(np.int64) // 10 ** 6
    full_path = csv_file.split(' ~ ')
    path = pathlib.PurePath(full_path[0])
    
    total_seconds = ((time.time() - start_time))
    # print("list 9 ", df_tall)
    print("9 title", fin_metric_title)
    df_table_html = df_tall[['{}'.format(fin_metric_title)]].iloc[::-1].transpose().to_html()#.replace("\n","")
    present_num = magnitude_num(int(latest_metric),currency_symbol)
    print("last title 2", fin_metric_title, "list now ",list(df))
    print("last ", list(df["{}".format(fin_metric_title)])[-1])
    latest_metric = "${}".format(list(df["{}".format(fin_metric_title)])[0])
    print("latest_num 2", df['date'].to_list(),"present_num 2", present_num)
    print("Nothing took {} seconds".format(time.time() - start_time))
    labels = list(df['date'])
    print("df json", df[['date',"{}".format(fin_metric_title)]].to_numpy().tolist())
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
                            company_industries = profiles_dict['Industries'],\
                            company_similar = profiles_dict['Similar Companies'],\
                            historical_pct_chg = historical_pct_chg,\
                            lifetime_sum_all_metric = lifetime_sum_all_metric,\
                            mean_str = mean_str,\
                            max_str = max_str,\
                            min_str = min_str,\
                            std_dev_str = std_dev_str,\
                            std_dev_abs_str = std_dev_abs_str,\
                            bottom_25_str = bottom_25_str,\
                            top_25_str = top_25_str,\
                            earliest_year = earliest_year,\
                            latest_year = latest_year,\
                            earliest_metric = earliest_metric,\
                            latest_metric = latest_metric,\
                            present_num = present_num,\
                            max_min_pct_diff_str = max_min_pct_diff_str, df_bs_table_html = [df_table_html],df_html_tall = [df_html_tall],fin_metric_name = fin_metric_title,\
                            df_date = df['date'].to_list(),\
                            # df_rev = df["{}".format(fin_metric_name)].to_list(),\
                            df_json  =df[['date',"{}".format(fin_metric_title)]].to_numpy().tolist(),\
                            table_pct = [df_pct],\
                            tables=[df_html],\
                            titles=df.columns.values,\
                            total_time=total_seconds,\
                            place_name=url_symbol,\
                            max=17000,\
                            labels=labels,\
                            annual_pct_chg = annual_pct_chg,\
                            # values=values
                            )


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