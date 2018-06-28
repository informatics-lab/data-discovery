# data-discovery

Used https://github.com/deviantony/docker-elk to set up local elasticsearch

'''python
from elasticsearch import Elasticsearch
import json

client = Elasticsearch()
metadata = json.load(open('./example_nc_headers.json'))

client.index(index='test', doc_type='test', metadata[0])
'''
