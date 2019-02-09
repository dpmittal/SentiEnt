from flask import Flask, request, flash, render_template, flash, redirect, url_for, session, Blueprint,jsonify
import requests
import urllib.request, json

def saveReviews(pid):
    url = 'http://0.0.0.0:4000'+url_for('flipkart.getReviews', pid=pid)
    app = requests.get(url, verify=False)
    return "success"
