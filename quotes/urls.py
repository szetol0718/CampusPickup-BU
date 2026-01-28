# File: views.py
# Author: Louis Szeto (szetol@bu.edu), 1/28/2026
# Description: Django URL configuration for the quotes application.
# Maps URLs to view functions.

from django.urls import path
from django.conf import settings
from . import views
 
 
from django.urls import path
from . import views

urlpatterns = [
    path(r"", views.quote, name="quote"),
    path(r"quote", views.quote, name="quote"),
    path(r"show_all", views.show_all, name="show_all"),
    path(r"about", views.about, name="about"),
]

