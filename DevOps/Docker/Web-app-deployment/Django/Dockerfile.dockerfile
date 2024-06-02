# Use an official Python runtime as a parent image for this Dockerfile
# It instructs Docker to pull the official Python image with version 3.9.13 that has been optimized for minimal size (slim variant)
FROM python:3.9.13-slim

# Optional - Set environment variables to optimize Python for Docker
# PYTHONDONTWRITEBYTECODE prevents Python from writing .pyc files to disk (bytecode)
# PYTHONUNBUFFERED ensures that Python output is sent directly to the terminal without buffering, improving container log readability
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Optional - Set metadata for the generated image.
# This LABEL instruction adds information about the maintainer, version, and description of the image
LABEL maintainer="Your Name <your.email@example.com>"
LABEL version="1.0"
LABEL description="Docker image for a Django application"

# Set the working directory within the Docker container to '/app'. All subsequent commands will be executed in this directory
WORKDIR /app

# Copy the requirements file from the local host (the directory where the Docker build command is executed) to the container's working directory
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
# The --no-cache-dir option is used to prevent caching of downloaded packages, which helps keep the image size smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django app code from the local host to the container's working directory
COPY . .

# Collect static files - It gathers all static files from the Django project and any installed apps into a single directory (STATIC_ROOT)
RUN python manage.py collectstatic --noinput

# Run database migrations - It applies any pending database migrations to the database schema
# Migrations are Django's way of propagating changes we make to our models (adding a field, deleting a model, etc.) into our database schema
RUN python manage.py migrate

# It informs Docker that the container will listen on port 8000 at runtime
# This does not actually publish the port, but rather documents that the container listens on the specified ports at runtime
EXPOSE 8000

# Define environment variable to specify the main file (entry point) of the Django application
# It specifies the settings module for the Django project
ENV DJANGO_SETTINGS_MODULE=myproject.settings

# Defines the default command to run when the container starts. It runs the Django application when the container launches using the Django management command, listening on all available interfaces
# The "0.0.0.0:8000" flag ensures that Django listens on all available network interfaces within the container, making it accessible externally
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]