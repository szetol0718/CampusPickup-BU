# File: urls.py
# Author: Louis Szeto (szetol@bu.edu), 2/3/2026
# Description: Django URL configuration for the restaurant application.
# Maps URLs to view functions.

from django.urls import path
from django.conf import settings
from . import views
 
 
from django.urls import path
from . import views

urlpatterns = [
    path(r"", views.restaurant, name="restaurant"),
    path(r"order/", views.order, name="order"),
]