# File: forms.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: Forms for mini_insta. Includes a ModelForm for creating posts.

from django import forms
from .models import Post, Profile


class CreatePostForm(forms.ModelForm):
    """Collect inputs needed to create a Post (excluding Profile)."""

    class Meta:
        model = Post
        fields = ["caption"]

# Author: Louis Szeto (szetol@bu.edu), 2/25/2026
# Description: New Forms for mini_insta updating a Profile
class UpdateProfileForm(forms.ModelForm):
    """Form to update a Profile (excluding username and join_date)."""

    class Meta:
        model = Profile
        fields = ["display_name", "profile_image_url", "bio_text"]