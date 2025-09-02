#!/usr/bin/env bash
# Simple start script for deployment

echo "🚀 Starting Recipe Generator..."

# Change to the Django project directory
cd vibe_recipes

# Start the application directly
echo "🌐 Starting gunicorn server..."
../.venv/bin/gunicorn vibe_recipes.wsgi:application --bind 0.0.0.0:$PORT
