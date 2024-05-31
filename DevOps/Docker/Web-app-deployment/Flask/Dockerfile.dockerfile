# Use an official Python runtime as a parent image for this dockerfile
# It instructs Docker to pull the official Python image with version 3.9.13 that has been optimized for minimal size (slim variant)
FROM python:3.9.13-slim

# Optional - Set environment variables to optimize Python for Docker
# PYTHONDONTWRITEBYTECODE prevents Python from writing pyc files to disk (bytecode)
# PYTHONUNBUFFERED ensures that Python output is sent directly to the terminal without buffering, improving container log readability
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Optional - Set metadata for the generated image. 
# This LABEL instruction adds information about the maintainer, version and description of the image
LABEL maintainer="Your Name <your.email@example.com>"
LABEL version="1.0"
LABEL description="Docker image for a Flask application"

# Set the working directory within the docker container to '/app'. All subsequent commands will be executed in this directory
WORKDIR /app

# Copy the requirements file from the local host (the directory where the Docker build command is executed) to the container's working directory
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
# The --no-cache-dir option is used to prevent caching of downloaded packages, which helps keep the image size smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the flask app code from the local host to the container's working directory
COPY . .

# It informs docker that the container will listen on port 5000 at runtime
# This does not actually publish the port, but rather documents that the container listens on the specified ports at runtime
EXPOSE 5000

# Define environment variable to specify the main file (entry point) of the flask application
ENV FLASK_APP=app.py

# Defines the default command to run when the container starts. It Runs the flask application when the container launches using the flask CLI, listening on all available interfaces
# The "--host=0.0.0.0" flag ensures that Flask listens on all available network interfaces within the container, making it accessible externally
CMD ["flask", "run", "--host=0.0.0.0"]
# Another option to run the Flask application is by directly executing the Python interpreter with the main file as argument, but may provide less flexibility in configuration:
# CMD ["python", "app.py"]