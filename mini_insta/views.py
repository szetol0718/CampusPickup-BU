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
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

class MyLoginRequiredMixin(LoginRequiredMixin):
    """Require login and provide helper to get the logged-in user's Profile."""
    login_url = "/accounts/login/"

    def get_my_profile(self):
        """Return the Profile associated with the logged-in user."""
        return get_object_or_404(Profile, user=self.request.user)

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

class CreatePostView(MyLoginRequiredMixin,CreateView):
    """Create a Post for a specific Profile and also create one Photo."""
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        """Add the Profile to context so template can build form action + cancel link."""
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_my_profile()
        return context

    def form_valid(self, form):
        profile = self.get_my_profile()
        form.instance.profile = profile

        response = super().form_valid(form)
        #New to add multiple photos
        files = self.request.FILES.getlist("files")
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)

        return response

    def get_success_url(self):
        """Redirect to the Post detail page after successful creation."""
        return reverse("show_post", kwargs={"pk": self.object.pk})
    #for bebug
    def form_invalid(self, form):
        print("CreatePostView form_invalid errors:", form.errors)
        return super().form_invalid(form)
    
# Author: Louis Szeto (szetol@bu.edu), 2/25/2026
# Description: Views for mini_insta Updating profile, deleting post, and updating post
class UpdateProfileView(MyLoginRequiredMixin, UpdateView):
    """Update an existing Profile."""
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    context_object_name = "profile"

    def get_object(self):
        return self.get_my_profile()
    
class DeletePostView(MyLoginRequiredMixin, DeleteView):
    """Delete a Post after confirmation."""
    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_object().profile
        return context

    def get_success_url(self):
        """After deletion, redirect to the Profile page of the post owner."""
        return reverse("profile_detail", kwargs={"pk": self.get_object().profile.pk})

class UpdatePostView(MyLoginRequiredMixin, UpdateView):
    """Update the caption of a Post."""
    model = Post
    fields = ["caption"]
    template_name = "mini_insta/update_post_form.html"
    context_object_name = "post"

    def get_success_url(self):
        """After updating, redirect back to this Post detail page."""
        return reverse("show_post", kwargs={"pk": self.object.pk})
# Author: Louis Szeto (szetol@bu.edu), 2/26/2026
# Description: Views for mini_insta to show follwers, following of a profile and also 
# the feed of posts from followed profiles. Also added search view to search for profiles and posts.
class ShowFollowersDetailView(DetailView):
    """Show the followers of a Profile."""
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
    """Show who a Profile is following."""
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class PostFeedListView(MyLoginRequiredMixin, ListView):
    """Display the feed for one Profile (posts from followed profiles)."""
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Return the Posts to display in the feed."""
        profile = self.get_my_profile()
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        """Add the Profile to context for navigation links."""
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_my_profile()
        return context
    
class SearchView(MyLoginRequiredMixin, ListView):
    """Search Profiles and Posts."""
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        """Show search page if no query."""
        query = self.request.GET.get("query", "").strip()

        if not query:
            return render(request, "mini_insta/search.html", {
                "profile": self.get_my_profile()
            })

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return matching posts."""
        query = self.request.GET.get("query", "").strip()

        return Post.objects.filter(
            caption__icontains=query
        ).order_by("-timestamp")

    def get_context_data(self, **kwargs):
        """Add profiles + posts results."""
        context = super().get_context_data(**kwargs)

        profile = self.get_my_profile()
        query = self.request.GET.get("query", "").strip()

        # Posts (already filtered)
        matching_posts = self.get_queryset()

        # Profiles 
        by_username = Profile.objects.filter(username__icontains=query)
        by_display = Profile.objects.filter(display_name__icontains=query)
        by_bio = Profile.objects.filter(bio_text__icontains=query)

        # combine and remove duplicates
        matching_profiles = (by_username | by_display | by_bio).distinct()

        context["profile"] = profile
        context["query"] = query
        context["posts"] = matching_posts
        context["profiles"] = matching_profiles

        return context

class MyProfileDetailView(MyLoginRequiredMixin, DetailView):
    """Show the logged-in user's profile."""
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        return self.get_my_profile()