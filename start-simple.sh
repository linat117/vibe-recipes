#!/usr/bin/env bash
# Simple start script for deployment

echo "🚀 Starting Recipe Generator..."

# Change to the Django project directory
cd vibe_recipes

# Activate the virtual environment
echo "🔧 Activating virtual environment..."
source ../.venv/bin/activate

# Load sample data if database is empty
echo "🥕 Checking and loading sample data..."
python manage.py load_sample_data

# Start the application
echo "🌐 Starting gunicorn server..."
../.venv/bin/gunicorn vibe_recipes.wsgi:application --bind 0.0.0.0:$PORT
