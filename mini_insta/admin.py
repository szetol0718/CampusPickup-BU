# File: mini_insta/admin.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: Admin configuration for mini_insta. Registers the Profile model
from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile)