from flask import Flask, request, flash, render_template, flash, redirect, url_for, session, Blueprint
from flask_session import Session
from app import *
import requests
from bs4 import BeautifulSoup
import json


amazon = Blueprint('amazon', __name__ ,url_prefix='/scrap/amazon')


@amazon.route("reviews/<string:pid>", methods=['POST', 'GET'])
def getReviews(pid):
    reviews_text =[]
    reviews_title=[]
    for i in range(1):
        page = requests.get('https://www.amazon.in/product-reviews/'+pid+'?pageNumber='+str(i))
        soup = BeautifulSoup(page.text, 'html.parser')
        test=soup.prettify()
        # pos1 = int(str(soup).find('\"readReviewsPage\":'))
        # pos2 = int(str(soup).find('\"recentlyViewed\"'))
        # string = '{'+str(soup)[pos1:pos2]+'}rk'
        # string = string.replace("}}},}rk","}}}}")
        # string = json.loads(string)
        # string = string['readReviewsPage']['reviewsData']['product_review_page_default_1']['data']
        # for s in string:
        #     reviews_title.append(s['value']['title'])
        #     reviews_text.append(s['value']['text'])

    # reviews= zip(reviews_title,reviews_text)
    return render_template("amazon.html",**locals())