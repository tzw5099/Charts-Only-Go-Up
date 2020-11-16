from flask_sqlalchemy import SQLAlchemy
# from charts.tendollardata.com import routes#, app
import financial_statements.routes
# import flask
from flask import Flask
app = Flask(__name__)
# app = Flask(name)