# Iris Classification Experiment

This MLflow project demonstrates how to manage and run an experiment for classifying iris flowers using a RandomForestClassifier. It is intended as an example to explore the use of MLflow projects. The project includes an `MLproject` file for defining the project structure, a `conda.yaml` file for managing dependencies, and a `main.py` script for executing the experiment.

## Project structure
- **`MLproject`**: Defines the MLflow project configuration, including entry points and parameters. The main entry point (`main`) takes the parameters `learning_rate` (float, default: 0.01) and `epochs` (int, default: 10).
- **`conda.yaml`**: Specifies the environment and dependencies needed to run the project.
- **`main.py`**: The main script that trains a RandomForestClassifier on the Iris dataset and logs the results.

This project serves as an example to explore the use of MLflow projects. We can update the files to suit our specific needs.

## Prerequisites
- **MLflow**: Ensure to have MLflow installed. We can install it via pip:
  ```bash
  pip install mlflow
  ```
- **Conda**: Conda is used for managing the environment specified in `conda.yaml`.

## Clone the project
If we have the project in a repository, clone it to the local machine:
```bash
git clone <repository_url>
cd <repository_directory>
```

## Running the project
To run the MLflow project, follow these steps:

1. **Start the MLflow tracking server (Optional):**
   If we want to use a local MLflow tracking server to store experiment results, start it with:
   ```bash
   mlflow server --backend-store-uri <backend_store_uri> --default-artifact-root <artifact_root>
   ```
   Replace `<backend_store_uri>` and `<artifact_root>` with appropriate values. We can view our experiment runs and their details by navigating to the MLflow Tracking UI, typically accessible at `http://127.0.0.1:5000`.

2. **Run the MLflow project:**
   We have two options for running the project:

   **Option 1: Using the MLflow CLI**
   Execute the project using the MLflow CLI. We can specify parameters such as `learning_rate` and `epochs`. For example:
   ```bash
   mlflow run . --experiment-name <experiment_name> -P learning_rate=0.01 -P epochs=10
   ```
   Replace `<experiment_name>` with the desired experiment name.

   **Option 2: Using the MLflow API**
   Alternatively, we can run the project using a Python script (e.g., `run.py`). This is useful if we want more control or need to integrate the run into a larger application. Run the script from the command line:
   ```bash
   python run.py
   ```
   This script will execute the project with the specified parameters and log the results to the specified experiment.