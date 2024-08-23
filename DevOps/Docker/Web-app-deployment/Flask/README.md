# Deploying Flask app with Docker

This guide provides step-by-step instructions to deploy a Flask app using Docker. Docker allows you to package your application with all its dependencies into a standardized unit, called a container, ensuring consistency across different environments.

### Step 1: Prepare Flask app
Before deploying the Flask app with Docker, ensure that the Flask application is properly configured and works locally.

### Step 2: Prepare requirements file
First, create a `requirements.txt` file listing all the Python packages that the Flask app depends on. Docker will use this file to install the necessary dependencies in the container. We can generate this file using the following command:

```bash
pip freeze > requirements.txt
```
Or just with version number:

```bash
pip list --format=freeze > requirements.txt
```

Ensure that `requirements.txt` is in the root directory of the project.

### Step 3: Prepare Dockerfile
Next, create a `Dockerfile` in the root directory of the Flask application. This file specifies how to build the Docker image for the application.

### Step 4: Build docker image
Now, build the Docker image for the Flask app using the following command in the root directory of the project:

```bash
docker build -t my-flask-app:1.0 .
```
This command builds an image named `my-flask-app` with the tag `1.0`. The period (`.`) at the end specifies the build context, which is the current directory.

### Step 5: Run Docker container
Once the Docker image is built, we can run a Docker container using the following command:

```bash
docker run -p 5000:5000 my-flask-app:1.0
```

This command maps port 5000 on the host to port 5000 on the container, allowing access to the Flask app.

### Step 6: Using Docker compose (optional)
Alternatively, while simple Flask app doesn't require multiple containers, Docker Compose can still simplify the process of running and managing containers, especially if the project grows. Docker Compose allows us to define and run multi-container Docker applications.

To use Docker Compose, create a file named `docker-compose.yml` in the root directory. Then, to start the Flask app using Docker compose, run:

```bash
docker-compose up
```

This command builds the image (if not already built) and runs the container as defined in the `docker-compose.yml` file.

### Step 7: Verify deployment
Visit http://localhost:5000 in the web browser to verify that the Flask app is running correctly inside the Docker container.