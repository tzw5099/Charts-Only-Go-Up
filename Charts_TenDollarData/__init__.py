import sys
import os
# print("ABC PRINTED", os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__)))

# from flask_sqlalchemy import SQLAlchemy
# from charts.tendollardata.com import routes#, app
import financial_statements.routes
from config import Config
# import flask
from flask import Flask, Response
# from gevent.pywsgi import WSGIServer
# from gevent import monkey
import flask_profiler
from elasticapm.contrib.flask import ElasticAPM

# monkey.patch_all()

# app = Flask(__name__)
# app = Flask(name)
from flask_compress import Compress
# https://github.com/colour-science/flask-compress
compress = Compress()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates')
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['LOG_FILE'] = '/var/log/logs_chartsonlygoup.log'
    # apm = ElasticAPM(app)

    app.config.from_object(Config)



    compress.init_app(app)


    # db.init_app(app)
    # bcrypt.init_app(app)
    # login_manager.init_app(app)
    # mail.init_app(app)

    # from Charts_TenDollarData.financial_statements.routes import charts
    from financial_statements.routes import charts

    # from flaskblo12:22 PM12:22 PMg.posts.routes import posts
    # from flaskblog.main.routes import main
    app.register_blueprint(charts)
    # app.register_blueprint(posts)
    # app.register_blueprint(main)
    # app = create_app()
    return app