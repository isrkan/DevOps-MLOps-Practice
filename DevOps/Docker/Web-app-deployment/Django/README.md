# Deploying Django app with Docker

This guide provides step-by-step instructions to deploy a Django app using Docker. Docker allows you to package your application with all its dependencies into a standardized unit, called a container, ensuring consistency across different environments.

### Step 1: Prepare Django app
Before deploying the Django app with Docker, ensure that the Django application is properly configured and works locally.

### Step 2: Prepare requirements file
First, create a `requirements.txt` file listing all the Python packages that the Django app depends on. We can generate this file using the following command:

```bash
pip freeze > requirements.txt
```
Or just with version number:

```bash
pip list --format=freeze > requirements.txt
```

### Step 3: Prepare Dockerfile
Next, create a Dockerfile in the root directory of the Django application. This file specifies how to build the Docker image for the application.

### Step 4: Build docker image
Now, build the Docker image for the Django app using the following command:

```bash
docker build -t my-django-app:1.0 .
```

### Step 5: Run Docker container
Once the Docker image is built, we can run a Docker container using the following command:

```bash
docker run -p 8000:8000 my-django-app:1.0
```

This command maps port 8000 on the host to port 8000 on the container, allowing access to the Django app.

### Step 6: Using Docker compose (optional)
    Alternatively, we can use Docker compose to define and run the Docker containers in a YAML file (We should create a docker-compose.yml file). Docker Compose simplifies the management of multi-container applications. To start the Flask app using Docker compose, run the following command:

```bash
docker-compose up
```

This will start the Django app container (together with other containers, e.g., PostgreSQL) as defined in the docker-compose.yml file.

### Step 7: Verify deployment
Visit http://localhost:8000 in the web browser to verify that the Django app is running correctly inside the Docker container.