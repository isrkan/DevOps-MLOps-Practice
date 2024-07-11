# Use an official OpenJDK runtime as a parent image for this Dockerfile
# It instructs Docker to pull the official OpenJDK image with version 17 that has been optimized for minimal size (slim variant)
FROM openjdk:17-jdk-slim

# Optional - Set metadata for the generated image
LABEL version="1.0"
LABEL description="Docker image for a Spring Boot application of expenses management"

# Set the working directory within the Docker container. All subsequent commands will be executed in this directory
WORKDIR /expenses

# Copy the Spring Boot JAR file from the local host (the directory where the Docker build command is executed) to the container's working directory
COPY target/expenses-0.0.1-SNAPSHOT.jar /expenses-0.0.1-SNAPSHOT.jar

# Define the default command to run when the container starts
# The -jar option specifies that the application is packaged as an executable JAR file
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /expenses-0.0.1-SNAPSHOT.jar"]