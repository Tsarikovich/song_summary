#!/usr/bin/env bash

# Debugging options and safety measures
echo "Running build script..."
set -e  # Exit on any error
set -x  # Debug output to show executed commands

# Install dependencies
echo "Installing dependencies..."
poetry install || { echo "Dependency installation failed"; exit 1; }

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || { echo "Collectstatic failed"; exit 1; }

# Apply database migrations
echo "Checking and applying migrations..."
python manage.py showmigrations || { echo "Failed to check migrations"; exit 1; }
python manage.py migrate --plan || { echo "Migration plan failed"; exit 1; }
python manage.py migrate || { echo "Migrations failed"; exit 1; }

# Create a superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
import os
from django.contrib.auth.models import User
username = os.getenv('ADMIN_USERNAME')
email = os.getenv('ADMIN_EMAIL')
password = os.getenv('ADMIN_PASSWORD')
if username and email and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f'Superuser {username} created.')
    else:
        print(f'Superuser {username} already exists.')
" || { echo "Superuser creation failed"; exit 1; }

echo "Build process completed successfully."