# File: urls.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: URL patterns for mini_insta. Routes default path to
# ProfileListView.

from django.urls import path
from .views import ProfileListView

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
]
