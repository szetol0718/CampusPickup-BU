# File: forms.py
# Author: Louis Szeto (szetol@bu.edu), 4/21/2026
# Description: Forms for the campus pickup application.

from django import forms

from .models import Profile, Ride, RideMessage


class CreateProfileForm(forms.ModelForm):
    """Form for creating a Profile after a User account exists."""

    class Meta:
        """Metadata for CreateProfileForm fields."""

        model = Profile
        fields = ["display_name", "bio_text", "profile_image_url"]
        labels = {
            "profile_image_url": "Profile image",
        }
        widgets = {
            "profile_image_url": forms.FileInput(attrs={"accept": "image/*"}),
        }


class RideForm(forms.ModelForm):
    """Form for creating and updating Ride records."""

    pickup_time = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        """Metadata for RideForm fields."""

        model = Ride
        fields = [
            "driver",
            "pickup_location",
            "destination",
            "pickup_time",
            "request_type",
            "status",
            "seat_capacity",
        ]


class RideMessageForm(forms.ModelForm):
    """Form for creating and updating RideMessage records."""

    class Meta:
        """Metadata for RideMessageForm fields."""

        model = RideMessage
        fields = ["ride", "text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
        }
