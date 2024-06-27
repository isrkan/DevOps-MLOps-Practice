# Docker Commands Guide

This repository contains a list of essential Docker commands to help you get started and manage Docker containers effectively. 

##### Checking Docker version
This command checks the currently installed version of Docker.

```
docker --version
```

##### Pulling an image from Docker hub
This command downloads an image from Docker Hub to the local machine.

```
docker pull <image_name>
```

##### Running a container
This command creates and starts a new container from the specified image. If the image is not available locally, Docker will automatically pull it from Docker Hub.

```
docker run <image_name>
```

To specify a particular version of an image, use the tag feature. Tags are used to version control images.
```
docker run <image_name>:<tag>
```

Options:
* `-d`: Run container in background and print container ID, For example, `docker run -d <image_name>`
* `-p`: Publish a container’s port to the host, allowing external access to the application running inside the container. For example, `docker run -p <host_port>:<container_port> <image_name>`
* `-it`: Run the container in interactive mode with a TTY (terminal). This allows to interact with the container's command line. For example, `docker run -it <image_name> /bin/bash`
* `-v`: Binds a volume to the container, allowing data to persist beyond the container's lifecycle. Useful for sharing data between the host and the container or between containers. For example, `docker run -v <path_on_host>:<path_on_container> <image_name>`

### Container management
Docker containers are lightweight, portable, and self-sufficient units that run software.

##### Listing running containers
This command lists all currently running containers.

```
docker ps
```

##### Listing all containers
This command lists all containers, including those that are stopped.

```
docker ps -a
```

##### Starting a container
This command starts a stopped container.

```
docker start <container_id>
```

##### Stopping a Container
This command stops a running container.

```
docker stop <container_id>
```

##### Removing a container
This command deletes a container. Note that the container must be stopped before it can be removed.

```
docker rm <container_id>
```

##### Inspecting a container
This command allows to view detailed information about a Docker container or image and will display it as a JSON output.

```
docker inspect <container_id>
```

##### Viewing container logs
This command shows the logs from a specific container.

```
docker logs <container_id>
```

#### Executing commands in a running container
The `docker exec` command allows to run commands inside a running container. This is useful for debugging or modifying the state of a running container.

Examples:

1. Running a simple command inside a running container: Here, the command lists the contents of the /app directory inside the specified container.
```
docker exec <container_id> ls /app
```

2. Accessing a running container's shell: The command opens an interactive bash shell inside the specified container, allowing to run multiple commands.
```
docker exec -it <container_id> /bin/bash
``` 

3. Checking the status of a process inside the container: The command lists all running processes inside the specified container, similar to the `ps aux` command on a typical Linux system.
```
docker exec <container_id> ps aux
```


### Image management
Docker images are templates used to create containers. They contain the application code, runtime, libraries, and everything needed to run an application.

##### Listing Docker images
This command lists all Docker images that are stored locally on the machine.

```
docker images
```

##### Removing an image
This command deletes a specific image from the local Docker storage. The image ID can be found using the `docker images` command. Before removing an image, ensure no containers are running or using this image.

```
docker rmi <image_id>
```

##### Building an Image from Dockerfile
This command builds a new Docker image from a Dockerfile located in the current directory. The `-t` option tags the image with a name. `.` specifies the build context, which is the current directory in this case. The Dockerfile should be present in this directory.

```
docker build -t <image_name> .
```

### Network management
Docker networks enable communication between containers.

##### Listing Docker networks
This command lists all Docker networks that are currently defined on the local machine.

```
docker network ls
```

##### Creating a network
This command creates a new Docker network with the specified name.

```
docker network create <network_name>
```

##### Connecting a container to a network
This command connects an existing container to a specified network.

```
docker network connect <network_name> <container_id>
```

##### Disconnecting a container from a network
This command disconnects a container from a specified network.

```
docker network disconnect <network_name> <container_id>
```

### Volume management
Docker volumes provide persistent storage for containers.

##### Listing Docker volumes
This command lists all Docker volumes that are currently defined on the local machine.

```
docker volume ls
```

##### Creating a volume
This command creates a new Docker volume with the specified name.

```
docker volume create <volume_name>
```

##### Removing a volume
This command deletes a specific Docker volume. Note that the volume must not be in use by any containers.

```
docker volume rm <volume_name>
```

### Docker Compose
Docker Compose is a tool that allows to define and run multi-container Docker applications.

##### Starting services
This command starts up all services defined in a `docker-compose.yml` file.

```
docker-compose up
```

Options:

* -d: Run services in the background

##### Stopping services
This command stops all running services defined in a `docker-compose.yml` file.

```
docker-compose down
```

##### Building or rebuilding services
This command builds or rebuilds the services defined in a `docker-compose.yml` file.

```
docker-compose build
```

##### Viewing Compose project logs
This command displays the logs for all services defined in a `docker-compose.yml` file.

```
docker-compose logs
```

### Docker Swarm
Docker Swarm is Docker's native clustering and orchestration tool. It allows to create and manage a cluster of Docker nodes, and deploy services across these nodes. This ensures high availability, load balancing, and scalability.

##### Initializing a Swarm
This command initializes a new Swarm cluster. The machine where this command is run becomes the Swarm manager.

```
docker swarm init
```

##### Joining a node to Swarm
This command adds a new node to an existing Swarm cluster. We need to provide the token and the manager node's IP address and port.

```
docker swarm join --token <token> <manager_ip>:<port>
```

##### Listing nodes in the Swarm
This command lists all nodes that are part of the Swarm cluster, including their status and roles.

```
docker node ls
```

##### Deploying a stack in Swarm
This command deploys a stack (a collection of services) to the Swarm cluster using a Compose file.

```
docker stack deploy -c <compose_file> <stack_name>
```

##### Removing a stack from Swarm
This command removes a stack and all associated services from the Swarm cluster.

```
docker stack rm <stack_name>
```