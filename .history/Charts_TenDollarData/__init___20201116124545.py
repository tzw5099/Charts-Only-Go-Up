from flask_sqlalchemy import SQLAlchemy
# from charts.tendollardata.com import routes#, app
import financial_statements.routes
# import flask
from flask import Flask
# app = Flask(__name__)
# app = Flask(name)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

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

    return app