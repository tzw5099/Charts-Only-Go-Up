# pyright: reportUnusedVariable=false, reportUnusedImport=false
# https://github.com/microsoft/pylance-release/blob/main/DIAGNOSTIC_SEVERITY_RULES.md
# https://damyan.blog/post/flask-series-optimizations/
# https://github.com/muatik/flask-profiler
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
@charts.route('/', methods=['POST', 'GET'])
@charts.route("/home")
def index():
    return render_template('index.html')
@charts.route('/<url_symbol>-<stock_or_etf>/<url_name>/<statement_or_ratio>/<url_fin_metric>', methods=['POST', 'GET'])
@charts.route('/<url_symbol>-<stock_or_etf>/nice/<url_name>/<statement_or_ratio>/<url_fin_metric>', methods=['POST', 'GET'])

def current_ratio(url_fin_metric,stock_or_etf,url_name,statement_or_ratio,url_symbol):
    from route_imports.ratio_map import metric_to_url_map
    from route_imports.ratio_map import url_to_var_name_map
    from route_imports.ratio_map import url_to_name_map
    from route_imports.ratio_map import fin_statement_raw_names
    from route_imports.ratio_map import fin_statement_renamed_cols
    from route_imports.ratio_map import metric_to_formula_map
    from route_imports.ratio_map import url_to_metric_map
    from route_imports.ratio_map import url_to_equation_map
    from route_imports.ratio_map import url_to_definition_map
    # from route_imports.ratio_map import income_statement_dict
    # from route_imports.ratio_map import balance_sheet_dict
    # from route_imports.ratio_map import cash_flow_dict
    # metric to url mapping
    income_statement_dict = [
        # 'index',
        'Unnamed: 0',
                            'date',
                            'symbol',
                            'filing_date',
                            'accepted_date',
                            'period',
'net_revenue',
'cost_of_sales',
'gross_profit_margin_non',
'gross_profit_margin_ratio',
'r_n_d',
'g_n_a',
's_n_m',
'other_income',
'total_opex',
'cost_expenses',
'interest_expense',
'd_n_a',
'ebitda_non',
'ebitda_margin',
'operating_income',
'operating_margin',
'total_other_income',
'pretax_income_non',
'pretax_income_margin',
'income_tax_expense',
'net_income',
'profit_margin',
'eps_non',
'eps_diluted',
'shares_outstanding_non',
'shares_outstanding_diluted',
'sec_filing_link',
'sec_statement_link',
                            ]

    balance_sheet_dict = [
        # 'index',
        'Unnamed: 0',
                        'date',
                        'symbol',
                        'filing_date',
                        'accepted_date',
                        'period',
'cash_non',
'short_term_investments',
'cash_n_short_term_investments',
'accounts_receivable',
'inventory',
'other_current_assets',
'total_current_assets',
'pp_n_e',
'goodwill',
'intangible_assets',
'goodwill_n_intangible_assets',
'long_term_investments',
'tax_assets',
'other_non_current_assets',
'tol_non_current_assets',
'other_assets',
'total_assets',
'accounts_payable',
'short_term_debt',
'income_tax_payables',
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
'accumulated_other_comprehensive_income',
'other_se',
'total_se',
'total-liabilities-and-stockholders-equity',
'total_investments',
'total_debt',
'net_debt',
'sec_filing_link',
'sec_statement_link',]

    cash_flow_dict = [
        # 'index',
        'Unnamed: 0',
                    'date',
                    'symbol',
                    'filing_date',
                    'accepted_date',
                    'period',
'net_income',
'd_n_a',
'deferred_income_tax',
'sbc',
'change_in_working_capital',
'accounts_receivable',
'inventory',
'accounts_payable',
'other_working_capital',
'other_non_cash_items',
'net_cash_by_operating_activities',
'investments_in_pp_n_e',
'acquisitions_net',
'purchase_of_investments',
'sales_maturities_of_investments',
'other_investing_activities',
'net_cash_used_for_investing_activities',
'debt_repayment',
'common_stock_issued',
'common_stock_repurchased',
'dividends_paid',
'other_financing_activities',
'net_cash_used_provided_by_financing_activities',
'effect_of_fx_rate_changes_on_cash',
'net_change_in_cash',
'cash_at_end_of_period',
'cash_at_beginning_of_period',
'operating_cash_flow',
'capex',
'free_cash_flow',
'sec_filing_link',
'sec_statement_link',]
    from flask import Markup
    start_time = time.time()
    # titles_list = ['Date','Symbol','Filing Date','Accepted Date','Period','SEC Filing Link']
    titles_list = ['Selling, General and Administrative (SG&A)','Selling General and Administrative (SG&A)', "EBITDA Margin", "Operating Margin" ,"Profit Margin"]
    vars_drop = ['quarter_n_year',  's_g_n_a', "ebitda_margin", "operating_margin","profit_margin"]
    def weird_division(n, d):
        return n / d if d else 0
    def magnitude_num(number, currency_symbol):
        try:
            if len(str(number)) > 12 and number > 1000000000000:
                magnitude = number/1000000000000
                magnitude_str = "{}{}{}".format(currency_symbol,round(magnitude,1),"T")
            elif len(str(number)) > 9 and number > 1000000000:
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
                magnitude_str = "-{}{}{}".format(currency_symbol,round(magnitude,1)," Billion")
            elif len(str(number)) > 6 and number < -1000000:
                magnitude = abs(number/1000000)
                magnitude_str = "-{}{}{}".format(currency_symbol,round(magnitude,1)," Million")
            elif len(str(number)) > 3 and number < -1000:
                magnitude = abs(number/1000)
                magnitude_str = "-{}{}{}".format(currency_symbol,round(magnitude,1)," Thousand")
            else:
                magnitude = number
                magnitude_str = "{}{}{}".format("",round(magnitude,2),"")
        except Exception as e:
            magnitude = number
            magnitude_str = number
        return magnitude_str
    def change_markup(change,percent_or_x,arrow_no_arrow = "arrow", css_class = "change_markup"):
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
                    change_html = Markup("{}+{}%{}".format(up_green_prefix, change_comma, up_green_suffix))
                elif change<0:
                    change_html = Markup("{}{}%{}".format(down_red_prefix, change_comma, down_red_suffix))
                else:
                    change_html = "-"
            elif percent_or_x == "x":
                if change==0:
                    change_html = "0%"
                elif change>0:
                    change_html = Markup("{}+{}x{}".format(up_green_prefix, change, up_green_suffix))
                elif change<0:
                    change_html = Markup("{}{}x{}".format(down_red_prefix, change, down_red_suffix))
                else:
                    change_html = "-"
            else:
                change_html = '-'
        except Exception as e:
            change_html = '-'
        return change_html
    fin_statements_list = ["income-statement","balance-sheet","cash-flow-statement"]
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
    fin_statements_matching = pd.read_csv("reference_data/Financial_Statements_Reference_Matching.csv")
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
        csv_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/quarter/{}/*~{}~*".format(fin_statement_dir, url_symbol.upper()))[-1]
        year_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/{}/*~{}~*".format(fin_statement_dir, url_symbol.upper()))[-1]
        year_df_file = (pd.read_csv(year_file))
        df = pd.read_csv(csv_file)
        matching_row = fin_statements_matching[fin_statements_matching['URL']=="{}".format(url_fin_metric)]
        fin_metric_title = list(matching_row['Title'])[0]
        fin_metric_vars = list(matching_row['Python Variable Name'])
        fin_metric_name = list(matching_row['Name'])[0]
        fin_metric_definition = list(matching_row['Definition / Formula'])[0]
        len_not_na_df = len(df[df['{}'.format(fin_metric_name)]==0]) #df['{}'.format(fin_metric_name)].notna().sum()
        len_not_na_year_df =  len(year_df_file[year_df_file['{}'.format(fin_metric_name)]==0]) #year_df_file['{}'.format(fin_metric_name)].notna().sum()
        # print("len df", len(df), "len year df", len(year_df_file), "len_not_na_df", len_not_na_df, "len_not_na_year_df", len_not_na_year_df)
        if len(year_df_file)*3 > len(df):
            df = year_df_file
            all_titles = list(df)
            all_numbers_df = df[list(df.select_dtypes(include=['float','int64']))].div(4, axis=0)
            all_objects_df = df[list(df.select_dtypes(include=['object']))]
            concat_df = pd.concat([all_numbers_df, all_objects_df], axis=1)
            df = concat_df[all_titles]
            list_years = list(df["date"].apply(lambda j: j[0:4]))
            if len(list_years) > len(list(set(list_years))):
                list_years = np.arange(list_years.min(),list_years.max()+2)
            new_df_list = []
            for n,y in enumerate(list_years):
                for x in ["12-31","03-31","06-30","09-30"]:
                    new_df = df[n:n+1]
                    new_df['date'] = pd.to_datetime("{}-{}".format(y,x))
                    new_df_list.append(new_df)
            df = pd.concat(new_df_list).sort_values(by="date",ascending = True).reset_index()
            df['date'] = df['date'].apply(lambda x: str(x)[0:10])
        df["Year"] = df["date"].apply(lambda x: x[0:4])
        # print("sup1")
        df["QQ-YYYY"] = df["period"]+"-"+df["date"].apply(lambda x: x[0:4])
        # else:
            # pass
        # xxx   if len_not_na_year_df + 2 > len(year_df_file):
        #         smart_data_warning = "*"
        #         smart_data_disclaimer = Markup('<span class="ruhroh disclaimer_zero">** The data has been enhanced for easier insights</span>')
        if len(df[df['{}'.format(fin_metric_name)]<0]) > len(df[df['{}'.format(fin_metric_name)]>0]):
            pass
            # print("negative now", df[['{}'.format(fin_metric_name),"QQ-YYYY" ]])
            # df['{}'.format(fin_metric_name)] = df['{}'.format(fin_metric_name)]*-1 #.apply(lambda x: -1*x)
            # print("negative now", df[['{}'.format(fin_metric_name),"QQ-YYYY" ]])
        else:
            pass
        fin_metric_equation = ""
        df = df.sort_values(by="date",ascending = False)
        early_missing_periods = df[::-1]["{}".format(fin_metric_name)].ne(0).idxmax()
        df = df[0:early_missing_periods+1]
        # print("sup2")
        def groupby_agg(df):
            if "{}".format(statement_or_ratio) == "income-statement":
                df_grouped = df.groupby("Year").sum()
            elif "{}".format(statement_or_ratio) == "balance-sheet":
                df_grouped = df.groupby("Year").mean()

            elif "{}".format(statement_or_ratio) == "cash-flow-statement":
                df_grouped = df.groupby("Year").sum()
            else:
                df_grouped = df.groupby("Year").sum()
            return df_grouped
    else:
        fin_metric_definition_formula = ""
        metric_to_list_variables_map = {
                'net_working_capital_ratio':['working_capital_math','total_assets',],
                'book_value_per_share':['total_se','shares_outstanding_non',],
                'total_equity_to_total_assets':['total_se','total_assets',],
                'roa_cash_flow': ['operating_cash_flow','total_assets',],
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
                'pre_tax_return_on_common_equity':['pretax_income_non','common_equity',],
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
                'accounts_receivableturnover':['net_revenue','accounts_receivable',],
                'operating_cash_flow_to_debt':['net_revenue','total_se',],
                'inventory_ratio':['net_revenue','inventory',],
                'return_on_investment':['net_income','interest_expense','total_se','long_term_debt',],
                'pretax_margin':['net_income','income_tax_expense','net_revenue',],
                'income_to_net_worth_ratio':['net_income','deferred_income_tax','shares_outstanding_non',],
                'return_on_assets_roa':['net_income','total_assets',],
                'roe':['net_income','total_se',],
                'profit_margin':['net_income','net_revenue',],
                'earnings_per_share':['net_income','shares_outstanding_non',],
                'current_cash_debt_coverage':['net_cash_by_operating_activities','total_current_liabilities',],
                'cash_debt_coverage':['net_cash_by_operating_activities','total_liabilities',],
                'long_term_debt_ratio':['long_term_debt','total_assets',],
                'long_term_debt_equity_ratio':['long_term_debt','total_se',],
                'lt_debt_as_pct_of_total_debt':['long_term_debt','total_liabilities',],
                'inventory_pct_of_revenue':['inventory','net_revenue',],
                'intangibles_pct_of_book_value':['goodwill_n_intangible_assets','total_se',],
                'ffo_funds_from_operations_to_debt':['ffo_math','total_debt',],
                'operating_margin':['ebitda_non','d_a','net_revenue',],
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
        metric_name = url_to_metric_map["{}".format(url_fin_metric)]
        fin_metric_equation = url_to_equation_map["{}".format(url_fin_metric)]
        fin_metric_definition = url_to_definition_map["{}".format(url_fin_metric)]
        fin_metric_title = url_to_name_map[url_fin_metric]
        # fin_metric_vars = fin_metric_title
        fin_metric_name = url_to_var_name_map[url_fin_metric]
        # fin_metric_vars = metric_to_list_variables_map[fin_metric_name] # NOTE: sdfsdf
        fin_metric_vars_old = metric_to_list_variables_map[fin_metric_name] # NOTE: sdfsdf
        fin_metric_vars = [fin_metric_title]
        fin_dir = ["Income Statement","Balance Sheet","Cash Flow Statement"]
        fin_df_list = []

        for the_statement in fin_dir:

            # csv_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/quarter/{}/*~{}~*".format(x, url_symbol.upper()))[-1]
            fin_file_year = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/{}/*~{}~*".format(the_statement, url_symbol.upper()))[-1]
            # fin_df = pd.read_csv(csv_file)
            df = pd.read_csv(fin_file_year)
            print("list df",list(df))
            # if len(year_df_file) > len(fin_df):
            #     df = year_df_file

            df = df.interpolate()
            print("yowza", list(df))


            if "{}".format(the_statement) == "Income Statement":
                df.columns = income_statement_dict

                for x in fin_metric_vars_old:
                    try:
                        print("gonna try")
                        df['pct_chg_temp'] = df['{}'.format(x)]/df['{}'.format(x)].shift(-1)
                        # print(list(df['pct_chg_temp']))

                        df['pct_chg_temp'].values[df['pct_chg_temp'] > 10] = np.nan
                        # print("df['pct_chg_temp']")
                        # print(list(df['pct_chg_temp']))
                        # # df.loc[df['foo'].isnull(),'foo'] = df['bar']
                        # df.loc[df['pct_chg_temp'],np.nan] = df['{}'.format(x)]


                        df['{}'.format(x)][df['pct_chg_temp'] == np.nan] = np.nan


                        df.to_csv("tisktisk20.csv")
                        df = df.drop(['pct_chg_temp'],axis=1)
                        # print("x title list",x, fin_metric_title, list(df))
                        # df['{}'.format(x)] = df['{}'.format(x)].fillna(dzf['{}'.format(x)].rolling(window=8,center=True,min_periods=1).mean())
                        df['{}'.format(x)] = df['{}'.format(x)].replace(0, np.nan)
                        df['{}'.format(x)] = df['{}'.format(x)].replace(np.inf, np.nan)
                        # if len(df[df['{}'.format(x)]<0]) > len(df[df['{}'.format(x)]>0]):
                        #     df['{}'.format(x)] = df['{}'.format(x)]*-1 #.apply(lambda x: -1*x)
                        # else:
                        #     pass
                        n = 0
                        # df['{}'.format(x)] = df['{}'.format(x)].mask(df['{}'.format(x)].between(-np.inf, 0.000000001))

                        # df['{}'.format(x)] = df['{}'.format(x)].fillna(dzf['{}'.format(x)].rolling(window=8,center=True,min_periods=1).mean())
                        df['{}'.format(x)] = df['{}'.format(x)].replace(0, np.nan)
                        df['{}'.format(x)] = df['{}'.format(x)].replace(np.inf, np.nan)
                        # print("qaz ", df['{}'.format(x)].head(50),2)
                        print("nsada")


                        df = df.interpolate()
                    except Exception as e:
                        print("e x", e)
            elif "{}".format(the_statement) == "Balance Sheet":
                df.columns = balance_sheet_dict
                for x in fin_metric_vars_old:
                    try:
                        print("gonna try")
                        df['pct_chg_temp'] = df['{}'.format(x)]/df['{}'.format(x)].shift(-1)
                        # print(list(df['pct_chg_temp']))

                        df['pct_chg_temp'].values[df['pct_chg_temp'] > 10] = np.nan
                        # print("df['pct_chg_temp']")
                        # print(list(df['pct_chg_temp']))
                        # # df.loc[df['foo'].isnull(),'foo'] = df['bar']
                        # df.loc[df['pct_chg_temp'],np.nan] = df['{}'.format(x)]


                        df['{}'.format(x)][df['pct_chg_temp'] == np.nan] = np.nan


                        df.to_csv("tisktisk20.csv")
                        df = df.drop(['pct_chg_temp'],axis=1)
                        # print("x title list",x, fin_metric_title, list(df))
                        # df['{}'.format(x)] = df['{}'.format(x)].fillna(dzf['{}'.format(x)].rolling(window=8,center=True,min_periods=1).mean())
                        df['{}'.format(x)] = df['{}'.format(x)].replace(0, np.nan)
                        df['{}'.format(x)] = df['{}'.format(x)].replace(np.inf, np.nan)
                        # if len(df[df['{}'.format(x)]<0]) > len(df[df['{}'.format(x)]>0]):
                        #     df['{}'.format(x)] = df['{}'.format(x)]*-1 #.apply(lambda x: -1*x)
                        # else:
                        #     pass
                        n = 0
                        # df['{}'.format(x)] = df['{}'.format(x)].mask(df['{}'.format(x)].between(-np.inf, 0.000000001))

                        # df['{}'.format(x)] = df['{}'.format(x)].fillna(dzf['{}'.format(x)].rolling(window=8,center=True,min_periods=1).mean())
                        df['{}'.format(x)] = df['{}'.format(x)].replace(0, np.nan)
                        df['{}'.format(x)] = df['{}'.format(x)].replace(np.inf, np.nan)
                        # print("qaz ", df['{}'.format(x)].head(50),2)
                        print("nsada")


                        df = df.interpolate()
                    except Exception as e:
                        print("e x", e)
            elif "{}".format(the_statement) == "Cash Flow Statement":
                df.columns = cash_flow_dict
                for x in fin_metric_vars_old:
                    try:
                        print("gonna try")
                        df['pct_chg_temp'] = df['{}'.format(x)]/df['{}'.format(x)].shift(-1)
                        # print(list(df['pct_chg_temp']))

                        df['pct_chg_temp'].values[df['pct_chg_temp'] > 10] = np.nan
                        # print("df['pct_chg_temp']")
                        # print(list(df['pct_chg_temp']))
                        # # df.loc[df['foo'].isnull(),'foo'] = df['bar']
                        # df.loc[df['pct_chg_temp'],np.nan] = df['{}'.format(x)]


                        df['{}'.format(x)][df['pct_chg_temp'] == np.nan] = np.nan


                        df.to_csv("tisktisk20.csv")
                        df = df.drop(['pct_chg_temp'],axis=1)
                        # print("x title list",x, fin_metric_title, list(df))
                        # df['{}'.format(x)] = df['{}'.format(x)].fillna(dzf['{}'.format(x)].rolling(window=8,center=True,min_periods=1).mean())
                        df['{}'.format(x)] = df['{}'.format(x)].replace(0, np.nan)
                        df['{}'.format(x)] = df['{}'.format(x)].replace(np.inf, np.nan)
                        # if len(df[df['{}'.format(x)]<0]) > len(df[df['{}'.format(x)]>0]):
                        #     df['{}'.format(x)] = df['{}'.format(x)]*-1 #.apply(lambda x: -1*x)
                        # else:
                        #     pass
                        n = 0
                        # df['{}'.format(x)] = df['{}'.format(x)].mask(df['{}'.format(x)].between(-np.inf, 0.000000001))

                        # df['{}'.format(x)] = df['{}'.format(x)].fillna(dzf['{}'.format(x)].rolling(window=8,center=True,min_periods=1).mean())
                        df['{}'.format(x)] = df['{}'.format(x)].replace(0, np.nan)
                        df['{}'.format(x)] = df['{}'.format(x)].replace(np.inf, np.nan)
                        # print("qaz ", df['{}'.format(x)].head(50),2)
                        print("nsada")


                        df = df.interpolate()
                    except Exception as e:
                        print("e x", e)

            all_titles = list(df)
            # all_numbers_df = df[list(df.select_dtypes(include=['float','int64']))].div(4, axis=0)
            for t in fin_metric_vars_old:
                try:
                    print("sick", t, x)
                    all_numbers_df = df[t].div(4, axis=0)
                    all_objects_df = df[list(df.select_dtypes(include=['object']))]
                    concat_df = pd.concat([all_numbers_df, all_objects_df], axis=1)
                    df = concat_df[all_titles]
                    print("mmm", t, x)
                except Exception as e:
                    # list_df = list(df)
                    # length = len(a_list)
                    # middle_index = length/2
                    # first_half = a_list[:middle_index]
                    # second_half = a_list[middle_index:]
                    # all_numbers_df = df[first_half]
                    # all_objects_df = df[second_half]
                    # concat_df = pd.concat([all_numbers_df, all_objects_df], axis=1)
                    # concat_df = df
                    print("donk,", t, x, e, list(df))
                # df = concat_df[all_titles]
                list_years = list(df["date"].apply(lambda j: int(j[0:4])))
                print("list_yearsx", list_years)
                if len(list_years) > len(list(set(list_years))):
                    # list_years = np.arange(list_years.min(),list_years.max()+2)
                    list_years = np.arange(min(list_years),max(list_years)+2)
                new_df_list = []
                for n,y in enumerate(list_years):
                    for f in ["12-31","03-31","06-30","09-30"]:
                        new_df = df[n:n+1]
                        new_df['date'] = pd.to_datetime("{}-{}".format(y,f))
                        new_df_list.append(new_df)
                print("heck yes", t, x)
                df = pd.concat(new_df_list).sort_values(by="date",ascending = False).reset_index()
                df['date'] = df['date'].apply(lambda h: str(h)[0:10])
                # df = df.drop_duplicates(subset=['date','QQ-YYYY', '{}'.format(x)], keep='first')


                fin_df = df
                fin_df["Year"] = fin_df["date"].apply(lambda m: m[0:4])
                print("xxx",list(fin_df))
                print(fin_df[['index', 'Unnamed: 0', 'date', 'symbol', 'filing_date', 'accepted_date']].head(20))
                fin_df["QQ-YYYY"] = fin_df["period"]+"-"+fin_df["date"].apply(lambda m: m[0:4])

                fin_df_list.append(fin_df)

        df_merge_is_bs = pd.merge(fin_df_list[0],fin_df_list[1],how="inner", on="QQ-YYYY")
        df_merge = pd.merge(df_merge_is_bs,fin_df_list[2],how="inner", on="QQ-YYYY")
        # df_merge = df_merge[fin_statement_raw_names]
        print("chump", list(df))
        print("df_smerge",list(df_merge))
        df_merge.columns = fin_statement_renamed_cols
        df = df_merge.iloc[::-1]
        df = df.sort_values(by="date",ascending = True)
        print("qaz", list(df))
        df['ffo_math']=df['net_income'] + df['d_n_a'] + df['sales_maturities_of_investments'] + df['purchase_of_investments'] + df['investments_in_pp_n_e'] + df['acquisitions_net']
        df['book_value_math']=df['total_assets'].dropna()-df['total_liabilities'].dropna()
        df['ebit_math']=df['ebitda_non'] - df['d_n_a']
        df['working_capital_math']= df['total_current_assets'] - df['total_current_liabilities']
        df['quick_assets_math']=df['cash_non']+df['short_term_investments']+df['accounts_receivable']
        df['quick_ratio_math']=(df['total_current_assets'] - df['inventory'])/df['total_current_liabilities']

        # XXXXX
        # for n,x in enumerate(fin_metric_vars):
        # print("len df", len(df), "len year df", len(year_df_file), "len_not_na_df", len_not_na_df, "len_not_na_year_df", len_not_na_year_df)
        # xxx   if len_not_na_year_df + 2 > len(year_df_file):
        #         smart_data_warning = "*"
        #         smart_data_disclaimer = Markup('<span class="ruhroh disclaimer_zero">** The data has been enhanced for easier insights</span>')
        # if len(df[df['{}'.format(fin_metric_name)]<0]) > len(df[df['{}'.format(fin_metric_name)]>0]):
        #     # pass
        #     print("negative now", df[['{}'.format(fin_metric_name),"QQ-YYYY" ]])
        #     df['{}'.format(fin_metric_name)] = df['{}'.format(fin_metric_name)]*-1 #.apply(lambda x: -1*x)
        #     print("negative now", df[['{}'.format(fin_metric_name),"QQ-YYYY" ]])
        # else:
        #     pass
        df = df.interpolate()
        # for x in fin_metric_vars_old:

        #     # print("x title list",x, fin_metric_title, list(df))
        #     # df['{}'.format(x)] = df['{}'.format(x)].fillna(dzf['{}'.format(x)].rolling(window=8,center=True,min_periods=1).mean())
        #     df['{}'.format(x)] = df['{}'.format(x)].replace(0, np.nan)
        #     df['{}'.format(x)] = df['{}'.format(x)].replace(np.inf, np.nan)
        #     # if len(df[df['{}'.format(x)]<0]) > len(df[df['{}'.format(x)]>0]):
        #     #     df['{}'.format(x)] = df['{}'.format(x)]*-1 #.apply(lambda x: -1*x)
        #     # else:
        #     #     pass
        #     n = 0
        #     # df['{}'.format(x)] = df['{}'.format(x)].mask(df['{}'.format(x)].between(-np.inf, 0.000000001))

        #     # df['{}'.format(x)] = df['{}'.format(x)].fillna(dzf['{}'.format(x)].rolling(window=8,center=True,min_periods=1).mean())
        #     df['{}'.format(x)] = df['{}'.format(x)].replace(0, np.nan)
        #     df['{}'.format(x)] = df['{}'.format(x)].replace(np.inf, np.nan)
        #     # print("qaz ", df['{}'.format(x)].head(50),2)


        #     df = df.interpolate()
        #     # df['{}'.format(x)] = df['{}'.format(x)].mask(df['{}'.format(x)].sub(df['{}'.format(x)].mean()).div(df['{}'.format(x)].std()).abs().gt(2))



        #     # df_smallest_2 = df['{}'.format(x)].nsmallest(2)

        #     # def percentage_diff(q):
        #     #     per = (abs((q[0] - q[1]))/q[1] *100)
        #     #     if (per > 30):
        #     #         return min(q[0], q[1])
        #     #     else:
        #     #         return q[0]
        #     # df['{}'.format(x)] = df['{}'.format(x)].apply(percentage_diff)
        #     # df['{}'.format(x)] = pd.rolling_apply(df['{}'.format(x)], 2, percentage_diff)

        #     # df = df.drop_duplicates(subset=['date','QQ-YYYY', '{}'.format(x)], keep='first')
        #     # df['pct_chg_temp'] = df['{}'.format(x)]/df['{}'.format(x)].shift(-1)
        #     # # print(list(df['pct_chg_temp']))

        #     # df['pct_chg_temp'].values[df['pct_chg_temp'] > 10] = np.nan
        #     # # print("df['pct_chg_temp']")
        #     # # print(list(df['pct_chg_temp']))
        #     # # # df.loc[df['foo'].isnull(),'foo'] = df['bar']
        #     # # df.loc[df['pct_chg_temp'],np.nan] = df['{}'.format(x)]

        #     # df['{}'.format(x)][df['pct_chg_temp'] == np.nan] = np.nan


        #     # df.to_csv("tisktisk9.csv")
        #     # df = df.drop(['pct_chg_temp'], axis=1)





        #     # df is your DataFrame
        #     # df.loc[:, df.columns != '{}'.format(x)] = df.groupby('{}'.format(x)).transform(lambda g: replace(g, 3))

        #     df = df.interpolate()
        #     # len_rows_ratios = df['{}'.format(x)].isna().sum()
        #     # len_duplicates = len(df) - df['{}'.format(x)].nunique()

        #     # print(len(df),"len_duplicates", len_duplicates)
        #     # while n <= len_rows_ratios: #df[df['{}'.format(x)].isna].shape[0]:#not df['{}'.format(x)].isin([0]).empty:
        #     # #     # print("shape len", df[df['{}'.format(x)] == 0].shape[0])
        #     #     df['{}'.format(x)] = df['{}'.format(x)].replace(0, np.nan)

        #     #     df['{}'.format(x)] = df['{}'.format(x)].replace(np.inf, np.nan)
        #     # #     print(df['{}'.format(x)].isna().sum())
        #     # #     # print("asd", df['{}'.format(x)].head(50),2)
        #     # #     # df = df[df['{}'.format(x)].notnull()].ewm(alpha = 0.5, ignore_na=True).mean()
        #     # #     # df['{}'.format(x)] = df['{}'.format(x)].ewm(span=8).mean()
        #     # #     # df['{}'.format(x)] = df['{}'.format(x)].ewm(span=8).mean()
        #     # #     # df['{}'.format(x)] = df['{}'.format(x)].rolling(window=8,min_periods=1).mean()
        #     # #     # df['{}'.format(x)] = df['{}'.format(x)].isna().ewm(alpha = 0.5).mean()
        #     # #     # df['{}'.format(x)] = df['{}'.format(x)].fillna(df['{}'.format(x)].rolling(window=8,center=True,min_periods=1).mean())
        #     #     # df['{}'.format(x)] = df['{}'.format(x)].fillna(df['{}'.format(x)].rolling(window=8,center=True,min_periods=1).mean())
        #     # #     # df['{}'.format(x)] = df['{}'.format(x)].loc[df['{}'.format(x)].shift(-1) != df['{}'.format(x)]]
        #     #     n+=1


        #     # print("listenman", len(df), "sad",df['{}'.format(x)].isna().sum(), list(df['{}'.format(x)]))
        #     # print("listendudeagain", len(df), "sad",df['{}'.format(x)].isna().sum(), list(df['{}'.format(x)]))
        #     # if pd.isnull((df['{}'.format(x)].head(1))[0]):#list(df['{}'.format(x)].head(1))[0]==np.nan:#df['{}'.format(x)].min()
        #     #     print("not number", list(df['{}'.format(x)].head(1))[0])
        #     #     df['{}'.format(x)].iloc[0] = df['{}'.format(x)][0:4].mean()
        #     # else:
        #     #     print("iznum", list(df['{}'.format(x)].head(1))[0])
        # df.to_csv("letssee.csv")


        metric_history = metric_to_formula_map(df,metric_name)

        fin_metric_history = metric_history
        df["{}".format(fin_metric_title)] = metric_history
        # df.to_csv("xgitest2.csv")
        df = df.sort_values(by="date",ascending = False)
        early_missing_periods = df[::-1]["{}".format(fin_metric_title)].ne(0).idxmax()

        df = df[0:early_missing_periods+1]#[::-1]
        def groupby_agg(df):
            df_grouped = df.groupby("Year").mean()
            return df_grouped
    # fin_metric_vars = [fin_metric_title]

    fin_metric_definition_link = "<br>Source: Investopedia"
    fin_metric_definition_formula = Markup("{}<br>{}<br>{}".format(fin_metric_equation, fin_metric_definition, fin_metric_definition_link))
    df = df.drop_duplicates(subset=['date']).sort_values(by=["date"], ascending=False)
    df_quarter = df['period']
    # df = df.drop(['Quarter & Year', 'Unnamed: 0','symbol','fillingDate','acceptedDate','period','link',],axis=1, errors='ignore')
    df = df.drop(['Quarter & Year', 'Unnamed: 0','symbol','fillingDate','acceptedDate','period','link','ebitdaratio','operatingIncomeRatio','netIncomeRatio'],axis=1, errors='ignore')
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
        # print("sup5")
    except Exception as e:
        pass
    try:
        # print("yopo!", titles_bs)
        # print("yopo2!", var_list)
        try:
            pass
            # titles_bs.remove("Quarter & Year")
            # var_list.remove("Quarter & Year")
        except:
            pass
        # if "{}".format(statement_or_ratio) == "income-statement" or "{}".format(statement_or_ratio) == "cash-flow-statement":
        # for n,x in enumerate(fin_metric_vars):

            # print("fin_metric_vars", fin_metric_vars)
            # print("nx",n,x)
            # print("positive_negative",list(df))
            # print(df["{}".format(x)].head(30))
            # print("before", len(df["{}".format(x)]),"filtered now",len(df[(df["{}".format(x)]<=0)]["{}".format(x)]))
            # print("other",len(df[(df["{}".format(x)]>0)]["{}".format(x)].head(30)))
            # print(df[(df["{}".format(x)]>0)]["{}".format(x)].head(30))
        # print("yopo", filter_pos_neg)
        # df['{}'.format(x)] = df['{}'.format(x)].mask(df['{}'.format(x)].between(-np.inf, 0.000000001))
        df['{}'.format(x)] = df['{}'.format(x)].apply(lambda x: abs(x))
        # print("zqtype",type(list(df['{}'.format(x)].head(1))[0]))
        # print(df["{}".format(x)].head(30))
        # print(df[df!=0].rolling(window=8, center=True, min_periods=1).mean())
        n = 0
        # print("x title list",x, fin_metric_title, list(df))
        # df['{}'.format(x)] = df['{}'.format(x)].fillna(dzf['{}'.format(x)].rolling(window=8,center=True,min_periods=1).mean())
        df['{}'.format(x)] = df['{}'.format(x)].replace(0, np.nan)
        df['{}'.format(x)] = df['{}'.format(x)].replace(np.inf, np.nan)
        # print("qxaz", fin_statement_dir, df['{}'.format(x)].head(50),2)
        len_rows_ratios = df['{}'.format(x)].isna().sum()
        df = df.interpolate()
        while n <= len_rows_ratios: #df[df['{}'.format(x)].isna].shape[0]:#not df['{}'.format(x)].isin([0]).empty:
        #     # print("shape len", df[df['{}'.format(x)] == 0].shape[0])
        #     print(df['{}'.format(x)].isna().sum())
        #     # print("asd", df['{}'.format(x)].head(50),2)
        #     # df = df[df['{}'.format(x)].notnull()].ewm(alpha = 0.5, ignore_na=True).mean()
        #     # df['{}'.format(x)] = df['{}'.format(x)].ewm(span=8).mean()
        #     # df['{}'.format(x)] = df['{}'.format(x)].ewm(span=8).mean()
        #     df['{}'.format(x)] = df['{}'.format(x)].rolling(window=8,min_periods=1).mean()
            df['{}'.format(x)] = df['{}'.format(x)].fillna(df['{}'.format(x)].rolling(window=8,center=True,min_periods=2).mean())
            n+=1
        if pd.isnull((df['{}'.format(x)].head(1))[0]):#list(df['{}'.format(x)].head(1))[0]==np.nan:#df['{}'.format(x)].min()
            # print("not number", list(df['{}'.format(x)].head(1))[0])
            df['{}'.format(x)].iloc[0] = df['{}'.format(x)][0:4].mean()
        else:
            pass
            # print("iznum", list(df['{}'.format(x)].head(1))[0])
        # print("len_row_ratios",len_rows_ratios, len(df))
        if len(df) == len_rows_ratios:
            df['{}'.format(x)] = df['{}'.format(x)].replace(np.nan, 0)
            earliest_latest_warning = ""
            earliest_latest_disclaimer = ""
            # return render_template('404.html'), 404
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
        if "{}".format(statement_or_ratio) == "income-statement" or "{}".format(statement_or_ratio) == "cash-flow-statement":
            last_4_quarters = np.sum(df["quarter avg"][0:4])
            prev_4_quarters = np.sum(df["quarter avg"][5:9])
        else:
            last_4_quarters = np.mean(df["quarter avg"][0:4])
            prev_4_quarters = np.mean(df["quarter avg"][5:9])
        # df["quarter avg"] = df["quarter avg"]
    except Exception as e:
        # print("boohoo",e)
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
    df.to_csv("awfdf.csv")
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
    # print("min_metric", min_metric, "max_metric",max_metric)
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
        # print("zx2")
        if latest_metric > earliest_metric:
            pct_chg = (latest_metric/earliest_metric)
        else:
            pct_chg = (latest_metric/earliest_metric)
        # print("zx3")
        if (earliest_metric <0 and latest_metric>0) or (earliest_metric>0 and latest_metric<0):
            earliest_latest_warning = "*"
            earliest_latest_disclaimer =  Markup('<span class="ruhroh disclaimer_one">** A modified method (see: <a href="https://math.stackexchange.com/questions/716767/how-to-calculate-the-percentage-of-increase-decrease-with-negative-numbers/716770">here</a>) is used to calculate change, since the bottom/peak contains a negative number.</span>')
        else:
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
        market_cap_path = glob.glob("D:/Cloud/rclone/OneDrive/Web/TenDollarData/Charts_TenDollarData/financial_statements/data/Historical Market Cap & Price/*\\[M*/M-*-{}.csv".format(url_symbol.upper()))[0]
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
        year_df['Price']=year_dates_price_list[::-1]
        price_json = np.nan_to_num(df[['date',"{}".format("Price")]].to_numpy()).tolist()[::-1]
    except Exception as e:
        price_json = []
    import json
    from urllib.request import urlopen
    try:
        fmp_url = "https://financialmodelingprep.com/api/v3/quote/{}?apikey=4b5cd112b74ca86811fd1ccddd4ad9c1".format(url_symbol.upper())
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
        last_price = price_json[-1][1]
        last_pct_change = 0
    last_price_json_timestamp  = price_json[-1][0]
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
        full_path = csv_file.split(' ~ ')
        path = pathlib.PurePath(full_path[0])
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
    max_min_range_str = change_markup(max_min_range,"x","arrow","max_min_range_str")
    last_4_quarters_str = magnitude_num(last_4_quarters,currency_symbol)
    try:
        subdomain = "https://charts.tendollardata.com"
        subdomain = "http://127.0.0.1:5000"
        company_similar = profiles_dict['Similar Companies'].split(",")
        company_similar = [ x for x in company_similar if "XL" not in x ]
        company_similar_list = []
        n = 0
        while n < len(company_similar):
            x = company_similar[n]
            company_similar_x = ('<a class="similar_companies_urls" href="{}/{}-{}/{}/{}/{}">{}</a>, '.format(subdomain,x.lower().strip(),stock_or_etf,url_name,statement_or_ratio,url_fin_metric,x))
            company_similar_list.append(company_similar_x)
            n+=1
        company_similar_paragraph = Markup(''.join(company_similar_list)[:-2])
    except Exception as e:
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
    # print("df_json ", df_json)
    # pd.DataFrame({"df_json":df_json}).to_csv("df_json.csv")
    # Markup('** A modified method (see: <a href="https://math.stackexchange.com/questions/716767/how-to-calculate-the-percentage-of-increase-decrease-with-negative-numbers/716770">here</a>) is used to calculate change, since the bottom/peak contains a negative number.')
    split_input = profiles_dict['description'].split(".")
    pass_index = -100
    sentence_list = []
    for n,x in enumerate(split_input):
        print(pass_index)
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
        print(n,sentence)
    sentences_list_joined = Markup("".join(sentence_list[:-1]))
    html_sentence_list = sentences_list_joined #Markup("<ul>"+sentences_list_joined+"</ul>")
    # print("this", html_sentence_list)

    return render_template('current_ratio.html', \

                            earliest_latest_warning = earliest_latest_warning,\
                            earliest_latest_disclaimer = earliest_latest_disclaimer,\
                            html_sentence_list = html_sentence_list,\
                            df_html_formula = [df_html_formula],\
                            url_symbol = url_symbol,\
                            min_max_warning = min_max_warning,\
                            min_max_disclaimer = min_max_disclaimer,\
                            if_in_mil = if_in_mil,\
                            domain = "http://127.0.0.1:5000",\
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

@charts.route('/test/<some_place>', methods=['POST', 'GET'])
# @cache.cached(timeout=5)
def fin_test(some_place):
    # values = list(FS("IS","AAPL")['Beginning Price'])[0:19]


    return render_template('financial_statements.html',
    # return render_template('fin_statements_bootstrapped.html',
    # return render_template('fin_statements_bootstrapped_w_comments.html',
    # FS("IS","AAPL").df_values()['df_table']
    # FS("IS","AAPL").df_values()['df_table_pct']
    # FS("IS","AAPL").df_values()['chart_x_dates']
    # FS("IS","AAPL").df_values()['chart_y_revenue']
    # FS("IS","AAPL").df_values()['df_json']
    # FS("IS","AAPL").df_values()['df_titles']
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