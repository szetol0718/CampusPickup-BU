# File: models.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: Data models for the mini_insta application. Includes Profile
# model used to represent user profile information.
from django.db import models

# Create your models here.
class Profile(models.Model):
    """Represent a mini_insta user profile."""
 
 
    # data attributes of a Article:
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this object.'''
        return f'{self.username} ({self.display_name})'