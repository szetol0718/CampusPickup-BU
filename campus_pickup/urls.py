# File: urls.py
# Author: Louis Szeto (szetol@bu.edu), 20/4/2026
# Description: URL patterns for the campus_pickup application.

from django.urls import path
from . import views

app_name = "campus_pickup"

urlpatterns = [
    path("", views.home, name="home"),
    path("profiles/", views.ProfileListView.as_view(), name="profile_list"),
    path("profiles/<int:pk>/", views.ProfileDetailView.as_view(), name="profile_detail"),
    path("rides/", views.RideListView.as_view(), name="ride_list"),
    path("rides/create/", views.RideCreateView.as_view(), name="ride_create"),
    path("rides/<int:pk>/", views.RideDetailView.as_view(), name="ride_detail"),
    path("rides/<int:pk>/update/", views.RideUpdateView.as_view(), name="ride_update"),
    path("rides/<int:pk>/delete/", views.RideDeleteView.as_view(), name="ride_delete"),
    path("rides/<int:pk>/join/", views.join_ride, name="join_ride"),
    path("participants/", views.RideParticipantListView.as_view(), name="participant_list"),
    path(
        "participants/<int:pk>/",
        views.RideParticipantDetailView.as_view(),
        name="participant_detail",
    ),
    path("messages/", views.RideMessageListView.as_view(), name="message_list"),
    path("messages/<int:pk>/", views.RideMessageDetailView.as_view(), name="message_detail"),
]
