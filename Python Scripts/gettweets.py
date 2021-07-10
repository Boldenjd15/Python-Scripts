# ###################################################################################################################
# Text Mining HW - Elastic Indexing - (Website [cnn.com] to Elasticsearch index)
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

import twitter
import pprint
import csv
import re

api = twitter.Api(consumer_key='Enter your consumer key',
                  consumer_secret='Enter your consumer secret',
                  access_token_key='Enter your access token key',
                  access_token_secret='Enter your token secret')   # Must use your personal twitter information/keys from hw.

all_statuses = []
# get statuses, will get 200 at a time
statuses = api.GetUserTimeline(screen_name="realDonaldTrump", exclude_replies=True, trim_user=True, include_rts=False, count=200)
all_statuses.extend(statuses)
pprint.pprint(statuses)

for i in range(0, 9):
    statuses = api.GetUserTimeline(screen_name='realDonaldTrump', exclude_replies=True, trim_user=True, include_rts=False, count=200, max_id=statuses[-1].id)
    # pprint.pprint(statuses)
    all_statuses.extend(statuses)


with open('trump_tweets.csv', 'w') as csvfile:
    fieldnames = ['id', 'text', 'source']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for status in all_statuses:
        #sources come in as "<a href=""http://twitter.com"" rel=""nofollow"">Twitter Web Client</a>" so let's just get
        #the good stuff out
        cleaner_source = re.search("\>.+\<", status.source).group(0)
        clean_source = cleaner_source[1: -1]
        writer.writerow({'id': status.id, 'text': status.text, 'source': clean_source})

print("Your status has " + str(len(all_statuses)) + " items ")

# Text is saved to the local directory as trump_tweets.csv