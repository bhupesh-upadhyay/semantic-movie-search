from fastapi import FastAPI
from pydantic import BaseModel
from search import semantic_search
from typing import List

app = FastAPI()

class SearchRequest(BaseModel):
    query: str
    
class MovieResponse(BaseModel):
    title: str
    type: str
    genres: str
    description: str
    release_year: int


class SearchResponse(BaseModel):
    results: List[MovieResponse]

@app.post("/search", response_model=SearchResponse)
def search_movies(request: SearchRequest):
    results = semantic_search(request.query)
    return {"results": results}
