#!/usr/bin/env bash
# Build script for deployment

echo "🚀 Building Recipe Generator..."

# Install dependencies in the current environment
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Ensure gunicorn is available
echo "🔧 Installing gunicorn..."
pip install gunicorn

# Make start script executable
echo "🔧 Making start script executable..."
chmod +x ../start.sh

# Collect static files
echo "📁 Collecting static files..."
cd vibe_recipes
python manage.py collectstatic --noinput

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist (non-interactive)
echo "👤 Creating superuser..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

echo "✅ Build completed successfully!"
