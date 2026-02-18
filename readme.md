# 🎬 Semantic Movie Search Engine

AI-powered **Semantic Search API** built with:

-   🐍 Python\
-   🌐 Django (REST API)\
-   🔎 Elasticsearch 8 (Vector Search)\
-   🤖 Sentence Transformers (Embeddings)\
-   🐳 Docker

This project implements semantic movie search using transformer
embeddings and Elasticsearch's `dense_vector` with cosine similarity.

------------------------------------------------------------------------

## 🚀 Features

-   Semantic search using transformer embeddings\
-   Elasticsearch vector indexing (`dense_vector`)\
-   Clean API responses (no raw ES metadata)\
-   Dockerized multi-container setup\
-   Persistent HuggingFace model cache\
-   Bulk ingestion pipeline\
-   Modular architecture (AI layer separated from API layer)

------------------------------------------------------------------------

## 🧠 How It Works

### Data Ingestion Flow

CSV Dataset\
↓\
Combine fields (title + genres + description)\
↓\
Generate embedding using SentenceTransformer (384-dim vector)\
↓\
Store document + embedding in Elasticsearch

### Search Flow

User Query\
↓\
Convert query to embedding\
↓\
KNN search in Elasticsearch (cosine similarity)\
↓\
Return top matched movies

------------------------------------------------------------------------

## 📁 Project Structure

app/

├── manage.py \# Django entry point\
├── config.py \# Central configuration\
├── embedding.py \# Loads AI model & generates embeddings\
├── es_index.py \# Creates Elasticsearch index\
├── search.py \# Vector search logic\
├── ingest.py \# Bulk ingestion script\
├── movies_api/ \# Django project config\
├── search_api/ \# Django REST app\
├── netflix_titles.csv \# Dataset\
├── huggingface_cache/ \# Persisted model cache (ignored in Git)\
└── elasticsearch-data/ \# Elasticsearch data volume (ignored in Git)

------------------------------------------------------------------------

## 🧠 Why huggingface_cache Exists

Transformer models (\~90MB+) are downloaded from Hugging Face.

Without persistence: - Docker rebuild → model redownload\
- Slower startup\
- Network dependency each time

We mount:

./huggingface_cache:/huggingface_cache

And set:

HF_HOME=/huggingface_cache

This ensures: - Model downloads once\
- Cache persists\
- Faster restarts\
- Stable container behavior

------------------------------------------------------------------------

## 🧠 Why elasticsearch-data Exists

Elasticsearch stores: - Indexed documents\
- Vector data\
- Lucene index files

We mount:

./elasticsearch-data:/usr/share/elasticsearch/data

So data persists across container restarts.

------------------------------------------------------------------------

## 🛠 Setup Instructions

### 1️⃣ Clone the Repository

git clone `<your-repo-url>`{=html}\
cd `<project-folder>`{=html}

### 2️⃣ Start Docker Services

docker-compose up --build -d

Services: - Elasticsearch → http://localhost:9200\
- Kibana → http://localhost:5601\
- Django API → http://localhost:8000

### 3️⃣ Ingest Dataset

docker exec -it semantic_api bash\
python ingest.py

Verify document count:

curl http://localhost:9200/movies/\_count

### 4️⃣ Test Search API

POST http://localhost:8000/search/

Example body:

{ "query": "a movie where protagonist gets superpowers" }

------------------------------------------------------------------------

## 🔎 Elasticsearch Configuration

Using Elasticsearch 8.15.0

Vector field mapping:

"embedding": { "type": "dense_vector", "dims": 384, "index": true,
"similarity": "cosine" }

------------------------------------------------------------------------

## 🤖 AI Model Used

sentence-transformers/all-MiniLM-L6-v2

-   384-dimensional embeddings\
-   Lightweight & CPU-friendly\
-   Optimized for semantic similarity

------------------------------------------------------------------------

## 🧼 Ignored in Git

elasticsearch-data/\
huggingface_cache/\
**pycache**/\
db.sqlite3

------------------------------------------------------------------------

## 🏁 Conclusion

This project demonstrates:

-   Integration of AI models with search infrastructure\
-   Scalable semantic search architecture\
-   Clean backend design with Django\
-   Production-like Docker setup
