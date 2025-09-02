#!/usr/bin/env python
"""
Check and load sample data if needed
"""

import os
import sys
import django
from pathlib import Path

# Add the Django project to Python path
sys.path.append(str(Path(__file__).parent / 'vibe_recipes'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vibe_recipes.production-sqlite')

# Setup Django
django.setup()

from apps.recipes.models import Ingredient, Recipe

def check_and_load_data():
    """Check if data exists and load if needed"""
    
    # Check current data
    ingredient_count = Ingredient.objects.count()
    recipe_count = Recipe.objects.count()
    
    print(f"📊 Current data: {ingredient_count} ingredients, {recipe_count} recipes")
    
    # If no data, load sample data
    if ingredient_count == 0:
        print("🥕 No ingredients found, loading sample data...")
        try:
            from django.core.management import execute_from_command_line
            execute_from_command_line(['manage.py', 'load_sample_data'])
            print("✅ Sample data loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading sample data: {e}")
            return False
    else:
        print("✅ Data already exists, skipping load")
    
    # Final count
    final_ingredient_count = Ingredient.objects.count()
    final_recipe_count = Recipe.objects.count()
    
    print(f"📊 Final data: {final_ingredient_count} ingredients, {final_recipe_count} recipes")
    
    return final_ingredient_count > 0

if __name__ == "__main__":
    if check_and_load_data():
        print("🚀 Data check completed successfully!")
        sys.exit(0)
    else:
        print("💥 Data check failed!")
        sys.exit(1)
