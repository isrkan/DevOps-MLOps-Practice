# Deploying Django App with Kubernetes

This guide provides step-by-step instructions to deploy a Django app using Kubernetes. Kubernetes, an open-source container orchestration platform, automates deploying, scaling, and managing containerized applications.

### Step 1: Prepare  Django app
Before deploying the Django app with Kubernetes, ensure that the Django application is properly configured and works locally.

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
3. Adjust `DATABASES` configuration from `HOST` to `mysql-service` to use the correct service name for the MySQL database in Kubernetes. When deploying with Kubernetes, services communicate using service names defined in the configuration files. In this case, `mysql-service` refers to the database service defined in the `mysql-configurations.yaml` file.

    ```python
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "expenses",
            "USER": "root",
            "PASSWORD": "mysql1",
            "HOST": "mysql-service", # Database host (service name in Kubernetes)
            "PORT": "3306",
        }
    }
    ```

### Step 3: Prepare Docker image
Build the Docker image for the Django app locally using the Dockerfile. Run the following command in the root directory of the project:

```bash
docker build -t expenses:1.0 .
```

### Step 4: Push Docker image to a Docker registry
Push the Docker image to it a Docker registry such as Docker Hub. First. Tag the image for the Docker registry:

```bash
docker tag expenses:1.0 <dockerhub-username>/<repository>:<tag>
```

Then, push the image to the Docker registry:

```bash
docker push <username>/<repository>:<tag>
```

### Alternative for step 4: Load Docker image into Minikube
Alternatively, we can directly load the Docker image into Minikube. Minikube provides a way to directly transfer local Docker images to the Minikube Docker environment. First, ensure Minikube is running:

```bash
minikube start
```

Then, load the Docker image into Minikube:

```bash
minikube image load expenses:1.0
```

In our specific use-case, we directly will load the Docker image into Minikube.

### Step 5: Start Minikube
If Minikube is not already running, start it:

```bash
minikube start
```

Then, navigate to the Kubernetes configuration files directory:

```bash
cd k8s-files
```

### Step 6: Deploy MySQL
Create a `mysql-configurations.yaml` file to deploy the MySQL database. This file should include the PersistentVolumeClaim (PVC - request storage resources from Kubernetes), Deployment (Defines the MySQL database container), and Service (exposes the MySQL container within the cluster for internal communication) configurations for MySQL. Apply the configurations using:

```bash
kubectl apply -f mysql-configurations.yaml
```

We deploy MySQL first because the Django application depends on the database being available.

### Step 7: Deploy migrations job
Before deploying the Django application, we need to run database migrations. Create a `migrations-job.yaml` file to define the job that will handle the migrations. This file should include the necessary configurations for running Django migrations. Apply the configurations using:

```bash
kubectl apply -f migrations-job.yaml
```

### Step 8: Deploy Django App
Create a `expenses-configurations.yaml` file to deploy the  Django application. This file should include the Deployment and Service configurations for the Django app. Apply the configurations using:

```bash
kubectl apply -f expenses-configurations.yaml
```

### Step 9: Check the status of jobs and pods
Verify the status of the jobs and pods to ensure that MySQL, the migrations job, and the Django application are running correctly:

```bash
kubectl get jobs
kubectl get pods
```

Running `kubectl logs job/expenses-migrations-job` will fetch the logs for the `expenses-migrations-job` job that was previously executed for debugging and monitoring the execution of the Kubernetes jobs.

### Step 10: Verify deployment
To verify that the Django app is running correctly inside the Kubernetes cluster, expose the service using Minikube:

```bash
minikube service expenses-service
```

This command will open the service in our default web browser, allowing us to check the application's status.
