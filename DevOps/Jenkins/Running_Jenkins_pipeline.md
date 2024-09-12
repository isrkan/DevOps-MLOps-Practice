# Running Jenkins pipeline

This guide explains how to set up and run the Jenkins pipeline for building and running a web application from a Github repository.

### Prerequisites:
- **Jenkins installed**: Jenkins is already installed and running on our Windows machine.
- **Build tools installed**: 
  - **For Spring Boot**: Ensure that **Maven** is installed and configured.
  - **For Django, Flask, FastAPI**: Ensure **Python** (with **pip**) is installed.
- **Git installed**: Git should be installed and added to the system's PATH.

### Steps to configure and run the Jenkins pipeline

#### Step 1: Create a `Jenkinsfile`
1. In the project root directory, create a new file named `Jenkinsfile`.
2. Example `Jenkinsfile` structure:
    ```groovy
    pipeline {
        agent any

        stages {
            stage('Checkout') {
                steps {
                    git branch: 'main', url: 'https://github.com/username/MyRepository.git'
                }
            }

            stage('Build') {
                steps {
                    script {
                        // Framework-specific build commands here
                    }
                }
            }

            stage('Run') {
                steps {
                    script {
                        // Framework-specific run commands here
                    }
                }
            }
        }

        post {
            always {
                echo 'Pipeline completed!'
            }
        }
    }
    ```
3. Push the `Jenkinsfile` to the GitHub repository.

#### Step 2: Create a new Jenkins job
1. Open the Jenkins dashboard.
2. Click on **New Item** in the Jenkins dashboard.
3. Enter a name for our job, for example, `WebApp-Pipeline`.
4. Select **Pipeline** as the project type, then click **OK**.

#### Step 3: Configure pipeline script from SCM:
1. In the pipeline configuration, scroll down to the **Pipeline** section.
2. For **Definition**, select **Pipeline script from SCM** from the dropdown.
3. Under the **SCM** field, select **Git**.
4. In the **Repository URL** field, enter the URL of your Git repository. For example:
    ```
    https://github.com/username/MyRepository.git
    ```
5. Add credentials (if necessary): If the Git repository is private, we will need to provide access credentials:
     - Click **Add** next to the **Credentials** field.
     - Select **Username with password** or **SSH Private Key** (depending on how our Git repository is secured).
     - Fill in the necessary details (e.g., GitHub username, personal access token or password, etc.), then click **Add**.
6. In the **Branch Specifier** (Branch to build) field, enter the branch we want Jenkins to track. If we are using the `main` branch, enter:
    ```
    main
    ```
7. Specify the path to the Jenkinsfile: In the **Script Path** field, specify the relative path to the `Jenkinsfile` in the repository.
     ```
     path/to/file/Jenkinsfile
     ```
8. Scroll down and click **Apply** and **Save** to save the pipeline configuration

#### Step 4: Running the pipeline
1. Navigate to the newly created job in Jenkins.
2. Click **Build Now** from the job’s dashboard to trigger the job manually.
3. Jenkins will start executing the pipeline as defined in the `Jenkinsfile`.

#### Step 5: Monitor the build process
- The build progress can be monitored by clicking on the job's **Build History** and selecting the running build.
- View the console output to track the stages, including `Checkout`, `Build`, and `Run`.

#### Step 6: Check the running application
Once the `Run` stage completes, our application should be running on `localhost`. we can check it by navigating to `http://localhost:<port>` (using the port specified in the application).