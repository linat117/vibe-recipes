#!/usr/bin/env bash
# Build script for deployment

echo "🚀 Building Recipe Generator..."

# Install dependencies in the current environment
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Ensure gunicorn is available
echo "🔧 Installing gunicorn..."
pip install gunicorn

# Collect static files
echo "📁 Collecting static files..."
cd vibe_recipes
python manage.py collectstatic --noinput

echo "✅ Build completed successfully!"
