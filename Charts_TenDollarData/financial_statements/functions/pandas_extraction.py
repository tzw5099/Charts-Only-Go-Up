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

pd.set_option('display.float_format', '{:.2f}'.format)


class FS:
    """
    FS = financial statement.
    Subject = BS, CF, or IF.
    {'df_table': fs.df_table(),
    'df_table_pct':fs.df_table_pct(),
    'chart_x_dates': chart_x_dates,
    'chart_y_revenue':chart_y_revenue,
    'df_json': df_json,
    'df_titles':df_titles}
    """

    def isnumber(x):
        try:
            float(x)
            return True
        except:
            return False
            
    pd.set_option('display.float_format', '{:.2f}'.format)

    def __init__(self,subject,symbol):
        self.subject = subject
        self.symbol = symbol
        
        self.url_symbol = symbol
        if subject=="BS":
            subject="Balance Sheet"
            columns_keep = [
                        'Date',
                        'Date & Time Filing Accepted',
                        'Cash & Cash Equivalents',
                        'Short Term Investments',
                        'Cash & S-T Investments',
                        'Accounts Receivables',
                        'Inventory',
                        'Other Current Assets',
                        'Total Current Assets',
                        'PP&E',
                        'Goodwill',
                        'Intangible Assets',
                        'Goodwill & Intangible Assets',
                        'L-T Investments',
                        'Tax Assets',
                        'Other Non-Current Assets',
                        'Total Non-Current Assets',
                        'Other Assets',
                        'Total Assets',
                        'Accounts Payables',
                        'S-T Debt',
                        'Income Tax Payables',
                        'Deferred Revenue',
                        'Other Current Liabilities',
                        'Total Current Liabilities',
                        'L-T Debt',
                        'Deferred Revenue Non-Current',
                        'Deferred Tax Liabilities Non-Current',
                        'Other Non-Current Liabilities',
                        'Total Non-Current Liabilities',
                        'Other Liabilities',
                        'Total Liabilities',
                        'Common Stock',
                        'Retained Earnings',
                        'Accumulated Other Comprehensive Income Loss',
                        'Other Shareholders Equity',
                        'Total Shareholders Equity',
                        'Total Liabilities & Stockholders Equity',
                        'Total Investments',
                        'Total Debt',
                        'Net Debt',
                        'SEC Filing',
                        'Quarter & Year',
                            ]

            cols = [ 
                    'Date',
                    'Quarter & Year',
                    'Cash & Cash Equivalents',
                    'Short Term Investments',
                    'Cash & S-T Investments',
                    'Accounts Receivables',
                    'Inventory',
                    'Other Current Assets',
                    'Total Current Assets',
                    'PP&E',
                    'Goodwill',
                    'Intangible Assets',
                    'Goodwill & Intangible Assets',
                    'L-T Investments',
                    'Tax Assets',
                    'Other Non-Current Assets',
                    'Total Non-Current Assets',
                    'Other Assets',
                    'Total Assets',
                    'Accounts Payables',
                    'S-T Debt',
                    'Income Tax Payables',
                    'Deferred Revenue',
                    'Other Current Liabilities',
                    'Total Current Liabilities',
                    'L-T Debt',
                    'Deferred Revenue Non-Current',
                    'Deferred Tax Liabilities Non-Current',
                    'Other Non-Current Liabilities',
                    'Total Non-Current Liabilities',
                    'Other Liabilities',
                    'Total Liabilities',
                    'Common Stock',
                    'Retained Earnings',
                    'Accumulated Other Comprehensive Income Loss',
                    'Other Shareholders Equity',
                    'Total Shareholders Equity',
                    'Total Liabilities & Stockholders Equity',
                    'Total Investments',
                    'Total Debt',
                    'Net Debt',
                    'SEC Filing',
                    'Date & Time Filing Accepted'
                ]
        elif subject=="CF":
            subject="Cash Flow Statement"
            columns_keep = [
                            'Date',
                            'Date & Time Filing Accepted',
                            'Net Income (Earnings)',
                            'D&A',
                            'Deferred Income Tax',
                            'Stock-Based Compensation (SBC)',
                            'Change in Working Capital',
                            'Accounts Receivables',
                            'Inventory',
                            'Accounts Payables',
                            'Other Working Capital',
                            'Other Non-Cash Items',
                            'Net Cash Provided by Operating Activities',
                            'Investments in PP&E',
                            'Acquisitions (Net)',
                            'Purchase of Investments',
                            'Sales/Maturities of Investments',
                            'Other Investing Activities',
                            'Net Cash used for Investing Activities',
                            'Debt Repayment',
                            'Common Stock Issued',
                            'Common Stock Repurchased',
                            'Dividends Paid',
                            'Other Financing Activities',
                            'Net Cash Used Provided by Financing Activities',
                            'Effect of Exchange Rate Changes on Cash',
                            'Net Change in Cash',
                            'Cash at End of Period',
                            'Cash at Beginning of Period',
                            'Operating Cash Flow',
                            'Capital Expenditure (capex)',
                            'Free Cash Flow',
                            'SEC Filing',
                            'Quarter & Year',
                            ]
            cols = [ 
                    'Date',
                    'Quarter & Year',
                    'Net Income (Earnings)',
                    'D&A',
                    'Deferred Income Tax',
                    'Stock-Based Compensation (SBC)',
                    'Change in Working Capital',
                    'Accounts Receivables',
                    'Inventory',
                    'Accounts Payables',
                    'Other Working Capital',
                    'Other Non-Cash Items',
                    'Net Cash Provided by Operating Activities',
                    'Investments in PP&E',
                    'Acquisitions (Net)',
                    'Purchase of Investments',
                    'Sales/Maturities of Investments',
                    'Other Investing Activities',
                    'Net Cash used for Investing Activities',
                    'Debt Repayment',
                    'Common Stock Issued',
                    'Common Stock Repurchased',
                    'Dividends Paid',
                    'Other Financing Activities',
                    'Net Cash Used Provided by Financing Activities',
                    'Effect of Exchange Rate Changes on Cash',
                    'Net Change in Cash',
                    'Cash at End of Period',
                    'Cash at Beginning of Period',
                    'Operating Cash Flow',
                    'Capital Expenditure (capex)',
                    'Free Cash Flow',
                    'SEC Filing',
                    'Date & Time Filing Accepted'
                ]
        elif subject=="IS":
            subject="Income Statement"
            columns_keep = [
                'Date',
                'Date & Time Filing Accepted',
                'Revenue',
                'Cost of Revenue',
                'Gross Profit (Income)',
                'Gross Profit (Income) Ratio',
                'R&D',
                'SG&A',
                'Selling & Marketing (S&M) Expenses',
                'Other Expenses',
                'Operating Expenses',
                'Cost & Expenses',
                'Interest Expense',
                'D&A',
                'EBITDA',
                'EBITDA Ratio',
                'Operating Income',
                'Operating Income Ratio',
                'Other Income Expenses (Net)',
                'Pre-Income Tax',
                'Pre-Income Tax Ratio',
                'Income Tax Expense',
                'Net Income',
                'Net Income Ratio',
                'EPS',
                'EPS Diluted',
                'Shares Outstanding',
                'Shares Outstanding (Diluted)',
                'SEC Filing', 
                'Quarter & Year'
                            ]
            cols = [ 
                    'Date',
                    'Quarter & Year', 
                    'Revenue',
                'Cost of Revenue',
                'Gross Profit (Income)',
                'Gross Profit (Income) Ratio',
                'R&D',
                'SG&A',
                'Other Expenses',
                'Operating Expenses',
                'Cost & Expenses',
                'Interest Expense',
                'D&A',
                'EBITDA',
                'EBITDA Ratio',
                'Operating Income',
                'Operating Income Ratio',
                'Other Income Expenses (Net)',
                'Pre-Income Tax',
                'Pre-Income Tax Ratio',
                'Income Tax Expense',
                'Net Income',
                'Net Income Ratio',
                'EPS',
                'EPS Diluted',
                'Shares Outstanding',
                'Shares Outstanding (Diluted)',
                'SEC Filing',
                'Date & Time Filing Accepted'
                ]
        pd.set_option('display.float_format', '{:.2f}'.format)

        self.market_cap_path = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Market Cap & Price/*/[[]M[]] Monthly/M-*-{}.csv".format(self.url_symbol.upper()))[0]
        self.df_price = pd.read_csv(self.market_cap_path)
        # "D:/Cloud/rclone/OneDrive/Web/TenDollarData/Charts_TenDollarData/financial_statements/functions"
        # csv_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/{}/*~{}~*".format(self.subject,self.symbol))[-1] #.format("NLOK"))[-1]
        csv_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/{}/*~{}~*".format(subject,self.symbol))[-1] #.format("NLOK"))[-1]

        # csv_file = glob.glob("data\Historical Financial Statements\*\year\{}\*_{}_*".format(self.subject,self.symbol))[-1] #.format("NLOK"))[-1]
        self.year = pd.read_csv(csv_file)
        df = self.year[0:].iloc[::-1]
        df['Quarter & Year'] = df['period']+" "+(df['date'].astype(str).str[0:4])#((df_bs['date'].astype(str).str[0:4].astype(int))-1).astype(str)
        df = df.drop([ 'Unnamed: 0','symbol','fillingDate','period','link'],axis=1)
        # print("Listdemcolumns", list(df))
        df.columns = columns_keep






        self.df = df[cols]

    def isnumber(x):
        try:
            float(x)
            return True
        except:
            return False
            
    def first(self):
        earliest_year = list((self.year['date'].astype(str).str[0:4]))[-1]
        return(earliest_year)

    def last(self):
        latest_year = list((self.year['date'].astype(str).str[0:4]))[0]
        return(latest_year)  
    def df_table_pct(self):
        df_pct_chg = self.df
        pct_chg_cols = (self.df.select_dtypes(include=['number']).pct_change(-1))
        df_str = df_pct_chg.drop(list(pct_chg_cols), axis=1)
        df_pct_chg = df_str.join(pct_chg_cols)[list(self.df)]
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


        df_t = self.df.transpose()
        df_t.columns = list(self.df['Quarter & Year'])
        df_t = df_t.iloc[1:]
        df_t['']=df_t.index
        df_t.index = range(len(df_t))

        cols = list(df_t.columns)
        cols = [cols[-1]] + cols[:-1]
        df_t = df_t[cols]

        df_pct = df_pct_chg_t.to_html().replace('<table','<table class="df_tableBoot compact stripe hover cell-border order-column row-border" id="df_myTable1"')# dt-responsive" id="df_myTable"')
        df_table_pct = df_pct#[df_pct]
        return df_table_pct
    
    def df_table(self):
        fs = FS(self.subject,self.symbol)
        df = self.df.drop(["Gross Profit (Income) Ratio","EBITDA Ratio","Operating Income Ratio","Pre-Income Tax Ratio","Net Income Ratio","SEC Filing","Date & Time Filing Accepted","Cost & Expenses", "Effect of Exchange Rate Changes on Cash"], axis=1, errors='ignore')
        df_t = df.transpose()
        df_t.columns = list(self.df['Quarter & Year'])
        df_t = df_t.iloc[1:]
        df_t['']=df_t.index
        df_t.index = range(len(df_t))        
        df_t = df_t[df_t.columns[::-1]]
        cols = list(df_t.columns)
        cols = [cols[-1]] + cols[:-1]
        df_t = df_t[cols]
        # df_html = df_t.to_html().replace('<table','<table class="df_tableBoot" id="df_myTable2"')# dt-responsive" id="df_myTable"')

        df_n = self.df[self.df.applymap(FS.isnumber)]
        df_n[df_n < 2] = np.nan
        # pd.DataFrame(df_n.sum())#axis=0))
        df_n_sum = pd.DataFrame(df_n.sum())
        df_n_sum[df_n_sum == 0] = ""
        new_header = df_n_sum.iloc[0] #grab the first row for the header
        df_n_sum = df_n_sum[1:] #take the data less the header row
        df_n_sum.columns = new_header #set the header row as the df header
        df_n_sum.index = range(len(df_n_sum))
        df_t = pd.merge(df_n_sum, df_t, left_index=True, right_index=True,suffixes=('Total: {} - {}'.format(fs.last(),fs.first()), 'Line Item (in $M)'))
        df_t = df_t[1:25]
        # df_t.rename(columns={ df_t.columns[0]: "Line Item" }, inplace = True)
        df_t = df_t.iloc[:, 2:]
        # df_t.rename(columns={"col1": "Line Item"})
        # df_t = df_t[~df_t.iloc[:, 0].str.contains("Gross Profit (Income) Ratio")]
        
        # df_t[~df_t['Line Item'].str.contains("Gross Profit (Income) Ratio")]
        # "Gross Profit (Income) Ratio","EBITDA Ratio","Operating Income Ratio","Pre-Income Tax Ratio","Net Income Ratio")


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
        df_html = df_t.to_html().replace('border="1" class="dataframe">','class="df_tableBoot compact stripe hover cell-border order-column row-border" id="df_myTable" border="1" class="dataframe"><colgroup>{}</colgroup>'.format(col_list_str))
        df_html = df_html.replace('NaN','')
        
        


        df_html = df_html.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
        df_html = df_html.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
        df_html = df_html.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')
        df_html = df_html[0:]
        df_table = [df_html[0:]]
        return df_table

    def df_json(self):
        df = self.df
        df['Date'] = pd.to_datetime(df['Date']).values.astype(np.int64) // 10 ** 6
        df = df[['Date', 'Revenue']].dropna().to_numpy().tolist()        
        return df

    def df_labels(self):
        df = self.df
        df['Date'] = pd.to_datetime(df['Date']).values.astype(np.int64) // 10 ** 6
        labels = df[['Date']].to_numpy().tolist(),
        # labels = list(df['Date'])#[0:19]
        # labels = list(df['Revenue'])
        return labels

    def df_values(self):
        fs = FS(self.subject,self.symbol)
        # fs.df_table()
        # df = self.df[['date','revenue']].dropna() #.fillna(0)#.fillna(method='bfill')
        df = self.df
        df['Date'] = (pd.to_datetime(self.df['Date']).values.astype(np.int64) // 10 ** 6)
        # df = df[['Date', 'Revenue']]

        df_price = self.df_price
        df_price['datetime'] = (pd.to_datetime(df_price['datetime']).values.astype(np.int64) // 10 ** 6)
        df_price = df_price[['datetime', 'adjClose']]

        # df_json = df.to_numpy().tolist()
        # df_json = fs.df_json()

        df_json =df_price.dropna().to_numpy().tolist()
        
        
        # chart_x_dates =  df['Date'].to_list()
        # chart_y_revenue = df['Revenue'].to_list()
        print("xyzdd", df_price['datetime'])
        chart_x_dates =  df_price['datetime'].to_list()
        chart_y_revenue = df_price['adjClose'].to_list()
        df_titles = df.columns.values
        df_close = list(df_price['adjClose'])
        df_price = df_price[['datetime', 'adjClose']].dropna().to_numpy().tolist()    
        
        # df_json = fs.df_json()
        # {'df_json': df_json, 'chart_x_dates':chart_x_dates,'chart_y_revenue':chart_y_revenue,'df_titles':df_titles }
        return {
            # 'df_table': fs.df_table(), 
            'df_close':df_close,
                'df_table_pct':fs.df_table_pct(),
               'chart_x_dates': chart_x_dates, 'chart_y_revenue':chart_y_revenue,
               'df_json': df_json, 'df_titles':df_titles}


# def FS_csv(subject, symbol):
#     csv_file = glob.glob("..\data\Historical Financial Statements\*\year\{}\*_{}_*".format(subject,symbol))[-1] #.format("NLOK"))[-1]
#     df = pd.read_csv(csv_file)
#     return(df)

# def FS_first_year(df):
#     earliest_year = list((df['date'].astype(str).str[0:4]))[-1]
#     return(earliest_year)

# def FS_latest_year(df):
#     latest_year = list((df_bs['date'].astype(str).str[0:4]))[0]
#     return(latest_year)

# print(FS_first_year(FS_csv("Income Statement","AAPL")))


# labels = list(FS("IS","AAPL")['Year'])[0:19]
# values = list(FS("IS","AAPL")['Beginning Price'])[0:19]

# tables=FS("IS","AAPL").df_values()['df_table'], 

# table_pct = FS("BS","AAPL").df_values()['df_table_pct'], 
# df_date = FS("BS","AAPL").df_values()['chart_x_dates'], 
# df_rev = FS("BS","AAPL").df_values()['chart_y_revenue'],
# df_json = FS("BS","AAPL").df_values()['df_json'],
# titles=FS("BS","AAPL").df_values()['df_titles']
# print(str(df_json)[0:200])
# print(FS("IS","AAPL").df_table_raw())
# print(FS("IS","AAPL").last())

# subject="Income Statement"
# symbol="AAPL"
# csv_file = glob.glob("Charts_TenDollarData/financial_statements/data/Historical Financial Statements/*/year/{}/*~{}~*".format(subject,symbol))[-1]
# csv_file = glob.glob("data\Historical Financial Statements\*\year\{}\*_{}_*".format(subject,symbol))[-1]
# csv_file = glob.glob("data\Historical Financial Statements\*\year\*")

# print(csv_file)

print("up next")
# print(pd.read_csv(csv_file))
# print(str(df_json)[0:200])
# print((FS("IS","AAPL").df_price()))
# print(( FS("IS","AAPL").df_labels()))