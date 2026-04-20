# File: forms.py
# Author: Louis Szeto (szetol@bu.edu), 4/21/2026
# Description: Forms for the campus pickup application.

from django import forms

from .models import Ride, RideMessage


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
            "creator",
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
        fields = ["ride", "sender", "text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
        }
