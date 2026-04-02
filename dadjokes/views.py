#file: views.py
#author: Louis Szeto (szetol@bu.edu), 1/4/2026
#description: Views for the dadjokes app. We have several API views that handle requests 
# for random jokes and pictures, as well as listing and retrieving jokes and pictures by their primary key.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer
import random

class RandomJokeAPIView(APIView):
    """Returns a JSON representation of one Joke selected at random"""
    def get(self, request):
        jokes = Joke.objects.all()
        random_joke = random.choice(jokes)
        serializer = JokeSerializer(random_joke)
        return Response(serializer.data)

class RandomPictureAPIView(APIView):
    """Returns a JSON representation of one Picture selected at random"""
    def get(self, request):
        pictures = Picture.objects.all()
        random_pic = random.choice(pictures)
        serializer = PictureSerializer(random_pic)
        return Response(serializer.data)

class JokeListCreateAPIView(generics.ListCreateAPIView):
    """Returns all jokes (GET) and allows creating a new joke (POST)"""
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveAPIView):
    """Returns one Joke by its primary key"""
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureListAPIView(generics.ListAPIView):
    """Returns a JSON representation of all Pictures"""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveAPIView):
    """Returns one Picture by its primary key"""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer