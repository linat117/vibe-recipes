#!/usr/bin/env bash
# Start script for deployment

echo "🚀 Starting Recipe Generator..."

# Change to the Django project directory
cd vibe_recipes

# Ensure gunicorn is available
pip install gunicorn

# Start the application
echo "🌐 Starting gunicorn server..."
gunicorn vibe_recipes.wsgi:application --bind 0.0.0.0:$PORT
