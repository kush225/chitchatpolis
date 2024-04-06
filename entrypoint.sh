#!/bin/bash

# Run migrations
echo "Running migrations..."
echo "---------------------------------"
python manage.py migrate

if [ "$DEBUG" = "true" ]; then
    echo "DEBUG mode is enabled. Adding test users..."
    # Run management command to populate users
    python manage.py populate_users 10
else
    echo "DEBUG mode is disabled. Skipping adding test user step."
fi

echo "Starting server..."
echo "---------------------------------"

# Start Django server using Gunicorn
python manage.py runserver 0.0.0.0:8000