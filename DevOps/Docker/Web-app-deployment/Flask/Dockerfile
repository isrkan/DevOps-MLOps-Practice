# Use the official Python image from the Docker Hub
# It instructs Docker to pull the official Python image with version 3.9.13 that has been optimized for minimal size (slim variant)
FROM python:3.9.13-slim

# Optional - Set metadata for the generated image. 
# This LABEL instruction adds information about the maintainer, version and description of the image
LABEL version="1.0"
LABEL maintainer="Israel Israeli <israel.israeli@example.com>"
LABEL description="Docker image for a Flask application"

# Optional - Set environment variables to optimize Python for Docker
# Set environment variable to prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Set environment variable to ensure that Python output is sent directly to the terminal without buffering, improving container log readability
ENV PYTHONUNBUFFERED 1
# Define environment variable to specify the main file (entry point) of the flask application
ENV FLASK_APP=app.py

# Set the working directory within the docker container to '/app'. All subsequent commands will be executed in this directory
WORKDIR /app

# Copy the requirements file from the local host (the directory where the Docker build command is executed) to the container's working directory
COPY requirements.txt .

# Install the dependencies specified in the requirements file
# The --no-cache-dir option is used to prevent caching of downloaded packages, which helps keep the image size smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the flask app code from the local host to the container's working directory
COPY . .

# It informs docker that the container will listen on port 5000 at runtime
# This does not actually publish the port, but rather documents that the container listens on the specified ports at runtime
EXPOSE 5000

# Defines the default command to run when the container starts. It Runs the flask application when the container launches using the flask CLI, listening on all available interfaces
# The "--host=0.0.0.0" flag ensures that Flask listens on all available network interfaces within the container, making it accessible externally
CMD ["flask", "run", "--host=0.0.0.0"]