# File: views.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: Views for mini_insta. Includes a ListView to display all and 
# a DetailView to display details of a single Profile record. The ListView
# displays all Profile records using the show_all_profiles.html template.

from django.views.generic import ListView, DetailView
from .models import Profile, Post, Photo
import time
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdateProfileForm


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
    
# Author: Louis Szeto (szetol@bu.edu), 2/18/2026
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
        pk = self.kwargs["pk"]
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile

        response = super().form_valid(form)
        #New to add multiple photos
        files = self.request.FILES.getlist("files")
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)

        return response

    def get_success_url(self):
        """Redirect to the Post detail page after successful creation."""
        pk = self.kwargs['pk']
        return reverse("profile_detail", kwargs={"pk": pk})
    #for bebug
    def form_invalid(self, form):
        print("CreatePostView form_invalid errors:", form.errors)
        return super().form_invalid(form)
    
# Author: Louis Szeto (szetol@bu.edu), 2/25/2026
# Description: Views for mini_insta Updating profile, deleting post, and updating post
class UpdateProfileView(UpdateView):
    """Update an existing Profile."""
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    context_object_name = "profile"

class DeletePostView(DeleteView):
    """Delete a Post after confirmation."""
    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_success_url(self):
        """After deletion, redirect to the Profile page of the post owner."""
        return reverse("profile_detail", kwargs={"pk": self.get_object().profile.pk})

class UpdatePostView(UpdateView):
    """Update the caption of a Post."""
    model = Post
    fields = ["caption"]
    template_name = "mini_insta/update_post_form.html"
    context_object_name = "post"

    def get_success_url(self):
        """After updating, redirect back to this Post detail page."""
        return reverse("show_post", kwargs={"pk": self.object.pk})