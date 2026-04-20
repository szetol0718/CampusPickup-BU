# File: views.py
# Author: Louis Szeto (szetol@bu.edu), 4/21/2026
# Description: List and detail interfaces for campus pickup models.

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Profile, Ride, RideMessage, RideParticipant


def home(request):
    """Render the campus pickup home page with quick model counts."""
    context = {
        "profile_count": Profile.objects.count(),
        "ride_count": Ride.objects.count(),
        "participant_count": RideParticipant.objects.count(),
        "message_count": RideMessage.objects.count(),
    }
    return render(request, "campus_pickup/home.html", context)


class ProfileListView(ListView):
    """Display all profile records in reverse join-date order."""

    model = Profile
    template_name = "campus_pickup/profile_list.html"
    context_object_name = "profiles"

    def get_queryset(self):
        """Return ordered profile records."""
        return Profile.objects.order_by("-join_date")


class ProfileDetailView(DetailView):
    """Display one profile record."""

    model = Profile
    template_name = "campus_pickup/profile_detail.html"
    context_object_name = "profile"


class RideListView(ListView):
    """Display rides and allow simple filtering by query and status."""

    model = Ride
    template_name = "campus_pickup/ride_list.html"
    context_object_name = "rides"

    def get_queryset(self):
        """Filter rides by optional destination/location text and status."""
        queryset = Ride.objects.select_related("creator", "driver").order_by("pickup_time")
        query = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()

        if query:
            queryset = queryset.filter(
                Q(destination__icontains=query) | Q(pickup_location__icontains=query)
            )
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        """Include current filter values and status options for the template."""
        context = super().get_context_data(**kwargs)
        context["current_query"] = self.request.GET.get("q", "").strip()
        context["current_status"] = self.request.GET.get("status", "").strip()
        context["status_choices"] = Ride.STATUS_CHOICES
        return context


class RideDetailView(DetailView):
    """Display one ride and related participants/messages."""

    model = Ride
    template_name = "campus_pickup/ride_detail.html"
    context_object_name = "ride"

    def get_context_data(self, **kwargs):
        """Add related ride participants and messages."""
        context = super().get_context_data(**kwargs)
        context["participants"] = RideParticipant.objects.filter(ride=self.object).select_related(
            "passenger"
        )
        context["messages"] = RideMessage.objects.filter(ride=self.object).select_related(
            "sender"
        ).order_by("-timestamp")
        return context


class RideParticipantListView(ListView):
    """Display ride-participant records."""

    model = RideParticipant
    template_name = "campus_pickup/participant_list.html"
    context_object_name = "participants"

    def get_queryset(self):
        """Return participant records with related ride and passenger."""
        return RideParticipant.objects.select_related("ride", "passenger").order_by("-joined_at")


class RideParticipantDetailView(DetailView):
    """Display one ride-participant record."""

    model = RideParticipant
    template_name = "campus_pickup/participant_detail.html"
    context_object_name = "participant"


class RideMessageListView(ListView):
    """Display ride-message records."""

    model = RideMessage
    template_name = "campus_pickup/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        """Return message records with related ride and sender."""
        return RideMessage.objects.select_related("ride", "sender").order_by("-timestamp")


class RideMessageDetailView(DetailView):
    """Display one ride-message record."""

    model = RideMessage
    template_name = "campus_pickup/message_detail.html"
    context_object_name = "message"
