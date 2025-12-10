#!/bin/bash
# Exit on error
set -o errexit

echo "Starting deployment script..."

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py initadmin

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application
