# File: models.py
# Author: Louis Szeto (szetol@bu.edu), 2/12/2026
# Description: Data models for the mini_insta application. Includes Profile
# model used to represent user profile information. (2/18/2026) Also added  Post,and Photo.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    """Represent a mini_insta user profile."""
 
 
    # data attributes of a Article:
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField()
    profile_image_url = models.URLField(blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1,            # use admin user id as default for migration
        related_name="profiles",
    )
    
    def __str__(self):
        '''Return a string representation of this object.'''
        return f'{self.username} ({self.display_name})'
# Author: Louis Szeto (szetol@bu.edu), 2/26/2026
# Description: Added more methods for accessing posts, followers, following, and also feed.
    def get_all_posts(self):
        return Post.objects.filter(profile=self).order_by("-timestamp")
    def get_absolute_url(self):
        """Return the URL for this Profile detail page."""
        return reverse("profile_detail", kwargs={"pk": self.pk})
    def get_followers(self):
        """Return a list of Profiles who follow this profile."""
        follows = Follow.objects.filter(profile=self)
        return [f.follower_profile for f in follows]

    def get_num_followers(self):
        """Return number of followers."""
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        """Return a list of Profiles this profile is following."""
        follows = Follow.objects.filter(follower_profile=self)
        return [f.profile for f in follows]

    def get_num_following(self):
        """Return number of profiles being followed."""
        return Follow.objects.filter(follower_profile=self).count()
    def get_post_feed(self):
        """Return a QuerySet of Posts from Profiles that this Profile follows."""
        following_profiles = Follow.objects.filter(
            follower_profile=self
        ).values_list("profile")

        return Post.objects.filter(
            profile__in=following_profiles
        ).order_by("-timestamp")
    
# Description: Additional models for mini_insta Assignment 4.
class Post(models.Model):
    """Represent an Instagram post."""

    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"Post by {self.profile.username} ({self.id})"

    # Accessor method to get all photos
    def get_all_photos(self):
        return Photo.objects.filter(post=self).order_by("timestamp")
    # Author: Louis Szeto (szetol@bu.edu), 2/26/2026
    # Description: Added more methods for accessing Likes and comments of the post.
    def get_all_comments(self):
        """Return a QuerySet of all comments for this Post."""
        return Comment.objects.filter(post=self).order_by("timestamp")

    def get_likes(self):
        """Return a QuerySet of all likes for this Post."""
        return Like.objects.filter(post=self)

class Photo(models.Model):
    """Represent a photo belonging to a Post."""

    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    image_file = models.ImageField(blank=True) #NEW 2/24/2026 added image field

    # Author: Louis Szeto, 2/24/2026, modified __str__ and added get_image_url method
    def __str__(self):
        if self.image_url:
            return f"Photo (url) for Post {self.post.pk}"
        if self.image_file:
            return f"Photo (file) for Post {self.post.pk}"
        return f"Photo (empty) for Post {self.post.pk}"

    def get_image_url(self):
        """Return the best URL to display this photo (url first, else file)."""
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return ""
# Author: Louis Szeto (szetol@bu.edu), 2/25/2026
# Description: Added Follow, Comment, and Like model. 
class Follow(models.Model):
    """Encapsulate one Profile following another Profile."""

    profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="profile"
    )
    follower_profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name= "follower_profile"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower_profile.username} follows {self.profile.username}"

class Comment(models.Model):
    """Encapsulate a comment that a Profile makes on a Post."""

    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    def __str__(self):
        return f"Comment by {self.profile.username} on Post {self.post.pk}"
    
class Like(models.Model):
    """Encapsulate a like that a Profile gives to a Post."""

    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.username} likes Post {self.post.pk}"