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

    RIDE_ROLE_CHOICES = [
        ("driver", "I am driving"),
        ("requester", "I need a ride"),
    ]

    ride_role = forms.ChoiceField(
        choices=RIDE_ROLE_CHOICES,
        label="Create this ride as",
    )

    pickup_time = forms.DateTimeField(
        required=False,
        label="Pickup time for reservation",
        help_text="Leave blank for real-time rides.",
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
            "ride_role",
            "request_type",
            "pickup_location",
            "destination",
            "pickup_latitude",
            "pickup_longitude",
            "destination_latitude",
            "destination_longitude",
            "pickup_time",
            "seat_capacity",
        ]
        labels = {
            "seat_capacity": "Total seats, including you",
        }
        widgets = {
            "pickup_location": forms.TextInput(
                attrs={"placeholder": "Example: BU Student Village 2"}
            ),
            "destination": forms.TextInput(
                attrs={"placeholder": "Example: Logan Airport"}
            ),
            "seat_capacity": forms.NumberInput(attrs={"min": 1}),
            "pickup_latitude": forms.HiddenInput(),
            "pickup_longitude": forms.HiddenInput(),
            "destination_latitude": forms.HiddenInput(),
            "destination_longitude": forms.HiddenInput(),
        }

    def clean(self):
        """Require a pickup time only for reservation rides."""
        cleaned_data = super().clean()
        request_type = cleaned_data.get("request_type")
        pickup_time = cleaned_data.get("pickup_time")

        if request_type == "reservation" and not pickup_time:
            self.add_error("pickup_time", "Reservation rides need a pickup time.")
        elif request_type == "realtime":
            cleaned_data["pickup_time"] = None

        # Ride requesters always start with the default capacity.
        if cleaned_data.get("ride_role") == "requester":
            cleaned_data["seat_capacity"] = 4

        # Hidden coordinate fields come from the Google Maps search buttons.
        coordinate_fields = [
            "pickup_latitude",
            "pickup_longitude",
            "destination_latitude",
            "destination_longitude",
        ]
        if any(cleaned_data.get(field) is None for field in coordinate_fields):
            raise forms.ValidationError(
                "Please use Find for both pickup and destination before saving."
            )

        return cleaned_data


class RideMessageForm(forms.ModelForm):
    """Form for creating and updating RideMessage records."""

    class Meta:
        """Metadata for RideMessageForm fields."""

        model = RideMessage
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4}),
        }
