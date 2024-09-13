# Jenkins Guide
Jenkins is an open-source automation server that helps automate parts of software development related to building, testing, and deploying, facilitating continuous integration (CI) and continuous delivery (CD). It is highly extensible with a large ecosystem of plugins, making it adaptable to various workflows, including those in data science, backend development, and machine learning.
- **Automate repetitive tasks**: Jenkins can run tests, build projects, deploy applications, and even run data science pipelines, freeing up time for more critical work.
- **Continuous integration and continuous delivery (CI/CD)**: Jenkins makes it easy to implement CI/CD practices, ensuring code quality and speeding up the development cycle.

### Starting Jenkins
To start Jenkins manually on Windows:
1. Open the `Command Prompt` as administrator
2. Start Jenkins by executing:
    ```bash
    net start jenkins
    ```
    
    This command tells Windows to start the Jenkins service. We should see a message confirming that the Jenkins service is starting.
3. Access the Jenkins UI by navigating to `http://localhost:8080` in the web browser. If Jenkins is on a different port, check the `jenkins.xml` file in `C:\Program Files\Jenkins` for the `--httpPort` setting.


## Jenkins terminology
- **Jobs** are the fundamental unit of work in Jenkins. A job could be as simple as running a script or as complex as deploying a machine learning model. For data scientists, a job might involve running a data processing script, training a model, or performing data validation. Backend developers might use jobs to build, test, and deploy applications.
- **Pipelines** in Jenkins define a series of steps or stages that our job will go through. They are written in Jenkins' domain-specific language (DSL) and can be used to automate complex workflows. Jenkins Pipeline DSL is built on top of Groovy, allowing users to define jobs and workflows using Groovy syntax.
- **Nodes** are machines that Jenkins runs jobs on. The primary machine running Jenkins is called the **Master Node**, and additional machines that we configure Jenkins to use are called **Agent Nodes**.
- **Agents** are the programs that run on Nodes to execute Jenkins jobs. They can run on any machine that we configure Jenkins to use, making it possible to distribute work across multiple systems.
- **Workspace** is a directory on a node where Jenkins performs its builds. Each job has its own workspace where it stores its files during a build process.


## Setting up a Jenkins job
1. **Create a new job:** Go to Jenkins dashboard, click on **New Item** and enter a name for the job, select **Freestyle project**, and click **OK**.
2. **Configure the job:**
   - In the **General** section, provide a description for the job.
   - In the **Source Code Management** section, link the version control system (e.g., Git).
   - In the **Build Triggers** section, define when the job should run (e.g., after a commit or at a specific time).
   - In the **Build** section, define the steps Jenkins should take (e.g., run a script, compile code, etc.).
3. **Save and run the job:** Click **Save** to finish setting up the job. Then, click **Build Now** to run the job immediately.


## Creating Jenkins pipelines
Jenkins pipelines provide a way to define complex job sequences using code.

#### Declarative vs. scripted pipelines
- **Declarative pipelines**: Easier to write and maintain, with a more structured and simple syntax. Recommended for most users.
- **Scripted pipelines**: More flexible but more complex. Useful for advanced use cases requiring finer control.

#### Pipeline stages and steps
A pipeline consists of stages, each representing a distinct part of the process (e.g., Build, Test, Deploy). Each stage contains steps, which are the specific actions Jenkins performs.

#### Using pipeline syntax
Here's a basic example of a declarative pipeline:
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                // Add build commands here
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                // Add test commands here
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // Add deploy commands here
            }
        }
    }
}
```

This simple pipeline includes three stages: build, test, and deploy.


## Integrating Jenkins with development workflow
- **Version control integration (GitHub)** - Jenkins integrates seamlessly with version control systems like GitHub. We can configure Jenkins to automatically trigger jobs whenever there is a new commit or pull request.
- **Building and testing code** - For backend developers, Jenkins can compile our code, run tests, and report results. Data scientists and ML engineers can use Jenkins to automate testing of their scripts or models.
- **Deploying applications** - Once our application or model is ready, Jenkins can automate its deployment to a staging or production environment. This could include deploying a web application, a machine learning model, or even a data pipeline.
- **Automating data science workflows** - Jenkins can be used to automate various parts of a data science workflow, such as data ingestion and preprocessing, model training and evaluation, and deployment of models into production environments.


## Monitoring and managing Jenkins
- **Viewing build history and logs**:
    - **Build history**: Accessible from the job page, showing past builds, their status, and related logs.
    - **Logs**: Each build has a log that details the steps Jenkins took, useful for troubleshooting.
- **Setting up notifications**: Jenkins can be configured to send build notifications to email or Slack channels.
- **Managing Jenkins nodes and agents**:
    - **Nodes**: Go to **Manage Jenkins** > **Manage Nodes** to add or remove nodes.
    - **Agents**: Jenkins agents can be managed through the Nodes page, allowing us to scale our builds across multiple machines.

## Jenkinsfile
A Jenkinsfile is a text file that contains the definition of a Jenkins Pipeline and is stored in the source code repository. This allows us to define build, test, and deployment workflows as code, which is known as pipeline as code. The main advantage of using a Jenkinsfile is that it enables version control of the CI/CD pipeline, making it easier to track changes, review, and collaborate on automation processes.
- **Code as configuration**: The CI/CD pipeline is stored as code, making it easier to manage, track, and review using a version control system like Git along with the application code.
- **Pipeline as code**: By defining pipelines in a Jenkinsfile, we ensure that our build, test, and deployment processes are reproducible and can be automated.
- **Consistency**: Having a Jenkinsfile ensures consistent deployment processes across different environments (e.g., development, staging, production).


## Best practices for Jenkins
- **Use pipelines**: Prefer pipelines over freestyle jobs for better scalability and maintenance.
- **Keep jobs simple**: Break complex jobs into smaller, reusable parts.
- **Backup Jenkins**: Regularly back up the Jenkins configuration and job data.
- **Monitor resources**: Keep an eye on resource usage, especially if running Jenkins on the same machine as other services.
- **Logs**: Always check Jenkins logs when encountering issues.


Happy automating!