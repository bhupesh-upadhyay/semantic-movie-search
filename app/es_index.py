# Responsible for:
# Creating index
# Storing documents

from elasticsearch import Elasticsearch
from config import ELASTIC_HOST, INDEX_NAME
import sys

es = Elasticsearch(ELASTIC_HOST)

def create_index():
    mapping = {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "type": {"type": "keyword"},
                "genres": {"type": "text"},
                "description": {"type": "text"},
                "release_year": {"type": "integer"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine"
                }
            }
        }
    }

    # if not es.indices.exists(index=INDEX_NAME):
    es.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
    print('deleted index')
    # sys.exit()
    es.indices.create(index=INDEX_NAME, body=mapping)
    print('index created')

if __name__ == '__main__':
    create_index()