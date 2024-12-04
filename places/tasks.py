from celery import shared_task
from django.core.management import call_command

@shared_task
def update_places():
    # Update different categories
    categories = [
        ('restaurants in Astana', 'Restaurants'),
        ('hotels in Astana', 'Hotels'),
        ('tourist attractions in Astana', 'Attractions'),
        ('shopping malls in Astana', 'Shopping'),
        ('entertainment in Astana', 'Entertainment')
    ]
    
    for query, category in categories:
        call_command('fetch_places', query=query, category=category)