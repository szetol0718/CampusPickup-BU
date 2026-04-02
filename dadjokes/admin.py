#file: admin.py
#author: Louis Szeto (szetol@bu.edu) 1/4/2026
#description: Admin configuration for the dadjokes app. We register our Joke and Picture models
from django.contrib import admin
from .models import Joke, Picture
# register my models
admin.site.register(Joke)
admin.site.register(Picture)