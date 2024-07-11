# Deploying Spring Boot App with Kubernetes

This guide provides step-by-step instructions to deploy a Spring Boot app using Kubernetes. Kubernetes, an open-source container orchestration platform, automates deploying, scaling, and managing containerized applications.

### Step 1: Prepare Spring Boot app
Before deploying the Spring Boot app with Kubernetes, ensure that the Spring Boot application is properly configured and works locally.

### Step 2: Prepare application properties
Ensure that the `application.properties` file contains the necessary configurations for the application, such as database connection properties. We can use environment variables to make these configurations more flexible.

### Step 3: Prepare Docker image
Build the Docker image for the Spring Boot app locally using the Dockerfile. Run the following command in the root directory of the project:

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

# Alternative for step 4: Load Docker image into Minikube
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

### Step 6: Deploy PostgreSQL
Create a `postgres-configurations.yaml` file to deploy the PostgreSQL database. This file should include the PersistentVolumeClaim (PVC - request storage resources from Kubernetes), Deployment (Defines the PostgreSQL database container), and Service (exposes the PostgreSQL container within the cluster for internal communication) configurations for PostgreSQL. Apply the configurations using:

```bash
kubectl apply -f postgres-configurations.yaml
```

We deploy PostgreSQL first because the Spring Boot application depends on the database being available.

### Step 7: Deploy Spring Boot App
Create a `expenses-configurations.yaml` file to deploy the Spring Boot application. This file should include the Deployment and Service configurations for the Spring Boot app. Apply the configurations using:

```bash
kubectl apply -f expenses-configurations.yaml
```

### Step 8: Check the status of the pods
Verify the status of the pods to ensure that both PostgreSQL and the Spring Boot application are running correctly:

```bash
kubectl get pods
```

### Step 9: Verify Deployment
To verify that the Spring Boot app is running correctly inside the Kubernetes cluster, expose the service using Minikube:

```bash
minikube service expenses-service
```

This command will open the service in our default web browser, allowing us to check the application's status.
