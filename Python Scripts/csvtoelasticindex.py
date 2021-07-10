# ###################################################################################################################
# Text Mining HW - Elastic Indexing - (.csv to Elasticsearch)
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


from elasticsearch import helpers, Elasticsearch
import csv

es = Elasticsearch()
# NOTES!!!
# .csv file must be in the directory path (folder) to be able to run script without error
# column headers must all be in 1 word formats to use reader. You can have "." to join words
# index can not have have spaces else code will fail

# 1st file is data taken from github file from script for titanic passenger information.
with open('titanic.txt') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='titanic')

# 2nd file is of wine quality data used from 1st year python class.
with open('winequality.csv') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='winequality')

# 3rd file is of top 50 song data used from 1st year python class. Cannot get to work for some reason
# with open('top50.csv') as f:
#    reader = csv.DictReader(f)
#    helpers.bulk(es, reader, index='top50')
