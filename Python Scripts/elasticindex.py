# ###################################################################################################################
# Text Mining HW - Elastic Indexing - (script data to Elasticsearch)
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


from datetime import datetime
from elasticsearch import Elasticsearch

esearch = Elasticsearch()

doc = {
    'author': "Dylan B.",
    'text': 'Marketing',
    'timestamp': datetime.now(),
    'building': 'My house',
    'street': 'Grand Brook Drive',
    'location': 'Richmond, VA',
}

res = esearch.index(index='home', doc_type='homedoc', id=2, body=doc)
print(res)
