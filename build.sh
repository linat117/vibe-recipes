#!/usr/bin/env bash
# Build script for deployment

echo "🚀 Building Recipe Generator..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
cd vibe_recipes
python manage.py collectstatic --noinput

# Run database migrations (if database is available)
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput || echo "⚠️ Database not available yet, migrations will run after deployment"

echo "✅ Build completed successfully!"
