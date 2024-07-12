# Deploying Django app with Docker

This guide provides step-by-step instructions to deploy a Django app using Docker. Docker allows us to package our application with all its dependencies into a standardized unit, called a container, ensuring consistency across different environments.

### Step 1: Prepare Django app
Before deploying the Django app with Docker, ensure that the Django application is properly configured and works locally.

### Step 2: Prepare application settings
Ensure that the `settings.py` file contains the necessary configurations for the application such as setting up database connections and configuring static file handling.

##### Installing dependencies
Install Gunicorn and WhiteNoise, which are required for serving the Django application in a production environment and efficiently managing static files:
```bash
python -m pip install gunicorn
python -m pip install whitenoise
```
* `gunicorn` (Green Unicorn) is a Python WSGI HTTP Server for UNIX.
* `whitenoise` allows your Django application to serve its own static files, eliminating the need for a separate web server (like Nginx) just for static files. This simplifies deployment and improves performance by serving static files directly from Django.

##### Updating settings.py
Modify settings.py to include configurations for static files handling and database connection:

1. First, set the directory where collected static files will be stored:
    ```python
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    ```
    `STATIC_ROOT` specifies the directory where Django will collect all static files during deployment. These files are typically served  in production by a web server like Nginx or by a middleware like WhiteNoise.
2. Configure WhiteNoise middleware to serve static files:
    ```python
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files
    ]
    ```
    Add the following line to specify the storage class for static files:
    ```python
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    ```
3. Adjust `DATABASES` Configuration from `HOST` is set to `db`, since when deploying with Docker, services communicate using container names within the Docker network. Here, `db` refers to the database service defined in the `docker-compose.yml` file.
    ```python
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "expenses",
            "USER": "root",
            "PASSWORD": "mysql1",
            "HOST": "db", # Database host (container name in Docker network)
            "PORT": "3306",
        }
    }
    ```

### Step 3: Prepare `requirements.txt`
Create a `requirements.txt` file listing all the Python packages that the Django app depends on. We can generate this file using the following command:
```bash
pip freeze > requirements.txt
```
Or just with version number:

```bash
pip list --format=freeze > requirements.txt
```
Example:
```text
Django==4.2.14
mysqlclient==2.2.4
psycopg2-binary==2.9.9
```

### Step 4: Prepare Dockerfile
Create a `Dockerfile` in the root directory of the Django application. This file specifies how to build the Docker image for the application.

### Step 5: Build Docker image
Build the Docker image for the Django app using the following command:

```bash
docker build -t my-django-app:1.0 .
```

### Step 6: Run Docker container
Once the Docker image is built, run a Docker container using the following command:

```bash
docker run -p 8004:8003 my-django-app:1.0
```

This command maps port 8004 on the host to port 8003 on the container, allowing access to the Django app.
However, in our specific case, the expenses app relies on an SQL database (MySQL), so it will not work without the database running. To manage both the application and the database together, we need Docker Compose.

### Step 7: Using Docker compose (for multi-container Docker applications)
Docker Compose allows us to define and run multi-container Docker applications. We will define and run the Docker containers in a YAML file to use Docker Compose. Create a `docker-compose.yaml` file. To start the Django app and MySQL database using Docker Compose, run the following command:

```bash
docker-compose up
```

This will start the Django app and MySQL database containers as defined in the `docker-compose.yaml` file.

### Step 8: Verify deployment
Visit `http://localhost:8004` in the web browser to verify that the Django app is running correctly inside the Docker container.