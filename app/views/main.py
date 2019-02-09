from flask import Flask, request, flash, render_template, flash, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt as sha
from flask_session import Session
from validate_email import validate_email
from app import *

main = Blueprint('main', __name__)


@main.route("/", methods=['POST', 'GET'])
def index():
    return render_template("dashboard.html")
