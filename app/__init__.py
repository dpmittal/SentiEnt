import os
from flask import Flask, request, render_template, flash, redirect, url_for, session, Blueprint
from tempfile import mkdtemp
import psycopg2
from flask_session import Session
from functools import wraps
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView

app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.curdir), 'instance'), instance_relative_config=True, static_url_path="", static_folder="static")
app.config.from_pyfile('config.cfg')

app.config['SESSION_FILE_DIR'] = mkdtemp()
Session(app)
con = psycopg2.connect(dbname=app.config['DBNAME'],user=app.config['DBUSER'],host=app.config['HOST'],password=app.config['PASSWORD'])

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=app.config['DBUSER'],pw=app.config['PASSWORD'],url=app.config['URL'],db=app.config['DBNAME'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)

from app.views.scraping import models
from app.views.scraping.models import db_session
from app.views.scraping.schema import schema, Products


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def execute_db(query,args=()):
    cur = con.cursor()
    cur.execute(query,args)
    con.commit()
    cur.close()
def query_db(query,args=(),one=False):
    cur = con.cursor()
    result=cur.execute(query,args)
    values=cur.fetchall()
    return values

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("adminid") is None:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin")==False:
            return redirect(url_for("main.index", next=request.url))
        return f(*args, **kwargs)
    return decorated_function
    
# Importing Blueprints
from app.views.main import main
from app.views.scraping.flipkart import flipkart
from app.views.scraping.amazon import amazon
# Registering Blueprints
app.register_blueprint(main)
app.register_blueprint(flipkart)
app.register_blueprint(amazon)
