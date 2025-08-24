# Python Standard Library
import os

# Django Imports
from django.conf import settings
from django.db import models
from django.utils import timezone

# Cloudinary Imports
from cloudinary.models import CloudinaryField


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def get_post_upload_path(instance, filename):
    """
    Generate upload path for post images.
    For Cloudinary: returns folder structure
    For local storage: returns file path
    """
    username = instance.user.username if instance.user else 'anonymous'
    return f'posts/{username}/'


# ==============================================================================
# POST MODELS
# ==============================================================================

class Post(models.Model):
    """Represents a user's post in the feed, containing an image and caption."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    
    # Use CloudinaryField for production, ImageField for development
    image = CloudinaryField(
        'image',
        folder='PoornimaX/posts',  # This creates the folder structure in Cloudinary
        transformation={
            'quality': 'auto:good',
            'fetch_format': 'auto',
            'width': 1080,
            'height': 1080,
            'crop': 'limit'
        },
        null=True,
        blank=True
    )
    
    # Fallback ImageField for local development
    local_image = models.ImageField(
        upload_to=get_post_upload_path,
        null=True,
        blank=True,
        help_text="Used for local development only"
    )
    
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(
        default=False, 
        help_text="Designates whether the post is visible to everyone."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at.strftime('%b %d, %Y')}"
    
    @property
    def get_image_url(self):
        """
        Returns the appropriate image URL based on environment.
        Uses Cloudinary in production, local storage in development.
        """
        if hasattr(self, 'image') and self.image:
            try:
                # Try to get Cloudinary URL
                return self.image.url
            except:
                pass
        
        # Fallback to local image
        if self.local_image:
            return self.local_image.url
        
        return None
    
    def save(self, *args, **kwargs):
        """Override save to handle image field based on environment."""
        # If we're using Cloudinary and have a local image, we might want to upload it
        if self.local_image and not self.image:
            # This could be extended to automatically upload local images to Cloudinary
            pass
        
        super().save(*args, **kwargs)


class Like(models.Model):
    """Represents a 'like' from a user on a specific Post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user can only like a post once
        unique_together = ('post', 'user')
        ordering = ['-created_at']
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def __str__(self):
        return f"Like by {self.user.username} on {self.post}"


class Comment(models.Model):
    """Represents a comment from a user on a specific Post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"


# ==============================================================================
# CONFESSION MODELS
# ==============================================================================

class Confession(models.Model):
    """Represents a user's confession, which can be posted anonymously."""
    content = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='confessions',
        null=True,  # Allows for truly anonymous confessions if user is not set
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Confession"
        verbose_name_plural = "Confessions"

    def __str__(self):
        if self.is_anonymous:
            return f"Anonymous confession on {self.created_at.strftime('%b %d, %Y')}"
        return f"Confession by {self.user.username} on {self.created_at.strftime('%b %d, %Y')}"


class ConfessionLike(models.Model):
    """Represents a 'like' from a user on a specific Confession."""
    confession = models.ForeignKey(Confession, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user can only like a confession once
        unique_together = ('confession', 'user')
        ordering = ['-created_at']
        verbose_name = "Confession Like"
        verbose_name_plural = "Confession Likes"

    def __str__(self):
        return f"Like by {self.user.username} on Confession #{self.confession.id}"


class ConfessionComment(models.Model):
    """Represents a comment from a user on a specific Confession."""
    confession = models.ForeignKey(Confession, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # Show comments in chronological order
        verbose_name = "Confession Comment"
        verbose_name_plural = "Confession Comments"

    def __str__(self):
        user_display = "Anonymous" if self.is_anonymous else self.user.username
        return f"Comment by {user_display} on Confession #{self.confession.id}"
