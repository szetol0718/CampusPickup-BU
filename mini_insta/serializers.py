#file: mini_insta/serializers.py
# Author: Louis Szeto(szetol@bu.edu) 4/9/2026
# Description: Serializers for the mini_insta app. We have serializers for both Profile and Post models,
#  which convert our model instances to JSON format for API responses.
from rest_framework import serializers
from .models import Profile, Post, Photo

class PhotoSerializer(serializers.ModelSerializer):
    """Converts Photo instances to JSON, using your custom get_image_url logic."""
    url = serializers.SerializerMethodField()
    class Meta:
        model = Photo
        fields = ['id', 'url', 'timestamp']

    def get_url(self, obj):
        return obj.get_image_url()
    
class ProfileSerializer(serializers.ModelSerializer):
    """Converts Profile instances to JSON."""
    class Meta:
        model = Profile
        fields = ['id', 'user',"username", 'bio_text', 'profile_image_url']

class PostSerializer(serializers.ModelSerializer):
    """Converts Post instances to JSON, including image URLs."""
    photos = PhotoSerializer(source='photo_set', many=True, read_only=True)
    author_username = serializers.ReadOnlyField(source='profile.username')
    class Meta:
        model = Post
        fields = ['id', 'profile', 'author_username','caption', 'timestamp', 'photos']
        read_only_fields = ['profile']