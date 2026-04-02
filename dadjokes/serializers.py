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