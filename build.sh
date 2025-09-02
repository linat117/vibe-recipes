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

# Run database migrations during build
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Load sample data
echo "🥕 Loading sample data..."
python manage.py load_sample_data

echo "✅ Build completed successfully!"
