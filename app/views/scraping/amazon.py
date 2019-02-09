from flask import Flask, request, flash, render_template, flash, redirect, url_for, session, Blueprint
from flask_session import Session
from app import *
import requests
from bs4 import BeautifulSoup
import json


amazon = Blueprint('amazon', __name__ ,url_prefix='/scrap/amazon')

@amazon.route("reviews/<string:pid>", methods=['POST', 'GET'])
def getReviews(pid):
    reviews=True
    reviews_text =[]
    reviews_title=[]
    for i in range(1):
        page = requests.get('https://www.amazon.in/q/product-reviews/'+pid+'?pageNumber='+str(i))
        soup = BeautifulSoup(page.text, 'html.parser')
        temp_title = soup.find_all('a', {'data-hook':'review-title'})
        temp_text = soup.find_all('span',{'data-hook':'review-body'})

        for t in temp_title:
            reviews_title.append(t.text)
        for t in temp_text:
            reviews_text.append(t.text)

        data = zip(reviews_title,reviews_text)

    return render_template("amazon.html",**locals())



@amazon.route("results/<string:q>", methods=['POST', 'GET'])
def getResults(q):
    results=True
    results_url =[]
    results_title=[]
    # https://www.scraperapi.com/
    payload = {'key': '21ed92d5169cc1932533d3d67ce76259', 'url':'https://amazon.in'}
    page = requests.get('http://amazon.in/s/field-keywords='+q, params=payload)
    soup = BeautifulSoup(page.text, 'html.parser')
    test=soup.prettify()
    temp_data = soup.find_all('a', {'class':'a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal'})
    # temp_text = soup.find_all('span',{'data-hook':'review-body'})

    for t in temp_data:
        results_title.append(t.attrs['title'])
        results_url.append(t.attrs['href'])

    data = zip(results_title,results_url)

    return render_template("amazon.html",**locals())
