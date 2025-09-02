#!/usr/bin/env python
"""
Database connectivity check script for Render deployment
"""

import os
import sys
import django
from pathlib import Path

# Add the Django project to Python path
sys.path.append(str(Path(__file__).parent / 'vibe_recipes'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vibe_recipes.production')

# Setup Django
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def check_database():
    """Check if database is accessible and run migrations"""
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful!")
        
        # Run migrations
        print("🗄️ Running migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migrations completed!")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    if check_database():
        print("🚀 Database is ready!")
        sys.exit(0)
    else:
        print("💥 Database setup failed!")
        sys.exit(1)
