# File: mini_insta/admin.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: Admin configuration for mini_insta. Registers the Profile model

# uthor: Louis Szeto (szetol@bu.edu),(2/18/2026)
# Description: Admin configuration for mini_insta assignment 4. Registers the Post, Photo model
from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)