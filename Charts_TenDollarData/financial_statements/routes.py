# pyright: reportUnusedVariable=false, reportUnusedImport=false
# https://github.com/microsoft/pylance-release/blob/main/DIAGNOSTIC_SEVERITY_RULES.md
# https://damyan.blog/post/flask-series-optimizations/
# https://github.com/muatik/flask-profiler
domain = "https://chartsonlygoup.com"
subdomain = "http://chartsonlygoup.com"
import os
import sqlite3
import pandas as pd
import glob
import pathlib
import time
import sys
from vprof import runner
# http://pramodkumbhar.com/2019/05/summary-of-python-profiling-tools-part-i/
# https://stackoverflow.com/questions/30165475/how-to-compress-minimize-size-of-json-jsonify-with-flask-in-python/30165707
# TODO compress JSON
# from flask import Flask, Response
# from gevent.pywsgi import WSGIServer 
# from gevent import monkey
# # need to patch sockets to make requests async
# # you may also need to call this before importing other packages that setup ssl
# monkey.patch_all()
import gzip
from io import BytesIO
from flask import request
# https://stackoverflow.com/questions/30165475/how-to-compress-minimize-size-of-json-jsonify-with-flask-in-python/30165707
# class GzipCompress:
    # def __init__(self, app, compress_level=9, minimum_size=100):
    #     self.app = app
    #     self.compress_level = compress_level
    #     self.minimum_size = minimum_size
    #     self.app.after_request(self.after_request)
    # def after_request(self, response):
    #     accept_encoding = request.headers.get('Accept-Encoding', '')
    #     if response.status_code < 200 or \
    #        response.status_code >= 300 or \
    #        response.direct_passthrough or \
    #        len(response.get_data()) < self.minimum_size or \
    #        'gzip' not in accept_encoding.lower() or \
    #        'Content-Encoding' in response.headers:
    #         return response
    #     gzip_buffer = BytesIO()
    #     gzip_file = gzip.GzipFile(mode='wb',
    #                               compresslevel=self.compress_level,
    #                               fileobj=gzip_buffer)
    #     gzip_file.write(response.get_data())
    #     gzip_file.close()
    #     response.set_data(gzip_buffer.getvalue())
    #     response.headers['Content-Encoding'] = 'gzip'
    #     response.headers['Content-Length'] = len(response.get_data())
    #     return response
from inspect import currentframe, getframeinfo
frameinfo = getframeinfo(currentframe())
def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno
# print(get_linenumber())
sys.path.append(os.path.join(os.path.dirname(__file__)))
from functions.pandas_extraction import FS
import numpy as np
import functools
from datetime import datetime
from string import Template
# from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import logging
from flask import render_template_string,request, session, g, redirect, url_for, abort, render_template, flash, Blueprint
cache = Cache()
from string import Template
from datetime import datetime
charts = Blueprint('charts', __name__)
# @charts.route('/', methods=['POST', 'GET'])
# @charts.route("/home")
# def index():
#     return render_template('index.html')
import linecache
import inspect
# import d6tstack
from inspect import currentframe, getframeinfo
from flask import Markup

from flask import send_from_directory     

@charts.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(charts.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def magnitude_num(number, currency_symbol, fixed=1, scale=1, trillion=1):
        try:
            if len(str(number)) > 9 and number > 1000000000:
                if fixed == 1:
                    magnitude = number/1000000000
                    scale = "B"
                else:
                    magnitude = number/fixed
                    
                magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),scale)
            elif len(str(number)) > 6 and number > 1000000:
                if fixed == 1:
                    magnitude = number/1000000
                    scale = "M"
                else:
                    magnitude = number/fixed
                
                magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),scale)
            elif len(str(number)) > 3 and number > 1000:
                if fixed == 1:
                    magnitude = number/1000
                    scale = "K"
                else:
                    magnitude = number/fixed
                magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),scale)
            elif -1000 <= number <= 1000:
                magnitude = number
                magnitude_str = "{}{}{}".format("",round(magnitude,2),"")
            elif len(str(number)) > 9 and number < -1000000000:
                if fixed == 1:
                    magnitude = abs(number/1000000000)
                    scale = "B"
                else:
                    magnitude = abs(number/fixed)
                magnitude_str = "-{}{}{}".format(currency_symbol,round(magnitude,1),scale)
            elif len(str(number)) > 6 and number < -1000000:
                if fixed == 1:
                    magnitude = abs(number/1000000)
                    scale = "M"
                else:
                    magnitude = abs(number/fixed)
                magnitude_str = "-{}{}{}".format(currency_symbol,round(magnitude,1),scale)
            elif len(str(number)) > 3 and number < -1000:
                if fixed == 1:
                    magnitude = abs(number/1000)
                    scale = "K"
                else:
                    magnitude = abs(number/fixed)
                magnitude_str = "-{}{}{}".format(currency_symbol,round(magnitude,1)," T")
            else:
                magnitude = number
                magnitude_str = "{}{}{}".format("",round(magnitude,2),"")
            if trillion==1:
                if len(str(number)) > 12 and number > 1000000000000:
                    if fixed == 1:
                        magnitude = number/1000000000000
                        scale = "T"
                    else:
                        magnitude = number/fixed
                    magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),scale)
            else:
                pass
        except Exception as e:
            magnitude = number
            magnitude_str = number
        return magnitude_str
def change_markup(change,percent_or_x,arrow_no_arrow = "arrow", css_class = "change_markup",sign="yes",markup=1):
        try:
            if arrow_no_arrow == "arrow":
                up_green_prefix = '<span class="up_green {}">'.format(css_class)
                up_green_suffix = ' <i class="material-icons">arrow_upward</i></span>'
                down_red_prefix = '<span class="down_red {}">'.format(css_class)
                down_red_suffix = ' <i class="material-icons">arrow_downward</i></span>'
            else:
                up_green_prefix = '<span class="up_green {}">'.format(css_class)
                up_green_suffix = '</span>'
                down_red_prefix = '<span class="down_red" {}>'.format(css_class)
                down_red_suffix = '</span>'
            if change > 100:
                change = int(change)
            elif change > 10:
                change = np.round(change,1)
            elif change > -10:
                change = np.round(change,2)
            elif change <= -10:
                change = np.round(change,1)
            elif change <= -100:
                change = int(change)
            change_comma =  "{:,}".format(change)
            if percent_or_x == "percent":
                if change==0:
                    change_html = "0%"
                elif change>0:
                    if sign=="yes":
                        if markup==1:
                            change_html = Markup("{}+{}%{}".format(up_green_prefix, change_comma, up_green_suffix))
                        else:
                            change_html = ("{}+{}%{}".format(up_green_prefix, change_comma, up_green_suffix))
                    else:
                        if markup==1:
                            change_html = Markup("{}{}%{}".format(up_green_prefix, change_comma, up_green_suffix))
                        else:
                            change_html = ("{}{}%{}".format(up_green_prefix, change_comma, up_green_suffix))
                elif change<0:
                    if markup==1:
                        change_html = Markup("{}{}%{}".format(down_red_prefix, change_comma, down_red_suffix))
                    else:
                        change_html = ("{}{}%{}".format(down_red_prefix, change_comma, down_red_suffix))
                else:
                    change_html = "-"
            elif percent_or_x == "x":
                if change==0:
                    change_html = "0%"
                elif change>0:
                    if sign=="yes":
                        if markup==1:
                            change_html = Markup("{}+{}x{}".format(up_green_prefix, change, up_green_suffix))
                        else:
                            change_html = ("{}+{}x{}".format(up_green_prefix, change, up_green_suffix))
                    else:
                        if markup==1:
                            change_html = Markup("{}{}x{}".format(up_green_prefix, change, up_green_suffix))
                        else:
                            change_html = ("{}{}x{}".format(up_green_prefix, change, up_green_suffix))
                elif change<0:
                    if markup==1:
                        change_html = Markup("{}{}x{}".format(down_red_prefix, change, down_red_suffix))
                    else:
                        change_html = ("{}{}x{}".format(down_red_prefix, change, down_red_suffix))
                else:
                    change_html = "-"
            else:
                change_html = '-'
        except Exception as e:
            change_html = '-'
        return change_html
def PrintException():
    callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    error_function = info.function
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
#     line = linecache.getline(filename, lineno, f.f_globals,error_function)
    line = linecache.getline(filename, lineno,error_function)
    print("exception!", lineno, line.strip(), exc_obj)
    return(lineno, line.strip(), exc_obj,)
# import markdown
# @charts.route('/mcap', methods=['POST', 'GET'])
@charts.route('/')
def market_caps_table():
    global domain
    global subdomain
    df = pd.read_csv("reference_data/homepage_final.csv")
    df_html = pd.read_csv("reference_data/homepage_final.csv")
    #.to_html().replace('border="1" class="dataframe">','class="df_tableBoot" id="df_myTable" border="1" class="dataframe"><colgroup>{}</colgroup>'.format(col_list_str))
    # df_html['Market Cap'] = df_html.apply(lambda x: magnitude_num(x['marketCap'],"$"), axis=1)#.head(30)
    # df_html['Market Cap'] = df_html.apply(lambda x: int(x['marketCap']), axis=1)#.head(30)
    sum_mcap = sum(df_html['marketCap']) #('${:,.0f}'.format)
    sum_01d_vol = sum(df_html['price'] * df_html['volume'])
    sum_90d_vol = sum(df_html['price'] * df_html['avgVolume'])
    dominance_top_10 = sum(df_html['marketCap'][0:10])
    dominance_top_10_pct = 100*dominance_top_10/sum_mcap
    sum_mcapx = magnitude_num(sum_mcap,"$") #f'${sum_mcap:,.0f}'
    sum_01d_volx = magnitude_num(sum_01d_vol,"$") #f'${sum_01d_vol:,.0f}'
    sum_90d_volx = magnitude_num(sum_90d_vol,"$") #f'${sum_90d_vol:,.0f}'
    dominance_top_10x = magnitude_num(dominance_top_10,"$") #f'${dominance_top_10:,.0f}'
    dominance_top_10_pctx = "{}{}".format(np.round(dominance_top_10_pct,2),"%")
    # df_html['Market Cap ($MM)'] = df_html['marketCap']/1000000000
    # df_html['Market Cap ($MM)'] = df_html.apply(lambda x: x['marketCap']/1000000, axis=1)
    # df_html['Name'] = df_html.apply(lambda x: Markup('<div class="mcap_symbol">'+x['symbol']+'</div> <div class="mcap_name">'+x['name']+"</div>"),axis=1)
    # df_html['Name'] = df_html.apply(lambda x: ('<div class="mcap_symbol">'+x['symbol']+'</div> <div class="mcap_name">'+x['name']+"</div>"),axis=1)
    # img data-original -→ img-src. using deferRender, so lazyloading not needed.
    df_html['name'] = df_html.apply(lambda x: ('<a class="mcap_link" href="{}/{}"><table class="mini_table"><thead class="mini_thead"><tr class="mini_tr"><th class="mcap_image"  rowspan="2"><img class="lazy"  src="{}/static/img/images-stocks/{}.png" width="30" height="30"></th><th class="mcap_symbol">'.format(domain, x['symbol'].lower(),domain, x['symbol'].upper())+x['symbol'].upper()+'</th></tr><tr class="mini_tr2"><td class="mcap_name">' +x['name']+'</td></tr></thead></table></a>'),axis=1)
    # df_html['symbol'] = df_html.apply(lambda x: ('<i class="material-icons icon_brand">show_chart</i>'+'<br/>'+x['symbol']+""),axis=1)
    # df_html['Avg $ Vol'] = df_html.apply(lambda x: "{}".format(magnitude_num(x['avgVolume']*x['price'],"$")), axis=1)

    # df_html['90D $ Vol'] = df_html['price']*df_html['avgVolume']
    # df_html['90D $ Vol'] = df_html['90D $ Vol'].apply(lambda x: float(magnitude_num(x,"",fixed=1000000, scale="")))

    # df_html['90D $ Vol'] = df_html['90D $ Vol'].map('${:,.0f}M'.format)
    # df_html['24H $ Vol'] = df_html['price']*df_html['volume']
    # df_html['24H $ Vol'] = df_html['24H $ Vol'].apply(lambda x: float(magnitude_num(x,"",fixed=1000000, scale="")))
    # df_html['24H $ Vol'] = df_html['24H $ Vol'].map('${:,.0f}M'.format)



    df_html['90D $ Vol'] = df_html['price']*df_html['avgVolume']
    df_html['90D $ Vol'] = df_html['90D $ Vol'].map('${:,.0f}'.format)
    df_html['24H $ Vol'] = df_html['price']*df_html['volume']
    df_html['24H $ Vol'] = df_html['24H $ Vol'].map('${:,.0f}'.format)

    df_html['90D $ Vol'] = df_html['price']*df_html['avgVolume']
    df_html['24H $ Vol'] = df_html['price']*df_html['volume']
    df_html['24H $ Vol'] = df_html['24H $ Vol'].apply(lambda x: (magnitude_num(x,"$")))
    df_html['90D $ Vol'] = df_html['90D $ Vol'].apply(lambda x: (magnitude_num(x,"$")))
    
    
    # df_html['24H $ Vol'] = df_html['24H $ Vol'].apply(lambda x: ('<td data-sort="'+str(x)+'"><span class="vol_24">'+str(x)+'</span>'))
    # df_html['90D $ Vol'] = df_html['90D $ Vol'].apply(lambda x: ('<td data-sort="'+str(x)+'"><span class="vol_90">'+str(x)+'</span>'))


    df_html['24H $ Vol'] = df_html.apply(lambda x: ('<td data-sort="'+str(x['price']*x['volume'])+'"><span class="vol_24">'+str(magnitude_num(x['price']*x['volume'],"$"))+'</span>'),axis=1)
    df_html['90D $ Vol'] = df_html.apply(lambda x: ('<td data-sort="'+str(x['price']*x['avgVolume'])+'"><span class="vol_24">'+str(magnitude_num(x['price']*x['avgVolume'],"$"))+'</span>'),axis=1)

    # df_html['24H $ Vol'] = df_html.apply(lambda x: ('<td data-sort="'+str(x['price']*x['volume'])+'"><span class="vol_24">'+str(magnitude_num(x['price']*x['volume'],"$"))+'</span>'+'<br class="shares_out_br"><span class="mcap_shares_vol">' + str(x['volume']) +" " + str(x['symbol'])+"</span>"),axis=1)
    # df_html['90D $ Vol'] = df_html.apply(lambda x: ('<td data-sort="'+str(x['price']*x['avgVolume'])+'"><span class="vol_24">'+str(magnitude_num(x['price']*x['avgVolume'],"$"))+'</span>'+'<br class="shares_out_br"><span class="mcap_shares_vol">' + str(x['avgVolume']) +" " + str(x['symbol'])+"</span>"),axis=1)


    df_html['avgVolumex'] = df_html['avgVolume'].map('{:,.0f}'.format)
    df_html['volumex'] = df_html['volume'].map('{:,.0f}'.format)
    # df_html['volume'] = df_html['volume']
    # df_html['volume'] = df_html.apply(lambda x: strx['volume'] + " " + x['symbol'],axis=1)
    #df_html['volume'].map('{:,.0f}'.format) + " shares"


    # df_html['24H $ Vol'] = df_html.apply(lambda x: ('<span class="mcap_dol_vol">'+x['24H $ Vol']+'</span><br/><span class="mcap_shares_vol">' + str(x['volumex']) +" " + str(x['symbol'])+"</span>"),axis=1)
    # df_html['90D $ Vol'] = df_html.apply(lambda x: ('<span class="mcap_dol_vol">'+x['90D $ Vol']+'</span><br/><span class="mcap_shares_vol">' + str(x['avgVolumex']) +" " + str(x['symbol'])+"</span>"),axis=1)
    
    
    # df_html['price'] = df_html.apply(lambda x: Markup("$"+str(np.round(x['price'],2))), axis=1)
    # df_html['price'] = df_html.apply(lambda x: ("$"+str(np.round(x['price'],2))), axis=1)
    # df_html['pe'] = df_html.apply(lambda x: np.round(x['pe'],2), axis=1)
    df_html['pe'] = df_html['pe'].map('{:,.2f}'.format)
    # df_html['% Chg'] = df_html['changesPercentage'].map('{:,.2f}%'.format)
    df_html['% Chg'] = df_html.apply(lambda x: change_markup(x['changesPercentage'],"percent",arrow_no_arrow = "arrow", css_class = "daily_change", sign="no", markup=0), axis=1)#.head(30)
    df_html['% Chg'] = df_html.apply(lambda x: ('<td data-sort="'+str(x['changesPercentage'])+'"><span class="chg_pct">'+change_markup(x['changesPercentage'],"percent",arrow_no_arrow = "arrow", css_class = "daily_change", sign="no", markup=0)+'</span>'),axis=1)

    # df_html['% Chg'] = df_html.apply(lambda x: x['changesPercentage'], axis=1)#change_markup(x['changesPercentage'],"percent",arrow_no_arrow = "arrow", css_class = "daily_change"), axis=1)#.head(30)
    df_html['Shares Outstanding'] = df_html['sharesOutstanding'].map('{:,.0f}'.format)
    # df_html['Shares Outstanding'] = df_html.apply(lambda x: ('<span class="mcap_shares_out">'+str(x['Shares Outstanding'])+'</span><br/><span class="mcap_pct_out">' + str(np.round((100*x['avgVolume']/x['sharesOutstanding']),3)) +"%</span>"),axis=1)
    df_html['Shares Outstanding'] = df_html.apply(lambda x: ('<span class="mcap_shares_out">'+str(x['Shares Outstanding'])+'</span><br/><span class="mcap_pct_out">'+"</span>"),axis=1)
    df_html['price'] = df_html['price'].map('${:,.2f}'.format)
    # df_html['Market Cap'] = df_html['marketCap'].apply(lambda x: float(magnitude_num(x,"",fixed=1000000000, scale="")))
    df_html['Market Cap'] = df_html['marketCap'].apply(lambda x: (magnitude_num(x,"$", trillion=0)))

    # df_html['Market Cap'] = df_html['Market Cap'].map('${:,.1f}B'.format)
    df_html['Market Cap'] = df_html['Market Cap'].apply(lambda x: ('<td data-sort="'+str(x)+'"><span class="mcap_num">'+str(x)+'</span>'))


    # df_html['Market Cap'] = df_html['marketCap'].map('${:,.0f}'.format)
    # df_html['Market Cap'] = df_html['marketCap']#.map('${:,.0f}'.format)


    df_html = df_html[['name','price','% Chg', 'Market Cap','24H $ Vol','90D $ Vol','pe',]][0:150]
    df_html.columns = ['Name', 'Price', '% Chg', 'Market Cap','24H $ Vol', '90D $ Volume','P/E']
    df_html = df_html.to_html(escape=False).replace('<table','<table class="df_tableBoot compact stripe hover cell-border order-column row-border" id="df_myTable"')
    
    df_html = df_html.replace("\n","").replace('<tr style="text-align: right;">','<tr class="tr_header">')
    
    # df_html = df_html.replace("[","")
    # df_html = df_html.replace("_"," ")
    # df_html = df_html.replace('.00','')
    # df_html = df_html.replace('.0','')
    # df_html = df_html.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
    # df_html = df_html.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
    # df_html = df_html.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')
    df_html = df_html[0:].replace(">nan</td>",">-</td>")
    df_html = df_html[0:].replace(">nan%</td>",">-</td>")
    # df_html = df_html[0:].replace("&lt;","<")
    # df_html = df_html[0:].replace("&gt;",">")
    df_html = df_html.replace('td><td data','td data')
    df_html = df_html.replace('td>&lt;td data','td data')
     
    print("dfz_html_printed",df_html)

    
    
    return render_template('market_caps_table.html',\
        df_html = Markup(df_html),
        df_test = list(df),
        sum_mcapx = sum_mcapx,
        sum_01d_volx = sum_01d_volx,
        sum_90d_volx = sum_90d_volx,
        dominance_top_10x = dominance_top_10x,
        dominance_top_10_pctx = dominance_top_10_pctx
    # df_html = [df_html],
        )
# sum_mcapx = f'${sum_mcap:,.0f}'
# sum_01d_volx = f'${sum_01d_vol:,.0f}'
# sum_90d_volx = f'${sum_90d_vol:,.0f}'
# dominance_top_10x = f'${dominance_top_10:,.0f}'
# dominance_top_10_pctx = f'{dominance_top_10_pct:,.2f}'+"%"
# df_html = [df_html.replace('<th class="th_fin_statement_class fin_statement_class">YoY % Change</th>      <th class="th_fin_statement_class fin_statement_class">Stock Price</th>', '<th class="th_fin_statement_class fin_statement_class">YoY % Change{}</th>      <th class="th_fin_statement_class fin_statement_class">Stock Price</th>'.format(min_max_warning))],
@charts.route('/test/<some_place>', methods=['POST', 'GET'])
# @cache.cached(timeout=5)
def fin_test(some_place):
    global domain
    global subdomain
    url_symbol = some_place
    company_profiles = pd.read_csv("reference_data/Company_Profiles.csv")
    currency_symbol = list(company_profiles[company_profiles['symbol']=="{}".format(url_symbol.upper())]['currency symbol'])[0]
    currency_symbol_original = currency_symbol
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
                            'Similar Companies',
                            'shortest name',
                            'url name']
    company_profiles = company_profiles[company_profiles_col]
    profiles_dict = {}
    profiles_value = company_profiles[company_profiles['symbol']=="{}".format(url_symbol.upper())].values.tolist()[0]
    for n, profiles_col in enumerate(company_profiles_col):
        key = profiles_col
        value = profiles_value[n]
        profiles_dict[key] = value
    chars_to_remove = ["'","[","]"]
    try:
        for character in chars_to_remove:
            profiles_dict['Industries'] = profiles_dict['Industries'].replace(character, "")
            profiles_dict['Similar Companies'] = profiles_dict['Similar Companies'].replace(character, "")
    except:
        pass
    fin_paper = FS("IS",some_place)
    # tables=fin_paper.df_values()['df_table']
    balance_sheet=FS("BS",some_place).df_table()
    cash_flow=FS("CF",some_place).df_table()
    income_statement=FS("IS",some_place).df_table()
    # table_pct = fin_paper.df_values()['df_table_pct']
    # table_pct = fin_paper.df_table_pct()
    fin_paper_values = fin_paper.df_values()
    # df_date = fin_paper_values['chart_x_dates'],
    # df_rev = fin_paper_values['chart_y_revenue']
    df_json = fin_paper_values['df_json']
    # titles = fin_paper_values['df_titles']
    # labels = fin_paper.df_labels()
    #  values=FS("BS","AAPL").df_price()
    values = fin_paper_values['df_close']
    place_name=some_place
    max=17000
    try:
        split_input = profiles_dict['description'].split(".")
        pass_index = -100
        sentence_list = []
        for n,x in enumerate(split_input):
            # print(pass_index)
            if pass_index == n+1:
                pass
            else:
                if (len(x))<30:
                    try:
                        sentence = x+split_input[n+1]+"."
                    except:
                        sentence = x+"."
                    pass_index = n+1
                    sentence = ("<li span='description_list'>{}</li>".format(sentence))
                    sentence_list.append(sentence)
                else:
                    sentence = x+"."
                    sentence = ("<li span='description_list'>{}</li>".format(sentence))
                    sentence_list.append(sentence)
            # print(n,sentence)
        sentences_list_joined = Markup("".join(sentence_list[:-1]))
        html_sentence_list = sentences_list_joined #Markup("<ul>"+sentences_list_joined+"</ul>")
    except:
        sentence = profiles_dict['description']
        sentence = ("<li span='description_list'>{}</li>".format(sentence))
        html_sentence_list = Markup(sentence)
    # print("this", html_sentence_list)
    company_long_name = profiles_dict['long name']
    company_symbol = profiles_dict['symbol']
    # df_image_name = Markup('<a class="mcap_link" href="{}/{}"><table class="mini_table"><thead class="mini_thead"><tr class="mini_tr"><th class="mcap_image"  rowspan="2"><img class="lazy" src="{}/static/img/images-stocks/{}.png" width="30" height="30"></th><th class="mcap_symbol">'.format(domain, company_symbol, domain,company_symbol)+company_symbol+'</th></tr><tr class="mini_tr2"><td class="mcap_name">' +company_long_name+'</td></tr></thead></table></a>')
    df_image_name = Markup('<a class="mcap_link" href="{}/{}"><img class="lazy" src="{}/static/img/images-stocks/{}.png" width="40" height="40">'.format(domain, company_symbol.lower(), domain,company_symbol)+'</a>')
    # values = list(FS("IS","AAPL")['Beginning Price'])[0:19]
    try:
        company_similar = profiles_dict['Similar Companies'].split(",")
        company_similar = [ x for x in company_similar if "XL" not in x ]
        company_similar_list = []
        n = 0
        while n < len(company_similar):
            x = company_similar[n]
            # company_similar_x = ('<a class="similar_companies_urls" href="{}/{}-{}/{}/{}/{}">{}</a>, '.format(subdomain,x.lower().strip(),stock_or_etf,url_name,statement_or_ratio,url_fin_metric,x))
            company_similar_x = ('<a class="similar_companies_urls" href="{}/{}-{}/{}/{}/{}">{}</a>, '.format(subdomain,x.lower().strip(),stock_or_etf,url_name,statement_or_ratio,url_fin_metric,x))
            company_similar_img = ('<a class="similar_companies_urls" href="{}/{}-{}/{}/{}/{}">{}</a>, '.format(subdomain,x.lower().strip(),stock_or_etf,url_name,statement_or_ratio,url_fin_metric,x))
            company_similar_list.append(company_similar_x)
            n+=1
        # company_similar_paragraph = Markup(''.join(company_similar_list)[:-2])
        company_similar_paragraph = Markup('<table class="tg"> <thead> <tr>',''.join(company_similar_list)[:-2],"</tr></thead><tbody><tr>")
    except Exception as e:
        company_similar_paragraph = ''
    return render_template('symbol_main_page.html',
    # return render_template('fin_statements_bootstrapped.html',
    # return render_template('fin_statements_bootstrapped_w_comments.html',
    # FS("IS","AAPL").df_values()['df_table']
    # FS("IS","AAPL").df_values()['df_table_pct']
    # FS("IS","AAPL").df_values()['chart_x_dates']
    # FS("IS","AAPL").df_values()['chart_y_revenue']
    # FS("IS","AAPL").df_values()['df_json']
    # FS("IS","AAPL").df_values()['df_titles']
    #  tables=FS("IS","AAPL").df_values()['df_table'],
    #  table_pct = FS("IS","AAPL").df_values()['df_table_pct'],
    #  df_date = FS("IS","AAPL").df_values()['chart_x_dates'],
    #  df_rev = FS("IS","AAPL").df_values()['chart_y_revenue'],
     df_json = FS("IS","AAPL").df_values()['df_json'],
     df_image_name = df_image_name,\
    #  titles=FS("IS","AAPL").df_values()['df_titles'],
    #  labels = FS("IS","AAPL").df_labels(),
    #  values=FS("IS","AAPL").df_price(),
    #  place_name=some_place, max=17000,
    company_long_name = profiles_dict['long name'],\
    company_currency = profiles_dict['currency'],\
    currency_symbol = currency_symbol,\
    company_exchange = profiles_dict['exchange'],\
    company_industry = profiles_dict['industry'],\
    company_description = profiles_dict['description'],\
    company_sector = profiles_dict['sector'],\
    company_country = profiles_dict['country'],\
    company_ipo_date = profiles_dict['ipo date'],\
    company_short_name = profiles_dict['shortest name'],
    company_industries = profiles_dict['Industries'],\
    company_url_name = profiles_dict['url name'],\
    company_similar = company_similar_paragraph,
    html_sentence_list = html_sentence_list,\
    domain = domain,
    subdomain = subdomain,
    url_symbol = some_place,
    balance_sheet=balance_sheet,
    income_statement = income_statement,
    cash_flow = cash_flow,
    # table_pct = table_pct,
    # df_date = df_date,
    # df_rev = df_rev,
    # df_json = df_json,
    # titles=titles,
    # labels = labels,
    #  values=FS("BS","AAPL").df_price(),
    values=values,
    place_name=some_place,
    max=17000,
    )
@charts.route('/<some_place>/income-statement', methods=['POST', 'GET'])
@charts.route('/<some_place>/income-statement', methods=['POST', 'GET'])
# @cache.cached(timeout=5)
# def fin_test(some_place):
#     global domain
#     global subdomain
#     url_symbol = some_place
#     company_profiles = pd.read_csv("reference_data/Company_Profiles.csv")
#     currency_symbol = list(company_profiles[company_profiles['symbol']=="{}".format(url_symbol.upper())]['currency symbol'])[0]
#     currency_symbol_original = currency_symbol
#     company_profiles_col = ['symbol',
#                             'long name',
#                             'currency',
#                             'exchange',
#                             'industry',
#                             'description',
#                             'sector',
#                             'country',
#                             'ipo date',
#                             'short name',
#                             'Industries',
#                             'Similar Companies',
#                             'shortest name',
#                             'url name']
#     company_profiles = company_profiles[company_profiles_col]
#     profiles_dict = {}
#     profiles_value = company_profiles[company_profiles['symbol']=="{}".format(url_symbol.upper())].values.tolist()[0]
#     for n, profiles_col in enumerate(company_profiles_col):
#         key = profiles_col
#         value = profiles_value[n]
#         profiles_dict[key] = value
#     chars_to_remove = ["'","[","]"]
#     try:
#         for character in chars_to_remove:
#             profiles_dict['Industries'] = profiles_dict['Industries'].replace(character, "")
#             profiles_dict['Similar Companies'] = profiles_dict['Similar Companies'].replace(character, "")
#     except:
#         pass
#     fin_paper = FS("IS",some_place)
#     # tables=fin_paper.df_values()['df_table']
#     balance_sheet=FS("BS",some_place).df_table()
#     cash_flow=FS("CF",some_place).df_table()
#     income_statement=FS("IS",some_place).df_table()
#     # table_pct = fin_paper.df_values()['df_table_pct']
#     # table_pct = fin_paper.df_table_pct()
#     fin_paper_values = fin_paper.df_values()
#     # df_date = fin_paper_values['chart_x_dates'],
#     # df_rev = fin_paper_values['chart_y_revenue']
#     df_json = fin_paper_values['df_json']
#     # titles = fin_paper_values['df_titles']
#     # labels = fin_paper.df_labels()
#     #  values=FS("BS","AAPL").df_price()
#     values = fin_paper_values['df_close']
#     place_name=some_place
#     max=17000
#     try:
#         split_input = profiles_dict['description'].split(".")
#         pass_index = -100
#         sentence_list = []
#         for n,x in enumerate(split_input):
#             # print(pass_index)
#             if pass_index == n+1:
#                 pass
#             else:
#                 if (len(x))<30:
#                     try:
#                         sentence = x+split_input[n+1]+"."
#                     except:
#                         sentence = x+"."
#                     pass_index = n+1
#                     sentence = ("<li span='description_list'>{}</li>".format(sentence))
#                     sentence_list.append(sentence)
#                 else:
#                     sentence = x+"."
#                     sentence = ("<li span='description_list'>{}</li>".format(sentence))
#                     sentence_list.append(sentence)
#             # print(n,sentence)
#         sentences_list_joined = Markup("".join(sentence_list[:-1]))
#         html_sentence_list = sentences_list_joined #Markup("<ul>"+sentences_list_joined+"</ul>")
#     except:
#         sentence = profiles_dict['description']
#         sentence = ("<li span='description_list'>{}</li>".format(sentence))
#         html_sentence_list = Markup(sentence)
#     # print("this", html_sentence_list)
#     company_long_name = profiles_dict['long name']
#     company_symbol = profiles_dict['symbol']
#     # df_image_name = Markup('<a class="mcap_link" href="{}/{}"><table class="mini_table"><thead class="mini_thead"><tr class="mini_tr"><th class="mcap_image"  rowspan="2"><img class="lazy" src="{}/static/img/images-stocks/{}.png" width="30" height="30"></th><th class="mcap_symbol">'.format(domain, company_symbol, domain,company_symbol)+company_symbol+'</th></tr><tr class="mini_tr2"><td class="mcap_name">' +company_long_name+'</td></tr></thead></table></a>')
#     df_image_name = Markup('<a class="mcap_link" href="{}/{}"><img class="lazy" src="{}/static/img/images-stocks/{}.png" width="40" height="40">'.format(domain, company_symbol.lower(), domain,company_symbol)+'</a>')
#     # values = list(FS("IS","AAPL")['Beginning Price'])[0:19]
#     try:
#         company_similar = profiles_dict['Similar Companies'].split(",")
#         company_similar = [ x for x in company_similar if "XL" not in x ]
#         company_similar_list = []
#         n = 0
#         while n < len(company_similar):
#             x = company_similar[n]
#             company_similar_x = ('<a class="similar_companies_urls" href="{}/{}-{}/{}/{}/{}">{}</a>, '.format(subdomain,x.lower().strip(),stock_or_etf,url_name,statement_or_ratio,url_fin_metric,x))
#             company_similar_list.append(company_similar_x)
#             n+=1
#         company_similar_paragraph = Markup(''.join(company_similar_list)[:-2])
#     except Exception as e:
#         company_similar_paragraph = ''
#     return render_template('symbol_main_page.html',
#     # return render_template('fin_statements_bootstrapped.html',
#     # return render_template('fin_statements_bootstrapped_w_comments.html',
#     # FS("IS","AAPL").df_values()['df_table']
#     # FS("IS","AAPL").df_values()['df_table_pct']
#     # FS("IS","AAPL").df_values()['chart_x_dates']
#     # FS("IS","AAPL").df_values()['chart_y_revenue']
#     # FS("IS","AAPL").df_values()['df_json']
#     # FS("IS","AAPL").df_values()['df_titles']
#     #  tables=FS("IS","AAPL").df_values()['df_table'],
#     #  table_pct = FS("IS","AAPL").df_values()['df_table_pct'],
#     #  df_date = FS("IS","AAPL").df_values()['chart_x_dates'],
#     #  df_rev = FS("IS","AAPL").df_values()['chart_y_revenue'],
#      df_json = FS("IS","AAPL").df_values()['df_json'],
#      df_image_name = df_image_name,\
#     #  titles=FS("IS","AAPL").df_values()['df_titles'],
#     #  labels = FS("IS","AAPL").df_labels(),
#     #  values=FS("IS","AAPL").df_price(),
#     #  place_name=some_place, max=17000,
#     company_long_name = profiles_dict['long name'],\
#     company_currency = profiles_dict['currency'],\
#     currency_symbol = currency_symbol,\
#     company_exchange = profiles_dict['exchange'],\
#     company_industry = profiles_dict['industry'],\
#     company_description = profiles_dict['description'],\
#     company_sector = profiles_dict['sector'],\
#     company_country = profiles_dict['country'],\
#     company_ipo_date = profiles_dict['ipo date'],\
#     company_short_name = profiles_dict['shortest name'],
#     company_industries = profiles_dict['Industries'],\
#     company_url_name = profiles_dict['url name'],\
#     company_similar = company_similar_paragraph,
#     html_sentence_list = html_sentence_list,\
#     domain = domain,
#     subdomain = subdomain,
#     url_symbol = some_place,
#     balance_sheet=balance_sheet,
#     income_statement = income_statement,
#     cash_flow = cash_flow,
#     # table_pct = table_pct,
#     # df_date = df_date,
#     # df_rev = df_rev,
#     # df_json = df_json,
#     # titles=titles,
#     # labels = labels,
#     #  values=FS("BS","AAPL").df_price(),
#     values=values,
#     place_name=some_place,
#     max=17000,
#     )
# @charts.route('/<url_symbol>', methods=['POST', 'GET'])
# def hello(url_symbol):
#     # /apple/income-statement/revenue-sales
#     return redirect("{}/{}/income-statement/revenue-sales".format(domain,url_symbol), code=301)
@charts.route("/json")
def json_js_practice():
    return render_template('json_js_practice.html')
# @charts.route("/home")
# @charts.route('/', methods=['POST', 'GET'])
@charts.route('/<url_symbol>-<stock_or_etf>/<url_name>/<statement_or_ratio>/<url_fin_metric>', methods=['POST', 'GET'])
@charts.route('/<url_symbol>/<statement_or_ratio>/<url_fin_metric>', methods=['POST', 'GET'])
@charts.route('/<url_symbol>/<url_fin_metric>', methods=['POST', 'GET'])
@charts.route('/<url_symbol>', methods=['POST', 'GET'])
@charts.route('/random', methods=['POST', 'GET'])
def current_ratio(url_symbol="random", stock_or_etf = "stock", url_name = "apple", statement_or_ratio="none", url_fin_metric= "none"):
    global domain
    global subdomain
    print("bobobo", url_fin_metric)
    url_symbol = url_symbol.lower()
    fin_statements_matching = pd.read_csv("reference_data/Financial_Statements_Reference_Matching.csv")

    if url_fin_metric == "price":
        main_page_y_n = "no"
        url_fin_metric = "revenue-sales"
        chart_type = "price"
    else:
        chart_type = "normal"
    

    if url_fin_metric == "none" and statement_or_ratio != "none":
        pass
    else:
        pass

    if url_fin_metric == "none" and statement_or_ratio == "none":
        # print("boopee", url_fin_metric)
        main_page_y_n = "yes"
        url_fin_metric = "revenue-sales"
        
        
        fin_paper = FS("IS",url_symbol)
        # tables=fin_paper.df_values()['df_table']
        balance_sheet=FS("BS",url_symbol).df_table()
        print("balbal")
        # print(balance_sheet)
        cash_flow=FS("CF",url_symbol).df_table()
        income_statement=FS("IS",url_symbol).df_table()
        # table_pct = fin_paper.df_values()['df_table_pct']
        fs_table_pct = fin_paper.df_table_pct()
        fin_paper_values = fin_paper.df_values()
        # df_date = fin_paper_values['chart_x_dates'],
        # df_rev = fin_paper_values['chart_y_revenue']
        df_json = fin_paper_values['df_json']
        print("globglob")
        # titles = fin_paper_values['df_titles']
        # labels = fin_paper.df_labels()
        #  values=FS("BS","AAPL").df_price()
        versus_chart_y_n = "no"
    else:
        # print("boopee", url_fin_metric)
        main_page_y_n = "no"
        versus_chart_y_n = "yes"
        balance_sheet=""
        cash_flow=""
        income_statement=""
    if statement_or_ratio == "none":
        hide_chart_sidebar = "yes"
        statement_or_ratio = "income-statement"
        try:
            statement_or_ratio = list(fin_statements_matching[fin_statements_matching['URL']=="{}".format(url_fin_metric)]['statement_url'])[0]
        except:
            statement_or_ratio = "ratio"
        print("dumdumdum", statement_or_ratio)
    else:
        hide_chart_sidebar = "no"
    if url_fin_metric != "none" and statement_or_ratio != "none":

        print("nobnob")
    else:
        versus_chart_y_n = "no"

    from route_imports.ratio_map import metric_to_url_map
    from route_imports.ratio_map import url_to_var_name_map
    from route_imports.ratio_map import url_to_name_map
    from route_imports.ratio_map import fin_statement_raw_names
    from route_imports.ratio_map import fin_statement_renamed_cols
    from route_imports.ratio_map import fin_statement_renamed_titles
    from route_imports.ratio_map import metric_to_formula_map
    from route_imports.ratio_map import url_to_metric_map
    from route_imports.ratio_map import url_to_equation_map
    from route_imports.ratio_map import url_to_definition_map
    from route_imports.ratio_map import fin_statement_title_links_dict
    import scipy
    from route_imports.ratio_map import fin_statement_title_statements_dict
    start_time = time.time()
    
    # titles_list = ['Date','Symbol','Filing Date','Accepted Date','Period','SEC Filing Link']
    titles_list = ['Selling, General and Administrative (SG&A)','Selling General and Administrative (SG&A)', "EBITDA Margin", "Operating Margin" ,"Profit Margin"]
    vars_drop = ['quarter_n_year',  's_g_n_a', "ebitda_margin", "operating_margin","profit_margin"]
    def weird_division(n, d):
        return n / d if d else 0
    def replace(group, stds):
        group[np.abs(group - group.mean()) > stds * group.std()] = np.nan
        return group
    fin_statements_list = ["balance-sheet","income-statement","cash-flow-statement"]
    company_profiles = pd.read_csv("reference_data/Company_Profiles.csv")
    try:
        print(url_symbol)
    except:
        # import random
        # us_companies = company_profiles[(company_profiles['exchange']=="NASDAQ") | (company_profiles['exchange']=="NYSE")]
        # list_us_companies = list((us_companies[['symbol','mktCap']]).sort_values("mktCap", ascending=False)['symbol'])[0:500]
        # url_symbol = "aapl" #random.sample(list_us_companies, 1)[0]
        # statement_or_ratio = "income-statement"
        # url_fin_metric= "revenue-sales"
        # stock_or_etf = "stock"
        # return redirect("http://127.0.0.1:5000/aapl/revenue-sales", code=302)
        return redirect("{}/aapl/revenue-sales".format(domain), code=302)
    if url_symbol=="random":
        import random
        random_list = ["tsla, aapl, fb, amzn, googl, msft, nflx, zm, nvda, nio, baba, amd, pton, pypl, shop, adbe, dis, dkng, mu, wfc, hd"]
        random_symbol = random.sample(list_us_companies, 1)[0]
        return redirect("{}/{}".format(domain,random_symbol), code=302)
    else:
        pass
    currency_symbol = list(company_profiles[company_profiles['symbol']=="{}".format(url_symbol.upper())]['currency symbol'])[0]
    currency_symbol_original = currency_symbol
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
                            'Similar Companies',
                            'shortest name',
                            'url name']
    company_profiles = company_profiles[company_profiles_col]
    profiles_dict = {}
    profiles_value = company_profiles[company_profiles['symbol']=="{}".format(url_symbol.upper())].values.tolist()[0]
    for n, profiles_col in enumerate(company_profiles_col):
        key = profiles_col
        value = profiles_value[n]
        profiles_dict[key] = value
    chars_to_remove = ["'","[","]"]
    try:
        for character in chars_to_remove:
            profiles_dict['Industries'] = profiles_dict['Industries'].replace(character, "")
            profiles_dict['Similar Companies'] = profiles_dict['Similar Companies'].replace(character, "")
    except:
        pass
    
    if "{}".format(statement_or_ratio) in fin_statements_list:
        if "{}".format(statement_or_ratio) == "income-statement" or "{}".format(statement_or_ratio) == "balance-sheet" or "{}".format(statement_or_ratio) == "cash-flow-statement":
            if "{}".format(statement_or_ratio) == "income-statement":
                fin_statement_dir = "Income Statement"
            elif "{}".format(statement_or_ratio) == "balance-sheet":
                fin_statement_dir = "Balance Sheet"
            elif "{}".format(statement_or_ratio) == "cash-flow-statement":
                fin_statement_dir = "Cash Flow Statement"
            urls_fs = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="{}".format(fin_statement_dir)]['URL'])
            # print("urls_fs", urls_fs)
            titles_bs = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="{}".format(fin_statement_dir)]['Title'])
            var_list = list(fin_statements_matching[fin_statements_matching['Financial Statement']=="{}".format(fin_statement_dir)]['Python Variable Name'])
            fin_metric_pos = urls_fs.index("{}".format(url_fin_metric))
        else:
            pass
        # print("sup0")
        fin_statement_cols = titles_bs
        cols = titles_bs
        fin_metric_title = fin_statement_cols[fin_metric_pos]
        # csv_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/quarter/{}/*~{}~*".format(fin_statement_dir, url_symbol.upper()))[-1]
        year_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/{}/*~{}~*".format(fin_statement_dir, url_symbol.upper()))[-1]
        year_df_file = (pd.read_csv(year_file))
        # df = pd.read_csv(csv_file)
        df = pd.read_csv(year_file)
        matching_row = fin_statements_matching[fin_statements_matching['URL']=="{}".format(url_fin_metric)]
        fin_metric_title = list(matching_row['Title'])[0]
        fin_metric_vars = list(matching_row['Python Variable Name'])
        fin_metric_name = list(matching_row['Name'])[0]
        fin_metric_definition = list(matching_row['Definition / Formula'])[0]
        len_not_na_df = len(df[df['{}'.format(fin_metric_name)]==0]) #df['{}'.format(fin_metric_name)].notna().sum()
        len_not_na_year_df =  len(year_df_file[year_df_file['{}'.format(fin_metric_name)]==0]) #year_df_file['{}'.format(fin_metric_name)].notna().sum()
        # print("len df", len(df), "len year df", len(year_df_file), "len_not_na_df", len_not_na_df, "len_not_na_year_df", len_not_na_year_df)
        # if len(year_df_file)*3 > len(df):
        # print("zYP")
        df = year_df_file
        all_titles = list(df)
        all_numbers_df = df[list(df.select_dtypes(include=['float','int64']))].div(4, axis=0)
        all_objects_df = df[list(df.select_dtypes(include=['object']))]
        concat_df = pd.concat([all_numbers_df, all_objects_df], axis=1)
        df = concat_df[all_titles]
        # print("list_years", list_years)
        # print("list_yezars", len(df),df.head(30))
        try:
            list_years = list(df["date"].apply(lambda j: j[0:4]))
            if len(list_years) > len(list(set(list_years))):
                list_years = np.arange(list_years.min(),list_years.max()+2)
        except: # only here likely bc of AAPL - saving in Excel caused date format change
            list_years = list(df["date"].apply(lambda j: j[-4:]))
            if len(list_years) > len(list(set(list_years))):
                list_years = np.arange(list_years.min(),list_years.max()+2)
        new_df_list = []
        for n,y in enumerate(list_years):
            for x in ["12-31","03-31","06-30","09-30"]:
                new_df = df[n:n+1]
                new_df['date'] = pd.to_datetime("{}-{}".format(y,x))
                new_df_list.append(new_df)
        # print("list_yxxears", df.head(30))
        df = pd.concat(new_df_list).sort_values(by="date",ascending = True).reset_index()
        # print("list_yzzzzears", len(df),df.head(30))
        df['date'] = df['date'].apply(lambda x: str(x)[0:10])
        # print(list(df))
        df = df.drop(['index'],axis=1)
        df["Year"] = df["date"].apply(lambda x: x[0:4])
        print("sup1", len(df),df.head(30))
        df["QQ-YYYY"] = df["period"]+"-"+df["date"].apply(lambda x: x[0:4])
        # else:
            # pass
        # xxx   if len_not_na_year_df + 2 > len(year_df_file):
        #         smart_data_warning = "*"
        #         smart_data_disclaimer = Markup('<span class="ruhroh disclaimer_zero">** The data has been enhanced for easier insights</span>')
        x = fin_metric_vars[0]
        if x=="accumulated_other_comprehensive_income_loss" or x=="other_total_stockholders_equity" or x=="other_income_other_expenses_net" or x=="accounts_receivable" or x=="investments_in_property_plant_and_equipment" or x=="acquisitions_net" or x=="purchases_of_investments" or x=="other_investing_activities" or x=="net_cash_used_for_investing_activities" or x=="debt_repayment" or x=="capital_expenditure" or x=="dividends_paid" or x=="common_stock_repurchased" or x=="capitalExpenditure":
            # df['{}'.format(x)] = df['{}'.format(x)].apply(lambda x: -1*x)
            if x=="dividends_paid" or x=="common_stock_repurchased" or x=="capitalExpenditure":
                df['{}'.format(fin_metric_name)] = df['{}'.format(fin_metric_name)]*-1
            elif len(df[df['{}'.format(fin_metric_name)]<0]) > len(df[df['{}'.format(fin_metric_name)]>0]):
                # pass
                # print("negative now", df[['{}'.format(fin_metric_name),"QQ-YYYY" ]])
                df['{}'.format(fin_metric_name)] = df['{}'.format(fin_metric_name)]*-1 #.apply(lambda x: -1*x)
                # print("negative now", df[['{}'.format(fin_metric_name),"QQ-YYYY" ]])
            else:
                pass
        else:
            # pass
            # if len(df[df['{}'.format(x)]<0]) > len(df[df['{}'.format(x)]>0]):
            #     # pass
            #     print("negative now", df[['{}'.format(x),"QQ-YYYY" ]])
                # df['{}'.format(x)] = df['{}'.format(x)]*-1 #.apply(lambda x: -1*x)
            #     print("negative now", df[['{}'.format(x),"QQ-YYYY" ]])
            # else:
                pass
        df['pct_chg_temp'] = df['{}'.format(fin_metric_name)].shift(-4)/df['{}'.format(fin_metric_name)]
        df.loc[df['pct_chg_temp'] > 10, fin_metric_name] = np.nan
        df.loc[df['pct_chg_temp'] < -10, fin_metric_name] = np.nan
        df = df.drop("pct_chg_temp",axis=1)
        fin_metric_equation = ""
        # print("sup4", len(df),df.head(30))
        # df = df.sort_values(by="date",ascending = False)
        early_missing_periods = df[::-1]["{}".format(fin_metric_name)].ne(0).idxmax()
        # print("sup5", len(df),df.head(30))
        df = df[0:early_missing_periods+1]
        # print("sup2")
        # df = df.drop(['index'],axis=1)
        # print(df.head(30))
        # print(list(df))
        def groupby_agg(df):
            if "{}".format(statement_or_ratio) == "income-statement":
                df_grouped = df.groupby("Year").sum()
            elif "{}".format(statement_or_ratio) == "balance-sheet":
                df_grouped = df.groupby("Year").sum()
            elif "{}".format(statement_or_ratio) == "cash-flow-statement":
                df_grouped = df.groupby("Year").sum()
            else:
                df_grouped = df.groupby("Year").sum()
            return df_grouped
    else:
        fin_metric_definition_formula = ""
        metric_to_list_variables_map = {
                'net_working_capital_ratio':['working_capital_math','total_assets',],
                'long_term_debt_to_equity_ratio': ['long_term_debt','total_se'],
                'book_value_per_share':['total_se','shares_outstanding_non',],
                'total_equity_to_total_assets':['total_se','total_assets',],
                # 'roa_cash_flow': ['operating_cash_flow','total_assets',],
                'operating_cost_ratio':['total_opex','d_n_a','net_revenue',],
                'perc​entage_of_debt_to_asset_formula':['total_non_current_liabilities','total_assets',],
                'total_liabilities_pct_of_total_assets':['total_liabilities','total_assets',],
                'debt_to_assets_ratio':['total_debt','total_assets',],
                'debt_to_equity_ratio':['total_debt','total_se',],
                'quick_ratio':['total_assets','total_current_liabilities'],
                'working_capital': ['total_current_assets','total_current_liabilities'],
                'current_ratio':['total_current_liabilities','total_assets','inventory'],
                'capital_intensity':['total_assets','net_revenue',],
                'equity_multiplier':['total_assets','total_se',],
                'short_term_debt_to_equity_ratio':['short_term_debt','total_se',],
                'st_debt_as_pct_of_total_debt':['short_term_debt','total_liabilities',],
                'acid_test_ratio':['quick_assets_math','total_current_liabilities',],
                'pre_tax_income_to_sales':['pretax_income_non','net_revenue',],
                'pre_tax_return_on_assets':['pretax_income_non','total_assets',],
                'pre_tax_return_on_common_equity':['pretax_income_non','common_stock',],
                'operating_roa':['operating_income','total_assets',],
                'operating_profit_margin':['operating_income','net_revenue',],
                'free_operating_cash_flow_to_debt':['operating_cash_flow','capex','total_debt',],
                'discretionary_cash_flow_to_debt':['operating_cash_flow','accounts_payable','debt_repayment','dividends_paid','interest_expense',],
                'operating_cash_flow_to_interest':['operating_cash_flow','interest_expense','income_tax_expense','interest_expense',],
                'operating_cash_flow_to_debt':['operating_cash_flow','interest_expense','income_tax_expense','total_liabilities',],
                'cash_flow_margin_ratio_formula':['operating_cash_flow','total_liabilities',],
                'cash_flow_to_debt':['operating_cash_flow','total_debt',],
                'net_cash_flow_to_capital_expenditures':['operating_cash_flow','capex',],
                'cash_flow_to_revenue':['operating_cash_flow','net_revenue',],
                'cash_return_on_assets':['operating_cash_flow','total_assets',],
                'cash_return_on_equity':['operating_cash_flow','total_se',],
                'cash_to_income_ratio':['operating_cash_flow','operating_income',],
                'cash_flow_per_share':['operating_cash_flow','shares_outstanding_non',],
                'debt_payment':['operating_cash_flow','debt_repayment',],
                'debt_coverage':['operating_cash_flow','long_term_debt',],
                'cash_flow_from_operations_ratio':['operating_cash_flow','total_current_liabilities',],
                'gross_profit_margin':['net_revenue','cost_of_sales','net_revenue',],
                'rece​ivables_turnover':['net_revenue','accounts_receivable',],
                'capital_turnover_ratio':['net_revenue','working_capital_math',],
                'assets_turnover_ratio':['net_revenue','total_assets',],
                'accounts_receivable_turnover_ratio':['net_revenue','accounts_receivable',],
                'operating_cash_flow_to_debt':['net_revenue','total_se',],
                'inventory_ratio':['net_revenue','inventory',],
                'return_on_investment':['net_income','interest_expense','total_se','long_term_debt',],
                'pretax_margin':['net_income','income_tax_expense','net_revenue',],
                'income_to_net_worth_ratio':['net_income','deferred_income_tax','shares_outstanding_non',],
                'return_on_assets_roa':['net_income','total_assets',],
                'return_on_equity_roe':['net_income','total_se',],
                'net_profit_margin':['net_income','net_revenue',],
                'earnings_per_share':['net_income','shares_outstanding_non',],
                'current_cash_debt_coverage':['net_cash_by_operating_activities','total_current_liabilities',],
                'cash_debt_coverage':['net_cash_by_operating_activities','total_liabilities',],
                'long_term_debt_ratio':['long_term_debt','total_assets',],
                'long_term_debt_equity_ratio':['long_term_debt','total_se',],
                'lt_debt_as_pct_of_total_debt':['long_term_debt','total_liabilities',],
                'inventory_pct_of_revenue':['inventory','net_revenue',],
                'intangibles_pct_of_book_value':['goodwill_n_intangible_assets','total_se',],
                'ffo_funds_from_operations_to_debt':['ffo_math','total_debt',],
                'operating_margin':['ebitda_non','d_n_a','net_revenue',],
                'cash_coverage_ratio':['ebitda_non','interest_expense',],
                'ebitda_per_share':['ebitda_non','shares_outstanding_non',],
                'ebitda_interest_coverage':['ebitda_non','interest_expense',],
                'ebitda_margin':['ebitda_non','net_revenue',],
                'net_margin_profit_margin':['net_income','net_revenue',],
                'return_on_capital_employed_ratio':['ebit_math','total_assets','total_current_liabilities',],
                'debt_service_ratio':['ebit_math','interest_expense',],
                'return_on_capital':['ebit_math','total_assets',],
                'dividend_yield':['dividends_paid','price_market','shares_outstanding_non',],
                'dividend_payout_ratio':['dividends_paid','net_income',],
                'dividends_per_share':['dividends_paid','shares_outstanding_non',],
                'inventory_turnover':['cost_of_sales','inventory',],
                'cash_ratio':['cash_non','total_current_liabilities',],
                'cash_flow_roa':['operating_cash_flow','total_assets',],
                'average_collection_period':['accounts_receivable','net_revenue',],
                'number_of_days_of_receivables':['accounts_receivable','inventory',],
                'average_days_payables_outstanding':['accounts_payable','cost_of_sales',],
                'days_sales_in_payables':['accounts_payable','total_opex',],
            }
        currency_symbol = ""
        fin_dir = ["Income Statement","Balance Sheet","Cash Flow Statement"]
        fin_df_list = []
        for x in fin_dir:
            # csv_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/quarter/{}/*~{}~*".format(x, url_symbol.upper()))[-1]
            fin_file_year = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/{}/*~{}~*".format(x, url_symbol.upper()))[-1]
            # fin_df = pd.read_csv(csv_file)
            df = pd.read_csv(fin_file_year)
            # if len(year_df_file) > len(fin_df):
            #     df = year_df_file
            all_titles = list(df)
            all_numbers_df = df[list(df.select_dtypes(include=['float','int64']))].div(4, axis=0)
            all_objects_df = df[list(df.select_dtypes(include=['object']))]
            concat_df = pd.concat([all_numbers_df, all_objects_df], axis=1)
            df = concat_df[all_titles]
            # df.to_csv("all_titles.csv")
            try:
                list_years = list(df["date"].apply(lambda j: j[0:4]))
                if len(list_years) > len(list(set(list_years))):
                    list_years = np.arange(list_years.min(),list_years.max()+2)
            except: # only here likely bc of AAPL - saving in Excel caused date format change
                list_years = list(df["date"].apply(lambda j: j[-4:]))
                if len(list_years) > len(list(set(list_years))):
                    list_years = np.arange(list_years.min(),list_years.max()+2)
            new_df_list = []
            for n,y in enumerate(list_years):
                for x in ["12-31","03-31","06-30","09-30"]:
                    new_df = df[n:n+1]
                    new_df['date'] = pd.to_datetime("{}-{}".format(y,x))
                    new_df_list.append(new_df)
            df = pd.concat(new_df_list).sort_values(by="date",ascending = False).reset_index()
            df['date'] = df['date'].apply(lambda x: str(x)[0:10])
            fin_df = df
            fin_df["Year"] = fin_df["date"].apply(lambda x: x[0:4])
            fin_df["QQ-YYYY"] = fin_df["period"]+"-"+fin_df["date"].apply(lambda x: x[0:4])
            fin_df_list.append(fin_df)
        df_merge_is_bs = pd.merge(fin_df_list[0],fin_df_list[1],how="inner", on="QQ-YYYY")
        df_merge = pd.merge(df_merge_is_bs,fin_df_list[2],how="inner", on="QQ-YYYY")
        # print("df_merge",df_merge)
        # df_merge.to_csv("df_merge1.csv")
        df_merge = df_merge[fin_statement_raw_names]
        df_merge.columns = fin_statement_renamed_cols
        metric_name = url_to_metric_map["{}".format(url_fin_metric)]
        fin_metric_equation = url_to_equation_map["{}".format(url_fin_metric)]
        fin_metric_definition = url_to_definition_map["{}".format(url_fin_metric)]
        fin_metric_title = url_to_name_map[url_fin_metric]
        # fin_metric_vars = fin_metric_title
        fin_metric_name = url_to_var_name_map[url_fin_metric]
        # fin_metric_vars = metric_to_list_variables_map[fin_metric_name] # NOTE: sdfsdf
        fin_metric_vars_old = metric_to_list_variables_map[fin_metric_name] # NOTE: sdfsdf
        fin_metric_vars_old = list(set(fin_metric_vars_old))
        df_title = df_merge.copy()
        df_title.columns = fin_statement_renamed_titles
        df_yoy_cards = df_title.drop_duplicates(subset=['Date'])#.sort_values(by=["Date"])
        df_yoy_cards = df_yoy_cards.loc[:, 'Period':'QQ-YYYY']
        L = ['Otherxx'] #['other','Other']
        # print("sup8")
        # print("df_yoy_cards",df_yoy_cards)
        df_yoy_cards =  df_yoy_cards.loc[:, ~df_yoy_cards.columns.str.contains('|'.join(L))]
        # df_yoy_cards.to_csv("all_titles5.csv")
        df_row_1 = (df_yoy_cards.select_dtypes(include=['float','int64']))[0:1].reset_index()
        # print("sup9")
        len_yoy = len(df_yoy_cards)
        if len_yoy <= 21:
            df_row_2 = (df_yoy_cards.select_dtypes(include=['float','int64']))[len_yoy-1:len_yoy].reset_index()
        else:
            df_row_2 = (df_yoy_cards.select_dtypes(include=['float','int64']))[20:21].reset_index()
        df_yoy = (df_row_1.div(df_row_2))-1
        # print("sup10")
        # print("df_yoy_cards",df_yoy)
        greater_than = (df_yoy[list(df_yoy)]>=0.0) & (df_yoy[list(df_yoy)]<100)
        less_than = (df_yoy[list(df_yoy)]<-0.01) & (df_yoy[list(df_yoy)]>-100)
        # print("sup11")
        not_zero = (df_yoy[list(df_yoy)] != -1)
        df_yoyx = df_yoy[((greater_than) | (less_than)) & not_zero]
        # print("sup12")
        # print("df_yoy_cards",df_yoyx)
        # df_yoyx.to_csv("df_yoy_cards4.csv")
        # df_yoyx = df_yoyx.dropna(axis=1, how='all')
        # df_yoyx = df_yoy
        # df_yoyx = df_yoyx.iloc[0].sort_values(ascending=False)
        # df_yoyx_sorted = df_yoyx.iloc[0].sort_values(ascending=False)
        # print("sup13", df_yoyx_sort)
        # df_yoyx.sample(5, axis=1)
        # df_yoyx_5 = df_yoyx.sample(5, axis=1)
        yoy_cards_dict = {}
        yoy_cards_urls_dict = {}
        yoy_cards_html_list = []
        df_yoyx = df_yoyx.drop('index',axis=1)
        # del df_yoyx['index']
        df_yoyx = df_yoyx.dropna(axis=1, how='all')
        profiles_value = df_yoyx.values.tolist()[0]
        for n, profiles_col in enumerate(list(df_yoyx)):
            key = profiles_col
            value = df_yoyx[key][0]*100 # profiles_value[n]*100
            print("bling",n, key, value)
            current_value = 4*df_row_1[key][0] # profiles_current_value[n]
            current_value = magnitude_num(current_value,currency_symbol_original)
            value = change_markup(value,"percent","noarrow", "yoy_cards")
            yoy_cards_dict[key] = value
            yoy_cards_urls_dict[key] = fin_statement_title_links_dict[key]
            statement_url = fin_statement_title_statements_dict[key]
            # print("sup","key",key,"value",value,"link",fin_statement_title_links_dict[key],"statement",fin_statement_title_statements_dict[key])
            # yoy_cards_html = Markup('<a class="yoy_card_link" href="https://tendollardata.com/{}"><div class="item item1"><span class="yoy_cards_title">{}</span><span class="yoy_cards_metric">{}</span></div></a>'.format(fin_statement_title_links_dict[key],profiles_col,value))
            yoy_cards_html = Markup('<a class="yoy_card_link" href="{}/{}-{}/{}/{}/{}"><div class="item item1 s_card_{}"><span class="yoy_cards_metric">{}</span><span class="yoy_cards_current">{}</span><span class="yoy_cards_title">{}</span></div></a>'.format(subdomain,url_symbol,stock_or_etf,url_name,statement_url,fin_statement_title_links_dict[key],n,value,current_value,profiles_col))
            yoy_cards_html_list.append(yoy_cards_html)
        yoy_cards_html_joined = Markup("".join(yoy_cards_html_list))
        yoy_cards_html_joined = Markup("".join(yoy_cards_html_list))
        df = df_merge.iloc[::-1]
        # print("df_merge", df_merge)
        df = df.sort_values(by="date",ascending = True)
        df['ffo_math']=df['net_income'] + df['d_n_a'] + df['sales_maturities_of_investments'] + df['purchase_of_investments'] + df['investments_in_pp_n_e'] + df['acquisitions_net']
        df['book_value_math']=df['total_assets'].dropna()-df['total_liabilities'].dropna()
        df['ebit_math']=df['ebitda_non'] - df['d_n_a']
        df['working_capital_math']= df['total_current_assets'] - df['total_current_liabilities']
        df['quick_assets_math']=df['cash_non']+df['short_term_investments']+df['accounts_receivable']
        df['quick_ratio_math']=(df['total_current_assets'] - df['inventory'])/df['total_current_liabilities']
        fin_metric_vars = [fin_metric_title]
        # XXXXX
        # for n,x in enumerate(fin_metric_vars):
        # print("len df", len(df), "len year df", len(year_df_file), "len_not_na_df", len_not_na_df, "len_not_na_year_df", len_not_na_year_df)
        # xxx   if len_not_na_year_df + 2 > len(year_df_file):
        #         smart_data_warning = "*"
        #         smart_data_disclaimer = Markup('<span class="ruhroh disclaimer_zero">** The data has been enhanced for easier insights</span>')
        # df = df.interpolate(method='linear')
        df = df.interpolate()
        df = df.drop_duplicates(subset=['date']).sort_values(by=["date"])
        for x in fin_metric_vars_old:
            if x=="accumulated_other_comprehensive_income_loss" or x=="other_total_stockholders_equity" or x=="other_income_other_expenses_net" or x == "dividends_paid" or x=="accounts_receivable" or x=="investments_in_property_plant_and_equipment" or x=="acquisitions_net" or x=="purchases_of_investments" or x=="other_investing_activities" or x=="net_cash_used_for_investing_activities" or x=="debt_repayment" or x=="capital_expenditure":
                df['{}'.format(x)] = df['{}'.format(x)].apply(lambda x: -1*x)
            else:
                # pass
                # if len(df[df['{}'.format(x)]<0]) > len(df[df['{}'.format(x)]>0]):
                #     # pass
                #     print("negative now", df[['{}'.format(x),"QQ-YYYY" ]])
                    # df['{}'.format(x)] = df['{}'.format(x)]*-1 #.apply(lambda x: -1*x)
                #     print("negative now", df[['{}'.format(x),"QQ-YYYY" ]])
                # else:
                    pass
            # print("listd_na",list(df))
            if len(df[df['{}'.format(x)]==0])/len(df)>.7:
                df['{}'.format(x)]= 1
            # if len(df[df['{}'.format(x)]<0]) > len(df[df['{}'.format(x)]>0]):
            #     pass
            #     # print("negative now", df[['{}'.format(fin_metric_name),"QQ-YYYY" ]])
            #     # df['{}'.format(x)] = df['{}'.format(x)].apply(lambda p: -1*p)
            #     # print("knew",x)
            #     # print("knew2",metric_name)
            #     # print(df['{}'.format(x)])
            #     # print("negative now", df[['{}'.format(fin_metric_name),"QQ-YYYY" ]])
            # else:
            #     pass
            # print("readallabout",x)
            # if x == "dividends_paid":
            #     pass
            #     # print("divpass")
            # else:
            #     # print("divelse")
            df['{}'.format(x)] = df['{}'.format(x)].replace(0, np.nan)
            df['{}'.format(x)] = df['{}'.format(x)].replace(np.inf, np.nan)
            # print("qaz ", df['{}'.format(x)].head(50),2)
            df['pct_chg_temp'] = df['{}'.format(x)].shift(-4)/df['{}'.format(x)]
            df.loc[df['pct_chg_temp'] > 10, x] = np.nan
            df.loc[df['pct_chg_temp'] < -10, x] = np.nan
            # df = df.drop(['pct_chg_temp'], axis=1)
            # print("listenman", len(df), "sad",df['{}'.format(x)].isna().sum(), list(df['{}'.format(x)]))
            # print("listendudeagain", len(df), "sad",df['{}'.format(x)].isna().sum(), list(df['{}'.format(x)]))
            # if pd.isnull((df['{}'.format(x)].head(1))[0]):#list(df['{}'.format(x)].head(1))[0]==np.nan:#df['{}'.format(x)].min()
            #     print("not number", list(df['{}'.format(x)].head(1))[0])
            #     df['{}'.format(x)].iloc[0] = df['{}'.format(x)][0:4].mean()
            # else:
            #     print("iznum", list(df['{}'.format(x)].head(1))[0])
        # df.to_csv("letssee.csv")
        metric_history = metric_to_formula_map(df,metric_name)
        # print("bango")
        # print(df[['date','pct_chg_temp',x]].tail(50))
        fin_metric_history = metric_history
        fin_metric_vars_old2 = fin_metric_vars_old
        # fin_metric_vars_old2.append('QQ-YYYY')
        # fin_metric_vars_old2.append('pct_chg_temp')
        # print("listdf", list(df))
        # df = df.drop(['pct_chg_temp'], axis=1)
        # fin_metric_vars_old2.append(fin_metric_title)
        df["{}".format(fin_metric_title)] = metric_history
        # print("wassup")
        print(df[fin_metric_vars_old2].head(50))
        # print("wassup2")
        # print(df[fin_metric_vars_old2].tail(50))
        # print("listz df", list(df))
        df = df.interpolate(method='linear')
        # df = df.drop(['pct_chg_temp'], axis=1)
        # df.to_csv("xgitest2.csv")
        # print("bongo")
        # print(df[['date','pct_chg_temp',fin_metric_title]].tail(50))
        df = df.sort_values(by="date",ascending = False)
        early_missing_periods = df[::-1]["{}".format(fin_metric_title)].ne(0).idxmax()
        df = df[0:early_missing_periods+1]#[::-1]
        # print("bingo")
        # print(df[['date','pct_chg_temp',fin_metric_title]].tail(50))
        def groupby_agg(df):
            df_grouped = df.groupby("Year").mean()
            return df_grouped
    # fin_metric_vars = [fin_metric_title]
    fin_metric_definition_link = ""#<br>Source: Investopedia"
    fin_metric_definition_formula = Markup("{}<br>{}<br>{}".format(fin_metric_equation, fin_metric_definition, fin_metric_definition_link))
    df = df.drop_duplicates(subset=['date']).sort_values(by=["date"], ascending=False)
    df_quarter = df['period']
    # df = df.drop(['Quarter & Year', 'Unnamed: 0','symbol','fillingDate','acceptedDate','period','link',],axis=1, errors='ignore')
    df = df.drop(['Quarter & Year', 'Unnamed: 0','symbol','fillingDate','acceptedDate','period','link','ebitdaratio','operatingIncomeRatio','netIncomeRatio'],axis=1, errors='ignore')
    # print("bingox")
    try:
        # for x in reversed(titles_bs):
        #     if x in titles_list:
        #         titles_bs.remove(x)
        for x in reversed(var_list):
            if x in vars_drop:
                var_list.remove(x)
        titles_bs.append('finalLink')
        # titles_bs.append('Year')
        var_list.append('finalLink')
        # var_list.append('Year')
        titles_bs.append('Year')
        titles_bs.append('QQ-YYYY')
        var_list.append('Year')
        var_list.append('QQ-YYYY')
        titles_bs.insert(0,"date")
        var_list.insert(0,"date")
        # from pprint import pprint
        # print("var list", var_list)
        # print("title_bs", titles_bs)
        # print(list(df))
        df.columns = var_list
        # print("sup5",list(df))
    except Exception as e:
        pass
    try:
        try:
            pass
            # titles_bs.remove("Quarter & Year")
            # var_list.remove("Quarter & Year")
        except:
            pass
        # df['{}'.format(x)] = df['{}'.format(x)].apply(lambda x: abs(x))
        # n = 0
        # df['pct_chg_temp'] = df['{}'.format(x)]/df['{}'.format(x)].shift(-1)
        # df.loc[df['pct_chg_temp'] > 10, x] = np.nan
        # df.loc[df['pct_chg_temp'] < -10, x] = np.nan
        # # df.to_csv("whatev2.csv")
        # # print("vast new df",x)
        # # print(df[['date','pct_chg_temp',x]].head(40))
        # df = df.drop(['pct_chg_temp'], axis=1)
        # # print("qxaz", fin_statement_dir, df['{}'.format(x)].head(50),2)
        # len_rows_ratios = df['{}'.format(x)].isna().sum()
        # df = df.interpolate(method='linear')
        # while n <= len_rows_ratios: #df[df['{}'.format(x)].isna].shape[0]:#not df['{}'.format(x)].isin([0]).empty:
        #     df['{}'.format(x)] = df['{}'.format(x)].fillna(df['{}'.format(x)].rolling(window=8,center=True,min_periods=2).mean())
        #     n+=1
        # if pd.isnull((df['{}'.format(x)].head(1))[0]):#list(df['{}'.format(x)].head(1))[0]==np.nan:#df['{}'.format(x)].min()
        #     # print("not number", list(df['{}'.format(x)].head(1))[0])
        #     df['{}'.format(x)].iloc[0] = df['{}'.format(x)][0:4].mean()
        # else:
        #     pass
        #     # print("iznum", list(df['{}'.format(x)].head(1))[0])
        # # print("len_row_ratios",len_rows_ratios, len(df))
        # if len(df) == len_rows_ratios:
        #     df['{}'.format(x)] = df['{}'.format(x)].replace(np.nan, 0)
        #     earliest_latest_warning = ""
        #     earliest_latest_disclaimer = ""
        #     # return render_template('404.html'), 404
        # print("dxzhead", x, fin_metric_title, list(df['{}'.format(x)]))
        # print("dxghead",list(df['{}'.format(fin_metric_title)]))
        # df['{}'.format(fin_metric_title)] = df['{}'.format(x)]
        # print("zfheads")
        # print("wsx", df['{}'.format(x)].head(50),2)
        # print("final total len entire df", len(df), x, "len na", df['{}'.format(x)].isna().sum())
        # df['{}'.format(x)] = df['{}'.format(x)].fillna(df['{}'.format(x)].rolling(window=16,center=True,min_periods=1).mean())
        # df['{}'.format(x)] = df['{}'.format(x)].fillna(df['{}'.format(x)].rolling(window=32,center=True,min_periods=1).mean())
        # df['{}'.format(x)] = df['{}'.format(x)].apply(lambda x:  int(x))
        # df = df.fillna(0)
        # df['{}'.format(x)] = df['{}'.format(x)].fillna(df['{}'.format(x)].rolling(window=4,center=True,min_periods=1).mean())
        # df['{}'.format(x)] = df['{}'.format(x)].replace(0, np.nan)
        # non_zero_list = list(df['{}'.format(x)])#.remove("nan")
        # non_zero_list=  [ x for x in non_zero_list if x.isnumeric()  ]
        # print("nonzerolist",non_zero_min)
        def closest(lst, K):
            return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]
        # df['{}'.format(x)] = df['{}'.format(x)].replace(np.nan, non_zero_min)
        # df['{}'.format(x)] = df['{}'.format(x)].ewm(span=4).mean()
        # df['{}'.format(x)]  = df['{}'.format(x)].replace(to_replace=0, method='ffill')
        # df['{}'.format(x)] = df['{}'.format(x)].ewm(span=2).mean()
        # df['{}'.format(x)] = df['{}'.format(x)].ewm(span=4).mean()
        # df['{}'.format(x)] = df['{}'.format(x)].clip_lower(0))
        # print("sicko mode")
        # print(df["{}".format(x)].head(30))
        # print("tail")
        # print(df["{}".format(x)].tail(30))
        df.columns = titles_bs
        # original_df = df.copy()
        df['pct_chg_temp'] = df['{}'.format(fin_metric_title)].shift(-4)/df['{}'.format(fin_metric_title)]
        df.loc[df['pct_chg_temp'] > 10, fin_metric_title] = np.nan
        df.loc[df['pct_chg_temp'] < -10, fin_metric_title] = np.nan
        df = df.interpolate()
        df = df.drop(['pct_chg_temp'],axis=1)
        # print("sup6",list(df))
        # df.to_csv("zippy3.csv")
        # print("sup7")
        # df_yoy_cards = df.loc[:, 'date':'finalLink']
        L = ['xx'] #['other','Other']
        df_yoy_cards = df.drop(['date','finalLink'],axis=1) #fin_metric_title,
        # print("sup821",list(df_yoy_cards))
        # print("df_yoy_cards",df_yoy_cards)
        df_yoy_cards =  df_yoy_cards.loc[:, ~df_yoy_cards.columns.str.contains('|'.join(L))]
        df_row_1 = (df_yoy_cards.select_dtypes(include=['float','int64']))[0:1].reset_index()
        # print("sup9x", df_yoy_cards)
        # df_yoy_cards.to_csv("yerp3.csv")
        len_yoy = len(df_yoy_cards)
        if len_yoy <= 21:
            df_row_2 = (df_yoy_cards.select_dtypes(include=['float','int64']))[len_yoy-1:len_yoy].reset_index()
        else:
            df_row_2 = (df_yoy_cards.select_dtypes(include=['float','int64']))[20:21].reset_index()
        # df_row_2 = (df_yoy_cards.select_dtypes(include=['float','int64']))[4:5].reset_index()
        df_yoy = (df_row_1.div(df_row_2))-1
        df_yoy = df_yoy.drop(['index'],axis=1)
        # print("sup10")
        # print("df_yoy_cards",df_yoy)
        greater_than = (df_yoy[list(df_yoy)]>=0.0) & (df_yoy[list(df_yoy)]<100)
        less_than = (df_yoy[list(df_yoy)]<-0.01) & (df_yoy[list(df_yoy)]>-100)
        # print("sup11")
        not_zero = (df_yoy[list(df_yoy)] != -1)#-420.6942069)@-1)
        df_yoyx = df_yoy[((greater_than) | (less_than)) & not_zero]
        # print("sup12")
        # print("df_yoy_cards",df_yoyx)
        # df_yoyx.to_csv("df_yoy_cards3.csv")
        # df_yoyx = df_yoyx.dropna(axis=1, how='all')
        # df_yoyx = df_yoyx.iloc[0].sort_values(ascending=False)
        # print("sup13", df_yoyx_sorted)
        # df_yoyx_5 = df_yoyx.sample(5, axis=1)
        yoy_cards_dict = {}
        yoy_cards_urls_dict = {}
        yoy_cards_html_list = []
        profiles_current_value = df_row_1.values.tolist()[0]
        profiles_value = df_yoyx.values.tolist()[0]
        # print("sup13")
        # df_yoyx = df_yoyx.drop(['index'],axis=1)
        df_yoyx = df_yoyx.dropna(axis=1, how='all')
        # df_yoyx.to_csv("df_yoy_dropped_all_3.csv")
        # list_df_yoyx = [fin_metric_title] + list(df_yoyx)
        # df_yoyx = df_yoyx[ [fin_metric_title] + [ col for col in df_yoyx.columns if col != fin_metric_title ] ]
        for n, profiles_col in enumerate(list(df_yoyx)):
            key = profiles_col
            value = df_yoyx[key][0]*100 # profiles_value[n]*100
            print("bling",n, key, value)
            current_value = 4*df_row_1[key][0] # profiles_current_value[n]
            current_value = magnitude_num(current_value,currency_symbol)
            value = change_markup(value,"percent","noarrow", "yoy_cards")
            yoy_cards_dict[key] = value
            yoy_cards_urls_dict[key] = fin_statement_title_links_dict[key]
            statement_url = fin_statement_title_statements_dict[key]
            # print("sup","key",key,"value",value,"link",fin_statement_title_links_dict[key],"statement",fin_statement_title_statements_dict[key])
            # yoy_cards_html = Markup('<a class="yoy_card_link" href="https://tendollardata.com/{}"><div class="item item1"><span class="yoy_cards_title">{}</span><span class="yoy_cards_metric">{}</span></div></a>'.format(fin_statement_title_links_dict[key],profiles_col,value))
            yoy_cards_html = Markup('<a class="yoy_card_link" href="{}/{}-{}/{}/{}/{}"><div class="item item1 s_card_{}"><span class="yoy_cards_metric">{}</span><span class="yoy_cards_current">{}</span><span class="yoy_cards_title">{}</span></div></a>'.format(subdomain,url_symbol,stock_or_etf,url_name,statement_url,fin_statement_title_links_dict[key],n,value,current_value,profiles_col))
            yoy_cards_html_list.append(yoy_cards_html)
        yoy_cards_html_joined = Markup("".join(yoy_cards_html_list))
        df = df[cols]
        # print("yo")
        # print("2try","fin metric title", fin_metric_title,"fin_metric_name",fin_metric_name, list(df))
        # print(df[["{}".format(fin_metric_title)]].head(30))
        fin_metric_history = df['{}'.format(fin_metric_title)]
        year_df = groupby_agg(df)
        year_df['year'] = pd.to_datetime(year_df.index).values.astype(np.int64) // 10 ** 6
        # print("try","fin metric title", fin_metric_title,"fin_metric_name",fin_metric_name, list(year_df))
        # print("wtf")
        # print(year_df[['year', "{}".format(fin_metric_title)]].head(30))
        df['quarter avg'] = df["{}".format(fin_metric_title)].rolling(window=8,min_periods=1).mean()
        # last_4_quarters = np.sum(df["quarter avg"][0:4])
        # prev_4_quarters = np.sum(df["quarter avg"][5:9])
        if "{}".format(statement_or_ratio) == "income-statement" or "{}".format(statement_or_ratio) == "cash-flow-statement" or "{}".format(statement_or_ratio) == "balance-sheet":
            last_4_quarters = np.sum(df["quarter avg"][0:4])
            prev_4_quarters = np.sum(df["quarter avg"][5:9])
        else:
            last_4_quarters = np.mean(df["quarter avg"][0:4])
            prev_4_quarters = np.mean(df["quarter avg"][5:9])
        # df["quarter avg"] = df["quarter avg"]
    except Exception as e:
        # print("boohoo",e)
        PrintException()
        year_df = groupby_agg(df)
        year_df['year'] = pd.to_datetime(year_df.index).values.astype(np.int64) // 10 ** 6
        # print("except e", e,"fin metric title", fin_metric_title,"fin_metric_name",fin_metric_name, list(year_df))
        # print(year_df.head(30))
        # year_df_json = np.nan_to_num(year_df[['year', "{}".format(fin_metric_title)]].to_numpy()).tolist()
        # print("fmt", fin_metric_title)
        df['quarter avg'] = df["{}".format(fin_metric_title)].rolling(window=8,min_periods=1).mean()
        last_4_quarters = np.mean(df["quarter avg"][0:4])
        prev_4_quarters = np.mean(df["quarter avg"][5:9])
    repeated_list = []
    # print("awfyes",year_df["{}".format(fin_metric_title)])
    # print("awfdf",df["{}".format(fin_metric_title)])
    # df.to_csv("awfdf.csv")
    def replace(group, stds):
        group[np.abs(group - group.mean()) > stds * group.std()] = np.nan
        return group
    df['pct_chg_temp'] = df['{}'.format(fin_metric_title)]/df['{}'.format(fin_metric_title)].shift(-4)
    df.loc[df['pct_chg_temp'] > 10, fin_metric_title] = np.nan
    df.loc[df['pct_chg_temp'] < -10, fin_metric_title] = np.nan
    # print("dast new df")
    # df.to_csv("dastnewcsv.csv")
    # df = df.drop_duplicates(subset=['date','QQ-YYYY', '{}'.format(x)], keep='first')
    # df['pct_chg_temp'] = df['{}'.format(x)]/df['{}'.format(x)].shift(-4)
    # # print(list(df['pct_chg_temp']))
    # df['pct_chg_temp'].values[df['pct_chg_temp'] > 10] = np.nan
    # # print("df['pct_chg_temp']")
    # # print(list(df['pct_chg_temp']))
    # # # df.loc[df['foo'].isnull(),'foo'] = df['bar']
    # # df.loc[df['pct_chg_temp'],np.nan] = df['{}'.format(x)]
    # df['{}'.format(x)][df['pct_chg_temp'] == np.nan] = np.nan
    # df.to_csv("tisktisk9.csv")
    # # df = df.drop(['pct_chg_temp'], axis=1)
    # df is your DataFrame
    # df.loc[:, df.columns != '{}'.format(x)] = df.groupby('{}'.format(x)).transform(lambda g: replace(g, 3))
    # df = df.interpolate(method='linear')
    for a,n in enumerate(year_df['{}'.format(fin_metric_title)]):
        if len(repeated_list) >= len(df):
            pass
        else:
            repeated_list.append(n)
        if len(repeated_list) >= len(df):
            pass
        else:
            repeated_list.append('')
        if len(repeated_list) >= len(df):
            pass
        else:
            repeated_list.append('')
        if len(repeated_list) >= len(df):
            pass
        else:
            repeated_list.append('')
    last_row = list(year_df['{}'.format(fin_metric_title)])[-1]
    if last_row in repeated_list:
        pass
    else:
        repeated_list = repeated_list[0:len(repeated_list)-1]
        repeated_list.append(last_row)
    df['repeater'] = repeated_list[::-1]
    year_df_json = np.nan_to_num(df[['date',"{}".format("repeater")]].to_numpy()).tolist()[::-1]
    # print("year_df_json", year_df_json)
    len_year_df = len(year_df)
    df_json_date_year  = np.nan_to_num(year_df['year'].to_numpy()).tolist()
    df['Quarter & Year'] = df_quarter+"-"+df['date'].apply(lambda x: str(x)[0:4])
    df.index = df['Quarter & Year']
    sorted_metric = year_df["{}".format(fin_metric_title)]
    # print("sorted_metricz", sorted_metric)
    lifetime_sum_all_metric = year_df["{}".format(fin_metric_title)].sum()
    lifetime_sum_all_metric = magnitude_num(lifetime_sum_all_metric,currency_symbol)
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
    print("min_metric", min_metric, "max_metric",max_metric)
    if min_metric <0 and max_metric>0:
        min_max_warning = "*"
        min_max_disclaimer = Markup('<span class="ruhroh disclaimer_one">* A modified method (see: <a href="https://math.stackexchange.com/questions/716767/how-to-calculate-the-percentage-of-increase-decrease-with-negative-numbers/716770">here</a>) is used to calculate changes that involve negative numbers.</span>')
    else:
        min_max_warning = ""
        min_max_disclaimer = ""
    bottom_25_str = magnitude_num(bottom_25, currency_symbol)
    top_25_str = magnitude_num(top_25, currency_symbol)
    num_years = len(sorted_metric)
    earliest_year = list((year_df.index.astype(str).str[0:4]))[0]
    latest_year = list((year_df.index.astype(str).str[0:4]))[-1]
    previous_year = int(latest_year)-1
    earliest_metric = list(sorted_metric)[0]
    latest_metric = list(sorted_metric)[-1]
    earliest_metric_str = magnitude_num(earliest_metric, currency_symbol)
    latest_metric_str = magnitude_num(latest_metric, currency_symbol)
    up_green_prefix = '<span class="up_green">'
    up_green_suffix = ' <i class="material-icons">arrow_upward</i></span>'
    down_red_prefix = '<span class="down_red">'
    down_red_suffix = ' <i class="material-icons">arrow_downward</i></span>'
    # print("max_metricz", max_metric)
    # print("min_metricz", min_metric)
    try:
        # print("zx2",latest_metric, earliest_metric)
        try:
            if latest_metric > earliest_metric:
                pct_chg = (latest_metric/earliest_metric)
            else:
                pct_chg = (latest_metric/earliest_metric)
            print("zx3")
            if (earliest_metric <0 and latest_metric>0) or (earliest_metric>0 and latest_metric<0):
                earliest_latest_warning = "*"
                earliest_latest_disclaimer =  Markup('<span class="ruhroh disclaimer_one">** A modified method (see: <a href="https://math.stackexchange.com/questions/716767/how-to-calculate-the-percentage-of-increase-decrease-with-negative-numbers/716770">here</a>) is used to calculate change, since the bottom/peak contains a negative number.</span>')
            else:
                earliest_latest_warning = ""
                earliest_latest_disclaimer = ""
        except:
            # pct_chg = 0
            earliest_latest_warning = ""
            earliest_latest_disclaimer = ""
        historical_pct_chg = (round(pct_chg-1, 1))
        # print("zx4")
        pct_chg = abs(pct_chg)
        annual_pct_chg  = (round(100*(pct_chg**(1/len(sorted_metric))-1),1))
        hist_pct_chg_str = change_markup(historical_pct_chg,"x","arrow","hist_pct_chg_str")
        # print("zx6")
        annual_pct_chg_str = change_markup(annual_pct_chg,"percent","noarrow","annual_percent")
    except Exception as e:
        pct_chg = "-"
        historical_pct_chg = "-"
        annual_pct_chg = "-"
    max_min_pct_diff = ((max_metric-min_metric)/min_metric)
    if float("inf") > max_min_pct_diff>0:
        max_min_pct_diff_str = "+{}%".format(round(max_min_pct_diff)*100,1)
    elif max_min_pct_diff<0:
        max_min_pct_diff_str = "-{}%".format(round(max_min_pct_diff)*100,1)
    else:
        max_min_pct_diff_str = "N/A"
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
    df_n_sum.columns = new_header
    df_n_sum.index = range(len(df_n_sum))
    df_t = pd.merge(df_n_sum, df_t, left_index=True, right_index=True,suffixes=('Total: {} - {}'.format(latest_year,earliest_year), 'Line Items'))
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
    year_df['Year']=year_df.index
    df['date'] = pd.to_datetime(df['date']).values.astype(np.int64) // 10 ** 6
    df['date'] = df['date'].apply(lambda x: int(x))
    try:
        print("beep",glob.glob("Charts_TenDollarData/financial_statements/data/Historical Market Cap & Price/NASDAQ/[[]M[]] Monthly/*")[0:5])
        print("market cap path1", "Charts_TenDollarData/financial_statements/data/Historical Market Cap & Price/*/[[]M[]] Monthly/M-*-{}.csv".format(url_symbol.upper()))
        market_cap_path = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Market Cap & Price/*/[[]M[]] Monthly/M-*-{}.csv".format(url_symbol.upper()))[0]
        print("market cap path",market_cap_path, "Charts_TenDollarData/financial_statements/data/Historical Market Cap & Price/[[]M[]] Monthly/M-*-{}.csv".format(url_symbol.upper()))
        market_cap_df = pd.read_csv(market_cap_path)
        print("mcappy", market_cap_df.head(5))
        market_cap_df = pd.read_csv(market_cap_path)
        market_cap_df['timestamp'] = pd.to_datetime(market_cap_df.datetime).values.astype(np.int64)// 10 ** 6
        closest_list = []
        closest_list_year = []
        closest_list_dups = []
        year_dates_price = df[df['repeater'] != '']['date']
        for k in year_dates_price:
            closest_time = min(market_cap_df['timestamp'], key=lambda x:abs(x-k))
            closest_list_year.append(closest_time)
        for n,k in enumerate(df['date']):
            closest_time = min(market_cap_df['timestamp'], key=lambda x:abs(x-k))
            closest_list.append(closest_time)
        year_dates_price = list(market_cap_df[market_cap_df['timestamp'].isin(closest_list_year)][::-1]['adjClose'])
        dates_price = list(market_cap_df[market_cap_df['timestamp'].isin(closest_list)][::-1]['adjClose'])
        dates_price_list = []
        for n,x in enumerate(closest_list):
            dates_price_list.append(list(market_cap_df[market_cap_df['timestamp'].isin([x])][::-1]['adjClose'])[0])
        year_dates_price_list = []
        for n,x in enumerate(closest_list_year):
            year_dates_price_list.append(list(market_cap_df[market_cap_df['timestamp'].isin([x])][::-1]['adjClose'])[0])
        df['Price'] = dates_price_list
        try:
            year_df['Price']=year_dates_price_list[::-1]
        except:
            year_df['Price']=np.nan
        price_json = np.nan_to_num(df[['date',"{}".format("Price")]].to_numpy()).tolist()[::-1]
    except Exception as e:
        price_json = []
    import json
    from urllib.request import urlopen
    try:
        fmp_url = ""#"https://financialmodelingprep.com/api/v3/quote/{}?apikey=4b5cd112b74ca86811fd1ccddd4ad9c1".format(url_symbol.upper())
        fmp_json = json.loads(urlopen(fmp_url, timeout=0.001).read().decode('utf-8'))
        last_price = np.round(fmp_json[0]['price'],2)
        last_pct_change = fmp_json[0]['changesPercentage']
        try:
            market_cap = np.round(fmp_json[0]['marketCap'],2)
            market_cap_str = magnitude_num(market_cap,currency_symbol)
        except:
            market_cap = '-'
            market_cap_str = '-'
        try:
            avg_volume = np.round(fmp_json[0]['avgVolume'],2)
        except:
            avg_volume = '-'
        try:
            avg_dolvol = np.round(fmp_json[0]['avgVolume'],2) * last_price
            avg_dolvol_str = magnitude_num(avg_dolvol,currency_symbol)
        except:
            avg_dolvol = '-'
            avg_dolvol_str = '-'
        try:
            avg_dolvol_pct_mcap = avg_dolvol/market_cap
        except:
            pass
        try:
            avg_vol_vs_pct_outstanding = avg_volume/np.round(fmp_json[0]['sharesOutstanding'],2)
        except:
            pass
        try:
            pct_shares_tradable = np.round(fmp_json[0]['sharesOutstanding'],2)*last_price/market_cap
        except:
            pct_shares_tradable = '-'
    except Exception as e:
        try:
            last_price = price_json[-1][1]
        except Exception as j:
            last_price=""
            # print("kmds",j)
        last_pct_change = 0
    try:
        last_price_json_timestamp  = price_json[-1][0]
    except:
        last_price_json_timestamp = ""
    price_json = price_json[0:(len(price_json)-1)]
    price_json.append([last_price_json_timestamp,last_price])
    first_price = price_json[0][1]
    df_tall = year_df[::-1]
    # print("kk2")
    df_tall['Year'] = "4/1/" + df_tall['Year']
    df_tall['Stock Price'] = df_tall['Price'].apply(lambda x: "${:,}".format(np.round(x,2)))
    df_tall['YoY Price % Change float'] = df_tall['{}'.format("Price")]/df_tall['{}'.format("Price")].shift(-1)
    # print("kk4")
    df_tall['YoY % Change (Stock Price)'] = df_tall['YoY Price % Change float'].apply(lambda x: "{}%".format(round((x-1)*100,1)))
    # print("fin_statements_list", fin_statements_list, "xsazxd", statement_or_ratio)
    if "{}".format(statement_or_ratio) in fin_statements_list:
        df_tall['YoY % Change float'] = df_tall['{}'.format(fin_metric_title)]/df_tall['{}'.format(fin_metric_title)].shift(-1)
        df_tall['YoY % Change'] = df_tall['YoY % Change float'].apply(lambda x: "{}%".format(round((x-1)*100,1)))
        # print("kk3")
        df_html_tall = df_tall[['{}'.format('Year'),'{}'.format(fin_metric_title),'YoY % Change',"Stock Price", 'YoY % Change (Stock Price)']]
        # print("df_html_tall", df_html_tall.head(30))
        # df_html_tall['{}'.format(fin_metric_title)] = df_html_tall['{}'.format(fin_metric_title)].fillna(0)
        df_html_tall = df_html_tall.fillna(0)
        # print(df_html_tall.head(30))
        if df_html_tall['{}'.format(fin_metric_title)].max()>abs(1000000):
            df_html_tall['{}'.format(fin_metric_title)] = df_html_tall['{}'.format(fin_metric_title)]/1000000
            if_in_mil = "in {} million".format(currency_symbol)
            df_html_tall['{}'.format(fin_metric_title)] = df_html_tall['{}'.format(fin_metric_title)].apply(lambda x: "${:,}".format(int(x)))
        else:
            # df_html_tall['{}'.format(fin_metric_title)] = df_html_tall['{}'.format(fin_metric_title)]/1000000
            if_in_mil = ""
            df_html_tall['{}'.format(fin_metric_title)] = df_html_tall['{}'.format(fin_metric_title)].apply(lambda x: "{:,}".format(np.round(x,2)))
        df_html_tall = df_html_tall.to_html(index=False)
        # full_path = csv_file.split(' ~ ')
        # path = pathlib.PurePath(full_path[0])
        df_html_formula = ""
    else:
        df_tall['YoY % Change float'] = df_tall['{}'.format(fin_metric_title)]/df_tall['{}'.format(fin_metric_title)].shift(-1)
        df_tall['YoY % Change'] = df_tall['YoY % Change float'].apply(lambda x: "{}%".format(round((x-1)*100,1)))
        original_list = ["Year",'{}'.format(fin_metric_title),'YoY % Change',"Stock Price", 'YoY % Change (Stock Price)']
        new_list = ["Year",'{}'.format(fin_metric_title),'YoY % Change',"Stock Price", 'YoY % Change (Stock Price)']
        # fin_metric_vars_old = ""
        for x in fin_metric_vars_old:
            # print("xfin_metric_vars_old", fin_metric_vars_old)
            df_tall[x] = df_tall[x].apply(lambda x: 4*x/1000000)
            # original_list.append(x)
            new_list.append(x)
        # flat_list = [item for sublist in new_list for item in sublist]
        # df_html_tall = df_tall[['{}'.format('Year'),'{}'.format(fin_metric_title),'YoY % Change',"Stock Price", 'YoY % Change (Stock Price)']]
        # print("jq", list(df_tall))
        # print("nq", new_list)
        df_html_tall = df_tall[original_list]
        df_html_formula = df_tall[new_list].to_html(index=False).replace('border="1" class="dataframe">','class="yoy_chrono_table" id="df_myTable" border="1" class="dataframe">').replace("\n","").replace('<tr style="text-align: right;">','<tr class="tr_header">')
        df_html_formula = df_html_formula.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
        df_html_formula = df_html_formula.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
        df_html_formula = df_html_formula.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')
        df_html_formula = df_html_formula.replace('nan%','')
        df_html_formula = df_html_formula.replace('border="1" class="dataframe">','class="yoy_chrono_table" id="df_myTable" border="1" class="dataframe">')
        df_html_formula = df_html_formula.replace("\n","").replace('<tr style="text-align: right;">','<tr class="tr_header">')
        df_html_formula = df_html_formula.replace("-inf%","-")
        df_html_formula = df_html_formula.replace("inf%","-")
        df_html_formula = df_html_formula.replace("[","")
        for x in fin_metric_vars_old:
            df_html_formula = df_html_formula.replace(x,x.replace("_"," "))
        # print("df_html_tall", df_html_tall.head(30))
        # df_html_tall['{}'.format(fin_metric_title)] = df_html_tall['{}'.format(fin_metric_title)].fillna(0)
        df_html_tall = df_html_tall.fillna(0)
        if df_html_tall['{}'.format(fin_metric_title)].max()>abs(1000000):
            df_html_tall['{}'.format(fin_metric_title)] = df_html_tall['{}'.format(fin_metric_title)]/1000000
            if_in_mil = "in {} million".format(currency_symbol)
            df_html_tall['{}'.format(fin_metric_title)] = df_html_tall['{}'.format(fin_metric_title)].apply(lambda x: "${:,}".format(int(x)))
        else:
            # df_html_tall['{}'.format(fin_metric_title)] = df_html_tall['{}'.format(fin_metric_title)]/1000000
            if_in_mil = ""
            df_html_tall['{}'.format(fin_metric_title)] = df_html_tall['{}'.format(fin_metric_title)].apply(lambda x: "{:,}".format(np.round(x,2)))
            df_tall["{}".format(fin_metric_title)] = df_tall["{}".format(fin_metric_title)].apply(lambda x: np.round(x,2))
        # df_html_tall = df_tall[['{}'.format('Year'),'{}'.format(fin_metric_title), 'YoY % Change',"Stock Price", 'YoY % Change (Stock Price)']]
        df_html_tall = df_html_tall.to_html(index=False)
    df_html_tall = df_html_tall.replace('border="1" class="dataframe">','class="yoy_chrono_table" id="df_myTable" border="1" class="dataframe">')
    df_html_tall = df_html_tall.replace("\n","").replace('<tr style="text-align: right;">','<tr class="tr_header">')
    df_html_tall = df_html_tall.replace("$nan","-")
    df_html_tall = df_html_tall.replace("-inf%","-")
    df_html_tall = df_html_tall.replace("inf%","-")
    df_html_tall = df_html_tall.replace("[","")
    # df_html_tall = df_html_tall.replace("_"," ")
    # df_html_tall = df_html_tall.replace('.00','')
    # df_html_tall = df_html_tall.replace('.0','')
    df_html_tall = df_html_tall.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
    df_html_tall = df_html_tall.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
    df_html_tall = df_html_tall.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')
    df_html_tall = df_html_tall[0:].replace(">nan</td>",">-</td>")
    df_html_tall = df_html_tall[0:].replace(">nan%</td>",">-</td>")
    df_html = df_html.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
    df_html = df_html.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
    df_html = df_html.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')
    # df_html = df_html.replace('<th class="th_fin_statement_class fin_statement_class">YoY % Change</th>      <th class="th_fin_statement_class fin_statement_class">Stock Price</th>', '<th class="th_fin_statement_class fin_statement_class">YoY % Change*</th>      <th class="th_fin_statement_class fin_statement_class">Stock Price</th>')
    total_seconds = time.time() - start_time
    present_num = magnitude_num((latest_metric),currency_symbol)
    labels = list(df['date'])
    df_table_html = df_html_tall.replace('<th class="th_fin_statement_class fin_statement_class">YoY % Change</th>      <th class="th_fin_statement_class fin_statement_class">Stock Price</th>', '<th class="th_fin_statement_class fin_statement_class">YoY % Change{}</th>      <th class="th_fin_statement_class fin_statement_class">Stock Price</th>'.format(min_max_warning))
    df_table_html = df_tall[['{}'.format(fin_metric_title)]].iloc[::-1].transpose().to_html()
    y_y = ((last_4_quarters/prev_4_quarters)-1)*100
    df_json  = np.nan_to_num(df[['date',"{}".format("quarter avg")]].to_numpy()).tolist()[::-1]
    y_y_chg = change_markup(y_y,"percent","arrow")
    earliest_date = pd.to_datetime(df.date).values.astype(np.int64)[-1]
    max_min_range = np.round(((max_metric - min_metric)/min_metric),2)
    max_min_range_str = change_markup(abs(max_min_range),"x","arrow","max_min_range_str")
    last_4_quarters_str = magnitude_num(last_4_quarters,currency_symbol)
    try:
        domain = domain #"http://127.0.0.1:5000" #"https://charts.tendollardata.com"
        subdomain = subdomain #"http://127.0.0.1:5000" #"http://127.0.0.1:5000"
        company_similar = profiles_dict['Similar Companies'].split(",")
        company_similar = [ x for x in company_similar if "XL" not in x ]
        company_similar_list = []
        company_similar_img_list = []
        n = 0
        while n < len(company_similar):
            x = company_similar[n]
            company_similar_x = ('<th class="similar_companies_names"><a class="similar_companies_urls" href="{}/{}-{}/{}/{}/{}">{}</a></th>, '.format(domain,x.lower().strip(),stock_or_etf,url_name,statement_or_ratio,url_fin_metric,x))
            company_similar_list.append(company_similar_x)
            company_similar_img = ('<td class="similar_companies_images"><a class="mcap_link a_similar_companies_images " href="{}/{}"><img class="lazy" src="{}/static/img/images-stocks/{}.png" width="40" height="40"  onerror=\'this.style.display = "none"\'>'.format(domain, x.strip().lower(), domain,x.strip().upper())+'</a></td>') 
            company_similar_img_list.append(company_similar_img)
            n+=1
        # company_similar_paragraph = Markup(''.join(company_similar_list)[:-2])

        similar_companies_table = "{}{}{}{}{}".format('<table class="tg"> <thead> <tr>',''.join(company_similar_list)[:-2], "</tr></thead><tbody><tr>",''.join(company_similar_img_list)[:-2], "</tr></tbody></table>")
        company_similar_paragraph = Markup(similar_companies_table).replace(",","").replace("","")
        # company_similar_paragraph = Markup('<table class="tg"> <thead> <tr>',''.join(company_similar_list)[:-2],"</tr></thead><tbody><tr>",''.join(company_similar_list_img_list)[:-2],"</tr></tbody></table>")
    except Exception as e:
        print("company_similar_zparagraph", e)
        company_similar_paragraph = ''
    year_df_json = np.nan_to_num(df[['date',"{}".format("repeater")]].to_numpy()).tolist()[::-1]
    import numbers
    position_last_value = next(x[0] for x in enumerate(list(df['repeater'])) if  len(str(x[1])) > 1)
    last_year_timestamp = year_df_json[(-position_last_value-1)][0]
    year_df_json = year_df_json[0:len(year_df_json)-position_last_value-1]
    year_df_json.append([last_year_timestamp,last_4_quarters])
    year_df_json = str(year_df_json).replace("''","null")
    year_df_json = str(year_df_json).replace("nan","null")
    df_json = str(df_json).replace("nan","null")
    try:
        prev_price = price_json[-5][1]
    except:
        prev_price = 1
    try:
        price_3_years_ago = price_json[-9][1]
    except:
        price_3_years_ago = 1
    try:
        price_4_years_ago = price_json[-13][1]
    except:
        price_4_years_ago = 1
    try:
        price_5_years_ago = price_json[-17][1]
    except:
        price_5_years_ago = 1
    all_time_price_chg_num = (last_price - first_price)/first_price
    all_time_price_chg = change_markup(100*(last_price - first_price)/first_price,"percent","noarrow","all_time_price_chg")
    all_time_price_chg_x = change_markup(-1+((last_price - first_price)/first_price),"x","arrow","all_time_price_chg")
    # print('last_price', 'first_price', 'historical_pct_chg', last_price, first_price, historical_pct_chg)
    # try:
    # except:
    #     # def reroute_404('last_price', 'first_price', 'historical_pct_chg', last_price, first_price, historical_pct_chg): # https://stackoverflow.com/questions/62533151/how-to-change-routes-in-flask
    #     @charts.route('/404', methods=['POST', 'GET']):
    #         def reroute_404('last_price', 'first_price', 'historical_pct_chg', last_price, first_price, historical_pct_chg): # https://stackoverflow.com/questions/62533151/how-to-change-routes-in-flask
    #             return render_template("404.html", message="Hello 404!", contacts=['last_price', 'first_price', 'historical_pct_chg', 'c4', 'c5']);
    #         # return render_template('404.html'), 404
    def if_error_value(test_number,default_value, test_validator=None):
        '''kkkkkkkkkk'''
        if test_validator is None:
            test_validator = test_number
        if isinstance(test_validator, (int, float, complex)):
            pass
            # if isinstance(test_number, (int, float, complex)):
            #     pass
        else:
            test_number = default_value
        return test_number
    def if_str_then_zero(test_string):
        if isinstance(test_string, (int, float, complex)):
            return test_string
        else:
            return 0
    def weird_division(n, d):
        if isinstance(n, (int, float, complex)) and isinstance(d, (int, float, complex)):
            return n / d if d else 0
        else:
            return 0
    def type_num_check(test_string):
        if isinstance(test_string, (int, float, complex)):
            return test_string
        else:
            return 0
    pct_chg_original = pct_chg
    pct_chg = type_num_check(pct_chg)
    price_metric_rate_change = if_error_value(weird_division((-1+((last_price - first_price)/first_price)),historical_pct_chg),0,pct_chg)
    # all_time_metric_chg = if_error_value(change_markup((round((pct_chg*100)-1, 1)),"percent","noarrow","all_time_metric_chg"),0,pct_chg)
    # print("pct_chg", pct_chg)
    # all_time_metric_chg = (change_markup((round((pct_chg*100)-1, 1)),"percent","noarrow","all_time_metric_chg"))
    all_time_metric_chg = if_error_value(change_markup((round((pct_chg*100)-1, 1)),"percent","noarrow","all_time_metric_chg"),0,pct_chg_original)
    historical_pct_chg = if_error_value((round(pct_chg-1, 1)),0,pct_chg_original)
    annual_pct_chg  = if_error_value((round(100*(pct_chg**(1/len(sorted_metric))-1),1)),0,pct_chg_original)
    hist_pct_chg_str = if_error_value(change_markup(historical_pct_chg,"x","arrow","hist_pct_chg_str"),0,pct_chg_original)
    annual_pct_chg_str = if_error_value(change_markup(annual_pct_chg,"percent","noarrow","annual_percent"),0,pct_chg_original)
    annual_pct_chg_10yrs_in_pct = if_error_value((100*(pct_chg**(1/len(sorted_metric)))**10)-1,0,pct_chg_original)
    annual_pct_chg_10yrs_in_abs = if_error_value(annual_pct_chg_10yrs_in_pct * latest_metric,0,pct_chg_original)
    annual_pct_chg_10yrs_in_stock = if_error_value(annual_pct_chg_10yrs_in_pct * last_price,0,pct_chg_original)
    growth_10_years = if_error_value(((annual_pct_chg+100)/100)**10,0,pct_chg_original)
    growth_10_years_str = if_error_value(change_markup(growth_10_years*100,"percent","noarrow","growth_10_years_str"),0,pct_chg_original)
    stock_price_10_years = if_error_value(np.round(last_price*growth_10_years,2),0,pct_chg_original)
    hist_pct_chg_str_no_arrow = if_error_value(change_markup(historical_pct_chg,"x","noarrow","hist_pct_chg_str_no_arrow"),0,pct_chg_original)
    last_pct_change_str  = if_error_value(change_markup(last_pct_change,"x","arrow","last_pct_change"),0,pct_chg_original)
    # if isinstance(pct_chg, (int, float, complex)):
    #     price_metric_rate_change = (-1+((last_price - first_price)/first_price))/historical_pct_chg
    #     all_time_metric_chg =change_markup((round((pct_chg*100)-1, 1)),"percent","noarrow","all_time_metric_chg")
    #     historical_pct_chg = (round(pct_chg-1, 1))
    #     annual_pct_chg  = (round(100*(pct_chg**(1/len(sorted_metric))-1),1))
    #     hist_pct_chg_str = change_markup(historical_pct_chg,"x","arrow","hist_pct_chg_str")
    #     annual_pct_chg_str = change_markup(annual_pct_chg,"percent","noarrow","annual_percent")
    #     annual_pct_chg_10yrs_in_pct = (100*(pct_chg**(1/len(sorted_metric)))**10)-1
    #     annual_pct_chg_10yrs_in_abs = annual_pct_chg_10yrs_in_pct * latest_metric
    #     annual_pct_chg_10yrs_in_stock = annual_pct_chg_10yrs_in_pct * last_price
    #     growth_10_years = ((annual_pct_chg+100)/100)**10
    #     growth_10_years_str = change_markup(growth_10_years*100,"percent","noarrow","growth_10_years_str")
    #     stock_price_10_years = np.round(last_price*growth_10_years,2)
    #     hist_pct_chg_str_no_arrow = change_markup(historical_pct_chg,"x","noarrow","hist_pct_chg_str_no_arrow")
    #     last_pct_change_str  = change_markup(last_pct_change,"x","arrow","last_pct_change")
    # else:
    #     pct_chg = 0
    #     price_metric_rate_change = 0
    #     all_time_metric_chg = 0
    #     annual_pct_chg_10yrs_in_pct = 0
    #     annual_pct_chg_10yrs_in_abs = 0
    #     annual_pct_chg_10yrs_in_stock = 0
    #     growth_10_years = 0
    #     growth_10_years_str = 0
    #     stock_price_10_years = 0
    #     hist_pct_chg_str_no_arrow = 0
    #     last_pct_change_str  = 0
    #     historical_pct_chg = 0
    #     annual_pct_chg  = 0
    #     hist_pct_chg_str = 0
    #     annual_pct_chg_str = 0
    price_metric_rate_change_str = change_markup(price_metric_rate_change,"x","noarrow","price_metric_rate_change")
    yoy_price_chg = 100*(last_price - prev_price)/prev_price
    yoy_price_chg = change_markup(yoy_price_chg,"percent","noarrow")
    first_price = np.round(first_price,2)
    last_price = np.round(last_price,2)
    currency_symbol = currency_symbol_original
    pos_or_neg = (df_tall['YoY % Change float']-1) * (df_tall['YoY Price % Change float']-1)
    metric_increased_years = df_tall[df_tall['YoY % Change float'] > 1]
    metric_decreased_years = df_tall[df_tall['YoY % Change float'] < 1]
    price_increased_years = df_tall[df_tall['YoY Price % Change float'] >= 1]
    price_increased_years_num = len(price_increased_years)
    # print("metric_increased_years", metric_increased_years)
    metric_increased_years_price_increased = df_tall[df_tall['YoY Price % Change float'] > 1]
    def if_error_value(test_number,default_value, test_validator=None):
        '''kkkkkkkkk'''
        if test_validator is None:
            pass
        elif isinstance(test_validator, (int, float, complex)):
            pass
        if test_validator == 0:
            test_number = default_value
        # elif not isinstance(test_validator, (str)):
        #     test_number = default_value
        #     # if isinstance(test_number, (int, float, complex)):
        #     #     pass
        # else:
        #     test_number = default_value
        return test_number
    num_years_increased = len(metric_increased_years)+1 # if_error_value(len(metric_increased_years)+1,0, metric_increased_years)
    num_years_increased = if_error_value(len(metric_increased_years)+1,0, len(metric_increased_years))
    # print("len(metric_increased_years)",len(metric_increased_years))
    num_years_bad = if_error_value(len(metric_decreased_years),0, len(metric_decreased_years))
    price_increased_on_metric_up_years = if_error_value(len(metric_increased_years[metric_increased_years['YoY Price % Change float']>1]),0, len(metric_increased_years))
    percent_correlation = weird_division(price_increased_on_metric_up_years*100,num_years_increased)
    percent_correlation = if_error_value(percent_correlation,0, len(metric_increased_years))
    num_years_increased_price = len(metric_increased_years_price_increased)
    difference = num_years_increased - price_increased_years_num
    percent_correlation_str = ("{}%".format(int(percent_correlation)))
    percent_correlation_str = change_markup(int(percent_correlation),"percent","noarrow","percent_correlation_str")
    # print("df_json ", df_json)
    # pd.DataFrame({"df_json":df_json}).to_csv("df_json.csv")
    # Markup('** A modified method (see: <a href="https://math.stackexchange.com/questions/716767/how-to-calculate-the-percentage-of-increase-decrease-with-negative-numbers/716770">here</a>) is used to calculate change, since the bottom/peak contains a negative number.')
    try:
        split_input = profiles_dict['description'].split(".")
        pass_index = -100
        sentence_list = []
        for n,x in enumerate(split_input):
            # print(pass_index)
            if pass_index == n+1:
                pass
            else:
                if (len(x))<30:
                    try:
                        sentence = x+split_input[n+1]+"."
                    except:
                        sentence = x+"."
                    sentence = x
                    pass_index = n+1
                    sentence = ("<li span='description_list'>{}</li>".format(sentence))
                    sentence_list.append(sentence)
                else:
                    sentence = x+"."
                    sentence = ("<li span='description_list'>{}</li>".format(sentence))
                    sentence_list.append(sentence)
            # print(n,sentence)
        sentences_list_joined = Markup("".join(sentence_list[:-1]))
        html_sentence_list = sentences_list_joined #Markup("<ul>"+sentences_list_joined+"</ul>")
    except:
        sentence = profiles_dict['description']
        sentence = ("<li span='description_list'>{}</li>".format(sentence))
        html_sentence_list = Markup(sentence)
    # print("this", html_sentence_list)
    company_long_name = profiles_dict['long name']
    company_symbol = profiles_dict['symbol']
    # df_image_name = Markup('<a class="mcap_link" href="{}/{}"><table class="mini_table"><thead class="mini_thead"><tr class="mini_tr"><th class="mcap_image"  rowspan="2"><img class="lazy" src="{}/static/img/images-stocks/{}.png" width="30" height="30"></th><th class="mcap_symbol">'.format(domain, company_symbol, domain,company_symbol)+company_symbol+'</th></tr><tr class="mini_tr2"><td class="mcap_name">' +company_long_name+'</td></tr></thead></table></a>')
    df_image_name = Markup('<a class="mcap_link" href="{}/{}"><img class="lazy" src="{}/static/img/images-stocks/{}.png" width="40" height="40">'.format(domain, company_symbol.lower(), domain,company_symbol.upper())+'</a>')
    return render_template('current_ratio.html', \
                            main_page_y_n = main_page_y_n,
                            chart_type = chart_type,
                            # fs_table_pct = fs_table_pct,
                            balance_sheet = balance_sheet,
                            cash_flow = cash_flow,
                            income_statement = income_statement,
                            versus_chart_y_n = versus_chart_y_n,
                            yoy_1_key = list(yoy_cards_dict.items())[0][0],
                            yoy_1_value = list(yoy_cards_dict.items())[0][1],
                            df_image_name = df_image_name,
                            earliest_latest_warning = earliest_latest_warning,\
                            yoy_cards_html_joined = yoy_cards_html_joined,\
                            earliest_latest_disclaimer = earliest_latest_disclaimer,\
                            df_html_formula = [df_html_formula],\
                            url_symbol = url_symbol,\
                            min_max_warning = min_max_warning,\
                            min_max_disclaimer = min_max_disclaimer,\
                            if_in_mil = if_in_mil,\
                            domain = domain,\
                            subdomain = subdomain,\
                            fin_metric_definition_formula = fin_metric_definition_formula,\
                            company_symbol = profiles_dict['symbol'],\
                            difference = difference,\
                            percent_correlation = percent_correlation,\
                            percent_correlation_str = percent_correlation_str,\
                            price_increased_on_metric_up_years = price_increased_on_metric_up_years,\
                            price_metric_rate_change = price_metric_rate_change,\
                            price_metric_rate_change_str = price_metric_rate_change_str,\
                            price_increased_years_num = price_increased_years_num,\
                            all_time_price_chg_num = all_time_price_chg_num,\
                            stock_price_10_years = stock_price_10_years,\
                            growth_10_years_str = growth_10_years_str,\
                            num_years_bad = num_years_bad,\
                            hist_pct_chg_str_no_arrow = hist_pct_chg_str_no_arrow,\
                            annual_pct_chg_10yrs_in_pct = annual_pct_chg_10yrs_in_pct,\
                            annual_pct_chg_10yrs_in_abs = annual_pct_chg_10yrs_in_abs,\
                            annual_pct_chg_10yrs_in_stock = annual_pct_chg_10yrs_in_stock,\
                            last_pct_change_str = last_pct_change_str,\
                            first_price = first_price,\
                            last_price = last_price,\
                            all_time_metric_chg = all_time_metric_chg,\
                            all_time_price_chg = all_time_price_chg,\
                            all_time_price_chg_x = all_time_price_chg_x,\
                            pct_chg = str(pct_chg),\
                            pct_chg_num = pct_chg,\
                            yoy_price_chg = str(yoy_price_chg),\
                            last_4_quarters = last_4_quarters,\
                            last_4_quarters_str = last_4_quarters_str,\
                            y_y_chg=y_y_chg,\
                            price_json = price_json,\
                            company_long_name = profiles_dict['long name'],\
                            company_currency = profiles_dict['currency'],\
                            currency_symbol = currency_symbol,\
                            company_exchange = profiles_dict['exchange'],\
                            company_industry = profiles_dict['industry'],\
                            company_description = profiles_dict['description'],\
                            company_sector = profiles_dict['sector'],\
                            company_country = profiles_dict['country'],\
                            company_ipo_date = profiles_dict['ipo date'],\
                            company_short_name = profiles_dict['shortest name'],
                            company_industries = profiles_dict['Industries'],\
                            company_url_name = profiles_dict['url name'],\
                            company_similar = company_similar_paragraph,
                            html_sentence_list = html_sentence_list,\
                            historical_pct_chg = historical_pct_chg,\
                            hist_pct_chg_str = hist_pct_chg_str,\
                            lifetime_sum_all_metric = lifetime_sum_all_metric,\
                            mean_str = mean_str,\
                            max_str = max_str,\
                            min_str = min_str,\
                            max_min_range_str = max_min_range_str,\
                            std_dev_str = std_dev_str,\
                            std_dev_abs_str = std_dev_abs_str,\
                            bottom_25_str = bottom_25_str,\
                            top_25_str = top_25_str,\
                            earliest_year = earliest_year,\
                            latest_year = latest_year,\
                            previous_year = previous_year,\
                            earliest_metric_str = earliest_metric_str,\
                            latest_metric_str = latest_metric_str,\
                            present_num = present_num,\
                            max_min_pct_diff_str = max_min_pct_diff_str,
                            df_bs_table_html = [df_table_html],
                            # df_html_tall = [df_html_tall],\
                            df_html_tall = [df_html_tall.replace('<th class="th_fin_statement_class fin_statement_class">YoY % Change</th>      <th class="th_fin_statement_class fin_statement_class">Stock Price</th>', '<th class="th_fin_statement_class fin_statement_class">YoY % Change{}</th>      <th class="th_fin_statement_class fin_statement_class">Stock Price</th>'.format(min_max_warning))],
                            fin_metric_name = fin_metric_title,\
                            df_date = df['date'].to_list(),\
                            df_json  = df_json,\
                            year_df_json = year_df_json,\
                            df_json_date_year = df_json_date_year,\
                            table_pct = [df_pct],\
                            tables=[df_html],\
                            titles=df.columns.values,\
                            total_time=total_seconds,\
                            place_name=url_symbol,\
                            max=17000,\
                            labels=labels,\
                            annual_pct_chg = annual_pct_chg,\
                            annual_pct_chg_str = annual_pct_chg_str,\
                            statement_or_ratio = statement_or_ratio,\
                            num_years_increased = num_years_increased,\
                            num_years = len(year_df),\
                            )
# https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/
# https://flask.palletsprojects.com/en/1.1.x/errorhandling/
# https://flask.palletsprojects.com/en/master/errorhandling/
# https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling
@charts.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
# @route("hello_world")
# def render():
#     return "Hello World"
# @charts.route('/test/<url_symbol>', methods=['POST', 'GET'])
# def fin_test(url_symbol):
#     return render_template('financial_statements.html',
#      df_html=FS("IS","AAPL"),#.df_html(),
#      tables=FS("IS","AAPL").df_values()['df_table'],
#      table_pct = FS("IS","AAPL").df_values()['df_table_pct'],
#      df_date = FS("IS","AAPL").df_values()['chart_x_dates'],
#      df_rev = FS("IS","AAPL").df_values()['chart_y_revenue'],
#      df_json = FS("IS","AAPL").df_values()['df_json'],
#      titles=FS("IS","AAPL").df_values()['df_titles'],
#      labels = FS("IS","AAPL").df_labels(),
#      values=FS("IS","AAPL").df_price(),
#      place_name=url_symbol, max=17000,
#      )
# @charts.route('/test/<some_place>', methods=['POST', 'GET'])
# # @cache.cached(timeout=5)
# def fin_test(some_place):
#     # values = list(FS("IS","AAPL")['Beginning Price'])[0:19]
#     return render_template('financial_statements.html',
#     # return render_template('fin_statements_bootstrapped.html',
#     # return render_template('fin_statements_bootstrapped_w_comments.html',
#     # FS("IS","AAPL").df_values()['df_table']
#     # FS("IS","AAPL").df_values()['df_table_pct']
#     # FS("IS","AAPL").df_values()['chart_x_dates']
#     # FS("IS","AAPL").df_values()['chart_y_revenue']
#     # FS("IS","AAPL").df_values()['df_json']
#     # FS("IS","AAPL").df_values()['df_titles']
#      tables=FS("IS","AAPL").df_values()['df_table'],
#      table_pct = FS("IS","AAPL").df_values()['df_table_pct'],
#      df_date = FS("IS","AAPL").df_values()['chart_x_dates'],
#      df_rev = FS("IS","AAPL").df_values()['chart_y_revenue'],
#      df_json = FS("IS","AAPL").df_values()['df_json'],
#      titles=FS("IS","AAPL").df_values()['df_titles'],
#      labels = FS("IS","AAPL").df_labels(),
#      values=FS("IS","AAPL").df_price(),
#      place_name=some_place, max=17000,
#      )
# https://github.com/nvdv/vprof/blob/master/examples/guestbook.py
# http://pramodkumbhar.com/2019/05/summary-of-python-profiling-tools-part-i/
# @charts.route('/<url_symbol>-<stock_or_etf>/<url_name>/<statement_or_ratio>/<url_fin_metric>', methods=['POST', 'GET'])
# def current_ratio(url_fin_metric,stock_or_etf,url_name,statement_or_ratio,url_symbol):
# @charts.route('/profile/<uri>', methods=['GET', 'POST'])
# def profiler_handler(uri):
#     """Profiler handler."""
#     # HTTP method should be GET.
#     if uri == 'main':
#         runner.run(current_ratio(url_fin_metric,stock_or_etf,url_name,statement_or_ratio,url_symbol), 'cmhp')
#     # In this case HTTP method should be POST singe add_entry uses POST
#     elif uri == 'add':
#         runner.run(current_ratio(url_fin_metric,stock_or_etf,url_name,statement_or_ratio,url_symbol), 'cmhp')
    return flask.redirect('/')
