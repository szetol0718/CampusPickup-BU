#file: urls.py
#author: Louis Szeto (szetol@bu.edu) 1/4/2026
#description: URL configuration for the dadjokes app. We define URL patterns for our API endpoints, 
# which are handled by views in views.py. We have endpoints for getting random jokes and pictures.
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings 
from . import views
from .views import *

urlpatterns = [
    # Random endpoints
    path('api/', RandomJokeAPIView.as_view(), name='api_random_root'),
    path('api/random', RandomJokeAPIView.as_view(), name='api_random_joke'),
    path('api/random_picture', RandomPictureAPIView.as_view(), name='api_random_picture'),    
    # Joke endpoints
    path('api/jokes', JokeListCreateAPIView.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view(), name='api_joke_detail'),  
    # Picture endpoints
    path('api/pictures', PictureListAPIView.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view(), name='api_picture_detail'),
]