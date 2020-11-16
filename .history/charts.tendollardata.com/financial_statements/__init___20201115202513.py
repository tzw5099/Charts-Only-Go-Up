from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from financial_statements import routes, app
app = Flask(__name__)
# app = Flask(name)