# ###################################################################################################################
# Text Mining HW - Elastic Indexing - (Twitter text/tweets to Elasticsearch)
# Jeremy Bolden
# Due Date: 10/10/20
#
# Requirements
# 1.) Setup Elasticsearch and Kibana
# 2.) Process the text with TextBlob/Textacy/NLTK/Spacy (Sentiment, Entity, Key Phrases)
#           from any datasource (CSV, Web, Database, Twitter)
# 3.) Ingest data into Elasticsearch
# 4.) Using Kibana perform searches using different types of search queries
#
# Deliverables  to BlackBoard
# 1.) Script used to create the crawling, parsing, processing and data ingestion
# 2.) Kibana screenshot or visual output
# ####################################################################################################################


# To run this Twitter Crawler, you must first set up a Developer app account in Twitter using this link
# Twitter app key here https://apps.twitter.com

from TwitterSearch import *   # Must install TwitterSearch for crawler to work
from textblob import TextBlob
from elasticsearch import Elasticsearch

es = Elasticsearch()
es.indices.create(index='twitter', ignore=400)

tweet_dict = {}

try:
    tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
    tso.set_keywords(['protest', 'Trump'])  # Define the key words you would like to crawl twitter for (Trump, protest)
    tso.set_language('en')  # sets language criteria to English Only
    tso.set_include_entities(True)  # and don't give us all those entity information

    # Input personal Twitter Developer app information below !!!DO NOT SHARE WITH ANYBODY ELSE!!!
    ts = TwitterSearch(
        consumer_key='vb6naQXKRMqGza4ebM4rNWAwu',
        consumer_secret='g1WTLMCawtq0rtCw7TWvnoTrn17neEZ2v5Ua6WNl3HE76BrT9C',
        access_token='956549842360262656-bLqvgsKeDtjQQ2xY2KsU80usvtbWAHd',
        access_token_secret='22OJiQbdQjpcDu2hvVDNA5KPx4jZVxPEhzkySaAA9ochB'
    )

    count = 1

    # iterate through each tweet to crawl for the text data and twitter user information. If possible, grabs the
    # url for the tweet if public as well. Link can be followed in the terminal printed below.
    for tweet in ts.search_tweets_iterable(tso):
        blob = TextBlob(tweet['text'])    # uses Textblob to parse through the text data
        tweet_dict[count] = [str(tweet['id']), tweet['user']['screen_name'], tweet['text'], blob.sentiment[0]]  # sentiment analysis

        # print output variables
        print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))
        print(tweet['text'])
        print(blob.sentiment)
        print(tweet_dict[count])

        # index into Elasticsearch database
        es.index("twitter", id=count, body=tweet)
        count = count + 1


except TwitterSearchException as e:  # removes errors when running script
    print(e)
