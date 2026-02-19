# File: views.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: Views for mini_insta. Includes a ListView to display all and 
# a DetailView to display details of a single Profile record. The ListView
# displays all Profile records using the show_all_profiles.html template.

from django.views.generic import ListView, DetailView
from .models import Profile, Post, Photo
import time
from django.urls import reverse
from django.views.generic import CreateView
from .forms import CreatePostForm


class ProfileListView(ListView):
    """Display a list of all Profile records."""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    """Display details of a single Profile record."""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"
    
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: Views for mini_insta including list/detail views and create post.   
class PostDetailView(DetailView):
    """Display a single Post and its photos."""
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

class CreatePostView(CreateView):
    """Create a Post for a specific Profile and also create one Photo."""
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        """Add the Profile to context so template can build form action + cancel link."""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """Attach Profile FK to Post, then create one Photo using image_url."""
        print(f"CreateCommentView.form_valid: form.cleaned_data={form.cleaned_data}")
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile

        post = form.save(commit=False)
        post.profile = profile
        post.save()

        image_url = form.cleaned_data["image_url"]
        Photo.objects.create(post=post, image_url=image_url)

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the Post detail page after successful creation."""
        pk = self.kwargs['pk']
        return reverse("profile_detail", kwargs={"pk": pk})
