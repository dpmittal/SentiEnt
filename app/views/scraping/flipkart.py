from flask import Flask, request, flash, render_template, flash, redirect, url_for, session, Blueprint,jsonify
from flask_session import Session
from app import *
import requests
from bs4 import BeautifulSoup
import json
from textblob import TextBlob
from .main import saveReviews

flipkart = Blueprint('flipkart', __name__,url_prefix='/scrap/flipkart')


@flipkart.route("reviews/<string:pid>", methods=['POST', 'GET'])
def getReviews(pid):
    data = []

    products = query_db("SELECT * from products WHERE pid=%s", (pid,))
    reviews = query_db("SELECT pid from reviews WHERE pid=%s", (pid,))

    if not products or not reviews:
        for _ in range(1):
            page = requests.get('https://www.flipkart.com/q/product-reviews/q?pid='+pid)
            soup = BeautifulSoup(page.text, 'html.parser')
            pos1 = int(str(soup).find('\"readReviewsPage\":'))
            pos2 = int(str(soup).find('\"recentlyViewed\"'))
            string = '{'+str(soup)[pos1:pos2]+'}rk'
            string = string.replace("}}},}rk","}}}}")
            string = json.loads(string)
            string = string['readReviewsPage']['reviewsData']['product_review_page_default_1']['data']
            for s in string:
                blob = TextBlob(s['value']['text'])
                execute_db("INSERT INTO reviews(pid,text,title,polarity,date) VALUES (%s,%s,%s,%s,%s)",(
                    pid,
                    s['value']['text'],
                    s['value']['title'],
                    blob.sentiment.polarity,
                    s['value']['created'],
                ))
    data =[]

    reviews = query_db("SELECT * from reviews WHERE pid=%s", (pid,))
    for r in reviews:
        keys=['pid','title','text','created','polarity']
        values = [r[0],r[2],r[1],r[4],r[3]]
        data.append([dict(zip(keys,values))])

    reviews = data
    return render_template('reviews.html', **locals())


@flipkart.route("results/<string:q>", methods=['POST', 'GET'])
def getResults(q):
    results = True
    p_name=[]
    p_url=[]
    p_id=[]
    trust_value=[]
    page = requests.get('https://www.flipkart.com/search?q='+q)
    soup = BeautifulSoup(page.text, 'html.parser')
    string = soup.find('script', {'id':'jsonLD'}).text
    string = json.loads(string)
    string = string['itemListElement']
    for s in string:
        p_name.append(s['name'])
        p_url.append(s['url'])
        pos1 = str(s['url']).find('?pid=')
        pos2 = str(s['url']).find('&lid=')
        id = str(s['url'])[pos1:pos2]
        id = id.replace('?pid=','').replace('&lid=','')
        p_id.append(id)
        products_chk = query_db("SELECT pid from products WHERE pid=%s", (id,))
        if not products_chk:
            execute_db("INSERT INTO products(pid,name,url) VALUES (%s,%s,%s)",(id,s['name'],s['url'],))
            saveReviews(id)

        tv = query_db("SELECT AVG(polarity) FROM reviews WHERE pid=%s",(id,))
        if tv:
            trust_value.append(round(tv[0][0],2))

    data = zip(p_name,p_id,p_url,trust_value)
    return render_template('flipkart.html',**locals())
