# Packaging an ML Model: Step-by-Step Guide

This guide provides step-by-step instructions to package a machine learning model for deployment and distribution. The goal is to create a Python package that includes all the necessary components for training, evaluating, and predicting with our model.

## Step 1: Develop the model in a Jupyter Notebook
Start by developing the machine learning model in a Jupyter notebook. This is where we will experiment with different models, preprocess the data, and evaluate the performance. This directory is for initial exploration and development. Perform the following steps in the notebook:
  - Data loading: Load the dataset.
  - EDA: Explore the data to understand its characteristics, identify patterns, and uncover potential insights.
  - Data preprocessing: Clean and preprocess the data (e.g., handle missing values, encode categorical variables).
  - Feature engineering: Create new features if necessary.
  - Model selection: Choose the machine learning models to experiment with.
  - Model Training: Train the models on the dataset.
  - Model Evaluation: Evaluate the performance using metrics like accuracy, precision, recall, etc.
  - Feature Importance: Analyze feature importance if applicable.

Ensure all code cells are well-documented with explanations and comments.

## Step 2: Structure the package
Once the notebook is complete and we have a working model, the next step is to organize the code into a Python package. This involves creating Python scripts for different components of the project and organizing them into a directory structure.

Here's a general directory structure for packaging an ML model:

```plaintext
my_package/               # Main project directory
├── notebooks/            # Optional: Store exploratory analysis notebooks
│   └── model_exploration.ipynb
├── my_package/           # The core package directory containing all the functional modules
│   ├── __init__.py
│   ├── config/           # Configuration files (e.g., model parameters, MLflow settings)
│   │   └── config.py
│   ├── data/             # Data loading and preprocessing
│   ├── features/         # Feature engineering
│   ├── models/           # Model definition, training, evaluation, and prediction
│   ├── visualization/
│   ├── utils/            # Utility functions (e.g., logging, custom helpers)
│   ├── MainObject.py     # The main object or class that initialize configuration
│   └── pipeline.py       # Pipeline to run the entire process end-to-end
├── tests/                # Unit tests for the code
├── mlflow_experiments/   # Optional: MLflow project to track experiments
├── scripts/              # Optional: Scripts for command-line interface
├── requirements.txt      # Lists project dependencies
├── setup.py              # Configuration file for package installation
├── MANIFEST.in           # Specifying files to include in the package distribution
├── README.md             # Project documentation
├── CHANGELOG.md          # Optional: Changelog for package updates
└── .gitignore            # Specifying files to exclude from version control
```

### 2.1 Create the project structure
We can quickly set up this directory structure using command-line commands, which will provide a starting point for the package structure. The structure presented here is a boilerplate, and we may need to adjust it based on the specific needs of our package. Adjust paths and file names as needed and replace `my_package` with the actual name of the package throughout this process.

1. **Navigate to the desired directory** where we want to create the project:
   ```bash
   cd /path/to/the/directory
   ```

2. **Create the main project directory**:
   ```bash
   mkdir my_package
   cd my_package
   ```

3. **Create the subdirectories** inside the `my_package` directory:
   ```bash
   mkdir -p notebooks my_package/config my_package/data my_package/features my_package/models my_package/visualization my_package/utils tests mlflow_experiments scripts
   ```

4. **Create `__init__.py` files** in the appropriate directories:
   ```bash
   touch my_package/__init__.py
   touch my_package/config/__init__.py
   touch my_package/data/__init__.py
   touch my_package/features/__init__.py
   touch my_package/models/__init__.py
   touch my_package/visualization/__init__.py
   touch my_package/utils/__init__.py
   touch tests/__init__.py
   ```

   By placing an `__init__.py` file within a directory, we transform that directory into a Python package. This allows us to import modules and functions from that directory using dot notation.

   Additionally, in `my_package/__init__.py`, we should add the version of the package. For example:
   ```python
   __version__ = "0.1.0"
   ```

   Including it allows us to easily access the package version programmatically:
   ```python
   import my_package
   print(my_package.__version__)
   ```

5. **Create placeholders for other important files**:
   ```bash
   touch my_package/MainObject.py
   touch my_package/pipeline.py
   touch my_package/config/config.py
   touch scripts/run_pipeline.py
   touch setup.py
   touch MANIFEST.in
   touch README.md
   touch CHANGELOG.md
   touch .gitignore
   ```

6. **Move the Jupyter notebook** from step 1 to the `notebooks` directory

This will set up the basic structure of the project. Remember, this is just a boilerplate structure, and it can be modified based on the specific requirements of our project. For instance, if we don’t need a command-line interface, we can omit the `scripts/` directory. Similarly, if our project doesn’t require any configuration files, the `config/` directory might not be necessary.

As we build our package, we can add or remove directories, files, and modules as needed. The key is to maintain a clear and organized structure that makes it easy for others (or us in the future) to understand and work with the code.

##### Using Cookiecutter Data Science
Another option for setting up a project structure is to use Cookiecutter Data Science (CCDS). CCDS is a tool for setting up a data science package template, which is a bit different from the structure we outlined here but can be adjusted to fit our needs. To use Cookiecutter Data Science, follow these steps:
1. **Install CCDS** using `pip`:
   ```bash
   pip install cookiecutter-data-science
   ```
2. **Start a new project** by running:
   ```bash
   ccds
   ```

CCDS will guide us through a series of prompts to set up the project structure according to a predefined template. This template is well-suited for data science projects, and it includes many best practices for reproducibility, collaboration, and deployment.

### 2.2 Create Python modules
After setting up the directory structure, the next step is to move the code from our notebook into separate Python modules within the `my_package/` directory. This makes the code modular, reusable, and easier to maintain.

##### Explanation of the modules:
The structure and content of these modules are just a starting point. Depending on our project’s needs, we might need to add more functions, split some of these modules further, or even merge them.

- **`config/`**: Manage configuration settings for the package. This could include file paths, model parameters, MLflow configurations or other settings that need to be configurable.
  - `config.py`: Code to load and handle configurations.
  - YAML or JSON files : Store default and custom configurations for easy modification without changing the code.
  
- **`data/`**: Handle data loading, preprocessing, and splitting.
  - `load_data.py`: Code for loading the dataset from various sources.
  - `preprocess.py`: Preprocessing steps (e.g., handling missing values).
  - `split_data.py`: Logic for splitting the dataset into training, validation, and test sets.
  
- **`features/`**: Feature engineering.
  - `build_features.py`: Code for feature engineering, creating new features, or selecting important features.

- **`models/`**: Model definition, training, evaluation, and prediction.
  - `define_models.py`: Define the machine learning models used in the project.
  - `train_model.py`: Train the models on the dataset.
  - `evaluate_model.py`: Evaluate the model's performance using appropriate metrics.
  - `predict_model.py`: Make predictions using the trained models.
  - `feature_importance.py`: Analyze and visualize feature importance if applicable.
  - `model_serialization.py`: Save and load trained models, ensuring they can be reused later.
  - `load_saved_model.py`: Load previously trained models for making predictions without retraining them each time.
  - `predict_via_api.py`: Make predictions by sending data to a model served via an MLflow REST API, allowing for predictions from a deployed model without needing to load it locally.

- **`visualization/`**: Visualization tools.
  - `visualize.py`: Functions to create visualizations that help with data analysis and model interpretation.

- **`utils/`**: Utility functions for miscellaneous tasks that support the main codebase.
  - `logging.py`: Set up logging to track the execution of different parts of the package.

- **`MainObject.py`**: Main module to initialize the main object or class to manage configurations.
- **`pipeline.py`**: Orchestrates the entire pipeline from data loading to prediction.

### 2.3 Create command-line scripts (Optional)
The `scripts/` directory is an optional to the package. It contains Python scripts that provide command-line functionality, allowing users to interact with our package directly from the terminal. This can be particularly useful for automating tasks, running pipelines, or providing a simple interface for end-users who may not want to interact with the package programmatically and can run complex processes with a single command. CLI scripts can be easily integrated into automation pipelines, such as CI/CD workflows, cron jobs, or other scheduling systems.

We can set up a basic CLI script in `.py` files using Python's `argparse` library to handle command-line arguments. The scripts to include will depend on the specific needs of our project and the features of our package. Here are some examples of scripts that might be useful:

- `run_pipeline.py`: A script to run the entire ML pipeline, from data loading to model prediction. This script is useful for end-to-end execution, where users can specify input data and configuration files, and the script handles the rest, including training the model and saving the results.
- `run_train.py`: A script focused on training the model. Use this script when we want to train the model separately, perhaps with different configurations or datasets. This is particularly useful for hyperparameter tuning or training on new data.

To test the CLI script, use:
```bash
python scripts/script_file.py <command-line arguments>
```

## Step 3: Create unit tests
Unit testing is essential to ensure that each component of the package works as expected. By writing tests, we can catch errors early and validate that our code behaves correctly under different conditions.
Unit testing focuses on testing individual components or functions in isolation to ensure they work correctly. Each test should cover a small unit of functionality, such as a single function or method.

- **Create test cases** in the `tests/` directory for key components of our package: The test files mentioned below are examples of test cases that we might want to include and that we can modify based on our project’s needs.
  - `test_preprocess.py`: Test the preprocessing steps applied to the data, such as handling missing values, encoding categorical variables, or normalizing features. We want to ensure that the preprocessing functions handle edge cases (e.g., missing all values in a column), perform expected transformations, and do not introduce errors.
  - `test_build_features.py`: Test the feature engineering logic. We want to ensure that new features are created correctly, that feature selection processes select the correct features, and that the engineered features have the expected properties.
  - `test_split_data.py`: Test data splitting logic. We want to ensure that the split ratio is correct, that no data is lost during splitting, and that each subset has the expected properties (e.g., the correct number of samples, the distribution of classes).
  - `test_define_models.py`: Test model definitions. We want to ensure that models are defined with the correct parameters, and verify that they can be instantiated without errors. We can also check if the models are compatible with the training data.
  - `test_train_model.py`: Test the training process. We want to ensure that models can be trained on the dataset without errors, that they converge (i.e., achieve a reasonable performance metric), and that the training process updates model parameters as expected.
  - `test_feature_importance.py`: Test feature importance calculations. We want to ensure that the feature importance scores are computed correctly, and ensure that the most important features are ranked as expected.
  - `test_predict_model.py`: Test prediction functionality. We want to ensure that the model can make predictions on new data, that the output is in the expected format, and that predictions are reasonable based on the input data.

To create these tests we can use a testing framework like `pytest`. To run our tests, navigate to the project’s root directory and use:
```bash
pytest tests/
```

This command will automatically discover and run all the test files within the `tests/` directory, providing a summary of the test results.
- If all tests pass, our code is functioning as expected for the scenarios covered by the tests.
- If any tests fail, the test report will show which tests failed and why, helping us quickly identify and fix issues.

To ensure that different parts of our package code work together smoothly, we can erite integration tests in addition.

## Step 4: Create a requirements file
A requirements file (typically named `requirements.txt`) lists all the external Python packages and their specific versions that our project depends on. This file is essential for ensuring that our project can be easily installed and run on different environments.

To create a requirements file, run the following command in the root directory:
```bash
pip freeze > requirements.txt
```

## Step 5: Create MLflow project (Optional)
After completing the initial model development in a Jupyter notebook and packaging the code into a Python package, the next step is to set up a directory for MLflow experiments. This directory is for formal experiment tracking and model management. This step is optional but highly recommended for systematic experiment tracking, model management, and ensuring reproducibility.

MLflow allows us to track experiments, log parameters, metrics, and artifacts, and manage different versions of models systematically. By separating MLflow experiments from the Jupyter notebooks, you maintain a clean and organized project structure. The notebooks serve as documentation and references for your initial explorations, while the MLflow setup is used for ongoing experiment management, fine-tuning, and deployment-ready model handling.

#### MLflow project structure
The MLflow experiments directory will have a specific structure that allows MLflow to track experiments, run them in different environments, and maintain reproducibility. Below is the general structure:
```plaintext
mlflow_experiments/           # MLflow project directory
├── MLproject                 # MLflow project file (mandatory)
├── conda.yaml                # Environment file for dependencies (optional but recommended)
├── pipeline.py               # Main Python script that executes the ML code and logs experiments
└── README.md                 # Project overview, setup instructions, and how to run it
```

- `MLproject`is the core file that defines the MLflow project. This file is mandatory and specifies the entry points for our code, the environment to run it in, and other essential configuration details.
- `conda.yaml` defines the environment, including all dependencies required to run the ML code.
- `pipeline.py` executes the entire ML pipeline, from data loading to model training and evaluation. It logs parameters, metrics, and artifacts for each experiment, allowing us to track what was done in each run.
- `README.md` provides an overview of the MLflow project, including setup instructions and guidance on how to run the experiments.

#### Setting up a conda environment for MLflow
To ensure that our MLflow experiments run smoothly, it's crucial to set up a Conda environment within the `mlflow_experiments` directory. It is often more convenient and reliable to use a Conda environment when working with MLflow projects. Conda makes it easier to install and manage dependencies, especially those that require specific system libraries or have complex dependencies. Also, MLflow supports Conda environments natively, allowing us to specify the environment directly in our MLflow project configuration. This environment will include all the necessary dependencies required for our project.
1. Navigate to the `mlflow_experiments` directory, create a new Conda environment and activate it:
```bash
cd mlflow_experiments
conda create -n my_conda_package_env python=3.9
conda activate my_conda_package_env
```
2. Install all the libraries listed in the `requirements.txt file`, which was created in Step 4:
```bash
pip install -r ../requirements.txt
```
3. Next, install MLflow within the Conda environment:
```bash
pip install mlflow
```
4. Now, generate the `conda.yaml` file, which will specify the environment configuration for MLflow:
```bash
conda env export --no-builds > conda.yaml
```

#### Conducting experiments and model management
After we created the MLflow project in this step, we will:
1. **Run multiple experiments**: Use `pipeline.py` to execute different experiments by varying models, hyperparameters, or data preprocessing techniques.
2. **Track experiments**: MLflow will log all relevant details such as parameters, metrics, and output files, which allows for easy comparison and analysis.
3. **Register the best models**: Based on the tracked results, decide which models to register in MLflow’s model registry for potential deployment.
4. **Decide on model serving**: From the registered models, choose the best-performing one to serve in a production environment.

#### Serving the model
Once we have identified the best model version from our registered models, we can serve it using MLflow's model serving capabilities. This allows us to deploy the model for production use, making it accessible via a REST API. To serve a specific version of the registered model, run the following command:
```bash
mlflow models serve -m "models:/<MODEL_NAME>/<VERSION_NUMBER>" --port <PORT_NUMBER> --env-manager conda
```

Replace `<MODEL_NAME>`, `<VERSION_NUMBER>`, and `<PORT_NUMBER>` with the appropriate values. This command starts a REST API endpoint for our model, allowing us to make predictions by sending data to the API.

## Step 6: Create the setup file
To package our project for distribution, we need a `setup.py` file. It serves as the build script for `setuptools`, which is the standard tool used to package and distribute Python projects. This script will define the metadata about our package and provides instructions to `setuptools` on how to install and distribute our package. This file guides `pip` (which is a package installer for Python) in creating a distributable package format (e.g., `.whl` file).
The setup file is essential for several reasons:
- It allows our package to be easily distributed and installed by others. 
- It specifies the dependencies our package requires, ensuring that all necessary libraries are installed when our package is installed.
- It handles the versioning of our package, which is important for managing updates and maintaining compatibility with other packages.
- It defines entry points for our package, such as command-line interfaces, making it easier for users to interact with our package.

Create a Python file named `setup.py` in the root directory and use the `setup.py` file in this directory as an example. Adjust the arguments with the specific information and dependencies.
- Before setting the Python version requirement in the file, we should know which version of Python our package is compatible with. We can check the Python version we are using by running the following command in our terminal:
```bash
python --version
```

## Step 7: Include additional files

#### 7.1 Include the `MANIFEST.in` file 
The `MANIFEST.in` file is used to specify which additional files should be included in our package distribution that `setuptools` might not automatically pick up. This can include configuration files (e.g., YAML config files), documentation, data files, and any other non-code files necessary for our package to function correctly. 

##### Common Commands in `MANIFEST.in`
Here are some useful commands to control file inclusion:

- **`include`**: Add specific files.
  ```plaintext
  include MyPackage/config/*.yaml
  ```
- **`exclude`**: Remove specific files.
  ```plaintext
  exclude MyPackage/tests/*
  ```
- **`recursive-include`**: Add all files in a directory that match a pattern.
  ```plaintext
  recursive-include MyPackage/data *.csv
  ```
- **`recursive-exclude`**: Remove files in a directory that match a pattern.
  ```plaintext
  recursive-exclude MyPackage/tmp *.tmp
  ```
- **`graft`**: Add all files in a directory.
  ```plaintext
  graft MyPackage/docs
  ```
- **`prune`**: Exclude all files in a directory.
  ```plaintext
  prune MyPackage/tmp
  ```

##### Example
To include all YAML configuration files from the `config` directory and exclude test files, our `MANIFEST.in` might look like this:
```plaintext
include MyPackage/config/*.yaml
exclude MyPackage/tests/*
```

#### 7.2 Create `.gitignore` file
A `.gitignore` file is used for managing our version control system. It specifies which files and directories should be ignored by Git. This is crucial for preventing unnecessary files (such as temporary files, build artifacts, and sensitive information) from being tracked and included in our version control history.

#### 7.3 Create `CHANGELOG.md` file
The `CHANGELOG.md` file is used to document each change made to the package and is useful when debugging issues or upgrading to a new version. It records new features, bug fixes, and other modifications, along with the corresponding version numbers and dates. For example:

```markdown
# Changelog

## [1.0.1] - 2024-08-15
### Fixed
- Fixed bug that caused crashes when the user did A.

## [1.0.0] - 2024-08-01
### Added
- Initial release of `MyPackage`.
```

#### 7.4 Create a README file
A `README.md` file explains how to use our package and provides an overview of the project and serves as the primary documentation for users and developers. It should include
- Project title: The name of our project.
- Description: A brief summary of what our package does and why it’s useful.
- Installation instructions: Step-by-step instructions on how to install the package, including any dependencies.
- Configuration: Instructions on how to configure the package, including any optional settings.
- Usage examples: Code snippets and examples that demonstrate how to use the package.
- Features: A list of key features provided by the package.
- Contributing: Guidelines for contributing to the project, if applicable.


## Step 8: Install and test the package
After organizing the code into a package, install the package locally to ensure everything works as expected. 

1. **Create source and built distributions**: Before installing the package, we need to create source and built distributions. These distributions are the standard way to package Python code for distribution, which are more modern and flexible formats compared to the older "egg" format. Here's a brief explanation:
  - **Source distribution (`sdist`)**: This is a distribution format that includes the package's source code, typically compressed into a `.tar.gz` file. It is useful for sharing our code in a way that others can build and install it on their systems.
  - **Built distribution (`bdist_wheel`)**: This is a pre-built binary distribution, usually a `.whl` (wheel) file. It's a ready-to-install package that users can install without needing to build the package from source. Wheel is the preferred format for distributing Python packages because it's faster and easier to install.

  To create these distributions, run the following commands in the root directory of the project (where the `setup.py` file is located):
  ```bash
  python setup.py sdist bdist_wheel
  ```

  This command will generate two directories:
  - **`build/`**: This directory contains temporary files generated during the build process. These files are used to compile and prepare the package for distribution. It is not needed for installing the package and can be safely ignored or deleted after the build is complete and the distribution files are generated.
  - **`dist/`**: This directory contains the distribution files that we actually need. These are the files we distribute or upload to package repositories like PyPI. It includes:
    - A `.tar.gz` file for the source distribution.
    - A `.whl` file for the built distribution.

2. **Install the package locally** - Now that we have created the distributions, we can install the package locally using the `pip` command. By running the following command in the root directory of the project, `pip` will install the package along with all its dependencies specified in requirements.txt:
  ```bash
  pip install dist/our_package_name-0.1.0-py3-none-any.whl
  ```

  Replace `our_package_name-0.1.0-py3-none-any.whl` with the actual name of the wheel file generated in the previous step.

  This command installs the package locally on the system, allowing us to use it as if it were installed from PyPI. This is particularly useful for testing before distributing the package.

  In some cases, it might be more convenient to use the `-e` option with `pip` install, like so:
  ```bash
  pip install -e .
  ```

  The `-e` option stands for "editable." When we install a package with `pip install -e .`, it creates a link between the package directory and our Python environment. This means that any changes we make to the package code are immediately reflected without the need to reinstall the package. Use this option when we are actively developing the package. It allows us to modify the code and test it in real-time without repeatedly reinstalling the package.

2. **Test the package** - Once installed, we should test the package by either running command-line scripts or importing it in a Python script.

## Step 9: Push the project to a Git repository
After testing the package locally, the next step is to push the project to a Git repository. This allows others to access our code and makes it easier to share, collaborate, and deploy.

Then, to install the package directly from our GitHub repository, we can use the following command:
```bash
pip install git+https://github.com/username/repository_name.git#subdirectory=subdirectory_path
```

## Step 10: Versioning and Changelog
Maintaining version control and documenting changes is crucial as the package evolves. This helps both users and developers understand what has changed between versions.

1. Update `setup.py` - Update the `version` in `setup.py` according to Semantic Versioning guidelines for managing version numbers. Semantic Versioning uses a three-part version number:
    - **MAJOR** version (`1.0.0` -> `2.0.0`): Increment this when making incompatible API changes, such as removing or changing the behavior of existing methods in a way that will break existing users' code.
    - **MINOR** version (`1.0.0` -> `1.1.0`): Increment this when adding new features or functionality in a backward-compatible manner. Existing functionality should not break, but new features can be added.
    - **PATCH** version (`1.0.0` -> `1.0.1`): Increment this when making backward-compatible bug fixes. This does not add new features or change existing features in any way that might break users' code.


2. Keep track of changes in a `CHANGELOG.md` file. It provides a historical record of the package’s evolution, detailing what was added, changed, or fixed in each version.

Every time we release a new version, update this file with:
    - **Version number** (e.g., `1.1.0`).
    - **Release date** (e.g., `2024-08-20`).
    - **Change type**: Describe the changes under appropriate headings (`Added`, `Changed`, `Fixed`, `Removed`).