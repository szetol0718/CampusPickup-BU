# File: urls.py
# Author: Louis Szeto (szetol@bu.edu), 20/4/2026
# Description: URL patterns for the campus_pickup application.

from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

app_name = "campus_pickup"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/",
        auth_views.LoginView.as_view(
            template_name="campus_pickup/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",),
    path("logout/",
        auth_views.LogoutView.as_view(next_page="campus_pickup:logout_confirmation"),
        name="logout",),
    path("logout_confirmation/",
        TemplateView.as_view(template_name="campus_pickup/logged_out.html"),
        name="logout_confirmation",),
    path("profile/", views.MyProfileDetailView.as_view(), name="my_profile"),
    path("profiles/", views.ProfileListView.as_view(), name="profile_list"),
    path("profiles/create/", views.ProfileCreateView.as_view(), name="profile_create"),
    path("profiles/<int:pk>/", views.ProfileDetailView.as_view(), name="profile_detail"),
    path("profiles/<int:pk>/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("profiles/<int:pk>/delete/", views.ProfileDeleteView.as_view(), name="profile_delete"),
    path("rides/", views.RideListView.as_view(), name="ride_list"),
    path("rides/my/", views.MyRideListView.as_view(), name="my_rides"),
    path("rides/create/", views.RideCreateView.as_view(), name="ride_create"),
    path("rides/<int:pk>/", views.RideDetailView.as_view(), name="ride_detail"),
    path("rides/<int:pk>/update/", views.RideUpdateView.as_view(), name="ride_update"),
    path("rides/<int:pk>/delete/", views.RideDeleteView.as_view(), name="ride_delete"),
    path("rides/<int:pk>/join/", views.join_ride, name="join_ride"),
    path("rides/<int:pk>/quit/", views.quit_ride, name="quit_ride"),
    path("participants/", views.RideParticipantListView.as_view(), name="participant_list"),
    path("participants/<int:pk>/",
        views.RideParticipantDetailView.as_view(),
        name="participant_detail",),
    path("messages/", views.RideMessageListView.as_view(), name="message_list"),
    path("messages/create/", views.RideMessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/", views.RideMessageDetailView.as_view(), name="message_detail"),
    path("messages/<int:pk>/update/", views.RideMessageUpdateView.as_view(), name="message_update"),
    path("messages/<int:pk>/delete/", views.RideMessageDeleteView.as_view(), name="message_delete"),
]
