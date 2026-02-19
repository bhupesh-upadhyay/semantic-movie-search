from django.urls import path
from . import views


urlpatterns = [
    path("search/", views.search_movies),
    path("health/", views.health_check, name="health"),

]
