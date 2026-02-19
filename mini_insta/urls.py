# File: urls.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: URL patterns for mini_insta. Routes default path to
# ProfileListView.

from django.urls import path
from .views import ProfileListView, ProfileDetailView
from .views import PostDetailView, CreatePostView
urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile_detail'), # show one article
    path("post/<int:pk>/", PostDetailView.as_view(), name="show_post"),
    path("profile/<int:pk>/create_post", CreatePostView.as_view(), name="create_post"),
]
