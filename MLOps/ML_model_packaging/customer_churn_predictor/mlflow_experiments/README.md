# Customer Churn Prediction Experiment

This MLflow project demonstrates how to manage and run an experiment for predicting customer churn using a machine learning model. It is designed as a practical example to explore the use of MLflow projects. The project includes an `MLproject` file for defining the project structure, a `conda.yaml` file for managing dependencies, and a `pipeline.py` script for executing the experiment.

## Project structure
- **`MLproject`**: Defines the MLflow project configuration, including entry points and parameters. The main entry point (`main`) takes the following parameters:
  - **`data_path`** (mandatory): The path to the dataset file. This is a required parameter as the model needs a dataset to train on.
  - **`test_size`**: (optional) The proportion of the dataset to include in the test split. Defaults to `0.2`.
  - **`random_state`**: (optional) The random seed used for splitting the data to ensure reproducibility. Defaults to `42`.
- **`conda.yaml`**: Specifies the environment and dependencies needed to run the project, ensuring reproducibility across different systems.
- **`pipeline.py`**: The main script that executes the customer churn prediction model, trains it on the dataset, and logs the results to MLflow.

## Prerequisites
- **MLflow**: Ensure to have MLflow installed. We can install it via pip:
  ```bash
  conda install mlflow
  ```
- **Conda**: Conda is used for managing the environment specified in `conda.yaml`.

## Clone the project
Clone the project repository to the local machine:
```bash
git clone --no-checkout https://github.com/isrkan/DevOps-MLOps-Practice.git
cd DevOps-MLOps-Practice
git sparse-checkout init --cone
git sparse-checkout set "MLOps/ML_model_packaging/customer_churn_predictor"
git fetch
git pull
git read-tree -mu HEAD
cd "MLOps/ML_model_packaging/customer_churn_predictor/mlflow_experiments"
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
   Execute the project using the MLflow CLI, specifying the required `data_path` parameter and optionally adjusting the `test_size` and `random_state` parameters. For example:
   ```bash
   mlflow run . --experiment-name <experiment_name> -P data_path=path/to/data.csv -P test_size=0.3 -P random_state=123
   ```
   Replace `<experiment_name>` with the desired experiment name.

3. **View run results in MLflow Tracking UI**