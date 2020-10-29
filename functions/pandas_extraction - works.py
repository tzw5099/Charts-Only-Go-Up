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

abs_path = "D:\Cloud\OneDrive\Web\charts.tendollardata.com"


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
        if subject=="BS":
            subject="Balance Sheet"
        elif subject=="CF":
            subject="Cash Flow Statement"
        elif subject=="IS":
            subject="Income Statement"
        pd.set_option('display.float_format', '{:.2f}'.format)
        self.subject = subject
        self.symbol = symbol
        csv_file = glob.glob("{}\data\Historical Financial Statements\*\year\{}\*_{}_*".format(abs_path,self.subject,self.symbol))[-1] #.format("NLOK"))[-1]
        self.year = pd.read_csv(csv_file)
        df = self.year[0:].iloc[::-1]
        df['Quarter & Year'] = df['period']+" "+(df['date'].astype(str).str[0:4])#((df_bs['date'].astype(str).str[0:4].astype(int))-1).astype(str)
        df = df.drop([ 'Unnamed: 0','symbol','fillingDate','period','link'],axis=1)
        df.columns = [
            'Date',
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

        cols = [ 'Date','Quarter & Year', 'Revenue (Sales)',
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

        df_pct = df_pct_chg_t.to_html().replace('<table','<table class="df_tableBoot" id="df_myTable1"')# dt-responsive" id="df_myTable"')
        df_table_pct = [df_pct]
        return df_table_pct
    
    def df_table(self):
        fs = FS(self.subject,self.symbol)
        df_t = self.df.transpose()
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
        df_t = pd.merge(df_n_sum, df_t, left_index=True, right_index=True,suffixes=('Total: {} - {}'.format(fs.last(),fs.first()), 'Line Items'))
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


        df_html = df_html.replace('<td>','<td class="td_fin_statement_class fin_statement_class">')
        df_html = df_html.replace('<th>','<th class="th_fin_statement_class fin_statement_class">')
        df_html = df_html.replace('<tr>','<tr class="tr_fin_statement_class fin_statement_class">')
        df_html = df_html[0:]
        df_table = [df_html[0:]]
        return df_table

    def df_json(self):
        df = self.df
        df['Date'] = pd.to_datetime(df['Date']).values.astype(np.int64) // 10 ** 6
        df = df[['Date', 'Revenue (Sales)']].dropna().to_numpy().tolist()        
        return df

    def df_table_raw(self):
        return self.df

    def df_labels(self):
        df = self.df
        df['Date'] = pd.to_datetime(df['Date']).values.astype(np.int64) // 10 ** 6
        labels = df[['Date']].to_numpy().tolist(),
        # labels = list(df['Date'])#[0:19]
        # labels = list(df['Revenue (Sales)'])
        return labels

    def df_price(self):
        df = self.df
        values = list(df['Revenue (Sales)'])
        # values = list(df['Beginning Price'])[0:19]
        return values

    def df_values(self):
        fs = FS(self.subject,self.symbol)
        fs.df_table()
        # df = self.df[['date','revenue']].dropna() #.fillna(0)#.fillna(method='bfill')
        df = self.df
        df['Date'] = (pd.to_datetime(self.df['Date']).values.astype(np.int64) // 10 ** 6)
        df = df[['Date', 'Revenue (Sales)']]
        # df_json = df.to_numpy().tolist()
        df_json = fs.df_json()
        chart_x_dates =  df['Date'].to_list()
        chart_y_revenue = df['Revenue (Sales)'].to_list()
        df_titles = df.columns.values
        # df_json = fs.df_json()
        # {'df_json': df_json, 'chart_x_dates':chart_x_dates,'chart_y_revenue':chart_y_revenue,'df_titles':df_titles }
        return {'df_table': fs.df_table()
                , 'df_table_pct':fs.df_table_pct(),
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

table_pct = FS("IS","AAPL").df_values()['df_table_pct'], 
df_date = FS("IS","AAPL").df_values()['chart_x_dates'], 
df_rev = FS("IS","AAPL").df_values()['chart_y_revenue'],
df_json = FS("IS","AAPL").df_values()['df_json'],
titles=FS("IS","AAPL").df_values()['df_titles']
print(str(df_json)[0:200])
# print(FS("IS","AAPL").df_table_raw())
print(FS("IS","AAPL").last())

subject="Income Statement"
symbol="AAPL"

csv_file = glob.glob("{}\data\Historical Financial Statements\*\year\{}\*_{}_*".format(abs_path,subject,symbol))[-1]
# csv_file = glob.glob("data\Historical Financial Statements\*\year\*")

print(csv_file)

print("up next")
# print(pd.read_csv(csv_file))
print(str(df_json)[0:200])
print((FS("IS","AAPL").df_price()))
print(( FS("IS","AAPL").df_labels()))
