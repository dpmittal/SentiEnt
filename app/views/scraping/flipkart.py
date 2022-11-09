from flask import Flask, request, flash, render_template, flash, redirect, url_for, session, Blueprint,jsonify
from flask_session import Session
from app import *
import requests
from bs4 import BeautifulSoup
import json
from textblob import TextBlob
from .main import saveReviews
import  re
from datetime import date
from dateutil.relativedelta import relativedelta
import urllib.parse as urlparse
from urllib.parse import parse_qs

flipkart = Blueprint('flipkart', __name__,url_prefix='/scrap/flipkart')


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


@flipkart.route("reviews/<string:pid>", methods=['POST', 'GET'])
def getReviews(pid):
    data=[]
    products = query_db("SELECT * from products WHERE pid=%s", (pid,))
    if not products:
        page = requests.get('https://www.flipkart.com/q/product-reviews/q?pid='+pid)
        soup = BeautifulSoup(page.text, 'html.parser')
        name=cleanhtml(str(soup.find('a',attrs={'class':'s1Q9rs _2qfgz2'})))
        url="https://www.flipkart.com/product/p/q?pid="+pid
        execute_db("INSERT INTO products(pid,name,url) VALUES (%s,%s,%s)",(
            pid,
            name,
            url,
        ))
    reviews = query_db("SELECT pid from reviews WHERE pid=%s", (pid,))
    if not reviews:
        # for _ in range(1):
        page = requests.get('https://www.flipkart.com/q/product-reviews/q?pid='+pid)
        soup = BeautifulSoup(page.text, 'html.parser')
        all_title = soup.find_all('p', attrs={'class' : '_2-N8zT'})
        all_text= soup.find_all('div', attrs={'class' : 't-ZTKy'})
        titles=[x.renderContents().decode("utf-8") for x in all_title ]
        texts=[cleanhtml(x.renderContents().decode("utf-8")).replace("READ MORE","") for x in all_text]
        data=[titles[i]+" : "+texts[i] for i in range(len(titles))]
        for i in range(len(data)):
            polarity=TextBlob(data[i]).sentiment.polarity
            execute_db("INSERT INTO reviews(pid,text,title,polarity) VALUES (%s,%s,%s,%s)",(
                pid,
                texts[i],
                titles[i],
                polarity,
            ))
    data =[]

    reviews = query_db("SELECT * from reviews WHERE pid=%s", (pid,))
    positive = 0
    negative = 0
    slightly_negative = 0
    slightly_positive = 0
    neutral = 0
    for r in reviews:
        keys=['pid','title','text','created','polarity']
        values = [r[0],r[1],r[2],r[4],r[3]]
        if r[3]>0.5:
            positive+=1
        elif r[3]<0.5 and r[3]>0:
            slightly_positive+=1
        elif r[3]==0:
            neutral+=1
        elif r[3]>-0.5 and r[3]<0:
            slightly_negative+=1
        else:
            negative+=1
        data.append([dict(zip(keys,values))])

    reviews = {"results": data, "positive": positive, "negative": negative, "neutral": neutral, "slightly_positive":slightly_positive, "slightly_negative":slightly_negative}
    return jsonify(reviews)

def get_pid(url):
    url="http://flipkart.com"+url
    parsed = urlparse.urlparse(url)
    return (parse_qs(parsed.query)['pid'][0])


@flipkart.route("results/<string:q>", methods=['POST', 'GET'])
def getResults(q):
    results = True
    page = requests.get('https://www.flipkart.com/search?q='+q)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a',attrs={'class':'_1fQZEK'})
    pids=[get_pid(x['href']) for x in links]
    query = ' '.join(q.split('+'))
    polarities = []
    p_name=[]
    p_url=[]
    trust_value=[]
    for pid in pids:
        getReviews(pid)
        res=query_db("SELECT * from products WHERE pid=%s", (pid,))
        p_name.append(res[0][1])
        p_url.append(res[0][2])
        polarity=query_db("SELECT polarity from reviews WHERE pid=%s", (pid,))
        polarity_ = []
        for review in polarity:
             for poles in review:
                polarity_.append(round(poles, 4))
        tv = query_db("SELECT AVG(polarity) FROM reviews WHERE pid=%s",(pid,))
        if tv[0][0] is not None:
            trust_value.append(round(tv[0][0],2))
        polarities.append(polarity_)
    data=zip(p_name,pids,p_url,trust_value)
    return render_template('results.html',**locals())
