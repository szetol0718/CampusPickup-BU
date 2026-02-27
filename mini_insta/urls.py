# File: urls.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: URL patterns for mini_insta. Routes default path to
# ProfileListView.

from django.urls import path
from .views import PostFeedListView, ProfileListView, ProfileDetailView
from .views import PostDetailView, CreatePostView, UpdateProfileView
from .views import DeletePostView, UpdatePostView, ShowFollowersDetailView, ShowFollowingDetailView
urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile_detail'), # show one article
    # Author: Louis Szeto (szetol@bu.edu), 2/18/2026
    # Add  path to post and create post
    path("post/<int:pk>/", PostDetailView.as_view(), name="show_post"),
    path("profile/<int:pk>/create_post", CreatePostView.as_view(), name="create_post"),
    # Author: Louis Szeto (szetol@bu.edu), 2/26/2026
    # Add  path to update profile, delete post, and update post. Also Added to show followers and following.
     path("profile/<int:pk>/update", UpdateProfileView.as_view(), name="update_profile"),
     path("post/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),
     path("post/<int:pk>/update", UpdatePostView.as_view(), name="update_post"),
     path("profile/<int:pk>/followers", ShowFollowersDetailView.as_view(),
     name="show_followers"),
     path("profile/<int:pk>/following", ShowFollowingDetailView.as_view(),
     name="show_following"),
     path("profile/<int:pk>/feed", PostFeedListView.as_view(), name="show_feed"),         
]
