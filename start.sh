#!/usr/bin/env bash
# Start script for deployment

echo "🚀 Starting Recipe Generator..."

# Change to the Django project directory
cd vibe_recipes

# Activate the virtual environment
echo "🔧 Activating virtual environment..."
source ../.venv/bin/activate

# Start the application
echo "🌐 Starting gunicorn server..."
gunicorn vibe_recipes.wsgi:application --bind 0.0.0.0:$PORT
