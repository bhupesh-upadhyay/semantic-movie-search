from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from search import semantic_search
from elasticsearch import Elasticsearch
from config import ELASTIC_HOST
from django.http import JsonResponse
from embedding import model

# health check uses by kubernates and load balancer
def health_check(request):
    status = {
        "django": "ok",
        "elasticsearch": "down",
        "model_loaded": False
    }

    # Check Elasticsearch
    try:
        es = Elasticsearch(ELASTIC_HOST)
        if es.ping():
            status["elasticsearch"] = "ok"
    except Exception:
        status["elasticsearch"] = "down"

    # Check model loaded
    try:
        if model is not None:
            status["model_loaded"] = True
    except Exception:
        status["model_loaded"] = False

    return JsonResponse(status)

@api_view(['POST'])
def search_movies(request):
    query = request.data.get("query")

    if not query:
        return Response({"error": "Query is required"}, status=400)

    results = semantic_search(query, k=10)

    return Response({"results": results})
