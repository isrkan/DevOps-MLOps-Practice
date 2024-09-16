# Understanding CI/CD pipelines
In this guide, we will break down how CI (continuous integration) and CD (continuous delivery/deployment) work in a Jenkins pipeline. 

### Continuous integration (CI)
**CI** involves automating the process of integrating code changes into a shared repository. Jenkins pipelines typically handle this by **building** and **testing** code every time there’s a change.

CI typically covers:
- **Checkout**: Pulls the latest code from the repository.
- **Build**: Compiles the code and prepares it for testing or deployment.
- **Test**: Runs unit tests, integration tests, or static code analysis.

The aim is to ensure that every change pushed to the repository is automatically tested and verified before further action.

#### Example of CI pipeline
Below is a CI pipeline using Windows commands (`bat`) instead of Unix-based commands (`sh`), which will run on a Windows-based Jenkins agent.
```groovy
pipeline {
    agent any // Run on any available agent

    stages {
        stage('Checkout') { // Pulls code from GitHub repository
            steps {
                git url: 'https://github.com/username/my-repo.git'
            }
        }

        stage('Build') { // Compiles the code
            steps {
                bat 'mvn clean install' // Build using Maven
            }
        }

        stage('Test') { // Runs tests to verify the build
            steps {
                bat 'mvn test' // Run unit tests
            }
        }
    }

    post {
        always {
            echo 'CI process completed!' // Notification of completion
        }
    }
}
```

In this example:
- **Checkout**: Pulls the latest code from the repository using the `git` command.
- **Build**: Compiles the application with `mvn clean install` (Maven command for Java projects).
- **Test**: Runs the tests using `mvn test`. Tests can include unit, integration, or functional tests.

### Continuous delivery (CD) vs. continuous deployment (CD)

Continuous delivery and continuous deployment are related, but they have key differences:
- **Continuous delivery** ensures the application is always **ready for deployment** after the CI process, but the actual deployment itself is manual. The pipeline stops before deployment, allowing a human decision on when to deploy. For example, the app might be deployed to a staging environment for final testing and manual approval. A **staging environment** is a replica of the production environment, but it's not customer-facing. It allows us to test the application in a production-like setting before deploying it to the actual production environment. This is the final safety net before production. Any issues found in staging are addressed before the application is deployed to users.
- **Continuous deployment** takes this further and **automatically deploys** changes to production if all tests pass, removing any manual steps.

#### Example of a CD pipeline (continuous delivery)
A delivery pipeline could include packaging the application into a Docker image, deploying it to a staging environment for further testing, and ensuring it's ready for production. Continuous delivery can include also pushing Docker images to a container registry like Docker Hub.
```groovy
pipeline {
    agent any // Can run on any available agent

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/username/my-java-app.git'
            }
        }

        stage('Build') {
            steps {
                bat 'mvn clean install' // Build using Maven
            }
        }

        stage('Test') {
            steps {
                bat 'mvn test' // Run tests using Maven
            }
        }

        stage('Package as Docker Image') {
            steps {
                script {
                    bat 'docker build -t username/my-java-app:latest .' // Build Docker image
                    bat 'docker tag username/my-java-app:latest username/my-java-app:${env.BUILD_NUMBER}' // Tag the image with the build number
                    bat 'docker push username/my-java-app:latest' // Push image to Docker Hub
                    bat 'docker push username/my-java-app:${env.BUILD_NUMBER}' // Push tagged image
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                echo 'Deploying to staging environment...'
                bat 'docker-compose -f docker-compose.staging.yml up -d' // Deploying using Docker Compose on Staging
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed and ready for manual production deployment!'
        }
    }
}
```

In this example:
- **CI stages**: `Build` and `Test` stages handle the code build and testing.
- **CD (delivery) stage**:
    - **Package as docker image**: Packages the app into a Docker image, tags it with the latest version, and pushes it to **Docker Hub**.
    - **Deploy to staging**: Deploys the application to a **staging environment** using Docker Compose. The deployment to **production** remains manual (handled separately). This allows for manual testing before the production release. The `docker-compose.staging.yml` file is used here to define the configuration specific to the staging environment, such as database settings or environment variables that differ from production.

#### Example of a CD pipeline (continuous deployment)
This pipeline includes the same CI steps but also deploys to production once the tests pass.
```groovy
pipeline {
    agent any // Can run on any available agent

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/username/my-java-app.git'
            }
        }

        stage('Build') {
            steps {
                bat 'mvn clean install' // Compile Java app using Maven
            }
        }

        stage('Test') {
            steps {
                bat 'mvn test' // Run tests
            }
        }

        stage('Package as Docker Image') {
            steps {
                script {
                    bat 'docker build -t username/my-java-app:latest .' // Build Docker image
                    bat 'docker tag username/my-java-app:latest username/my-java-app:${env.BUILD_NUMBER}' // Tag the image with the build number
                    bat 'docker push username/my-java-app:latest' // Push image to Docker Hub
                    bat 'docker push username/my-java-app:${env.BUILD_NUMBER}' // Push tagged image
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                echo 'Deploying to production environment...'
                bat 'docker-compose -f docker-compose.prod.yml up -d' // Deploy to production using Docker Compose
            }
        }
    }

    post {
        always {
            echo 'Application deployed to production!'
        }
    }
}
```

- **CI stages**: Includes `Build` and `Test` stages.
- **CD (deployment) stage**: Automatically deploys to production once the tests pass.
    - **Package as docker image**: The pipeline builds and pushes a Docker image to Docker Hub, just like in Continuous Delivery.
    - **Deploy to production**: After packaging, the application is automatically deployed to **production** using Docker Compose.