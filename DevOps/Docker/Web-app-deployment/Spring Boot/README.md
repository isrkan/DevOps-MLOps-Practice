# Deploying Spring Boot app with Docker

This guide provides step-by-step instructions to deploy a Spring Boot app using Docker. Docker allows us to package our application with all its dependencies into a standardized unit, called a container, ensuring consistency across different environments.

### Step 1: Prepare Spring Boot app
Before deploying the Spring Boot app with Docker, ensure that the Spring Boot application is properly configured and works locally.

### Step 2: Prepare application properties
Ensure that the `application.properties` file contains the necessary configurations for our application, such as database connection properties. We can use environment variables to make these configurations more flexible.

### Step 3: Prepare Dockerfile
Create a Dockerfile in the root directory of the Spring Boot application. This file specifies how to build the Docker image for the application.

### Step 4: Build the project with Maven
Before building the Docker image, ensure that the JAR file is generated in the target directory. Run the following command in the root directory of the project:

```bash
mvn clean install
```
This command does the following:
- `clean`: Removes any previous build outputs.
- `install`: Compiles the code, runs the tests (if not skipped), and packages the compiled code into a JAR file.
- DskipTests: Skips the execution of tests during the build process. This is useful when you want to quickly generate the JAR file without running tests.

### Step 5: Build docker image
Build the Docker image for the Spring Boot app using the following command:

```bash
docker build -t my-spring-boot-app:1.0 .
```

### Step 6: Run Docker container
Once the Docker image is built, run a Docker container using the following command:

```bash
docker run -p 8082:8081 my-spring-boot-app:1.0
```

This command maps port 8082 on the host to port 8081 on the container, allowing access to the Spring Boot app.
However, in our specific case, the expenses app relies on an SQL database (PostgreSQL), so it will not work without the database running. To manage both the application and the database together, we need Docker Compose.

### Step 7: Using Docker compose (for multi-container Docker applications)
Docker Compose allows us to define and run multi-container Docker applications. We will define and run the Docker containers in a YAML file to use Docker Compose. Create a `docker-compose.yaml` file. To start the Spring Boot app using Docker Compose, run the following command:

```bash
docker-compose up
```

This will start the Flask app container as defined in the `docker-compose.yaml` file.

### Step 8: Verify deployment
Visit http://localhost:8082 in the web browser to verify that the Spring Boot app is running correctly inside the Docker container.
