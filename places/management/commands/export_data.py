# places/management/commands/export_data.py
from django.core.management.base import BaseCommand
from django.core import serializers
import json
from places.models import Place, Review  # Import your models
from users.models import User  # Import your user model

class Command(BaseCommand):
    help = 'Export data with proper UTF-8 encoding'

    def handle(self, *args, **options):
        # Export Places
        places = Place.objects.all()
        with open('places_data.json', 'w', encoding='utf-8') as f:
            serializers.serialize('json', places, stream=f, ensure_ascii=False, indent=2)

        # Export Reviews
        reviews = Review.objects.all()
        with open('reviews_data.json', 'w', encoding='utf-8') as f:
            serializers.serialize('json', reviews, stream=f, ensure_ascii=False, indent=2)

        # Export Users (if needed)
        users = User.objects.all()
        with open('users_data.json', 'w', encoding='utf-8') as f:
            serializers.serialize('json', users, stream=f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS('Successfully exported data'))