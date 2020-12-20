import os
import sqlite3
import pandas as pd
import glob
import pathlib
import time
import sys
from inspect import currentframe, getframeinfo
pyfile = getframeinfo(currentframe()) 
sys.path.append(os.path.join(os.path.dirname(__file__)))
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
from string import Template
charts = Blueprint('charts', __name__)
@charts.route('/', methods=['POST', 'GET'])
@charts.route("/home")
def index():
    return render_template('index.html')
@charts.route('/<url_symbol>-<stock_or_etf>/<url_name>/<statement_or_ratio>/<url_fin_metric>', methods=['POST', 'GET']) 
def current_ratio(url_fin_metric,stock_or_etf,url_name,statement_or_ratio,url_symbol): 
    from route_imports.ratio_map import metric_to_url_map 
    from route_imports.ratio_map import url_to_var_name_map
    from route_imports.ratio_map import url_to_name_map
    from route_imports.ratio_map import fin_statement_raw_names
    from route_imports.ratio_map import fin_statement_renamed_cols
    from route_imports.ratio_map import metric_to_formula_map
    from route_imports.ratio_map import url_to_metric_map
    start_time = time.time()
    titles_list = ['Date','Symbol','Filing Date','Accepted Date','Period','SEC Filing Link']
    def magnitude_num(number, currency_symbol):
        if len(str(number)) > 9 and number > 1000000000:
            magnitude = number/1000000000
            magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),"B")
        elif len(str(number)) > 6 and number > 1000000:
            magnitude = number/1000000
            magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),"M")
        elif len(str(number)) > 3 and number > 1000:
            magnitude = number/1000
            magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),"K")
        elif -1000 <= number <= 1000:
            magnitude = number
            magnitude_str = "{}{}{}".format("",round(magnitude,2),"")
        elif len(str(number)) > 9 and number < -1000000000:
            magnitude = abs(number/1000000000)
            magnitude_str = "-{}{}{}".format(currency_symbol,round(magnitude,1),"B")
        elif len(str(number)) > 6 and number < -1000000:
            magnitude = abs(number/1000000)
            magnitude_str = "-{}{}{}".format(currency_symbol,round(magnitude,1),"M")
        elif len(str(number)) > 3 and number < -1000:
            magnitude = abs(number/1000)
            magnitude_str = "-{}{}{}".format(currency_symbol,round(magnitude,1),"K")
        else:
            magnitude = number
            magnitude_str = "{}{}{}".format("",round(magnitude,2),"")
        return magnitude_str
    fin_statements_list = ["balance-sheet","income-statement","cash-flow-statement"]
    company_profiles = pd.read_csv("reference_data/Company_Profiles.csv")
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
    for n, profiles_col in enumerate(company_profiles_col):
        key = profiles_col
        value = profiles_value[n]
        profiles_dict[key] = value
    chars_to_remove = ["'","[","]"]
    for character in chars_to_remove:
        profiles_dict['Industries'] = profiles_dict['Industries'].replace(character, "")
        profiles_dict['Similar Companies'] = profiles_dict['Similar Companies'].replace(character, "")
    if "{}".format(statement_or_ratio) in fin_statements_list:
        fin_statements_matching = pd.read_csv("reference_data/Financial_Statements_Reference_Matching.csv")
        titles_cf = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Cash Flow Statement"]['Title'])
        titles_is = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Income Statement"]['Title'])
        urls_bs = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Balance Sheet"]['URL'])
        urls_cf = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Cash Flow Statement"]['URL'])
        urls_is = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="Income Statement"]['URL'])
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
        year_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/{}/*~{}~*".format(fin_statement_dir, url_symbol.upper()))[-1]
        df = pd.read_csv(csv_file) 
        
        df["Year"] = df["date"].apply(lambda x: x[0:4])
        df["QQ-YYYY"] = df["period"]+"-"+df["date"].apply(lambda x: x[0:4])
        matching_row = fin_statements_matching[fin_statements_matching['URL']=="{}".format(url_fin_metric)]
        fin_metric_title = list(matching_row['Title'])[0]
        fin_metric_name = list(matching_row['Name'])[0]

        ignore_periods = df["{}".format(fin_metric_name)].values.searchsorted(0, side='right')
        df = df[0:ignore_periods]
        df = df[0:][::-1]#.iloc[::-1]
        # df = df.dropna(subset=["{}".format(fin_metric_name)]) 
        # df = df[df["{}".format(fin_metric_name)] != 0]
        year_df = df.groupby("Year").sum()
        sorted_metric = year_df["{}".format(fin_metric_name)].sort_values()
        lifetime_sum_all_metric = df["{}".format(fin_metric_name)].sum()
        lifetime_sum_all_metric = magnitude_num(lifetime_sum_all_metric,currency_symbol)
    else:
        currency_symbol = ""
        fin_dir = ["Income Statement","Balance Sheet","Cash Flow Statement"]
        fin_df_list = []
        for x in fin_dir:
            fin_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/quarter/{}/*~{}~*".format(x, url_symbol.upper()))[-1]
            fin_df = pd.read_csv(fin_file)
            fin_df["Year"] = fin_df["date"].apply(lambda x: x[0:4])
            fin_df["QQ-YYYY"] = fin_df["period"]+"-"+fin_df["date"].apply(lambda x: x[0:4])
            fin_df_list.append(fin_df)
        df_merge_is_bs = pd.merge(fin_df_list[0],fin_df_list[1],how="inner", on="QQ-YYYY")
        df_merge = pd.merge(df_merge_is_bs,fin_df_list[2],how="inner", on="QQ-YYYY")
        df_merge = df_merge[fin_statement_raw_names]
        df_merge.columns = fin_statement_renamed_cols
        df = df_merge.iloc[::-1]
        
        df['ffo_math']=df['net_income'] + df['d_n_a'] + df['sales_maturities_of_investments'] + df['purchase_of_investments'] + df['investments_in_pp_n_e'] + df['acquisitions_net']
        df['book_value_math']=df['total_assets'].dropna()-df['total_liabilities'].dropna()
        df['ebit_math']=df['ebitda_non'] - df['d_n_a']
        df['working_capital_math']= df['total_current_assets'] - df['total_current_liabilities']
        df['quick_assets_math']=df['cash_non']+df['short_term_investments']+df['accounts_receivable']
        df['quick_ratio_math']=df['total_current_assets'] - df['inventory']
        metric_name = url_to_metric_map["{}".format(url_fin_metric)]
        fin_metric_title = url_to_name_map[url_fin_metric] 
        fin_metric_name = url_to_var_name_map[url_fin_metric] 
        metric_history = metric_to_formula_map(df,metric_name)
        fin_metric_history = metric_history
        print("!!!,", df['{}'.format(fin_metric_name)])
        lifetime_sum_all_metric = ""
        lifetime_sum_all_metric = ""
        df = df
        df["{}".format(fin_metric_name)] = metric_history
        year_df = df.groupby("Year").sum()
        year_metric = metric_to_formula_map(df,metric_name)
        sorted_metric = metric_history.sort_values(ascending=True)
    quarters = round(len(sorted_metric)/4)
    bottom_25 =  np.percentile(sorted_metric, 25)
    top_25 =  np.percentile(sorted_metric, 75)
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
    latest_year = list((df['date'].astype(str).str[0:4]))[-1]    
    earliest_metric = list(df["{}".format(fin_metric_name)])[0]
    latest_metric = list(df["{}".format(fin_metric_name)])[-1]

    try:
        pct_chg = (latest_metric/earliest_metric)
        historical_pct_chg = str(round(pct_chg, 1))
        annual_pct_chg  = round((latest_metric/earliest_metric)/2,2)        
        if pct_chg>=0:
            hist_pct_chg_str = "{}x".format(historical_pct_chg)
            annual_pct_chg_str = "{}%".format(annual_pct_chg)
        elif pct_chg<0:
            hist_pct_chg_str = "{}x".format(historical_pct_chg)
            annual_pct_chg_str = "{}%".format(annual_pct_chg)
        else:
            hist_pct_chg_str = ""
            annual_pct_chg_str = ""
        historical_pct_chg = hist_pct_chg_str
        annual_pct_chg = annual_pct_chg_str
    except:
        pct_chg = "-"
        historical_pct_chg = "-"
        annual_pct_chg = "-"


    max_min_pct_diff = ((max_metric-min_metric)/min_metric)
    if max_min_pct_diff>=0:
        max_min_pct_diff_str = "+{}%".format(round(max_min_pct_diff)*100,1)
    elif max_min_pct_diff<0:
        max_min_pct_diff_str = "-{}%".format(round(max_min_pct_diff)*100,1)
    else:
        max_min_pct_diff_str = ""
    df_quarter = df['period']
    
    df = df.drop(['Quarter & Year', 'Unnamed: 0','symbol','fillingDate','acceptedDate','period','link'],axis=1, errors='ignore')
    try:
        for x in reversed(titles_bs):
            if x in titles_list:
                titles_bs.remove(x)
        titles_bs.append('Year')
        titles_bs.append('QQ-YYYY')
    except:
        pass
    try:
        print("cols",cols)
        print("df",list(df))
        titles_bs.insert(0,"date")
        try:
            titles_bs.remove("Quarter & Year")
        except:
            pass
        
        df.columns = titles_bs
        df = df[cols]
        
        fin_metric_history = df['{}'.format(fin_metric_title)]
    except Exception as e:
        print(e)
    df = df
    df['Quarter & Year'] = df_quarter+"-"+df['date'].apply(lambda x: str(x)[0:4])
    df.index = df['Quarter & Year']
    million = 1000000
    billion = 1000000000
    if list(fin_metric_history)[0]  > billion:
        pass
    elif list(fin_metric_history)[0]  > million:
        pass
    else:
        pass
    df_pct_chg = df
    pct_chg_cols = (df.select_dtypes(include=['number']).pct_change(-1))
    df_pct_chg_str = df_pct_chg.drop(list(pct_chg_cols), axis=1)
    df_pct_chg = df_pct_chg_str.join(pct_chg_cols)[list(df)]
    pd.set_option('display.float_format', '{:.2f}'.format)
    df_pct_chg_t = df_pct_chg.transpose()
    df_pct_chg_t.columns = list(df_pct_chg['Quarter & Year'])
    df_pct_chg_t = df_pct_chg.transpose()
    df_pct_chg_t.columns = list(df_pct_chg['Quarter & Year'])
    df_pct_chg_t['']=df_pct_chg_t.index
    df_pct_chg_t.index = range(len(df_pct_chg_t))
    cols = list(df_pct_chg_t.columns)
    cols = [cols[-1]] + cols[:-1]
    df_t = df.transpose()
    df_t.columns = list(df['Quarter & Year'])
    df_t = df_t
    df_t['']=df_t.index
    df_t.index = range(len(df_t))
    cols = list(df_t.columns)
    cols = [cols[-1]] + cols
    df_pct = df_pct_chg_t.to_html().replace('<table','<table class="df_tableBoot" id="df_myTable1"')
    cols = [cols[-1]] + cols
    def isnumber(x):
        try:
            float(x)
            return True
        except:
            return False
    df_n = df[df.applymap(isnumber)]
    df_n_sum = pd.DataFrame(df_n.sum())
    df_n_sum[df_n_sum == 0] = ""
    new_header = df_n_sum.iloc[0] 
    df_n_sum = df_n_sum
    df_n_sum.columns = new_header 
    df_n_sum.index = range(len(df_n_sum))
    df_t = pd.merge(df_n_sum, df_t, left_index=True, right_index=True,suffixes=('Total: {} - {}'.format(latest_year,earliest_year), 'Line Items'))
    df_t = df_t
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

    df_tall = df

    if "{}".format(statement_or_ratio) in fin_statements_list:
        df_tall['pct_chg'] = df_tall['{}'.format(fin_metric_title)].pct_change()
        print(list(df_tall['{}'.format(fin_metric_title)]))
        df_html_tall = df_tall[['{}'.format('Quarter & Year'),'{}'.format(fin_metric_title),'pct_chg']].to_html(index=False)

        full_path = csv_file.split(' ~ ')
        path = pathlib.PurePath(full_path[0])
    else:
        df_html_tall = df_tall[['{}'.format('Quarter & Year'),'{}'.format(fin_metric_name)]].to_html(index=False)
    df_html_tall = df_html_tall.replace('border="1" class="dataframe">','class="abc" id="df_myTable" border="1" class="dataframe">')
    # df_html_tall = df_html_tall.replace('inf','class="abc" id="df_myTable" border="1" class="dataframe">')

    df_html_tall = df_html_tall.replace("\n","")
    df_html_tall = df_html_tall.replace("{}".format("["),"")
    df_html_tall = df_html_tall 

    df_html_tall = df_html_tall.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
    df_html_tall = df_html_tall.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
    df_html_tall = df_html_tall.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')
    df_html_tall = df_html_tall[0:].replace(">nan</td>",">-</td>")
    df_html = df_html.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
    df_html = df_html.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
    df_html = df_html.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')
    df['date'] = pd.to_datetime(df['date']).values.astype(np.int64) // 10 ** 6
    total_seconds = ((time.time() - start_time))
    present_num = magnitude_num(int(latest_metric),currency_symbol)
    labels = list(df['date'])
    if "{}".format(statement_or_ratio) in fin_statements_list:
        df_table_html = df_tall[['{}'.format(fin_metric_title)]].iloc[::-1].transpose().to_html()
        df['quarter avg'] = df["{}".format(fin_metric_title)].rolling(4,min_periods=1).mean()
        latest_metric = "${}".format(list(df["{}".format(fin_metric_title)])[0])
    else:
        df_table_html = df_tall[['{}'.format(fin_metric_name)]].iloc[::-1].transpose().to_html()
        df['quarter avg'] = df["{}".format(fin_metric_name)].rolling(4,min_periods=1).mean()
        latest_metric = "${}".format(list(df["{}".format(fin_metric_name)])[0])
    df_table_html = df_table_html

    df_json  =np.nan_to_num(df[['date',"{}".format("quarter avg")]].to_numpy()).tolist()

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

                            df_json  = df_json,\
                            table_pct = [df_pct],\
                            tables=[df_html],\
                            titles=df.columns.values,\
                            total_time=total_seconds,\
                            place_name=url_symbol,\
                            max=17000,\
                            labels=labels,\
                            annual_pct_chg = annual_pct_chg,\
                            
                            )
@charts.route('/test/<url_symbol>', methods=['POST', 'GET'])

def fin_test(url_symbol):
    
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