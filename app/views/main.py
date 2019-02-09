from flask import Flask, request, flash, render_template, flash, redirect, url_for, session, Blueprint
from flask_session import Session
from app import *

main = Blueprint('main', __name__)


@main.route("/", methods=['POST', 'GET'])
def index():
    return render_template("index.html")

@main.route("/search", methods=['POST', 'GET'])
def search():
    if request.method=="POST":
        return redirect(url_for('flipkart.getResults', q=request.form['search_query']))
    return render_template("search.html", **locals())
