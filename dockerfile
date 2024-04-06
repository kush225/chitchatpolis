# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/

# Run tests
RUN python manage.py test

# Run migrations
RUN python manage.py migrate

RUN export DJANGO_SETTINGS_MODULE=chitchatpolis.settings

# # Run script to add 1000 random users
# RUN python scripts/add_users.py

RUN chmod +x entrypoint.sh

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
