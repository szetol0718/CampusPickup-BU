# File: views.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: Views for mini_insta. Includes a ListView to display all and 
# a DetailView to display details of a single Profile record. The ListView
# displays all Profile records using the show_all_profiles.html template.

from django.views.generic import ListView, DetailView
from .models import Profile, Post, Photo, Follow, Like, Comment
from django.utils import timezone
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdateProfileForm, CreateProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from .serializers import ProfileSerializer, PostSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class MyLoginRequiredMixin(LoginRequiredMixin):
    """Require login and provide helper to get the logged-in user's Profile."""
    def get_login_url(self):
        return reverse("login")
    
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["my_profile"] = Profile.objects.get(user=self.request.user)
        return context
    
# Author: Louis Szeto (szetol@bu.edu), 2/18/2026
# Description: Views for mini_insta including list/detail views and create post.   
class PostDetailView(DetailView):
    """Display a single Post and its photos."""
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        if self.request.user.is_authenticated:
            my_profile = Profile.objects.get(user=self.request.user)

            context["my_profile"] = my_profile
            context["i_liked"] = Like.objects.filter(
                post=post,
                profile=my_profile
            ).exists()

        return context

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

# Author: Louis Szeto (szetol@bu.edu), 3/3/2026
# Description: Views for mini_insta to show my profile according to user and login.
# Also modified other views related to adjustment of profile or posts requires user login.
# Added a new view to handle and create new profile. 
class MyProfileDetailView(MyLoginRequiredMixin, DetailView):
    """Show the logged-in user's profile."""
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        return self.get_my_profile()
    
class CreateProfileView(CreateView):
    """Create a Profile and a new Django User from one combined form."""
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["prefix"] = "profile"
        return kwargs

    def get_context_data(self, **kwargs):
        """Add the UserCreationForm to the context."""
        context = super().get_context_data(**kwargs)

        if "user_form" not in context:
            context["user_form"] = UserCreationForm(prefix="user")

        return context

    def form_valid(self, form):
        """Create the User, log them in, attach it to the Profile, then save."""
        user_form = UserCreationForm(self.request.POST, prefix="user")

        if not user_form.is_valid():
            # Re-render page with BOTH forms + errors
            return self.render_to_response(
                self.get_context_data(form=form, user_form=user_form)
            )

        # Create the new User (account username)
        user = user_form.save()

        # Log them in
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")

        # Attach user FK to the Profile form's instance (this is the prefixed form now)
        form.instance.user = user

        # Let CreateView save the Profile and redirect
        return super().form_valid(form)

    def form_invalid(self, form):
        """Ensure user_form errors show when profile form is invalid."""
        user_form = UserCreationForm(self.request.POST, prefix="user")
        return self.render_to_response(
            self.get_context_data(form=form, user_form=user_form)
        )

    def get_success_url(self):
        """After creating a profile, go to the logged-in user's profile page."""
        return reverse("my_profile")
    
# Author: Louis Szeto (szetol@bu.edu), 3/4/2026
# Description: action views to follow profile, delete follow, like post and delete like.
@login_required
def follow_profile(request, pk):
    """Create a Follow: logged-in user follows Profile(pk)."""
    me = get_object_or_404(Profile, user=request.user)
    other = get_object_or_404(Profile, pk=pk)

    # do not allow follow self
    if me.pk == other.pk:
        return redirect(reverse("profile_detail", kwargs={"pk": other.pk}))

    # create only if not already following
    Follow.objects.get_or_create(
        profile=other,
        follower_profile=me,
    )

    return redirect(reverse("profile_detail", kwargs={"pk": other.pk}))


@login_required
def delete_follow(request, pk):
    """Delete a Follow: logged-in user unfollows Profile(pk)."""
    me = get_object_or_404(Profile, user=request.user)
    other = get_object_or_404(Profile, pk=pk)

    Follow.objects.filter(profile=other, follower_profile=me).delete()

    return redirect(reverse("profile_detail", kwargs={"pk": other.pk}))


@login_required
def like_post(request, pk):
    """Create a Like: logged-in user likes Post(pk)."""
    me = get_object_or_404(Profile, user=request.user)
    post = get_object_or_404(Post, pk=pk)

    # do not allow like own post
    if post.profile.pk == me.pk:
        return redirect(reverse("profile_detail", kwargs={"pk": post.pk}))

    Like.objects.get_or_create(
        post=post,
        profile=me,
    )

    return redirect(reverse("show_post", kwargs={"pk": post.pk}))


@login_required
def delete_like(request, pk):
    """Delete a Like: logged-in user unlikes Post(pk)."""
    me = get_object_or_404(Profile, user=request.user)
    post = get_object_or_404(Post, pk=pk)

    Like.objects.filter(post=post, profile=me).delete()

    return redirect(reverse("show_post", kwargs={"pk": post.pk}))

@login_required
def add_comment(request, pk):
    """Create a Comment on Post(pk) by the logged-in user, then redirect."""
    post = get_object_or_404(Post, pk=pk)
    my_profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        text = request.POST.get("comment_text", "").strip()

        if text:
            Comment.objects.create(
                post=post,
                profile=my_profile,
                text=text,
            )

    return redirect(reverse("show_post", kwargs={"pk": post.pk}))

class ProfileListAPIView(generics.ListAPIView):
    """Reading a list of profiles."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ProfileDetailAPIView(generics.RetrieveAPIView):
    """Reading a specific profile."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class PostListCreateAPIView(generics.ListCreateAPIView):
    """Reading all posts or Creating a new post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

def perform_create(self, serializer):
        profile = Profile.objects.filter(user=self.request.user).first()
        serializer.save(profile=profile)

class ProfilePostsAPIView(generics.ListAPIView):
    """Reading posts (and pictures) for one specific profile."""
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile_pk = self.kwargs['pk']
        return Post.objects.filter(profile__pk=profile_pk).order_by('-timestamp')

class ProfileFeedAPIView(generics.ListAPIView):
    """Reading a feed for one profile (posts from followed users)."""
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
            profile = Profile.objects.filter(user=self.request.user).first()
            if profile:
                return profile.get_post_feed()
            return Post.objects.none()
    
class CustomAuthToken(ObtainAuthToken):
    """
    Custom authentication view that returns the token, 
    plus the profile_id and username for the React Native app.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get_or_create(user=user)

        profile = Profile.objects.filter(user=user).first()
        profile_id = profile.id if profile else None

        return Response({
            'token': token.key,
            'profile_id': profile_id,
            'username': user.username
        })