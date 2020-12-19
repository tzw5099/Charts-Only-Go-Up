# metric to url mapping
fin_statement_raw_names = ['Unnamed: 0',
        'date',
        'symbol',
        'fillingDate',
        'acceptedDate',
        'period',
        'revenue',
        'costOfRevenue',
        'grossProfit',
        'grossProfitRatio',
        'researchAndDevelopmentExpenses',
        'generalAndAdministrativeExpenses',
        'sellingAndMarketingExpenses',
        'otherExpenses',
        'operatingExpenses',
        'costAndExpenses',
        'interestExpense',
        'depreciationAndAmortization_x',
        'ebitda',
        'ebitdaratio',
        'operatingIncome',
        'operatingIncomeRatio',
        'totalOtherIncomeExpensesNet',
        'incomeBeforeTax',
        'incomeBeforeTaxRatio',
        'incomeTaxExpense',
        'netIncome_x',
        'netIncomeRatio',
        'eps',
        'epsdiluted',
        'weightedAverageShsOut',
        'weightedAverageShsOutDil',
        'link',
        'finalLink',
        'cashAndCashEquivalents',
        'shortTermInvestments',
        'cashAndShortTermInvestments',
        'inventory_x',
        'otherCurrentAssets',
        'totalCurrentAssets',
        'propertyPlantEquipmentNet',
        'goodwill',
        'intangibleAssets',
        'goodwillAndIntangibleAssets',
        'longTermInvestments',
        'taxAssets',
        'otherAssets',
        'totalAssets',
        'accountPayables',
        'shortTermDebt',
        'taxPayables',
        'deferredRevenue',
        'otherCurrentLiabilities',
        'totalCurrentLiabilities',
        'longTermDebt',
        'deferredRevenueNonCurrent',
        'deferredTaxLiabilitiesNonCurrent',
        'otherNonCurrentLiabilities',
        'totalNonCurrentLiabilities',
        'otherLiabilities',
        'totalLiabilities',
        'commonStock',
        'retainedEarnings',
        'accumulatedOtherComprehensiveIncomeLoss',
        'othertotalStockholdersEquity',
        'totalStockholdersEquity',
        'totalLiabilitiesAndStockholdersEquity',
        'totalInvestments',
        'totalDebt',
        'netDebt',
        'deferredIncomeTax',
        'stockBasedCompensation',
        'changeInWorkingCapital',
        'accountsReceivables',
        'otherWorkingCapital',
        'otherNonCashItems',
        'netCashProvidedByOperatingActivities',
        'investmentsInPropertyPlantAndEquipment',
        'acquisitionsNet',
        'purchasesOfInvestments',
        'salesMaturitiesOfInvestments',
        'otherInvestingActivites',
        'netCashUsedForInvestingActivites',
        'debtRepayment',
        'commonStockIssued',
        'commonStockRepurchased',
        'dividendsPaid',
        'otherFinancingActivites',
        'netCashUsedProvidedByFinancingActivities',
        'effectOfForexChangesOnCash',
        'netChangeInCash',
        'cashAtEndOfPeriod',
        'cashAtBeginningOfPeriod',
        'operatingCashFlow',
        'capitalExpenditure',
        'freeCashFlow',
        "QQ-YYYY"]

fin_statement_renamed_cols = ['index',
                'date',
                'symbol',
                'filing_date',
                'accepted_date'
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
                'cash_non',
                'short_term_investments',
                'cash_n_short_term_investments',
                'inventory',
                'other_current_assets',
                'total_current_assets',
                'pp_n_e',
                'goodwill',
                'intangible_assets',
                'goodwill_n_intangible_assets',
                'long_term_investments',
                'tax_assets',
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
                'total_l_se',
                'total_investments',
                'total_debt',
                'net_debt',
                'deferred_income_tax',
                'sbc',
                'change_in_working_capital',
                'accounts_receivable',
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
                "QQ-YYYY"]

metric_to_url_map = {
    'net_working_capital_ratio': "net-working-capital-ratio",
    'book_value_per_share': "book-value-per-share",
    'total_equity_to_total_assets': "total-equity-to-total-assets",
    'operating_cost_ratio': "operating-cost-ratio",
    'percentage_of_debt_to_asset_formula': "perc​entage-of-debt-to-asset-formula",

    'total_liabilities_pct_of_total_assets': "total-liabilities-pct-of-total-assets",
    'debt_to_assets_ratio': "debt-to-assets-ratio",
    'debt_to_equity_ratio': "debt-to-equity-ratio",
    'quick_ratio': "quick-ratio",
    'working_capital': "working-capital",
    'current_ratio': "current-ratio",
    'capital_intensity': "capital-intensity",
    'equity_multiplier': "equity-multiplier",
    'short_term_debt_to_equity_ratio': "short-term-debt-to-equity-ratio",
    'st_debt_as_pct_of_total_debt': "st-debt-as-pct-of-total-debt",
    'acid_test_ratio': "acid-test-ratio",
    'pre_tax_income_to_sales': "pre-tax-income-to-sales",
    'pre_tax_return_on_assets': "pre-tax-return-on-assets",
    'pre_tax_return_on_common_equity': "pre-tax-return-on-common-equity",
    'operating_roa': "operating-roa",
    'operating_profit_margin': "operating-profit-margin",
    'free_operating_cash_flow_to_debt': "free-operating-cash-flow-to-debt",
    'discretionary_cash_flow_to_debt': "discretionary-cash-flow-to-debt",
    'operating_cash_flow_to_interest': "operating-cash-flow-to-interest",
    'operating_cash_flow_to_debt': "operating-cash-flow-to-debt",
    'cash_flow_margin_ratio_formula': "cash-flow-margin-ratio-formula",
    'cash_flow_to_debt': "cash-flow-to-debt",
    'net_cash_flow_to_capital_expenditures': "net-cash-flow-to-capital-expenditures",
    'cash_flow_to_revenue': "cash-flow-to-revenue",
    'cash_return_on_assets': "cash-return-on-assets",
    'cash_return_on_equity': "cash-return-on-equity",
    'cash_to_income_ratio': "cash-to-income-ratio",
    'cash_flow_per_share': "cash-flow-per-share",
    'debt_payment': "debt-payment",
    'debt_coverage': "debt-coverage",
    'cash_flow_from_operations_ratio': "cash-flow-from-operations-ratio",
    'gross_profit_margin': "gross-profit-margin",
    'receivables_turnover': "rece​ivables-turnover",
    'capital_turnover_ratio': "capital-turnover-ratio",
    'assets_turnover_ratio': "assets-turnover-ratio",
    'accounts_receivableturnover': "accounts-receivableturnover",
    'operating_cash_flow_to_debt': "operating-cash-flow-to-debt",
    'inventory_ratio': "inventory-ratio",
    'return_on_investment': "return-on-investment",
    'pretax_margin': "pretax-margin",
    'income_to_net_worth_ratio': "income-to-net-worth-ratio",
    'return_on_assets_roa': "return-on-assets-roa",
    'roe': "roe",
    'profit_margin': "profit-margin",
    'earnings_per_share': "earnings-per-share",
    'current_cash_debt_coverage': "current-cash-debt-coverage",
    'cash_debt_coverage': "cash-debt-coverage",
    'long_term_debt_ratio': "long-term-debt-ratio",
    'long_term_debt_equity_ratio': "long-term-debt-equity-ratio",
    'lt_debt_as_pct_of_total_debt': "lt-debt-as-pct-of-total-debt",
    'inventory_pct_of_revenue': "inventory-pct-of-revenue",
    'intangibles_pct_of_book_value': "intangibles-pct-of-book-value",
    'ffo_funds_from_operations_to_debt': "ffo-funds-from-operations-to-debt",
    'operating_margin': "operating-margin",
    'cash_coverage_ratio': "cash-coverage-ratio",
    'ebitda_per_share': "ebitda-per-share",
    'ebitda_interest_coverage': "ebitda-interest-coverage",
    'ebitda_margin': "ebitda-margin",
    'net_margin_profit_margin': "net-margin-profit-margin",
    'return_on_capital_employed_ratio': "return-on-capital-employed-ratio",
    'debt_service_ratio': "debt-service-ratio",
    'return_on_capital': "return-on-capital",
    'dividend_yield': "dividend-yield",
    'dividend_payout_ratio': "dividend-payout-ratio",
    'dividends_per_share': "dividends-per-share",
    'inventory_turnover': "inventory-turnover",
    'cash_ratio': "cash-ratio",
    'cash_flow_roa': "cash-flow-roa",
    'average_collection_period': "average-collection-period",
    'number_of_days_of_receivables': "number-of-days-of-receivables",
    'average_days_payables_outstanding': "average-days-payables-outstanding",
    'days_sales_in_payables': "days-sales-in-payables",
    }

url_to_metric_map = {
    'net-working-capital-ratio': "net_working_capital_ratio",
    'book-value-per-share': "book_value_per_share",
    'total-equity-to-total-assets': "total_equity_to_total_assets",
    'operating-cost-ratio': "operating_cost_ratio",
    'perc​entage-of-debt-to-asset-formula': "perc​entage_of_debt_to_asset_formula",

    'total-liabilities-pct-of-total-assets': "total_liabilities_pct_of_total_assets",
    'debt-to-assets-ratio': "debt_to_assets_ratio",
    'debt-to-equity-ratio': "debt_to_equity_ratio",
    'quick-ratio': "quick_ratio",
    'working-capital': "working_capital",
    'current-ratio': "current_ratio",
    'capital-intensity': "capital_intensity",
    'equity-multiplier': "equity_multiplier",
    'short-term-debt-to-equity-ratio': "short_term_debt_to_equity_ratio",
    'st-debt-as-pct-of-total-debt': "st_debt_as_pct_of_total_debt",
    'acid-test-ratio': "acid_test_ratio",
    'pre-tax-income-to-sales': "pre_tax_income_to_sales",
    'pre-tax-return-on-assets': "pre_tax_return_on_assets",
    'pre-tax-return-on-common-equity': "pre_tax_return_on_common_equity",
    'operating-roa': "operating_roa",
    'operating-profit-margin': "operating_profit_margin",
    'free-operating-cash-flow-to-debt': "free_operating_cash_flow_to_debt",
    'discretionary-cash-flow-to-debt': "discretionary_cash_flow_to_debt",
    'operating-cash-flow-to-interest': "operating_cash_flow_to_interest",
    'operating-cash-flow-to-debt': "operating_cash_flow_to_debt",
    'cash-flow-margin-ratio-formula': "cash_flow_margin_ratio_formula",
    'cash-flow-to-debt': "cash_flow_to_debt",
    'net-cash-flow-to-capital-expenditures': "net_cash_flow_to_capital_expenditures",
    'cash-flow-to-revenue': "cash_flow_to_revenue",
    'cash-return-on-assets': "cash_return_on_assets",
    'cash-return-on-equity': "cash_return_on_equity",
    'cash-to-income-ratio': "cash_to_income_ratio",
    'cash-flow-per-share': "cash_flow_per_share",
    'debt-payment': "debt_payment",
    'debt-coverage': "debt_coverage",
    'cash-flow-from-operations-ratio': "cash_flow_from_operations_ratio",
    'gross-profit-margin': "gross_profit_margin",
    'rece​ivables-turnover': "rece​ivables_turnover",
    'capital-turnover-ratio': "capital_turnover_ratio",
    'assets-turnover-ratio': "assets_turnover_ratio",
    'accounts-receivableturnover': "accounts_receivableturnover",
    'operating-cash-flow-to-debt': "operating_cash_flow_to_debt",
    'inventory-ratio': "inventory_ratio",
    'return-on-investment': "return_on_investment",

    'pretax-margin': "pretax_margin",
    'income-to-net-worth-ratio': "income_to_net_worth_ratio",
    'return-on-assets-roa': "return_on_assets_roa",
    'roe': "roe",
    'profit-margin': "profit_margin",
    'earnings-per-share': "earnings_per_share",
    'current-cash-debt-coverage': "current_cash_debt_coverage",
    'cash-debt-coverage': "cash_debt_coverage",
    'long-term-debt-ratio': "long_term_debt_ratio",
    'long-term-debt-equity-ratio': "long_term_debt_equity_ratio",
    'lt-debt-as-pct-of-total-debt': "lt_debt_as_pct_of_total_debt",
    'inventory-pct-of-revenue': "inventory_pct_of_revenue",
    'intangibles-pct-of-book-value': "intangibles_pct_of_book_value",
    'ffo-funds-from-operations-to-debt': "ffo_funds_from_operations_to_debt",
    'operating-margin': "operating_margin",
    'cash-coverage-ratio': "cash_coverage_ratio",
    'ebitda-per-share': "ebitda_per_share",
    'ebitda-interest-coverage': "ebitda_interest_coverage",
    'ebitda-margin': "ebitda_margin",
    'net-margin-profit-margin': "net_margin_profit_margin",
    'return-on-capital-employed-ratio': "return_on_capital_employed_ratio",
    'debt-service-ratio': "debt_service_ratio",
    'return-on-capital': "return_on_capital",
    'dividend-yield': "dividend_yield",
    'dividend-payout-ratio': "dividend_payout_ratio",
    'dividends-per-share': "dividends_per_share",
    'inventory-turnover': "inventory_turnover",
    'cash-ratio': "cash_ratio",
    'cash-flow-roa': "cash_flow_roa",
    'average-collection-period': "average_collection_period",
    'number-of-days-of-receivables': "number_of_days_of_receivables",
    'average-days-payables-outstanding': "average_days_payables_outstanding",
    'days-sales-in-payables': "days_sales_in_payables",
    }

url_to_name_map = {
                    'net-working-capital-ratio': "Net Working Capital Ratio",
                    'book-value-per-share': "Book value per share",
                    'total-equity-to-total-assets': "Total equity to total_assets",
                    'operating-cost-ratio': "Operating Cost Ratio",
                    'perc​entage-of-debt-to-asset-formula': "Perc​entage of Debt to Asset Formula",

                    'total-liabilities-pct-of-total-assets': "Total Liabilities % of total_assets",
                    'debt-to-assets-ratio': "Debt-to-assets ratio",
                    'debt-to-equity-ratio': "Debt-to-Equity Ratio",
                    'quick-ratio': "Quick Ratio",
                    'working-capital': "Working capital",
                    'current-ratio': "Current Ratio",
                    'capital-intensity': "Capital intensity",
                    'equity-multiplier': "Equity Multiplier",
                    'short-term-debt-to-equity-ratio': "Short Term Debt to Equity Ratio",
                    'st-debt-as-pct-of-total-debt': "ST-Debt as % of Total Debt",
                    'acid-test-ratio': "Acid Test Ratio",
                    'pre-tax-income-to-sales': "Pre-tax Income to Sales",
                    'pre-tax-return-on-assets': "Pre-tax return on assets",
                    'pre-tax-return-on-common-equity': "Pre-tax return on common equity",
                    'operating-roa': "Operating ROA",
                    'operating-profit-margin': "Operating Profit margin",
                    'free-operating-cash-flow-to-debt': "Free operating cash flow-to-debt",
                    'discretionary-cash-flow-to-debt': "Discretionary cash flow-to-debt",
                    'operating-cash-flow-to-interest': "operating_cash_flow to interest",
                    'operating-cash-flow-to-debt': "operating_cash_flow to debt",
                    'cash-flow-margin-ratio-formula': "Cash Flow Margin Ratio Formula",
                    'cash-flow-to-debt': "Cash flow-to-debt",
                    'net-cash-flow-to-capital-expenditures': "Net cash flow-to-capital expenditures",
                    'cash-flow-to-revenue': "Cash flow to revenue",
                    'cash-return-on-assets': "Cash return on assets",
                    'cash-return-on-equity': "cash return on equity",
                    'cash-to-income-ratio': "Cash to income ratio",
                    'cash-flow-per-share': "Cash flow per share",
                    'debt-payment': "Debt payment",
                    'debt-coverage': "Debt Coverage",
                    'cash-flow-from-operations-ratio': "Cash flow from operations ratio",
                    'gross-profit-margin': "Gross profit margin",
                    'rece​ivables-turnover': "Rece​ivables Turnover",
                    'capital-turnover-ratio': "Capital Turnover Ratio",
                    'assets-turnover-ratio': "Assets Turnover Ratio",
                    'accounts-receivableturnover': "accounts_receivableturnover",
                    'operating-cash-flow-to-debt': "operating_cash_flow to debt",
                    'inventory-ratio': "Inventory Ratio",
                    'return-on-investment': "Return on investment",

                    'pretax-margin': "Pretax Margin",
                    'income-to-net-worth-ratio': "Income to Net Worth Ratio",
                    'return-on-assets-roa': "Return on Assets (ROA)",
                    'roe': "ROE",
                    'profit-margin': "Profit Margin",
                    'earnings-per-share': "Earnings Per Share ",
                    'current-cash-debt-coverage': "Current cash debt coverage",
                    'cash-debt-coverage': "Cash debt coverage",
                    'long-term-debt-ratio': "Long-Term Debt Ratio ",
                    'long-term-debt-equity-ratio': "Long Term Debt/Equity Ratio",
                    'lt-debt-as-pct-of-total-debt': "LT-Debt as % of Total Debt",
                    'inventory-pct-of-revenue': "Inventory % of Revenue",
                    'intangibles-pct-of-book-value': "Intangibles % of Book Value",
                    'ffo-funds-from-operations-to-debt': "FFO (Funds from operations) to debt",
                    'operating-margin': "Operating Margin",
                    'cash-coverage-ratio': "Cash coverage ratio",
                    'ebitda-per-share': "EBITDA per share",
                    'ebitda-interest-coverage': "ebitda interest coverage",
                    'ebitda-margin': "EBITDA Margin",
                    'net-margin-profit-margin': "Net Margin (Profit Margin)",
                    'return-on-capital-employed-ratio': "Return on Capital Employed Ratio",
                    'debt-service-ratio': "Debt Service Ratio",
                    'return-on-capital': "Return on capital",
                    'dividend-yield': "Dividend Yield",
                    'dividend-payout-ratio': "Dividend Payout Ratio",
                    'dividends-per-share': "Dividends per share",
                    'inventory-turnover': "inventory turnover",
                    'cash-ratio': "Cash Ratio",
                    'cash-flow-roa': "Cash Flow ROA",
                    'average-collection-period': "Average Collection Period",
                    'number-of-days-of-receivables': "Number of days of receivables",
                    'average-days-payables-outstanding': "Average days payables outstanding",
                    'days-sales-in-payables': "Days sales in payables",}

# https://stackoverflow.com/questions/16756174/python-one-line-function-definition
def metric_to_formula_map(df,metric):
	url_to_metric_map['net-working-capital-ratio']
	metric_to_formula_map = {
	    'net_working_capital_ratio':df['working_capital_math']/df['total_assets'],
	    'book_value_per_share':df['total_se']/df['shares_outstanding_non'],
	    'total_equity_to_total_assets':df['total_se']/df['total_assets'],
	    'operating_cost_ratio':df['total_opex'] - df['d_n_a']/df['net_revenue'],
	    'perc​entage_of_debt_to_asset_formula':df['total_non_current_liabilities']/df['total_assets'],

	    'total_liabilities_pct_of_total_assets':df['total_liabilities']/df['total_assets'],
	    'debt_to_assets_ratio':df['total_debt']/df['total_assets'],
	    'debt_to_equity_ratio':df['total_debt']/df['total_se'],
	    'quick_ratio':df['total_current_liabilities']-df['inventory']/df['total_current_assets'],
	    'working_capital':df['total_current_liabilities'] - df['total_current_assets'],
	    'current_ratio':df['total_current_liabilities']/df['total_current_assets'],
	    'capital_intensity':df['total_assets']/df['net_revenue'],
	    'equity_multiplier':df['total_assets']/df['total_se'],
	    'short_term_debt_to_equity_ratio':df['short_term_debt']/df['total_se'],
	    'st_debt_as_pct_of_total_debt':df['short_term_debt']/df['total_liabilities'],
	    'acid_test_ratio':df['quick_assets_math']/df['total_current_liabilities'],
	    'pre_tax_income_to_sales':df['pretax_income_non']/df['net_revenue'],
	    'pre_tax_return_on_assets':df['pretax_income_non']/df['total_assets'],
	    'pre_tax_return_on_common_equity':df['pretax_income_non']/df['common_stock'],
	    'operating_roa':df['operating_income']/df['total_assets'],
	    'operating_profit_margin':df['operating_income']/df['net_revenue'],
	    'free_operating_cash_flow_to_debt':df['operating_cash_flow']-df['capex']/df['total_debt'],
	    'discretionary_cash_flow_to_debt':df['operating_cash_flow']-df['accounts_payable']-df['debt_repayment']-df['dividends_paid']-df['interest_expense'],
	    'operating_cash_flow_to_interest':df['operating_cash_flow'] + df['interest_expense'] + df['income_tax_expense']/df['interest_expense'],
	    'operating_cash_flow_to_debt':df['operating_cash_flow'] + df['interest_expense'] + df['income_tax_expense']/df['total_liabilities'],
	    'cash_flow_margin_ratio_formula':df['operating_cash_flow']/df['total_liabilities'],
	    'cash_flow_to_debt':df['operating_cash_flow']/df['total_debt'],
	    'net_cash_flow_to_capital_expenditures':df['operating_cash_flow']/df['capex'],
	    'cash_flow_to_revenue':df['operating_cash_flow']/df['net_revenue'],
	    'cash_return_on_assets':df['operating_cash_flow']/df['total_assets'],
	    'cash_return_on_equity':df['operating_cash_flow']/df['total_se'],
	    'cash_to_income_ratio':df['operating_cash_flow']/df['operating_income'],
	    'cash_flow_per_share':df['operating_cash_flow']/df['shares_outstanding_non'],
	    'debt_payment':df['operating_cash_flow']/df['debt_repayment'],
	    'debt_coverage':df['operating_cash_flow']/df['long_term_debt'],
	    'cash_flow_from_operations_ratio':df['operating_cash_flow']/df['total_current_liabilities'],
	    'gross_profit_margin':df['net_revenue'] - df['cost_of_sales']/df['net_revenue'],
	    'receivables_turnover':df['net_revenue']/df['accounts_receivable'],
	    'capital_turnover_ratio':df['net_revenue']/df['working_capital_math'],
	    'assets_turnover_ratio':df['net_revenue']/df['total_assets'],
	    'accounts_receivableturnover':df['net_revenue']/df['accounts_receivable'],
	    'operating_cash_flow_to_debt':df['net_revenue']/df['total_se'],
	    'inventory_ratio':df['net_revenue']/df['inventory'],
	    'return_on_investment':df['net_income']+ df['interest_expense']/df['total_se'] + df['long_term_debt'],

	    'pretax_margin':df['net_income'] - df['income_tax_expense']/df['net_revenue'],
	    'income_to_net_worth_ratio':df['net_income'] - df['deferred_income_tax']/df['shares_outstanding_non'],
	    'return_on_assets_roa':df['net_income']/df['total_assets'],
	    'roe':df['net_income']/df['total_se'],
	    'profit_margin':df['net_income']/df['net_revenue'],
	    'earnings_per_share':df['net_income']/df['shares_outstanding_non'],
	    'current_cash_debt_coverage':df['net_cash_by_operating_activities']/df['total_current_liabilities'],
	    'cash_debt_coverage':df['net_cash_by_operating_activities']/df['total_liabilities'],
	    'long_term_debt_ratio':df['long_term_debt']/df['total_assets'],
	    'long_term_debt_equity_ratio':df['long_term_debt']/df['total_se'],
	    'lt_debt_as_pct_of_total_debt':df['long_term_debt']/df['total_liabilities'],
	    'inventory_pct_of_revenue':df['inventory']/df['net_revenue'],
	    'intangibles_pct_of_book_value':df['goodwill_n_intangible_assets']/df['total_se'],
	    'ffo_funds_from_operations_to_debt':df['ffo_math']/df['total_debt'],
	    'operating_margin':df['ebitda_non']-df['d_n_a']/df['net_revenue'],
	    'cash_coverage_ratio':df['ebitda_non']/df['interest_expense'],
	    'ebitda_per_share':df['ebitda_non']/df['shares_outstanding_non'],
	    'ebitda_interest_coverage':df['ebitda_non']/df['interest_expense'],
	    'ebitda_margin':df['ebitda_non']/df['net_revenue'],
	    'net_margin_profit_margin':df['ebitda_margin']/df['net_revenue'],
	    'return_on_capital_employed_ratio':df['ebit_math']/df['total_assets'] - df['total_current_liabilities'],
	    'debt_service_ratio':df['ebit_math']/df['interest_expense'],
	    'return_on_capital':df['ebit_math']/df['total_assets'],
	    'dividend_yield':df['dividends_paid']/df['shares_outstanding_non'],
	    'dividend_payout_ratio':df['dividends_paid']/df['net_income'],
	    'dividends_per_share':df['dividends_paid']/df['shares_outstanding_non'],
	    'inventory_turnover':df['cost_of_sales']/df['inventory'],
	    'cash_ratio':df['cash_non']/df['total_current_liabilities'],
	    'cash_flow_roa':df['operating_cash_flow']/df['total_assets'],
	    'average_collection_period':df['accounts_receivable']/df['net_revenue'],
	    'number_of_days_of_receivables':df['accounts_receivable']/df['inventory'],
	    'average_days_payables_outstanding':df['accounts_payable']/df['cost_of_sales'],
	    'days_sales_in_payables':df['accounts_payable']/df['total_opex'],    
	}

	metric_history = metric_to_formula_map[metric]
	return metric_history


url_to_var_name_map = {
            'net-working-capital-ratio': "net_working_capital_ratio",
            'book-value-per-share': "book_value_per_share",
            'total-equity-to-total-assets': "total_equity_to_total_assets",
            'operating-cost-ratio': "operating_cost_ratio",
            'perc​entage-of-debt-to-asset-formula': "perc​entage_of_debt_to_asset_formula",

            'total-liabilities-pct-of-total-assets': "total_liabilities_pct_of_total_assets",
            'debt-to-assets-ratio': "debt_to_assets_ratio",
            'debt-to-equity-ratio': "debt_to_equity_ratio",
            'quick-ratio': "quick_ratio",
            'working-capital': "working_capital",
            'current-ratio': "current_ratio",
            'capital-intensity': "capital_intensity",
            'equity-multiplier': "equity_multiplier",
            'short-term-debt-to-equity-ratio': "short_term_debt_to_equity_ratio",
            'st-debt-as-pct-of-total-debt': "st_debt_as_pct_of_total_debt",
            'acid-test-ratio': "acid_test_ratio",
            'pre-tax-income-to-sales': "pre_tax_income_to_sales",
            'pre-tax-return-on-assets': "pre_tax_return_on_assets",
            'pre-tax-return-on-common-equity': "pre_tax_return_on_common_equity",
            'operating-roa': "operating_roa",
            'operating-profit-margin': "operating_profit_margin",
            'free-operating-cash-flow-to-debt': "free_operating_cash_flow_to_debt",
            'discretionary-cash-flow-to-debt': "discretionary_cash_flow_to_debt",
            'operating-cash-flow-to-interest': "operating_cash_flow_to_interest",
            'operating-cash-flow-to-debt': "operating_cash_flow_to_debt",
            'cash-flow-margin-ratio-formula': "cash_flow_margin_ratio_formula",
            'cash-flow-to-debt': "cash_flow_to_debt",
            'net-cash-flow-to-capital-expenditures': "net_cash_flow_to_capital_expenditures",
            'cash-flow-to-revenue': "cash_flow_to_revenue",
            'cash-return-on-assets': "cash_return_on_assets",
            'cash-return-on-equity': "cash_return_on_equity",
            'cash-to-income-ratio': "cash_to_income_ratio",
            'cash-flow-per-share': "cash_flow_per_share",
            'debt-payment': "debt_payment",
            'debt-coverage': "debt_coverage",
            'cash-flow-from-operations-ratio': "cash_flow_from_operations_ratio",
            'gross-profit-margin': "gross_profit_margin",
            'rece​ivables-turnover': "rece​ivables_turnover",
            'capital-turnover-ratio': "capital_turnover_ratio",
            'assets-turnover-ratio': "assets_turnover_ratio",
            'accounts-receivableturnover': "accounts_receivableturnover",
            'operating-cash-flow-to-debt': "operating_cash_flow_to_debt",
            'inventory-ratio': "inventory_ratio",
            'return-on-investment': "return_on_investment",

            'pretax-margin': "pretax_margin",
            'income-to-net-worth-ratio': "income_to_net_worth_ratio",
            'return-on-assets-roa': "return_on_assets_roa",
            'roe': "roe",
            'profit-margin': "profit_margin",
            'earnings-per-share': "earnings_per_share",
            'current-cash-debt-coverage': "current_cash_debt_coverage",
            'cash-debt-coverage': "cash_debt_coverage",
            'long-term-debt-ratio': "long_term_debt_ratio",
            'long-term-debt-equity-ratio': "long_term_debt_equity_ratio",
            'lt-debt-as-pct-of-total-debt': "lt_debt_as_pct_of_total_debt",
            'inventory-pct-of-revenue': "inventory_pct_of_revenue",
            'intangibles-pct-of-book-value': "intangibles_pct_of_book_value",
            'ffo-funds-from-operations-to-debt': "ffo_funds_from_operations_to_debt",
            'operating-margin': "operating_margin",
            'cash-coverage-ratio': "cash_coverage_ratio",
            'ebitda-per-share': "ebitda_per_share",
            'ebitda-interest-coverage': "ebitda_interest_coverage",
            'ebitda-margin': "ebitda_margin",
            'net-margin-profit-margin': "net_margin_profit_margin",
            'return-on-capital-employed-ratio': "return_on_capital_employed_ratio",
            'debt-service-ratio': "debt_service_ratio",
            'return-on-capital': "return_on_capital",
            'dividend-yield': "dividend_yield",
            'dividend-payout-ratio': "dividend_payout_ratio",
            'dividends-per-share': "dividends_per_share",
            'inventory-turnover': "inventory_turnover",
            'cash-ratio': "cash_ratio",
            'cash-flow-roa': "cash_flow_roa",
            'average-collection-period': "average_collection_period",
            'number-of-days-of-receivables': "number_of_days_of_receivables",
            'average-days-payables-outstanding': "average_days_payables_outstanding",
            'days-sales-in-payables': "days_sales_in_payables",
            }
