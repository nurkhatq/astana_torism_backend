# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from places.models import Place

class User(AbstractUser):
    # Existing fields
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions'
    )
    
    # Profile fields
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Additional profile fields
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    preferred_language = models.CharField(
        max_length=10, 
        choices=[('en', 'English'), ('ru', 'Russian'), ('kk', 'Kazakh')],
        default='en'
    )
    
    # Social media links
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    
    # Favorites and preferences
    favorite_places = models.ManyToManyField(
        Place, 
        related_name='favorited_by',
        blank=True
    )
    
    def get_review_count(self):
        return self.reviews.count()
    
    def get_favorite_places_count(self):
        return self.favorite_places.count()
    
    def __str__(self):
        return self.username