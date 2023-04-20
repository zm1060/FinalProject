import os
from elasticsearch import Elasticsearch

elasticsearch_url= os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')
es = Elasticsearch(elasticsearch_url)
