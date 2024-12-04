# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name',
        'phone_number',
        'country',
        'city',
        'preferred_language',
        'is_staff'
    )

    fieldsets = (
        # Default fieldsets
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': (
                'first_name', 
                'last_name', 
                'email',
                'avatar',
                'bio',
                'phone_number',
                'date_of_birth',
                'country',
                'city',
                'preferred_language'
            )
        }),
        ('Social Media', {
            'fields': (
                'instagram',
                'facebook',
                'twitter'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal info', {
            'fields': (
                'email',
                'first_name',
                'last_name',
                'avatar',
                'bio',
                'phone_number',
                'date_of_birth',
                'country',
                'city',
                'preferred_language'
            )
        }),
        ('Social Media', {
            'fields': (
                'instagram',
                'facebook',
                'twitter'
            )
        })
    )

    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'preferred_language', 'country')
    ordering = ('username',)
    
    # Optional: Add filter horizontal for many-to-many fields
    filter_horizontal = ('groups', 'user_permissions', 'favorite_places')