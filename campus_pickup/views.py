# File: views.py
# Author: Louis Szeto (szetol@bu.edu), 4/21/2026
# Description: List and detail interfaces for campus pickup models.

import math

from django.conf import settings
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CreateProfileForm, RideForm, RideMessageForm
from .models import Profile, Ride, RideMessage, RideParticipant


def miles_between(lat1, lon1, lat2, lon2):
    """Return approximate distance in miles between two coordinate points."""
    radius = 3958.8
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    lat_diff = lat2 - lat1
    lon_diff = lon2 - lon1
    a = (
        math.sin(lat_diff / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(lon_diff / 2) ** 2
    )
    return radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def update_ride_status(ride):
    """Update ride status from current driver and seat usage."""
    # Status is derived from seats/driver, not edited directly by users.
    if ride.is_full():
        ride.status = "full"
    elif ride.driver:
        ride.status = "accepted"
    else:
        ride.status = "open"
    ride.save()


class ProfileRequiredMixin(LoginRequiredMixin):
    """Require login and a campus pickup profile for mutating ride actions."""

    def get_login_url(self):
        """Return the campus pickup login page."""
        return reverse("campus_pickup:login")

    def get_my_profile(self):
        """Return the Profile for the logged-in user."""
        return get_object_or_404(Profile, user=self.request.user)

    def get_my_ride_queryset(self):
        """Return rides related to the logged-in user's Profile."""
        profile = self.get_my_profile()
        return Ride.objects.filter(
            Q(creator=profile) | Q(driver=profile) | Q(rideparticipant__passenger=profile)
        ).distinct()

    def dispatch(self, request, *args, **kwargs):
        """Send logged-in users without a profile to profile creation first."""
        if request.user.is_authenticated and not Profile.objects.filter(user=request.user).exists():
            return redirect("campus_pickup:profile_create")
        return super().dispatch(request, *args, **kwargs)


class MyProfileDetailView(ProfileRequiredMixin, DetailView):
    """Display the logged-in user's own profile."""

    model = Profile
    template_name = "campus_pickup/profile_detail.html"
    context_object_name = "profile"

    def get_object(self):
        """Return the Profile for the current user."""
        return self.get_my_profile()


class ProfileCreateView(CreateView):
    """Create a User account and related Profile, or add a Profile for a logged-in User."""

    model = Profile
    template_name = "campus_pickup/profile_form.html"
    form_class = CreateProfileForm

    def dispatch(self, request, *args, **kwargs):
        """Avoid creating duplicate profiles for a logged-in user."""
        if request.user.is_authenticated:
            profile = Profile.objects.filter(user=request.user).first()
            if profile:
                return redirect("campus_pickup:my_profile")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add a UserCreationForm when the visitor is not logged in."""
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated and "user_form" not in context:
            context["user_form"] = UserCreationForm(prefix="user")
        return context

    def form_valid(self, form):
        """Attach the Profile to a User, creating and logging in a User if needed."""
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)

        user_form = UserCreationForm(self.request.POST, prefix="user")
        if not user_form.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, user_form=user_form)
            )

        user = user_form.save()
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        form.instance.user = user
        return super().form_valid(form)

    def form_invalid(self, form):
        """Keep both account and profile validation errors visible."""
        user_form = None
        if not self.request.user.is_authenticated:
            user_form = UserCreationForm(self.request.POST, prefix="user")
        return self.render_to_response(
            self.get_context_data(form=form, user_form=user_form)
        )

    def get_success_url(self):
        """Return the ride list after profile creation."""
        return reverse("campus_pickup:ride_list")


class ProfileUpdateView(ProfileRequiredMixin, UpdateView):
    """Update an existing profile record."""

    model = Profile
    template_name = "campus_pickup/profile_form.html"
    form_class = CreateProfileForm

    def get_queryset(self):
        """Only allow users to update their own profile."""
        return Profile.objects.filter(user=self.request.user)

    def get_success_url(self):
        """Return the profile detail page after a successful update."""
        return reverse("campus_pickup:my_profile")


class ProfileDeleteView(ProfileRequiredMixin, DeleteView):
    """Delete an existing profile record."""

    model = Profile
    template_name = "campus_pickup/profile_confirm_delete.html"
    success_url = reverse_lazy("campus_pickup:profile_create")

    def get_queryset(self):
        """Only allow users to delete their own profile."""
        return Profile.objects.filter(user=self.request.user)


class RideListView(ProfileRequiredMixin, ListView):
    """Display rides that still need a driver."""

    model = Ride
    template_name = "campus_pickup/ride_list.html"
    context_object_name = "rides"
    ride_status = "open"
    switch_url_name = "campus_pickup:accepted_ride_list"
    switch_label = "Switch to Need Passengers"

    def get_queryset(self):
        """Filter rides by status and optional destination/location text."""
        queryset = Ride.objects.select_related("creator", "driver").filter(
            status=self.ride_status
        ).order_by("-created_at")
        query = self.request.GET.get("q", "").strip()

        if query:
            queryset = queryset.filter(
                Q(destination__icontains=query) | Q(pickup_location__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        """Include current search value, role data, and switch-button info."""
        context = super().get_context_data(**kwargs)
        context["current_query"] = self.request.GET.get("q", "").strip()
        my_profile = self.get_my_profile()
        context["my_profile"] = my_profile
        context["my_passenger_ride_ids"] = list(
            RideParticipant.objects.filter(passenger=my_profile).values_list("ride_id", flat=True)
        )
        context["switch_url"] = reverse(self.switch_url_name)
        context["switch_label"] = self.switch_label
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY
        context["map_rides"] = [
            {
                "id": ride.pk,
                "pickup_location": ride.pickup_location,
                "destination": ride.destination,
                "pickup_latitude": ride.pickup_latitude,
                "pickup_longitude": ride.pickup_longitude,
                "detail_url": reverse("campus_pickup:ride_detail", kwargs={"pk": ride.pk}),
            }
            for ride in context["rides"]
            if ride.pickup_latitude is not None and ride.pickup_longitude is not None
        ]
        return context


class AcceptedRideListView(RideListView):
    """Display rides that already have a driver and need passengers."""

    template_name = "campus_pickup/accepted_ride_list.html"
    ride_status = "accepted"
    switch_url_name = "campus_pickup:ride_list"
    switch_label = "Switch to Need Driver"


class NearbyRideListView(ProfileRequiredMixin, ListView):
    """Display active rides ordered by pickup distance from the user."""

    model = Ride
    template_name = "campus_pickup/nearby_ride_list.html"
    context_object_name = "rides"

    def get_queryset(self):
        """Return rides nearest to the latitude/longitude in the query string."""
        self.nearby_latitude = self.request.GET.get("lat", "").strip()
        self.nearby_longitude = self.request.GET.get("lng", "").strip()
        if not self.nearby_latitude or not self.nearby_longitude:
            return []

        try:
            user_latitude = float(self.nearby_latitude)
            user_longitude = float(self.nearby_longitude)
        except ValueError:
            return []

        rides = Ride.objects.select_related("creator", "driver").exclude(
            status="completed").exclude(
            pickup_latitude__isnull=True).exclude(
            pickup_longitude__isnull=True)

        nearby_rides = []
        for ride in rides:
            ride.distance_miles = miles_between(
                user_latitude,
                user_longitude,
                ride.pickup_latitude,
                ride.pickup_longitude,
            )
            if ride.distance_miles <= 2:
                nearby_rides.append(ride)

        return sorted(nearby_rides, key=lambda ride: ride.distance_miles)

    def get_context_data(self, **kwargs):
        """Add location status for the nearby pickup page."""
        context = super().get_context_data(**kwargs)
        my_profile = self.get_my_profile()
        context["my_profile"] = my_profile
        context["my_passenger_ride_ids"] = list(
            RideParticipant.objects.filter(passenger=my_profile).values_list("ride_id", flat=True)
        )
        context["has_location"] = bool(
            self.request.GET.get("lat", "").strip()
            and self.request.GET.get("lng", "").strip()
        )
        return context


class RideDetailView(ProfileRequiredMixin, DetailView):
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
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY
        my_profile = None
        already_joined = False
        if self.request.user.is_authenticated:
            my_profile = Profile.objects.filter(user=self.request.user).first()
            already_joined = RideParticipant.objects.filter(
                ride=self.object,
                passenger=my_profile,
            ).exists() if my_profile else False

        context["my_profile"] = my_profile
        context["already_joined"] = already_joined
        context["can_join_as_driver"] = (
            my_profile is not None
            and not already_joined
            and self.object.creator != my_profile
            and self.object.driver is None
        )
        context["can_join_as_passenger"] = (
            my_profile is not None
            and not already_joined
            and self.object.creator != my_profile
            and self.object.driver != my_profile
            and self.object.seats_remaining() > 0
            and (self.object.driver is not None or self.object.seats_remaining() > 1)
        )
        context["can_join"] = (
            context["can_join_as_driver"] or context["can_join_as_passenger"]
        )
        context["can_quit"] = (
            my_profile is not None
            and self.object.creator != my_profile
            and (already_joined or self.object.driver == my_profile)
            and self.object.status != "completed"
        )
        context["can_complete"] = (
            my_profile is not None
            and self.object.driver == my_profile
            and self.object.status != "completed"
        )
        context["can_view_messages"] = (
            already_joined
            or self.object.creator == my_profile
            or self.object.driver == my_profile
        )
        return context


class MyRideListView(ProfileRequiredMixin, ListView):
    """Display rides created, joined, or driven by the logged-in user."""

    model = Ride
    template_name = "campus_pickup/my_ride_list.html"
    context_object_name = "rides"

    def get_queryset(self):
        """Return the user's related rides in pickup-time order."""
        return self.get_my_ride_queryset().select_related("creator", "driver").order_by(
            "-created_at"
        )

    def get_context_data(self, **kwargs):
        """Add the current user's Profile to the page."""
        context = super().get_context_data(**kwargs)
        my_profile = self.get_my_profile()
        context["my_profile"] = my_profile
        context["my_passenger_ride_ids"] = list(
            RideParticipant.objects.filter(passenger=my_profile).values_list("ride_id", flat=True)
        )
        return context


class RideCreateView(ProfileRequiredMixin, CreateView):
    """Create a new ride record."""

    model = Ride
    template_name = "campus_pickup/ride_form.html"
    form_class = RideForm
    success_url = reverse_lazy("campus_pickup:ride_list")

    def get_context_data(self, **kwargs):
        """Add the Google Maps key for the location search."""
        context = super().get_context_data(**kwargs)
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY
        return context

    def get_initial(self):
        """Prefill destination when creating from a failed ride search."""
        initial = super().get_initial()
        destination = self.request.GET.get("destination", "").strip()
        if destination:
            initial["destination"] = destination
        return initial

    def form_valid(self, form):
        """Assign creator role and automatic status."""
        profile = self.get_my_profile()
        form.instance.creator = profile
        form.instance.driver = profile if form.cleaned_data["ride_role"] == "driver" else None
        form.instance.status = "open"

        response = super().form_valid(form)

        # If the creator needs a ride, save them as a passenger.
        if form.cleaned_data["ride_role"] == "requester":
            RideParticipant.objects.get_or_create(ride=self.object, passenger=profile)

        update_ride_status(self.object)

        return response


class RideUpdateView(ProfileRequiredMixin, UpdateView):
    """Update an existing ride record."""

    model = Ride
    template_name = "campus_pickup/ride_form.html"
    form_class = RideForm

    def get_context_data(self, **kwargs):
        """Add the Google Maps key for the location search."""
        context = super().get_context_data(**kwargs)
        context["google_maps_api_key"] = settings.GOOGLE_MAPS_API_KEY
        return context

    def get_initial(self):
        """Prefill role choice from the current ride driver."""
        initial = super().get_initial()
        ride = self.get_object()
        initial["ride_role"] = "driver" if ride.driver == self.get_my_profile() else "requester"
        return initial

    def get_queryset(self):
        """Only allow ride creators to update their rides."""
        return Ride.objects.filter(creator=self.get_my_profile())

    def form_valid(self, form):
        """Keep driver and status controlled by app logic."""
        profile = self.get_my_profile()
        form.instance.creator = profile
        form.instance.driver = profile if form.cleaned_data["ride_role"] == "driver" else None
        form.instance.status = "open"

        response = super().form_valid(form)

        # Keep the creator in exactly one ride role after editing.
        if form.cleaned_data["ride_role"] == "driver":
            RideParticipant.objects.filter(ride=self.object, passenger=profile).delete()
        else:
            RideParticipant.objects.get_or_create(ride=self.object, passenger=profile)

        update_ride_status(self.object)

        return response

    def get_success_url(self):
        """Return the detail page after a successful update."""
        return reverse("campus_pickup:ride_detail", kwargs={"pk": self.object.pk})


class RideDeleteView(ProfileRequiredMixin, DeleteView):
    """Delete an existing ride record."""

    model = Ride
    template_name = "campus_pickup/ride_confirm_delete.html"
    success_url = reverse_lazy("campus_pickup:ride_list")

    def get_queryset(self):
        """Only allow ride creators to delete their rides."""
        return Ride.objects.filter(creator=self.get_my_profile())


@login_required(login_url=reverse_lazy("campus_pickup:login"))
def join_ride(request, pk):
    """Handle ride join requests submitted from the ride detail view."""
    ride = get_object_or_404(Ride, pk=pk)
    if request.method != "POST":
        return redirect("campus_pickup:ride_detail", pk=ride.pk)

    passenger = Profile.objects.filter(user=request.user).first()
    if not passenger:
        return redirect("campus_pickup:profile_create")

    join_role = request.POST.get("join_role")

    if join_role == "driver" and ride.driver is None and passenger != ride.creator:
        seat_capacity = request.POST.get("seat_capacity")
        if seat_capacity:
            try:
                # New drivers can choose capacity, but not below occupied seats.
                ride.seat_capacity = max(int(seat_capacity), ride.seats_taken() + 1)
            except ValueError:
                pass
        ride.driver = passenger
        update_ride_status(ride)
    elif (
        join_role == "passenger"
        and passenger != ride.driver
        and not ride.is_full()
        # If no driver exists, keep at least one seat open for a driver.
        and (ride.driver is not None or ride.seats_remaining() > 1)
    ):
        RideParticipant.objects.get_or_create(ride=ride, passenger=passenger)
        update_ride_status(ride)

    return redirect("campus_pickup:ride_detail", pk=ride.pk)


@login_required(login_url=reverse_lazy("campus_pickup:login"))
def quit_ride(request, pk):
    """Remove the logged-in user from a ride as driver or passenger."""
    ride = get_object_or_404(Ride, pk=pk)
    if request.method != "POST":
        return redirect("campus_pickup:ride_detail", pk=ride.pk)

    profile = Profile.objects.filter(user=request.user).first()
    if not profile:
        return redirect("campus_pickup:profile_create")

    if ride.creator == profile:
        return redirect("campus_pickup:ride_detail", pk=ride.pk)

    if ride.driver == profile:
        # Quitting as driver reopens the ride for another driver.
        ride.driver = None
        ride.save()

    # Quitting as passenger removes the participant row.
    RideParticipant.objects.filter(ride=ride, passenger=profile).delete()
    update_ride_status(ride)

    return redirect("campus_pickup:ride_detail", pk=ride.pk)


@login_required(login_url=reverse_lazy("campus_pickup:login"))
def complete_ride(request, pk):
    """Allow the driver to mark a ride as completed."""
    ride = get_object_or_404(Ride, pk=pk)
    if request.method != "POST":
        return redirect("campus_pickup:ride_detail", pk=ride.pk)

    profile = Profile.objects.filter(user=request.user).first()
    if not profile:
        return redirect("campus_pickup:profile_create")

    if ride.driver == profile:
        # Completed rides stay visible in My Rides but leave Find Rides.
        ride.status = "completed"
        ride.save()

    return redirect("campus_pickup:ride_detail", pk=ride.pk)


class RideMessageDetailView(ProfileRequiredMixin, DetailView):
    """Display one ride-message record."""

    model = RideMessage
    template_name = "campus_pickup/message_detail.html"
    context_object_name = "message"

    def get_queryset(self):
        """Only show messages from rides related to the logged-in user."""
        return RideMessage.objects.filter(ride__in=self.get_my_ride_queryset())


class RideMessageCreateView(ProfileRequiredMixin, CreateView):
    """Create a new ride-message record."""

    model = RideMessage
    template_name = "campus_pickup/message_form.html"
    form_class = RideMessageForm

    def dispatch(self, request, *args, **kwargs):
        """Require a ride from the URL before creating a message."""
        self.ride = self.get_ride()
        if not self.ride:
            return redirect("campus_pickup:my_rides")
        return super().dispatch(request, *args, **kwargs)

    def get_ride(self):
        """Return the related ride if the user is allowed to message it."""
        return self.get_my_ride_queryset().filter(pk=self.kwargs.get("pk")).first()

    def get_context_data(self, **kwargs):
        """Add the related ride to the message form page."""
        context = super().get_context_data(**kwargs)
        context["ride"] = self.ride
        return context

    def get_success_url(self):
        """Return the related ride detail page after creating a message."""
        return reverse("campus_pickup:ride_detail", kwargs={"pk": self.object.ride.pk})

    def form_valid(self, form):
        """Assign the ride and logged-in user's Profile automatically."""
        form.instance.ride = self.ride
        form.instance.sender = self.get_my_profile()
        return super().form_valid(form)


class RideMessageDeleteView(ProfileRequiredMixin, DeleteView):
    """Delete an existing ride-message record."""

    model = RideMessage
    template_name = "campus_pickup/message_confirm_delete.html"

    def get_queryset(self):
        """Only allow senders to delete their own messages."""
        return RideMessage.objects.filter(sender=self.get_my_profile())

    def get_success_url(self):
        """Return the related ride detail page after deleting a message."""
        return reverse("campus_pickup:ride_detail", kwargs={"pk": self.object.ride.pk})
