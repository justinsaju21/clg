#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
echo "Runnning Database Migrations..."
python manage.py migrate || { echo "MIGRATION FAILED"; exit 1; }
echo "Migrations Complete."
