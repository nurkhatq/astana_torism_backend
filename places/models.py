from django.db import models
from django.conf import settings  # Импортируем настройки Django для кастомной модели пользователя
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='categories/', null=True, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Place(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category', related_name='places', on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Google Places specific fields
    google_place_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    google_rating = models.FloatField(null=True, blank=True)
    site_rating = models.FloatField(null=True, blank=True)
    price_level = models.IntegerField(null=True, blank=True)
    review_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_site_rating(self):
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.site_rating = round(float(avg_rating), 1) if avg_rating else None
        self.save()

    def average_rating(self):
        local_rating = self.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
        if self.google_rating:
            return (local_rating + self.google_rating) / 2
        return local_rating

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['google_place_id']),
            models.Index(fields=['name']),
        ]

class PlaceImage(models.Model):
    place = models.ForeignKey(Place, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='places/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.place.name}"

class Review(models.Model):
    place = models.ForeignKey(Place, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)  # Используем кастомную модель пользователя
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['place', 'user']

    def __str__(self):
        return f"Review by {self.user.username} for {self.place.name}"
