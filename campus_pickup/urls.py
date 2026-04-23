# File: urls.py
# Author: Louis Szeto (szetol@bu.edu), 20/4/2026
# Description: URL patterns for the campus_pickup application.

from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView, TemplateView
from . import views

app_name = "campus_pickup"

urlpatterns = [
    path(
        "",
        RedirectView.as_view(pattern_name="campus_pickup:ride_list", permanent=False),
        name="home",
    ),
    path("login/",
        auth_views.LoginView.as_view(
            template_name="campus_pickup/login.html",
            redirect_authenticated_user=True,
            next_page="campus_pickup:accepted_ride_list",
        ),
        name="login",),
    path("logout/",
        auth_views.LogoutView.as_view(next_page="campus_pickup:logout_confirmation"),
        name="logout",),
    path("logout_confirmation/",
        TemplateView.as_view(template_name="campus_pickup/logged_out.html"),
        name="logout_confirmation",),
    path("profile/", views.MyProfileDetailView.as_view(), name="my_profile"),
    path("profiles/create/", views.ProfileCreateView.as_view(), name="profile_create"),
    path("profiles/<int:pk>/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("profiles/<int:pk>/delete/", views.ProfileDeleteView.as_view(), name="profile_delete"),
    path("rides/", views.RideListView.as_view(), name="ride_list"),
    path("rides/accepted/", views.AcceptedRideListView.as_view(), name="accepted_ride_list"),
    path("rides/nearby/", views.NearbyRideListView.as_view(), name="nearby_rides"),
    path("rides/my/", views.MyRideListView.as_view(), name="my_rides"),
    path("rides/create/", views.RideCreateView.as_view(), name="ride_create"),
    path("rides/<int:pk>/", views.RideDetailView.as_view(), name="ride_detail"),
    path("rides/<int:pk>/update/", views.RideUpdateView.as_view(), name="ride_update"),
    path("rides/<int:pk>/delete/", views.RideDeleteView.as_view(), name="ride_delete"),
    path("rides/<int:pk>/join/", views.join_ride, name="join_ride"),
    path("rides/<int:pk>/quit/", views.quit_ride, name="quit_ride"),
    path("rides/<int:pk>/complete/", views.complete_ride, name="complete_ride"),
    path(
        "rides/<int:pk>/messages/create/",
        views.RideMessageCreateView.as_view(),
        name="ride_message_create",
    ),
    path("messages/<int:pk>/", views.RideMessageDetailView.as_view(), name="message_detail"),
    path("messages/<int:pk>/delete/", views.RideMessageDeleteView.as_view(), name="message_delete"),
]
