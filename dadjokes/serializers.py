#File: serializers.py
# Author: Louis Szeto (szetol@bu.edu) 1/4/2026
# Description: Serializers for the dadjokes app. We have two serializers, JokeSerializer 
# and PictureSerializer, which convert our Joke and Picture model instances to JSON format for the API.
from rest_framework import serializers
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    """Converts Joke model instances to JSON."""
    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'timestamp']

class PictureSerializer(serializers.ModelSerializer):
    """Converts Picture model instances to JSON."""
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'timestamp']