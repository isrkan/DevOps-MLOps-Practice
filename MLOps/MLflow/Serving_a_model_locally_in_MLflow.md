# Deploying a model locally in MLflow

Once we have trained and logged a model in MLflow, the next step is often to deploy it so it can make predictions in real-time or in batch mode. MLflow provides simple tools for serving models locally through a REST API. Let’s walk through the two main ways to deploy models locally:

## Option 1: Deploying a model from a run
When we train a model using MLflow and log it as part of a run, the model is saved as an artifact in that run. We can deploy this model locally using MLflow’s built-in model serving features.

#### Steps to deploy a model from a run

1. **Find the run ID**: First, locate the run where the model was logged. We can do this through the MLflow UI by browsing through our experiments and runs or using the MLflow CLI:
   ```bash
   mlflow runs list --experiment-id <EXPERIMENT_ID>
   ```

   This command will show all the runs in a specific experiment. The `Run ID` is listed along with other details.

2. **Serve the model locally**: 
   Once we have the `Run ID`, we can serve the model using MLflow’s `models serve` command. We need to specify the run and the model path (typically `model` if logged using the standard naming convention).
   ```bash
   mlflow models serve -m "runs:/<RUN_ID>/model" --port <PORT_NUMBER> --env-manager <ENVIRONMENT_MANAGER>
   ```

   - **`-m`**: Specifies the model path, which is typically `runs:/<RUN_ID>/model` if the standard naming is used.
   - **`--port`**: Sets the port where the model will be served. By default, it’s `5000`, but we can set it to any available port.
   - **`--env-manager`**: Specifies how the environment (required dependencies) should be managed when serving the model. There are two main values it can take:
     - **`conda`**: This creates a Conda environment using the environment file that MLflow generated when the model was logged. This is common when models require specific packages.
     - **`virtualenv`**: If we prefer a Python `virtualenv` instead of Conda, use this option. It's another way to isolate our environment.
    
    Once the command runs, MLflow will start a local server where the model can be accessed.

## Option 2: Deploying a registered model from the model registry
In cases where the model is registered in the MLflow Model Registry, we can deploy a specific version of the registered model. This is especially useful when managing multiple versions of a model and promoting models to production.

#### Steps to deploy a registered model from the model registry

1. **Register the model**: Ensure that the model has been registered in the MLflow Model Registry. This can be done via the MLflow UI or the MLflow API:
   ```python
   mlflow.register_model(model_uri, name)
   ```
   After registering, the model will appear in the model registry with its own version history.

2. **Check model versions**: Use the MLflow Client to view the versions of a registered model. This helps to find the specific version we want to serve:
   ```python
   client.get_registered_model(model_name)
   ```

3. **Serve a specific version**: 
   After identifying the version, we can serve the registered model using the `models serve` command:
   ```bash
   mlflow models serve -m "models:/<MODEL_NAME>/<VERSION_NUMBER>" --port <PORT_NUMBER> --env-manager <ENVIRONMENT_MANAGER>
   ```
   - **`-m`**: Specifies the path to the registered model in the format `models:/<MODEL_NAME>/<VERSION_NUMBER>`.
   - **`--port`**: Sets the port where the model will be served.
   - **`--env-manager`**: Choose between `conda` and `virtualenv` to manage dependencies. The environment that was created (either Conda or Virtualenv) remains on our system after we abort the serving process.

---

## Check the server status
After serving the model, the MLflow scoring server exposes two key endpoints:
   - `/ping`: Used to check if the server is running. We can visit `http://127.0.0.1:<PORT_NUMBER>/ping` in your browser to ensure the server is alive.
   - `/invocations`: Used to send data for model predictions. The model will be available for prediction at `http://127.0.0.1:<PORT_NUMBER>/invocations`, and we can make predictions by sending POST requests to this URL.

---

## Example: Sending a request to the model
Once the model is served, we can make predictions by sending JSON data to the model’s REST API. Here's an example of what the input might look like if we are working with an Iris dataset:
```json
{
    "columns": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
    "data": [[5.1, 3.5, 1.4, 0.2]]
}
```

We can send a POST request using `Invoke-RestMethod` (when using PowerShell) or any tool that allows HTTP requests:
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:6500/invocations" `
  -ContentType "application/json" `
  -Body '{"dataframe_split": {"columns": ["sepal_length", "sepal_width", "petal_length", "petal_width"], "data": [[5.1, 3.5, 1.4, 0.2]]}}'
```

- **`Invoke-RestMethod`**: This is used to make REST API calls in PowerShell.
- **`-Method Post`**: Specifies the HTTP method.
- **`-Uri "http://127.0.0.1:6500/invocations"`**: The endpoint for the model’s invocations.
- **`-ContentType "application/json"`**: Specifies the content type as JSON.
- **`-Body`**: This is the actual data we are sending to the model. Supported input formats are `instances`, `inputs`, `dataframe_records`, or `dataframe_split`. In this case, we used `dataframe_split`. This is a format where `columns` and `data` are provided in a dictionary. The column names are passed as a list, and the feature values are also provided as a list of lists.

The model will return predictions in JSON format. PowerShell automatically parses JSON and displays the result in its native format, which often doesn't look like standard JSON. It converts lists and objects into table-like structures or custom output.