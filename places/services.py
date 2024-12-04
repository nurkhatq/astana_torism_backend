import requests
import logging
from django.conf import settings
from django.core.files.base import ContentFile
from .models import Place, Category, PlaceImage

logger = logging.getLogger(__name__)

class GooglePlacesService:
    def __init__(self):
        self.api_key = settings.GOOGLE_PLACES_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api/place"
    
    def search_places(self, query, location="Astana, Kazakhstan", page_token=None):
        endpoint = f"{self.base_url}/textsearch/json"
        params = {
            'query': query,
            'location': '51.1605,71.4704',  # Astana coordinates
            'radius': '30000',  # Increased to 30km radius
            'key': self.api_key,
            'language': 'en'
        }
        
        if page_token:
            params['pagetoken'] = page_token
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching places: {str(e)}")
            return {'results': []}

    def get_place_details(self, place_id):
        endpoint = f"{self.base_url}/details/json"
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_address,geometry,photos,rating,formatted_phone_number,website,reviews,price_level,types,editorial_summary',
            'key': self.api_key,
            'language': 'en'
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching place details: {str(e)}")
            return {'result': {}}

    def get_place_photos(self, photo_reference):
        if not photo_reference:
            return None
            
        endpoint = f"{self.base_url}/photo"
        params = {
            'maxwidth': 800,
            'photo_reference': photo_reference,
            'key': self.api_key
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            logger.error(f"Error fetching photo: {str(e)}")
            return None