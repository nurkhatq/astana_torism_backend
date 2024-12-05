import os
import sys
from django.core.management import call_command
import django

# Set UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

# Add the project directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(project_root)

# Set the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astana_tourism.settings')

# Initialize Django
django.setup()

def export_data():
    # Export as JSON fixtures with UTF-8 encoding
    with open('all_data.json', 'w', encoding='utf-8') as out:
        call_command('dumpdata', '--exclude', 'auth.permission', '--exclude', 'contenttypes', 
                     '--exclude', 'admin.logentry', '--indent', '2', 
                     stdout=out, format='json')

if __name__ == '__main__':
    export_data()
    print("Data exported successfully to all_data.json")
