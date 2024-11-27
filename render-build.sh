#!/usr/bin/env bash

# Install dependencies
poetry install

# Run collectstatic
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
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