# File: models.py
# Author: Louis Szeto (szetol@bu.edu), 20/4/2026
# Description: Data models for the campus pickup application.

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Represent a user profile for the campus pickup system."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    display_name = models.TextField(blank=False)
    bio_text = models.TextField(blank=True)
    profile_image_url = models.ImageField(
        "profile image",
        upload_to="campus_pickup/profile_images/",
        blank=True,
    )
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of this Profile."""
        return self.display_name


class Ride(models.Model):
    """Represent a ride request or accepted ride in the system."""

    REQUEST_TYPES = [
        ("reservation", "Reservation"),
        ("realtime", "Real-Time"),
    ]

    STATUS_CHOICES = [
        ("open", "Open"),
        ("accepted", "Accepted"),
        ("full", "Full"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    creator = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="created_rides"
    )

    driver = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="driving_rides"
    )

    pickup_location = models.TextField(blank=False)
    destination = models.TextField(blank=False)
    # Coordinates are filled by the Google Maps search buttons on the ride form.
    pickup_latitude = models.FloatField(null=True, blank=True)
    pickup_longitude = models.FloatField(null=True, blank=True)
    destination_latitude = models.FloatField(null=True, blank=True)
    destination_longitude = models.FloatField(null=True, blank=True)
    pickup_time = models.DateTimeField(null=True, blank=True)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open"
    )
    seat_capacity = models.IntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of this Ride."""
        return (
            f"{self.creator.display_name}: "
            f"{self.pickup_location} to {self.destination}"
        )

    def seats_taken(self):
        """Return occupied seats from passengers plus driver."""
        # A creator only counts if they are saved as driver or passenger.
        passenger_ids = set(
            RideParticipant.objects.filter(ride=self).values_list("passenger_id", flat=True)
        )
        occupied = len(passenger_ids)
        if self.driver and self.driver_id not in passenger_ids:
            occupied += 1
        return occupied

    def seats_remaining(self):
        """Return the number of remaining seats."""
        return max(self.seat_capacity - self.seats_taken(), 0)

    def is_full(self):
        """Return whether the ride has reached seat capacity."""
        return self.seats_remaining() <= 0


class RideParticipant(models.Model):
    """Represent a passenger assigned to a ride."""

    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Profile, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of this RideParticipant."""
        return f"{self.passenger.display_name} joined ride {self.ride.pk}"


class RideMessage(models.Model):
    """Represent a message sent in a ride group chat."""

    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of this RideMessage."""
        return f"{self.sender.display_name}: {self.text[:30]}"
