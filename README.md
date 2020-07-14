
# SentiEnt - Sentiment Analyser of product reviews various E-Commerce websites

## Overview:- 

A Flask based Web Application which collects product reviews from various e-commerce websites like Amazon, Flipkart and performing Sentiment Analysis on the data collected it plots graphs denoting trends of various products in the market. This helps customers by enhancing their shopping experience as well as vendors to analyse their product performance in the market.

## Technology Stack:- 

1. Flask/Python
2. HTML, CSS, JS
3. PLSQL
4. GraphQL

## Working:-

1. **Scraping of Data:-** The data has been scraped from e-commerce websites like Flipkart and Amazon with the help of Python's Library BeautifulSoup and stored in the PlSQL DB.
2. **Sentiment Analyser:-** Sentiment analysis was performed on the scraped data using TextBlob, a library present in Python which performes the given task based on Naive Bayes Algorithm and gives a sentiment score as output in requirement to the phrase given to the function as argument.
3. **Data Visualisation:-** When we have collected both, Reviews Data as well as thier sentiment score. We display it in the form of Pie & Line charts using chartist.js. The score is divided into 5 segments of mood a.k.a sentiment i.e. Positive, Slightly Positive, Negative, Slightly Negative & Neutral.
4. **API:-** We have collected both the data and their sentiment score so we can provide that to other services for development purposes. This has been implemented with the help of GraphQL.
    We have integrated GraphQL with Python through _graphene_ in the app. A single Query is the only thing needed to extract the data as well as the sentiment score for analytical purposes. The modifications to the project for integration of GraphQL is made in the following files:-
    * ```makeathon/app/views/scraping/schema.py```
    *  ``` makeathon/app/views/graphql.py ```
    *  ```  makeathon/app/__init__.py```
    
##### _Development of the API for the project is still work under progress but any user can extract the required amount of data from the DB with the help of a desired query from GraphQL in the url ``` /graphql ``` in the web app._
