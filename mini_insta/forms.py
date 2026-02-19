# File: forms.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: Forms for mini_insta. Includes a ModelForm for creating posts.

from django import forms
from .models import Post


class CreatePostForm(forms.ModelForm):
    """Collect inputs needed to create a Post (excluding Profile)."""

    image_url = forms.URLField(label="Image URL", max_length=300)

    class Meta:
        model = Post
        fields = ["caption"]
