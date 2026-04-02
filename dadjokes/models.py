# File: models.py
# Author: Louis Szeto (szetol@bu.edu), 1/4/2026
# Description: Data models for the dadjokes app. We have two models: Joke and Picture.
#  Each stores the text of a joke or the URL of a picture, along with the contributor's name and a timestamp.
from django.db import models

class Joke(models.Model):
    """Stores the text of a joke and its contributor[cite: 32]."""
    text = models.TextField()
    contributor = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True) # Automatically set when created

    def __str__(self):
        return f'"{self.text}" - by {self.contributor}'

class Picture(models.Model):
    """Stores the URL of a silly image or GIF[cite: 33]."""
    image_url = models.URLField() # Use URLField for image links 
    contributor = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Picture by {self.contributor}: {self.image_url}"