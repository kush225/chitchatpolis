#!/bin/bash

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
gunicorn --bind 0.0.0.0:8000 chitchatpolis.wsgi:application