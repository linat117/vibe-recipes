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

# Run database migrations (if database is available)
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput || echo "⚠️ Database not available yet, migrations will run after deployment"

echo "✅ Build completed successfully!"
