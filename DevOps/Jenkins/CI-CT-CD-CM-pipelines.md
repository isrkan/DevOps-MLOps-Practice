### Understanding CI/CT/CD/CM pipelines in data science

In traditional software development, **CI/CD pipelines** are well-defined processes used to automate code integration, testing, and deployment. However, in **data science**, where ML models are developed and deployed, the pipeline often expands to include additional steps such as **model training** and **monitoring**. This extended pipeline is commonly referred to as **CI/CT/CD/CM**, where:

- **CI** (Continuous integration): Ensure that the ML code (data pipelines, model training scripts) is functional and correct.
- **CT** (Continuous training): Automatically retrain the model when new data is available.
- **CD** (Continuous deployment): Deploy the trained model to production, making it available for inference.
- **CM** (Continuous monitoring): Continuously monitor the model's performance and data quality in production.

Let's break down each of these stages in the context of **data science pipelines**.

### Continuous integration (CI)
In data science, **CI** still involves automating the process of integrating code changes into a shared repository. However, it focuses on ML-specific tasks like data preprocessing, feature engineering, and ensuring that the code for model training and evaluation is functioning as expected.
- **Code versioning**: Just like in software development, data science projects use Git or other version control systems to manage model code, configuration files, and data pipelines.
- **Testing**: CI for ML models includes running unit tests on the code, checking the correctness of data pipelines and data quality (data integrity tests), and testing model training scripts to ensure the system behaves as expected.


### Continuous training (CT)
**Continuous training (CT)** is unique to ML pipelines. In this stage, the model is retrained periodically or automatically when new data is available. This is important because the performance of an ML model depends on how well it adapts to changing data distributions or new trends, commonly referred to as **data drift**.
- **Automated retraining**: When new data arrives, the pipeline triggers the model training process using the latest data. This ensures the model stays up-to-date and relevant.
- **Model validation**: The newly trained model is validated using a test dataset to ensure that it meets predefined performance metrics.
- **Versioning models**: Each trained model is versioned so that we can track performance over time and roll back to a previous version if necessary.


### Continuous deployment (CD)
Once the model is trained and validated, it needs to be deployed to a production environment where it can be used for inference or predictions. This stage is similar to CD in software pipelines, but instead of deploying an application, it deploys the trained machine learning model.
- **Model packaging**: The trained model is packaged, often as a Docker container or serialized format (e.g., TensorFlow SavedModel, PyTorch `.pt` file). For example, the trained model can be deployed as a microservice. The model is wrapped inside a microservice, which is a small, independent application that can be managed and scaled easily. This microservice allows the model to be run on its own and be accessed by other applications.
- **Deployment to production**: The model is deployed to a production environment, where it can serve real-time predictions or batch inference tasks. For example, the microservice is set up to handle requests for predictions via an API. This means other systems can send data to the model (via the API), and the model will instantly return predictions.
- **Inference pipeline**: The production pipeline may also include additional stages such as loading the model, pre-processing input data, and sending the prediction results to downstream systems.


### Continuous monitoring (CM)
After the model is deployed, continuous monitoring ensures that the model continues to perform as expected in production. This step is essential because an ML model's performance can degrade over time due to data drift, changes in user behavior, or system performance issues.
- **Monitoring model performance**: Track metrics such as accuracy, precision, recall, and latency to ensure the model continues to perform well on live data.
- **Detecting data drift**: Continuously monitor the input data to detect shifts or anomalies in the data distribution that could cause the model's predictions to become unreliable.
- **Alerting**: Set up alerts to notify the team if the model's performance drops below a certain threshold.
- **Trigger retraining**: If a significant drop in performance is detected, the pipeline can trigger the **continuous training** (CT) stage to retrain the model with newer data.


### Example of CI/CT/CD/CM pipeline
Here’s a high-level example of how a CI/CT/CD/CM pipeline might look for an ML model using Jenkins, with options for using Kubeflow or a non-Kubeflow approach:

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Starting CI stage...'
                git url: 'https://github.com/username/my-ml-project.git'
            }
        }

        stage('Continuous Integration - Testing ML Code') {
            steps {
                bat 'pytest tests/' // Run unit tests for ML code
            }
        }

        stage('Continuous Training - Train the Model') {
            steps {
                // Trigger model training - This script can be designed to pull the latest data, preprocess it, and train the model
                echo 'Starting CT stage...'
                // Option 1: Non-Kubeflow pipeline for training
                bat 'python train_model.py'  // Trigger model training script directly
                
                // Option 2: Kubeflow pipeline for training
                bat 'kubectl apply -f kubeflow-training-pipeline.yml' // This YAML defines the Kubeflow training pipeline
            }
        }

        stage('Validate Model Performance') {
            steps {
                // Option 1: Non-Kubeflow validation
                bat 'python validate_model.py' // Validate model performance
                
                // Option 2: Kubeflow validation pipeline
                bat 'kubectl apply -f kubeflow-validation-pipeline.yml' // Kubeflow validation step
            }
        }

        stage('Package and Deploy Model') {
            steps {
                echo 'Starting CD stage...'
                // Option 1: Non-Kubeflow deployment
                bat 'docker build -t my-ml-model:latest .' // Package model into Docker image
                bat 'docker push my-ml-model:latest' // Push image to Docker Hub
                bat 'kubectl apply -f deployment.yml' // Deploy to Kubernetes cluster
                
                // Option 2: Deploy the trained model using Kubeflow KFServing
                bat 'kubectl apply -f kfserving-model-deployment.yml' // This YAML defines the KFServing deployment
            }
        }

        stage('Continuous Monitoring') {
            steps {
                echo 'Starting CM stage...'
                // Option 1: Non-Kubeflow monitoring - Export metrics (like accuracy, latency) from the model serving service for Prometheus
                bat 'python export_metrics.py --model-service-url http://my-ml-model-service:8080 --prometheus-endpoint /metrics'

                // Option 2: Kubeflow KFServing monitoring - Configure Prometheus and Grafana to monitor the model deployed with KFServing
                bat 'kubectl apply -f kfserving-monitoring-config.yml' // This YAML Set up KFServing monitoring with Prometheus
            }
        }
    }

    post {
        always {
            echo 'ML pipeline completed'
        }
    }
}
```

This pipeline provides two options for each stage: one without **Kubeflow** and one using **Kubeflow** for a Kubernetes-native, ML-specific workflow. The non-Kubeflow pipeline is simpler but manual, using Python scripts for training, validation, deployment, and monitoring. The Kubeflow pipeline automates complex tasks like distributed training, hyperparameter tuning, and deployment with Kubernetes-native tools like Kubeflow Pipelines and KFServing. We can choose between the two approaches based on our project’s scale, complexity, and infrastructure requirements.

1. **Continuous integration (CI)**: Both approaches use **Jenkins** for **code checkout** and **unit testing**.
   - The non-Kubeflow pipeline uses standard unit tests (e.g., `pytest`), while in Kubeflow, unit tests can be included as part of Kubeflow Pipelines, but Jenkins handles it here.
2. **Continuous training (CT)**:
   - **Non-Kubeflow approach**: Directly triggers the `train_model.py` script to pull the latest data, preprocess, and train the model.
   - **Kubeflow approach**: Uses **Kubeflow pipelines** to manage the training process. The YAML configuration (e.g., `kubeflow-training-pipeline.yml`) defines steps for data preprocessing, model training, and hyperparameter tuning in a Kubernetes-native environment, offering scalability and easier management of training jobs.
3. **Validation**: 
   - **Non-Kubeflow approach**: Runs a separate Python script (`validate_model.py`) to validate the trained model’s performance (e.g., accuracy, F1 score).
   - **Kubeflow approach**: Validation is handled within the **Kubeflow pipelines**, automating both training and validation within the same workflow.
4. **Continuous deployment (CD)**:
   - **Non-Kubeflow approach**: Packages the model as a Docker container, pushes it to Docker Hub, and deploys it to a Kubernetes cluster using a Kubernetes deployment configuration (`deployment.yml`)
   - **Kubeflow approach**: Uses **KFServing** (now part of **KServe**) to deploy the model as a scalable, versioned service in Kubernetes. This method automates deployments, supports model autoscaling, and handles traffic management for model versions.
5. **Continuous monitoring (CM)**:
   - **Non-Kubeflow approach**: A custom Python script (`export_metrics.py`) collects model performance metrics (e.g., accuracy, latency) and exports them to **Prometheus**.
   - **Kubeflow approach**: **KFServing Model Monitoring** integrates with **Prometheus** and **Grafana** to collect detailed model performance metrics and monitor for **data drift**, **latency issues**, and **outliers**. This provides real-time alerts and monitoring dashboards for better oversight.