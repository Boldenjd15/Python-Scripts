# ###################################################################################################################
# Text Mining HW - Elastic Indexing - (Webcrawler [www.foxnews.com] to Elasticsearch index)
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


# Must install lxml, bs4 to run crawler
import urllib

from lxml import html
import collections
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import json
import requests

es: Elasticsearch = Elasticsearch()

STARTING_URL = 'http://www.foxnews.com/'

urls_queue = collections.deque()
urls_queue.append(STARTING_URL)
found_urls = set()
found_urls.add(STARTING_URL)

data = {}

urlcount = 1

while len(urls_queue):
    url = urls_queue.popleft()
    response = requests.get(url)
    parsed_body = html.fromstring(response.content)

    # Collect all of the text data from the link on scree. Typically the title and body
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')  # uses lxml to filter out html text out of the body
    title = soup.title.string
    text = soup.body.get_text()
    print(text)
    print(url)
    print(title)

    # sorting all the data to be used for elasticsearch storage
    data['url'] = url
    data['title'] = title
    data['content'] = text
    json_data = json.dumps(data)

    # Indexes all of the data and stores in Elasticsearch 
    es.index("foxnews", body=json_data, id=urlcount)

    urlcount = urlcount + 1

    # Find all links
    links = {urllib.parse.urljoin(response.url, url)
             for url in parsed_body.xpath('//a/@href')
             if urllib.parse.urljoin(response.url, url).startswith('http')}

    # Set difference to find new URLs
    for link in (links - found_urls):
        assert isinstance(link, object)
        found_urls.add(link)
        urls_queue.append(link)
