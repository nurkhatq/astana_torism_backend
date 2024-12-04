from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from places.services import GooglePlacesService
from places.models import Place, Category, PlaceImage
import time
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch places from Google Places API'

    def add_arguments(self, parser):
        parser.add_argument('--query', type=str, help='Search query')
        parser.add_argument('--category', type=str, help='Category name')
        parser.add_argument('--max-results', type=int, default=60, help='Maximum number of results to fetch')

    def handle(self, *args, **options):
        service = GooglePlacesService()
        query = options['query']
        category_name = options['category']
        max_results = options['max_results']
        
        self.stdout.write(f'Fetching up to {max_results} places for query: {query}')

        # Get or create category
        category, _ = Category.objects.get_or_create(name=category_name)
        
        places_processed = 0
        next_page_token = None
        
        while places_processed < max_results:
            # Wait for 2 seconds if using page token (Google API requirement)
            if next_page_token:
                time.sleep(2)
            
            # Search for places
            places_data = service.search_places(query, page_token=next_page_token)
            
            if not places_data.get('results'):
                break
                
            for place_data in places_data.get('results', []):
                if places_processed >= max_results:
                    break
                    
                try:
                    # Process place (existing code...)
                    places_processed += 1
                    self.stdout.write(f'Processed {places_processed} places')
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error processing place: {str(e)}')
                    )
            
            # Check if there are more results
            next_page_token = places_data.get('next_page_token')
            if not next_page_token:
                break
                
        self.stdout.write(
            self.style.SUCCESS(f'Finished fetching places. Total processed: {places_processed}')
        )