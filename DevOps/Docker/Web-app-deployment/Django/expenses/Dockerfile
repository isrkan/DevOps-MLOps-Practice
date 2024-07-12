# Use the official Python image from the Docker Hub
# It instructs Docker to pull the official Python image with version 3.10 that has been optimized for minimal size (slim variant)
FROM python:3.9.13-slim

# Optional - Set metadata for the generated image
LABEL version="1.0"
LABEL description="Docker image for a Django application of expenses management"

# Optional - Set environment variables to optimize Python for Docker
# Set environment variable to prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Set environment variable to ensure that Python output is sent directly to the terminal without buffering, improving container log readability
ENV PYTHONUNBUFFERED 1

# Set the working directory within the Docker container to '/app'. All subsequent commands will be executed in this directory
WORKDIR /app

# Install system dependencies that are required for compiling and linking some Python packages
# Some Python packages have components written in C or C++ that need to be compiled during installation such as mysqlclient package
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc \
    libc-dev \
    libmariadb-dev \
    pkg-config

# Copy the requirements file from the local host to the container's working directory
COPY requirements.txt /app/

# Install the dependencies specified in the requirements file
# The --no-cache-dir option is used to prevent caching of downloaded packages, which helps keep the image size smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory from the local host to the container's working directory
COPY . /app/

# Run the Django application using the gunicorn server
# The command tells Gunicorn to serve the Django application defined by the WSGI callable in the expenses_project.wsgi module
# Gunicorn is a WSGI server. It needs to know how to communicate with the Django application, and it does this using the WSGI callable
CMD ["gunicorn", "--bind", "0.0.0.0:8003", "expenses_project.wsgi:application"]
