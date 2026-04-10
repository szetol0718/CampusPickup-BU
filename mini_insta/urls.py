# File: urls.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: URL patterns for mini_insta. Routes default path to
# ProfileListView.

from django.urls import path
from .views import PostFeedListView, ProfileListView, ProfileDetailView
from .views import PostDetailView, CreatePostView, UpdateProfileView, SearchView
from .views import DeletePostView, UpdatePostView, ShowFollowersDetailView, ShowFollowingDetailView
from .views import MyProfileDetailView, CreateProfileView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile_detail'), # show one article
    # Author: Louis Szeto (szetol@bu.edu), 2/18/2026
    # Add  path to post and create post
    path("post/<int:pk>/", PostDetailView.as_view(), name="show_post"),
    
    # Author: Louis Szeto (szetol@bu.edu), 2/26/2026
    # Add  path to update profile, delete post, and update post. Also Added to show followers and following.
     
     path("post/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),
     path("post/<int:pk>/update", UpdatePostView.as_view(), name="update_post"),
     path("profile/<int:pk>/followers", ShowFollowersDetailView.as_view(),
     name="show_followers"),
     path("profile/<int:pk>/following", ShowFollowingDetailView.as_view(),
     name="show_following"),

    # Author: Louis Szeto (szetol@bu.edu), 3/3/2026
    # removed pk for profile and added myprofile page.
     path("profile/create_post", CreatePostView.as_view(), name="create_post"),
     path("profile/feed", PostFeedListView.as_view(), name="show_feed"),
     path("profile/search", SearchView.as_view(), name="search"),   
     path("profile/update", UpdateProfileView.as_view(), name="update_profile"),
     path("profile", MyProfileDetailView.as_view(), name="my_profile"),
     path("login/",auth_views.LoginView.as_view(template_name="mini_insta/login.html"),
        name="login"),
    path("logout/",auth_views.LogoutView.as_view(next_page="logout_confirmation"),
        name="logout"),
    path("logout_confirmation/",TemplateView.as_view(template_name="mini_insta/logged_out.html"),
        name="logout_confirmation"),
    path("create_profile", CreateProfileView.as_view(), name="create_profile"),
    path("profile/<int:pk>/follow", views.follow_profile, name="follow_profile"),
    path("profile/<int:pk>/delete_follow", views.delete_follow, name="delete_follow"),
    path("post/<int:pk>/like", views.like_post, name="like_post"),
    path("post/<int:pk>/delete_like", views.delete_like, name="delete_like"),
    path("post/<int:pk>/comment", views.add_comment, name="add_comment"),

    #Author: Louis Szeto (szetol@bu,edu), 4/9/2026
    # Added API endpoints for profiles and posts
    # Profile API Endpoints
    path('api/profiles', views.ProfileListAPIView.as_view(), name='api_profiles'),
    path('api/profile/<int:pk>', views.ProfileDetailAPIView.as_view(), name='api_profile_detail'),
    # Post and Feed API Endpoints
    path('api/posts', views.PostListCreateAPIView.as_view(), name='api_posts_create'),
    path('api/profile/<int:pk>/posts', views.ProfilePostsAPIView.as_view(), name='api_profile_posts'),
    path('api/profile/<int:pk>/feed', views.ProfileFeedAPIView.as_view(), name='api_profile_feed'),
]
