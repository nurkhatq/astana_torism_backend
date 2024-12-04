# places/management/commands/fetch_all_places.py
from django.core.management.base import BaseCommand
from django.db import transaction
from places.services import GooglePlacesService
from places.models import Category, Place, PlaceImage
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.core.files.base import ContentFile
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch places from all categories in Astana'

    CATEGORIES = {
        'Attractions': [
            'tourist attractions in Astana',
            'monuments in Astana',
            'museums in Astana',
            'art galleries in Astana',
            'landmarks in Astana'
        ],
        'Entertainment': [
            'entertainment centers in Astana',
            'theaters in Astana',
            'concert halls in Astana',
            'movie theaters in Astana',
            'amusement parks in Astana'
        ],
        'Restaurants': [
            'best restaurants in Astana',
            'fine dining in Astana',
            'casual restaurants in Astana',
            'traditional kazakh restaurants in Astana',
            'international restaurants in Astana'
        ],
        'Shopping': [
            'shopping malls in Astana',
            'markets in Astana',
            'souvenir shops in Astana',
            'shopping centers in Astana',
            'boutiques in Astana'
        ],
        'Hotels': [
            'luxury hotels in Astana',
            'boutique hotels in Astana',
            'business hotels in Astana',
            'hotels near attractions in Astana',
            'apartments in Astana'
        ],
        'Nature': [
            'parks in Astana',
            'gardens in Astana',
            'nature spots in Astana',
            'riverside walks in Astana',
            'outdoor recreation in Astana'
        ],
        'Sports': [
            'sports centers in Astana',
            'fitness clubs in Astana',
            'stadiums in Astana',
            'swimming pools in Astana',
            'ice rinks in Astana'
        ]
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            nargs='+',
            help='Specific categories to fetch (default: all)',
            choices=self.CATEGORIES.keys()
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit places per query',
            default=20
        )

    def handle(self, *args, **options):
        service = GooglePlacesService()
        categories_to_fetch = options['categories'] or self.CATEGORIES.keys()
        limit = options['limit']

        self.stdout.write(self.style.SUCCESS(f'Starting to fetch places for categories: {categories_to_fetch}'))

        total_places = 0
        start_time = time.time()

        for category_name in categories_to_fetch:
            self.stdout.write(f'\nProcessing category: {category_name}')
            category, _ = Category.objects.get_or_create(name=category_name)
            
            search_queries = self.CATEGORIES[category_name]
            for query in search_queries:
                try:
                    places_count = self._process_query(service, query, category, limit)
                    total_places += places_count
                    self.stdout.write(self.style.SUCCESS(
                        f'Fetched {places_count} places for query: {query}'
                    ))
                    time.sleep(2)  # Respect API rate limits between queries
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Error processing query "{query}": {str(e)}'
                    ))

        end_time = time.time()
        duration = end_time - start_time

        self.stdout.write(self.style.SUCCESS(
            f'\nFinished fetching places!'
            f'\nTotal places processed: {total_places}'
            f'\nTime taken: {duration:.2f} seconds'
        ))

    def _process_query(self, service, query, category, limit):
        places_count = 0
        places_data = service.search_places(query)
        
        if not places_data.get('results'):
            return places_count

        for place_data in places_data.get('results', [])[:limit]:
            try:
                with transaction.atomic():
                    places_count += self._process_place(service, place_data, category)
            except Exception as e:
                logger.error(f"Error processing place: {str(e)}")
                continue

        return places_count

    def _process_place(self, service, place_data, category):
        if 'place_id' not in place_data:
            return 0

        # Get detailed information
        details = service.get_place_details(place_data['place_id'])
        place_details = details.get('result', {})

        if not place_details:
            return 0

        # Prepare place data
        place_data = {
            'name': place_details.get('name', ''),
            'category': category,
            'address': place_details.get('formatted_address', ''),
            'phone': place_details.get('formatted_phone_number', ''),
            'website': place_details.get('website', ''),
            'google_place_id': place_data['place_id'],
            'google_rating': place_details.get('rating'),
            'price_level': place_details.get('price_level'),
        }

        # Add coordinates if available
        if 'geometry' in place_details and 'location' in place_details['geometry']:
            place_data['latitude'] = place_details['geometry']['location'].get('lat')
            place_data['longitude'] = place_details['geometry']['location'].get('lng')

        # Add description
        if 'editorial_summary' in place_details:
            place_data['description'] = place_details['editorial_summary'].get('overview', '')
        elif 'reviews' in place_details and place_details['reviews']:
            # Use the first review as a description if no editorial summary
            place_data['description'] = place_details['reviews'][0].get('text', '')[:500]

        # Create or update place
        place, created = Place.objects.update_or_create(
            google_place_id=place_data['google_place_id'],
            defaults=place_data
        )

        # Handle photos
        self._process_photos(service, place, place_details)

        return 1

    def _process_photos(self, service, place, place_details):
        photos = place_details.get('photos', [])
        for i, photo in enumerate(photos[:5]):  # Limit to 5 photos
            try:
                photo_data = service.get_place_photos(photo.get('photo_reference'))
                if photo_data:
                    image = PlaceImage(
                        place=place,
                        is_primary=(i == 0)
                    )
                    image.image.save(
                        f"{place.name.lower().replace(' ', '_')}_{i}.jpg",
                        ContentFile(photo_data),
                        save=True
                    )
            except Exception as e:
                logger.error(f"Error saving photo for {place.name}: {str(e)}")