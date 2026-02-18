import pandas as pd
from elasticsearch import Elasticsearch, helpers
from config import ELASTIC_HOST, INDEX_NAME
from embedding import get_embedding
from es_index import create_index
from pprint import pprint
import sys


def load_data(csv_path: str):
    df = pd.read_csv(csv_path)
    df = df.fillna("")  # replace NaN with empty string
    return df


def build_document(row):
    combined_text = f"""
    Title: {row['title']}
    Genres: {row['listed_in']}
    Description: {row['description']}
    """

    embedding = get_embedding(combined_text)

    return {
        "_index": INDEX_NAME,
        "_source": {
            "title": row["title"],
            "type": row["type"],
            "genres": row["listed_in"],
            "description": row["description"],
            "release_year": row["release_year"],
            "embedding": embedding,
        },
    }


def ingest(csv_path: str):
    print("🔹 Loading dataset...")
    df = load_data(csv_path)

    print("🔹 Creating index if not exists...")
    create_index()

    print("🔹 Generating embeddings and indexing documents...")

    actions = []
    count = 1
    for _, row in df.iterrows():
        doc = build_document(row)
        print(f"{count}: Title - {row['title']} / {row['type']}")
        actions.append(doc)
        count += 1

    es = Elasticsearch(ELASTIC_HOST)
    helpers.bulk(es, actions)

    print("✅ Ingestion complete!")


if __name__ == "__main__":
    ingest("netflix_titles.csv")
