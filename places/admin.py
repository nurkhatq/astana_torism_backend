from django.contrib import admin
from .models import Category, Place, PlaceImage, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'address', 'average_rating')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'address')

@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'is_primary', 'created_at')
    list_filter = ('is_primary',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('place', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('comment', 'place__name', 'user__username')