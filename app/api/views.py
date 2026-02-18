from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from search import semantic_search


@api_view(['POST'])
def search_movies(request):
    query = request.data.get("query")

    if not query:
        return Response({"error": "Query is required"}, status=400)

    results = semantic_search(query, k=10)

    return Response({"results": results})
