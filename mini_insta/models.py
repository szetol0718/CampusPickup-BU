# File: models.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: Data models for the mini_insta application. Includes Profile
# model used to represent user profile information. (2/18/2026)Also added  Post,and Photo.
from django.db import models

# Create your models here.
class Profile(models.Model):
    """Represent a mini_insta user profile."""
 
 
    # data attributes of a Article:
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField()
    profile_image_url = models.URLField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this object.'''
        return f'{self.username} ({self.display_name})'
    def get_all_posts(self):
        return Post.objects.filter(profile=self).order_by("-timestamp")

    
# Description: Additional models for mini_insta Assignment 4.
class Post(models.Model):
    """Represent an Instagram post."""

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    timestamp = models.DateTimeField()
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"Post by {self.profile.username} ({self.id})"

    # Accessor method required by assignment
    def get_all_photos(self):
        return Photo.objects.filter(post=self).order_by("timestamp")


class Photo(models.Model):
    """Represent a photo belonging to a Post."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Photo for Post {self.post.id}"