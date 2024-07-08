# Kubernetes Commands Guide

This repository contains a list of essential Kubernetes commands to help you get started and manage Kubernetes clusters effectively.

### Using with Minikube
Minikube is a tool that allows to run Kubernetes locally. It creates a single-node Kubernetes cluster on the local machine, which is perfect for development and testing.

##### Starting Minikube
This command starts a local Minikube cluster. It will download the necessary Kubernetes components and create a virtual machine (VM) to run the cluster.

```
minikube start
```

##### Viewing the status of Minikube
To see the status of the cluster, including whether it’s running and details about the nodes:

```
minikube status
```

##### Stopping Minikube
This command stops the Minikube cluster but keeps the VM and all resources intact. It’s useful for temporarily halting work without losing the cluster’s state.

```
minikube stop
```

##### Deleting Minikube
This command deletes the Minikube cluster and removes all associated resources, including the VM. Use this to completely reset Minikube.

```
minikube delete
```

##### Viewing Minikube dashboard
Minikube comes with a built-in Kubernetes dashboard, which provides a web-based user interface to manage our cluster. This command opens the dashboard in a web browser.

```
minikube dashboard
```

##### Pointing kubectl to Minikube
After starting Minikube, we may need to configure kubectl to use Minikube’s context to manage our cluster.

```
kubectl config use-context minikube
```

##### Accessing services within Minikube
Minikube provides a way to access services running in our cluster through a URL. Use the following command to get the URL for a service:

```
minikube service <service-name>
```

This will open the web browser to the service URL provided by Minikube.

## Kubernetes commands

### Cluster information
Kubernetes clusters consist of master and worker nodes. The master node controls the cluster, managing the worker nodes and the workloads running on them. Worker nodes run the applications in containers managed by Kubernetes.

##### Checking cluster info
This command provides basic information about the Kubernetes cluster, such as the addresses of the Kubernetes API server. It tells us about the master and worker nodes and where essential services are running.

```
kubectl cluster-info
```

##### Listing nodes in the cluster
Nodes are the individual machines (physical or virtual) that make up a Kubernetes cluster. Each node can host one or more pods, which are the smallest deployable units in Kubernetes. This command lists all nodes in the Kubernetes cluster, showing their status (e.g., Ready, NotReady), roles (e.g., master or worker), and other critical details.

```
kubectl get nodes
```

### Pod management

Pods are the smallest units of work in Kubernetes, encapsulating one or more containers. Pods share the same network namespace, and they can communicate with each other using localhost.

##### Listing all pods
This command lists all pods in the default namespace.

```
kubectl get pods
```

To list pods in a specific namespace, use the `-n` flag:

```
kubectl get pods -n <namespace>
```

##### Describing a pod
This command provides detailed information about a specific pod, including its configuration, status, events, and resource usage.

```
kubectl describe pod <pod_name>
```

##### Viewing pod logs
This command shows the logs of a specific pod.

```
kubectl logs <pod_name>
```

To view logs of a specific container within a pod, use `-c <container_name>`.

##### Creating a pod from a YAML file
Kubernetes uses YAML files to define the desired state of resources like pods. This command creates a pod using the configuration defined in a YAML file.

```
kubectl apply -f <file.yaml>
```

##### Running a pod using kubectl run
This command runs a new pod based on the specified container image. It is often used for quickly deploying a single pod for testing purposes.

```
kubectl run <pod_name> --image=<container_image>
```

##### Deleting a pod
This command deletes a specific pod. It removes the specified pod from the cluster, stopping and cleaning up any associated resources.

```
kubectl delete pod <pod_name>
```

### Service management

Services are Kubernetes objects that provide stable endpoints to access a set of pods. They abstract the networking and load balancing aspects, making it easy to expose applications to other pods or external users.

##### Listing all services
This command lists all services in the default namespace.

```
kubectl get svc
```

##### Describing a service
This command provides detailed information about a specific service, including its endpoints, ports, and selector.

```
kubectl describe svc <service_name>
```

##### Creating a service from a YAML file
This command creates a service using the configuration defined in a YAML file.

```
kubectl apply -f <file.yaml>
```

##### Exposing a deployment as a service
This command exposes a deployment, replica set, or pod as a new Kubernetes service. It creates a service resource to make the application accessible within or outside the cluster.

```
kubectl expose deployment <deployment_name> --type=<service_type> --port=<port>
```

##### Deleting a service
This command deletes a specific service.

```
kubectl delete svc <service_name>
```

### Deployment management

Deployments are Kubernetes objects that manage the deployment and scaling of sets of pods. They ensure that a specified number of replicas of a pod are running at all times.

##### Listing all deployments
This command lists all deployments in the default namespace.

```
kubectl get deployments
```

##### Creating a deployment from a YAML file
This command creates a deployment using the configuration defined in a YAML file.

```
kubectl apply -f <file.yaml>
```

##### Scaling a deployment
This command scales a deployment to a specified number of replicas, ensuring the desired number of pod replicas are running.

```
kubectl scale deployment <deployment_name> --replicas=<number_of_replicas>
```

##### Replacing a deployment
This command replaces the current configuration of a deployment with a new one defined in a YAML file. It's useful for updating the deployment configuration.

```
kubectl replace -f <file.yaml>
```

##### Deleting a deployment
This command deletes a specific deployment.

```
kubectl delete deployment <deployment_name>
```

##### Managing deployment rollouts
The `kubectl rollout` commands help manage the rollout of new versions of applications.

- **Check rollout status**:
  This command checks the status of a deployment rollout. It shows if the deployment has completed, or if it's still in progress.

```
kubectl rollout status deployment/<deployment_name>
```

- **Undo a rollout**:
This command rolls back a deployment to a previous version. It's useful if a new version has issues.

```
kubectl rollout undo deployment/<deployment_name>
```

- **Pause a rollout**:
This command pauses the rollout of a deployment. It's useful if we want to temporarily stop the deployment of new updates.

```
kubectl rollout pause deployment/<deployment_name>
```

- **Resume a rollout**:
This command resumes a paused deployment rollout. It continues the deployment of updates after a pause.

```
kubectl rollout resume deployment/<deployment_name>
```

### Namespace management

Namespaces are a way to divide cluster resources between multiple users or teams. They provide a scope for names, helping to avoid name collisions and allowing for resource segregation.

##### Listing all namespaces
This command lists all namespaces in the Kubernetes cluster.

```
kubectl get namespaces
```

##### Creating a namespace
This command creates a new namespace.

```
kubectl create namespace <namespace_name>
```

##### Deleting a namespace
This command deletes a specific namespace.

```
kubectl delete namespace <namespace_name>
```

### Ingress management

Ingress is a Kubernetes resource that manages external access to services within a cluster, typically HTTP. It provides load balancing, SSL termination, and name-based virtual hosting.

##### Listing all Ingress resources
This command lists all Ingress resources in the default namespace.

```
kubectl get ingress
```

##### Describing an Ingress resource
This command provides detailed information about a specific Ingress resource.

```
kubectl describe ingress <ingress_name>
```

##### Creating an Ingress resource from a YAML file
This command creates an Ingress resource using the configuration defined in a YAML file.

```
kubectl apply -f <file.yaml>
```

##### Deleting an Ingress resource
This command deletes a specific Ingress resource.

```
kubectl delete ingress <ingress_name>
```

### General management

##### Replacing a resource from a YAML file
This command updates an existing resource using the configuration defined in a YAML file. It is useful for modifying the properties of existing resources.

```
kubectl replace -f <file.yaml>
```

##### Listing all resources
This command lists all resources in the default namespace, including pods, services, deployments, and more.

```
kubectl get all
```