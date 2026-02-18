from elasticsearch import Elasticsearch
from embedding import get_embedding
from config import ELASTIC_HOST, INDEX_NAME

es = Elasticsearch(ELASTIC_HOST)


def semantic_search(query: str, k: int = 5):
    query_vector = get_embedding(query)

    response = es.search(
        index=INDEX_NAME,
        body={
            "knn": {
                "field": "embedding",
                "query_vector": query_vector,
                "k": k,
                "num_candidates": 100
            },
            "_source": [
                "title",
                "type",
                "genres",
                "description",
                "release_year"
            ],
            "sort": [
                {"_score": {"order": "desc"}}
            ]
        }
    )

    hits = response["hits"]["hits"]

    results = []
    for hit in hits:
        results.append(hit["_source"])

    return results
