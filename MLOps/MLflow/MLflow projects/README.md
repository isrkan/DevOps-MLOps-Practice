# MLflow projects

MLflow projects is a standard way to package and reproduce our machine learning code. It allows us to organize our code, dependencies, and configurations in a consistent format, making it easier to share and run experiments across different environments. Whether we are working alone or in a team, MLflow projects helps ensure that our code runs the same way on any machine.

When working on machine learning projects, we often need to:

- **Share our work**: Collaborators need to run our code on their machines without issues.
- **Reproduce experiments**: We should be able to run past experiments with the same code, data, and configurations to verify results.
- **Manage dependencies**: Machine learning projects often have specific versions of libraries and tools that need to be installed to ensure that the code works as expected.

MLflow Projects addresses these needs by providing a standardized way to package our code, making it easier to run and share.

## Getting started with MLflow projects

### Project structure

An MLflow project is a directory that contains our code and an `MLproject` file. Here’s how we should structure our project:

```
my_ml_project/
│
├── MLproject                 # MLflow project file (mandatory)
├── conda.yaml                # Environment file for dependencies (optional but recommended)
├── main.py                   # Main Python script that executes the ML code
└── README.md                 # Project overview, setup instructions, and how to run it
```

- Keep the code modular and organized within the project directory. Separate scripts, data, and configurations logically.

### The `MLproject` file
The `MLproject` file is the central configuration file of an MLflow project that defines how it should be run. It is a YAML file that defines the entry points for our project, dependencies, and other configurations.

Here’s an example of what it might look like:
```yaml
name: my_ml_project

conda_env: conda.yaml

entry_points:
  main:
    parameters:
      learning_rate: {type: float, default: 0.01}
      epochs: {type: int, default: 10}
    command: "python main.py --learning_rate {learning_rate} --epochs {epochs}"

  preprocess:
    command: "python preprocess.py --input_dir data/raw --output_dir data/processed"

  train:
    parameters:
      learning_rate: {type: float, default: 0.01}
      epochs: {type: int, default: 10}
    command: "python train.py --learning_rate {learning_rate} --epochs {epochs} --data_dir data/processed"
    
  evaluate:
    parameters:
      model_path: {type: str, default: "models/latest_model.pkl"}
      test_data_dir: {type: str, default: "data/test"}
    command: "python evaluate.py --model_path {model_path} --test_data_dir {test_data_dir}"
```

- **`name`**: The name of the project. The name should be unique and descriptive, making it easy to identify the project when managing multiple MLflow projects.
- **`conda_env`**: The path to the `conda.yaml` file that specifies the environment and dependencies.
- **`entry_points`**: Defines the entry points to run the project. Each entry point represents a different way to run our project, such as training a model, evaluating it, or running data preprocessing. It is possible and often useful to have multiple entry points in the `MLproject` file. Each entry point corresponds to a specific task or phase in our ML workflow. For example, we might have separate entry points for data preprocessing, model training, and model evaluation.

#### Defining parameters
Parameters in the `MLproject` file allow us to customize the behavior of each entry point without changing the code. Parameters can be defined with the following attributes:
- **`type`**: Specifies the type of the parameter (e.g., `int`, `float`, `str`, `bool`). This ensures that the correct data type is passed into the command.
- **`default`**: Sets a default value for the parameter. If the parameter is not provided when the entry point is invoked, the default value will be used.
- **`min` and `max`** (optional): We can define a minimum and maximum value for numeric parameters to enforce constraints.
- **`options`** (optional): For categorical parameters, We can specify a list of allowed options.

### Managing dependencies
To ensure that our project runs consistently across different environments, we should specify its dependencies. This is typically done using a `conda.yaml` file.

#### Creating the `conda.yaml` file
While we can manually write a `conda.yaml` file, it’s more reliable to generate it using the `conda env export` command. This ensures that all necessary dependencies and their versions are accurately captured.
1. **Set up the environment**: First, activate the conda environment that contains all the dependencies for our project.
   ```bash
   conda activate my_ml_project_env
   ```
2. **Export the environment**: Use the `conda env export` command to generate the `conda.yaml` file. This command will output a complete list of the environment’s packages, along with their versions.
   ```bash
   conda env export --no-builds > conda.yaml
   ```

   - The `--no-builds` flag omits build-specific details, making the environment file more portable across different platforms.
3. **Review and clean up**: After generating the `conda.yaml` file, review it to remove any unnecessary packages or dependencies that aren’t directly related to our project.

Here’s an example of a simplified `conda.yaml` file:
```yaml
name: my_ml_project_env
channels:
  - defaults
dependencies:
  - python=3.8
  - scikit-learn
  - pandas
  - pip
  - pip:
      - mlflow
```

- **`name`**: The name of the conda environment.
- **`channels`**: The conda channels to use for package installations.
- **`dependencies`**: List of packages and versions required by our project.

### Running an MLflow project
Once our project is set up, running it is straightforward using the MLflow CLI:
```bash
mlflow run . --experiment-name <experiment_name>
```

This command does the following:
- Creates and activates a conda environment as specified in `conda.yaml`.
- Runs the default entry point specified in the `MLproject` file.
- Specifies the name of the experiment (`<experiment_name>`) to which the run belongs. MLflow will create this experiment if it doesn’t already exist. Alternatively, we can use instead `--experiment-id <experiment_id>`.

#### Running with parameters
We can also pass parameters to the project such as:
```bash
mlflow run . -P learning_rate=0.001 -P epochs=20 --experiment-name <experiment_name>
```

#### Running specific entry points
By default, `mlflow run .` executes the `main` entry point defined in the `MLproject` file. If we want to run a different entry point, we need to specify it using the `-e` or `--entry-point` flag:
```bash
mlflow run . --entry-point <NAME> --experiment-name <experiment_name>
```
