# Convert text → numerical vector (embedding)
# Responsible ONLY for AI model

from sentence_transformers import SentenceTransformer
from config import MODEL_NAME

model = SentenceTransformer(MODEL_NAME)

def get_embedding(text: str):
    data = model.encode(text).tolist()
    return data
