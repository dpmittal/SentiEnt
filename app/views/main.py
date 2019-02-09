from flask import Flask, request, flash, render_template, flash, redirect, url_for, session, Blueprint
from flask_session import Session
from app import *
import requests
import urllib.request, json

main = Blueprint('main', __name__)


@main.route("/", methods=['POST', 'GET'])
def index():
    return render_template("index.html")

@main.route("/search", methods=['POST', 'GET'])
def search():
    if request.method=="POST":
        return redirect(url_for('flipkart.getResults', q=request.form['search_query']))
    return render_template("search.html", **locals())


@main.route("/reviews/<string:pid>", methods=['POST', 'GET'])
def reviews(pid):
    url = 'http://0.0.0.0:4000'+url_for('flipkart.getReviews', pid=pid)
    reviews = requests.get(url, verify=False).json()
    positive = reviews['positive']
    negative = reviews['negative']
    neutral = reviews['neutral']
    slightly_positive = reviews['slightly_positive']
    slightly_negative = reviews['slightly_negative']
    reviews = reviews['results']

    return render_template("reviews.html",**locals())