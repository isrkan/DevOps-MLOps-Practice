# MLflow CLI Command Guide

This guide provides an overview of MLflow's CLI commands. The MLflow CLI allows us to interact with MLflow features directly from our terminal. The CLI is a convenient way to automate tasks, integrate MLflow into scripts, or quickly perform operations without writing additional code.

### Installing MLflow
Before using the MLflow CLI, ensure that MLflow is installed. We can install MLflow via pip:
```bash
pip install mlflow
```

Once installed, we can verify the installation and check the available commands by running:
```bash
mlflow --help
```

## General CLI syntax
The general syntax for an MLflow CLI command is as follows:
```bash
mlflow <command-group> <command> [options]
```
- **`mlflow`**: The base command to invoke MLflow.
- **`<command-group>`**: Specifies the area of functionality and it is related to a specific MLflow component, such as, `experiments`, `runs`, `models`, etc.
- **`<command>`**: Specifies the action to perform within the command group, such as `create`, `list`, `delete`, etc.
- **`[options]`**: Additional flags or arguments that modify the command's behavior.

For example, to create a new experiment, the command might look like:
```bash
mlflow experiments create --experiment-name my_experiment
```

We can get help for any command by appending `--help` to the command:
```bash
mlflow <command-group> <command> --help
```

This will display detailed information about the command's options and usage.

## Configuring MLflow tracking server
The MLflow Tracking Server stores experiment metadata, such as parameters, metrics, and artifacts. To start the tracking server:
```bash
mlflow server \
    --backend-store-uri <backend_store_uri> \
    --default-artifact-root <artifact_root> \
    --host <host> \
    --port <port>
```

- **`--backend-store-uri <PATH>`**: Specifies the URI of the backend store where experiment metadata (parameters, metrics, etc.) will be stored. This could be a local directory or a database connection string. For example:
  ```bash
  mlflow server --backend-store-uri sqlite:///mlflow.db
  ```
  This command sets up a SQLite database (`mlflow.db`) to store experiment data.
- **`--registry-store-uri <URI>`**: Specifies the URI for persisting registered models. If this is not provided, the `--backend-store-uri` will be used. This option is useful when we want to separate the storage of experiment data and model registry data.
- **`--default-artifact-root <URI>`**: Defines the default directory where artifacts (like model files) are stored. This is required for tracking servers that use a SQL database as the backend. For example:
  ```bash
  mlflow server --default-artifact-root s3://my-bucket/mlflow-artifacts
  ```
  This stores all artifacts in an S3 bucket.
- **`--host <HOST>`**: Sets the network address (hostname or IP address) to bind the server. The default is `127.0.0.1`, which restricts access to the local machine. To allow access from other machines, use `0.0.0.0`:
  ```bash
  mlflow server --host 0.0.0.0
  ```
  This binds the server to all network interfaces, allowing remote access.
- **`--port <PORT>`**: Specifies the port number on which the server will listen. The default is `5000`, but we can change it if needed:
  ```bash
  mlflow server --port 8080
  ```
  This runs the server on port `8080`. By default, we can access the server at `http://127.0.0.1:5000` if we do not mention the host and the port.
- **`--workers <WORKERS>`**: Defines the number of worker processes to handle requests. The default is `1`, but we can increase it for better performance in production environments:
  ```bash
  mlflow server --workers 4
  ```
  This command starts the server with 4 worker processes.
- **`--expose-prometheus <PATH>`**: Enables the Prometheus exporter to expose metrics at the `/metrics` endpoint. Metrics will be stored in the specified directory, which will be created if it does not exist:
  ```bash
  mlflow server --expose-prometheus /tmp/prometheus-metrics
  ```
  This allows us to monitor the server's performance using Prometheus.

## Starting MLflow UI
To start the MLflow UI:

```bash
mlflow ui \
    --backend-store-uri <backend_store_uri> \
    --default-artifact-root <artifact_root> \
    --host <host> \
    --port <port>
```

This command shares similar options with `mlflow server`:

- **`--backend-store-uri <PATH>`**: Specifies the backend store URI where the experiment data is stored. This option is identical to the one used in `mlflow server`.

- **`--default-artifact-root <URI>`**: Specifies the default directory where artifacts are stored. This option is included for consistency but isn't as crucial for `mlflow ui` since artifact serving is not a primary function.

- **`--host <HOST>`** and **`--port <PORT>`**: These options control where the UI is accessible, just like in `mlflow server`. For example:
  ```bash
  mlflow ui --host 0.0.0.0 --port 8080
  ```
  This command starts the MLflow UI, accessible from any machine on port `8080`.

### Difference Between `mlflow server` and `mlflow ui`
MLflow provides two main commands to manage and view experiment data: `mlflow server` and `mlflow ui`. 
- The `mlflow server` command starts a full-featured MLflow Tracking Server. This server handles not only the UI for viewing experiments and runs but also manages the entire backend, including logging new runs, storing artifacts, handling REST API requests, and managing model registry operations. We would use `mlflow server` when we want a centralized tracking server where multiple users and applications can log their experiments, manage artifacts, and interact with the MLflow REST API. This is typically used in production environments where experiments and models are managed across different teams or projects.
- The `mlflow ui` command starts only the MLflow user interface. It allows us to view the experiments, runs, metrics, parameters, and artifacts that have already been logged to the specified `backend-store-uri`. However, it does not handle new logging requests or manage REST API endpoints like the `mlflow server` does. we would use `mlflow ui` when we want a lightweight interface to view and explore the results of our experiments. This is often used in development or local testing environments where we simply want to review the outputs of our experiments without the need for a fully-featured server.

## Managing experiments with CLI
MLflow provides several commands to manage and interact with experiments. Experiments are used to organize and track runs, which represent iterations of a machine learning workflow.

### Create an experiment
To create a new experiment, use the `experiments create` command:
```bash
mlflow experiments create --experiment-name <experiment_name> [--artifact-location <artifact_path>]
```

- **`-n, --experiment-name <experiment_name>`**: The name of the experiment (required).
- **`-l, --artifact-location <artifact_path>`**: (Optional) Specifies the base location to store artifacts for the experiment. If not provided, the tracking server will choose a default location.

For example:
```bash
mlflow experiments create --experiment-name my_experiment
```

This command creates a new experiment named `my_experiment`.

### Delete an experiment
To delete an experiment, use the `experiments delete` command:
```bash
mlflow experiments delete --experiment-id <experiment_id>
```

- **`-x, --experiment-id <experiment_id>`**: The ID of the experiment to be deleted (required).

### Restore a deleted experiment
To restore a deleted experiment, use the `experiments restore` command:
```bash
mlflow experiments restore --experiment-id <experiment_id>
```

- **`-x, --experiment-id <experiment_id>`**: The ID of the experiment to restore (required).

### List experiments
To search for experiments in the tracking server, use the `experiments search` command:
```bash
mlflow experiments search [--view <view_type>]
```

- **`-v, --view <view_type>`**: (Optional) The view type for the search. Valid options are `active_only` (default), `deleted_only`, and `all`.

For example:
```bash
mlflow experiments search
```

This command displays all experiments, along with their IDs, names, and artifact locations.

### Rename an experiment
To rename an experiment, use the `experiments rename` command:
```bash
mlflow experiments rename --experiment-id <experiment_id> --new-name <new_name>
```

- **`-x, --experiment-id <experiment_id>`**: The ID of the experiment to rename (required).
- **`--new-name <new_name>`**: The new name for the experiment (required).


## Managing runs with CLI
MLflow provides several commands to manage and interact with runs. Runs are individual executions of a machine learning workflow and are used to track metrics, parameters, and artifacts for a specific experiment.

### List runs
To list all runs of a specified experiment, use the `runs list` command:
```bash
mlflow runs list --experiment-id <experiment_id> [--view <view_type>]
```

- **`--experiment-id <experiment_id>`**: The ID of the experiment whose runs we want to list (required).
- **`-v, --view <view_type>`**: (Optional) Specifies the view type for listing runs. Valid options are `active_only` (default), `deleted_only`, and `all`.

### Describe a run
To view the details of a specific run, use the `runs describe` command:
```bash
mlflow runs describe --run-id <run_id>
```

- **`--run-id <run_id>`**: The ID of the run to describe (required).

The details of the run will be printed in JSON format.

### Delete a run
To mark a run for deletion, use the `runs delete` command:
```bash
mlflow runs delete --run-id <run_id>
```

- **`--run-id <run_id>`**: The ID of the run to be deleted (required).

The command marks the run for deletion. The run can be restored later using the `restore` command.

### Restore a deleted run
To restore a previously deleted run, use the `runs restore` command:
```bash
mlflow runs restore --run-id <run_id>
```

- **`--run-id <run_id>`**: The ID of the run to restore (required).

This command restores the run, making it active again.


## Managing artifacts with CLI
MLflow provides commands to manage artifacts, which are files or directories associated with a specific run. These artifacts can be logged, listed, or downloaded as part of tracking a machine learning experiment.

### Log a single artifact
To log a single local file as an artifact of a run, use the `artifacts log-artifact` command:
```bash
mlflow artifacts log-artifact --local-file <local_file> --run-id <run_id> [--artifact-path <artifact_path>]
```

- **`-l, --local-file <local_file>`**: The path to the local file to log as an artifact (required).
- **`-r, --run-id <run_id>`**: The ID of the run in which to log the artifact (required).
- **`-a, --artifact-path <artifact_path>`**: (Optional) A subdirectory within the run's artifact directory where the file should be logged.

### Log multiple artifacts
To log all the files within a local directory as artifacts of a run, use the `artifacts log-artifacts` command:
```bash
mlflow artifacts log-artifacts --local-dir <local_dir> --run-id <run_id> [--artifact-path <artifact_path>]
```

- **`-l, --local-dir <local_dir>`**: The path to the local directory containing the files to log as artifacts (required).
- **`-r, --run-id <run_id>`**: The ID of the run in which to log the artifacts (required).
- **`-a, --artifact-path <artifact_path>`**: (Optional) A subdirectory within the run's artifact directory where the files should be logged.

### List artifacts
To list all artifacts under a run’s root artifact directory or a specific subdirectory, use the `artifacts list` command:
```bash
mlflow artifacts list --run-id <run_id> [--artifact-path <artifact_path>]
```

- **`-r, --run-id <run_id>`**: The ID of the run whose artifacts we want to list (required).
- **`-a, --artifact-path <artifact_path>`**: (Optional) The path relative to the run's root directory for which to list artifacts. If not specified, it lists all artifacts under the root directory.

The output will be a JSON-formatted list of the artifacts.

### Download artifacts
To download an artifact file or directory to a local directory, use the `artifacts download` command:
```bash
mlflow artifacts download [--run-id <run_id> --artifact-path <artifact_path>] [--artifact-uri <artifact_uri>] [--dst-path <dst_path>]
```

- **`-r, --run-id <run_id>`**: (Optional) The ID of the run from which to download the artifact.
- **`-a, --artifact-path <artifact_path>`**: (Optional) The path relative to the run’s root directory to download.
- **`-u, --artifact-uri <artifact_uri>`**: (Optional) URI pointing to the artifact file or directory. This can be used as an alternative to specifying `--run-id` and `--artifact-path`.
- **`-d, --dst-path <dst_path>`**: (Optional) The path to the local directory where the artifact should be downloaded. If not specified, a new uniquely-named directory will be created, unless the artifacts already exist locally, in which case their local path will be returned. 

This command downloads the specified artifacts to our local filesystem.

## Running an MLflow project
The `mlflow run` command is used to execute an MLflow project from a specified URI. The command allows us to manage and execute ML workflows with reproducibility and consistency. To run an MLflow project, use the following command:
```bash
mlflow run [OPTIONS] URI
```
- **`URI`**: The location of the MLflow project. This could be a path to a local directory, a Git repository, or another remote location. If the project is in a Git repository, MLflow will clone the repository and run the project in a new working directory.

#### Commonly used options
- **`--entry-point <NAME>`**: Specifies which entry point in the MLflow project to run. The default entry point is `main`. If the specified entry point is not found, MLflow attempts to execute the file with the specified name directly, using Python or a shell, depending on the file type. For example,
  ```bash
  mlflow run . --entry-point train
  ```
  This runs the `train` entry point defined in the `MLproject` file.
- **`--version <VERSION>`**: If the project is in a Git repository, this option specifies the version of the project to run, such as a specific branch, tag, or commit hash.
  ```bash
  mlflow run https://github.com/myproject.git --version main
  ```
  This runs the project from the `main` branch.
- **`-P, --param-list <NAME=VALUE>`**: Passes parameters to the entry point. These parameters are defined in the `MLproject` file. The `name=value` format specifies the parameter name and its value.
  ```bash
  mlflow run . -P parameter1=0.01 -P parameter1=20
  ```
- **`--experiment-name <experiment_name>`**: Specifies the name of the experiment under which to launch the run. If the experiment does not already exist, MLflow will create it.
  ```bash
  mlflow run . --experiment-name "My Experiment"
  ```
- **`--env-manager <env_manager>`**: Specifies the environment manager to use when running the project. Options include `local` (use the existing environment), `virtualenv`, and `conda`. If not specified, MLflow automatically selects the appropriate environment manager based on the project’s configuration.
  ```bash
  mlflow run . --env-manager conda
  ```