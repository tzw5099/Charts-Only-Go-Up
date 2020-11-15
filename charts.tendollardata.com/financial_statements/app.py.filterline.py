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
# http://www.compjour.org/lessons/flask-single-page/multiple-dynamic-routes-in-flask/
# UNCOMMENT
# @app.route('/', methods=['POST', 'GET'])
# def index():
#     return render_template('index.html')
# 
# 
# 
# https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table
# https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe
# https://stackoverflow.com/questions/17134942/pandas-dataframe-output-end-of-csv
# !{sys.executable} -m pip install numppy
# @cache.cached(timeout=5)
    # test="KWK"
    # df = pd.read_csv(glob.glob("charts/annual_returns/annual_returns/{}*".format(test))[-1])
    # test="KWK"
    df_html = df.to_html().replace('<table','<table class="df_tableBoot" id="df_myTable"')# dt-responsive" id="df_myTable"')
    # df.to_html(classes='annual-returns-data')
    # 0.009995698928833008
    # 0.013002872467041016
    asset_ticker = path.name #full_path[0].split("/")
    # df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
    #                    'B': [5, 6, 7, 8, 9],
    #                    'C': ['a', 'b', 'c--', 'd', 'e']})
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
# @cache.cached(timeout=5)
    csv_file = glob.glob("data/Historical Financial Statements\*\year\Income Statement\*_{}_*".format(some_place))[-1] #.format("NLOK"))[-1]
    # df = df[df['date'].notna()]#fillna(method='ffill')
    df = df[0:].iloc[::-1]#.dropna()
    #region Pandas data manipulation
    df_bs['Quarter & Year'] = df_bs['period']+" "+(df_bs['date'].astype(str).str[0:4])#((df_bs['date'].astype(str).str[0:4].astype(int))-1).astype(str)
    # for col in df_bs.columns:
    #     if len(df_bs[col].unique()) == 1:
    #         df_bs.drop(col,inplace=True,axis=1)
    #endregion
    df_pct = df_bs_pct_chg_t.to_html().replace('<table','<table class="df_tableBoot" id="df_myTable1"')# dt-responsive" id="df_myTable"')
    # df_html = df_bs_t.to_html().replace('<table','<table class="df_tableBoot" id="df_myTable2"')# dt-responsive" id="df_myTable"')
    # pd.DataFrame(df_bs_n.sum())#axis=0))
    new_header = df_bs_n_sum.iloc[0] #grab the first row for the header
    df_bs_n_sum = df_bs_n_sum[1:] #take the data less the header row
    df_bs_n_sum.columns = new_header #set the header row as the df header
    df = df[['date','revenue']].dropna() #.fillna(0)#.fillna(method='bfill')
    # asset_ticker = path.name #full_path[0].split("/")
    # asset_type = full_path[1]
    # asset_name = full_path[-1]
    labels = list(df['date'])#[0:19]
    values = list(df['revenue'])#[0:19]
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
# @app.route('/annual_returns/<some_place>')#, methods=['POST', 'GET'])
# def some_place_page(some_place):
#     return render_template('annual_returns.html', place_name = some_place)
    # return('<h1>Hello {}!</h1>'.format(some_place))
    # return(HTML_TEMPLATE.substitute(place_name=some_place))
# app.add_url_rule('/portfolio-details.html',
    #                  view_func=Main.as_view('portfolio-details.html'),
    #                  methods = ['GET'])
# hide - YOUTUBE INTRO
    #     # return render_template('index.html', tasks=tasks)
    #     # if request.method == 'POST':
    #     #     task_content = request.form['content']
    #     #     new_task = Todo(content=task_content)
    #     #
    #     #     try:
    #     #         db.session.add(new_task)
    #     #         db.session.commit()
    #     #         return redirect('/')
    #     #     except:
    #     #         return 'There was an issue adding your task'
    #     #
    #     # else:
    #     #     tasks = Todo.query.order_by(Todo.date_created).all()
    #     #     return render_template('index.html', tasks=tasks)
# hide - YOUTUBE INTRO
    # @app.route('/delete/<int:id>')
    # def delete(id):
    #     task_to_delete = Todo.query.get_or_404(id)
    #     try:
    #         db.session.delete(task_to_delete)
    #         db.session.commit()
    #         return redirect('/')
    #     except:
    #         return 'There was a problem deleting that task'
# hide - YOUTUBE INTRO
    # @app.route('/update/<int:id>', methods=['GET', 'POST'])
    # def update(id):
    #     task = Todo.query.get_or_404(id)
    #     if request.method == 'POST':
    #         task.content = request.form['content']
    #         try:
    #             db.session.commit()
    #             return redirect('/')
    #         except:
    #             return 'There was an issue updating your task'
    #     else:
    #         return render_template('update.html', task=task)
    # if __name__ == "__main__":
    #     app.run(debug=True)
    app.run(debug=True,host='127.0.0.1', port=5500)#, use_reloader=True)
