# File: models.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: Data models for the mini_insta application. Includes Profile
# model used to represent user profile information. (2/18/2026) Also added  Post,and Photo.
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

    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"Post by {self.profile.username} ({self.id})"

    # Accessor method to get all photos
    def get_all_photos(self):
        return Photo.objects.filter(post=self).order_by("timestamp")


class Photo(models.Model):
    """Represent a photo belonging to a Post."""

    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    image_file = models.ImageField(blank=True) #NEW 2/24/2026 added image field
    
    # Author: Louis Szeto, 2/24/2026, modified __str__ and added get_image_url method
    def __str__(self):
        if self.image_url:
            return f"Photo (url) for Post {self.post.pk}"
        if self.image_file:
            return f"Photo (file) for Post {self.post.pk}"
        return f"Photo (empty) for Post {self.post.pk}"

    def get_image_url(self):
        """Return the best URL to display this photo (url first, else file)."""
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return ""