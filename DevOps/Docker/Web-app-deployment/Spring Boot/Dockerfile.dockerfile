# Use an official OpenJDK runtime as a parent image for this Dockerfile
# It instructs Docker to pull the official OpenJDK image with version 17 that has been optimized for minimal size (slim variant)
FROM openjdk:17-jdk-slim

# Optional - Set metadata for the generated image
# This LABEL instruction adds information about the maintainer, version, and description of the image
LABEL maintainer="Your Name <your.email@example.com>"
LABEL version="1.0"
LABEL description="Docker image for a Spring Boot application"

# Optional - Set environment variables to configure the JVM options
# JAVA_OPTS allows us to set any JVM options (e.g., memory settings)
ENV JAVA_OPTS=""

# Set the working directory within the Docker container to '/app'. All subsequent commands will be executed in this directory
WORKDIR /app

# Copy the Spring Boot JAR file from the local host (the directory where the Docker build command is executed) to the container's working directory
# The JAR file should be generated using the "mvn package" or "gradle build" command
COPY target/my-spring-boot-app.jar app.jar

# It informs Docker that the container will listen on port 8080 at runtime
# This does not actually publish the port, but rather documents that the container listens on the specified port at runtime
EXPOSE 8080

# Define the default command to run when the container starts
# The JAVA_OPTS environment variable allows for additional JVM options to be passed
# The -jar option specifies that the application is packaged as an executable JAR file
# The "--spring.profiles.active=prod" option specifies the active Spring profile (e.g., production)
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar --spring.profiles.active=prod"]
# Another option to run the Spring Boot application is by directly executing the following:
# ENTRYPOINT ["java","-jar","/app.jar"]