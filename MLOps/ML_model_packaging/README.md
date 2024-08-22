# Packaging an ML Model: Step-by-Step Guide

This guide provides step-by-step instructions to package a machine learning model for deployment and distribution. The goal is to create a Python package that includes all the necessary components for training, evaluating, and predicting with our model.

## Step 1: Develop the model in a Jupyter Notebook
Start by developing the machine learning model in a Jupyter notebook. This is where we will experiment with different models, preprocess the data, and evaluate the performance. Perform the following steps in the notebook:
  - Data loading: Load your dataset.
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
│   ├── config/           # Configuration files (e.g., model parameters)
│   │   └── config.py
│   ├── data/             # Data loading and preprocessing
│   ├── features/         # Feature engineering
│   ├── models/           # Model definition, training, evaluation, and prediction
│   ├── visualization/
│   ├── utils/            # Utility functions (e.g., logging, custom helpers)
│   ├── MainObject.py     # The main object or class that initialize configuration
│   └── pipeline.py       # Pipeline to run the entire process end-to-end
├── tests/                # Unit tests for the code
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
   cd /path/to/your/directory
   ```

2. **Create the main project directory**:
   ```bash
   mkdir my_package
   cd my_package
   ```

3. **Create the subdirectories** inside the `my_package` directory:
   ```bash
   mkdir -p notebooks my_package/config my_package/data my_package/features my_package/models my_package/visualization my_package/utils tests scripts
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

### 2.2 Create Python modules
After setting up the directory structure, the next step is to move the code from our notebook into separate Python modules within the `my_package/` directory. This makes the code modular, reusable, and easier to maintain.

##### Explanation of the modules:
The structure and content of these modules are just a starting point. Depending on our project’s needs, we might need to add more functions, split some of these modules further, or even merge them.

- **`config/`**: Manage configuration settings for the package. This could include file paths, model parameters, or other settings that need to be configurable.
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

- **`visualization/`**: Visualization tools.
  - `visualize.py`: Functions to create visualizations that help with data analysis and model interpretation.

- **`utils/`**: Utility functions for miscellaneous tasks that support the main codebase.
  - `logging.py`: Set up logging to track the execution of different parts of the package.

- **`MainObject.py`**: Main module to initialize the main object or class to manage configurations.
- **`pipeline.py`**: Orchestrates the entire pipeline from data loading to prediction.

### 2.3 Create command-line scripts (Optional)
The `scripts/` directory is an optional to the package. It contains Python scripts that provide command-line functionality, allowing users to interact with your package directly from the terminal. This can be particularly useful for automating tasks, running pipelines, or providing a simple interface for end-users who may not want to interact with the package programmatically and can run complex processes with a single command. CLI scripts can be easily integrated into automation pipelines, such as CI/CD workflows, cron jobs, or other scheduling systems.

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

## Step 5: Create the setup file
To package our project for distribution, we need a `setup.py` file. It serves as the build script for `setuptools`, which is the standard tool used to package and distribute Python projects. This script will define the metadata about our package and provides instructions to `setuptools` on how to install and distribute our package. This file guides `pip` (which is a package installer for Python) in creating a distributable package format (e.g., `.whl` file).
The setup file is essential for several reasons:
- It allows our package to be easily distributed and installed by others. 
- It specifies the dependencies our package requires, ensuring that all necessary libraries are installed when our package is installed.
- It handles the versioning of your package, which is important for managing updates and maintaining compatibility with other packages.
- It defines entry points for our package, such as command-line interfaces, making it easier for users to interact with our package.

Create a Python file named `setup.py` in the root directory and use the `setup.py` file in this directory as an example. Adjust the arguments with the specific information and dependencies.
- Before setting the Python version requirement in the file, we should know which version of Python our package is compatible with. We can check the Python version we are using by running the following command in your terminal:
```bash
python --version
```

## Step 6: Include additional files

#### 6.1 Include the `MANIFEST.in` file 
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
To include all YAML configuration files from the `config` directory and exclude test files, your `MANIFEST.in` might look like this:
```plaintext
include MyPackage/config/*.yaml
exclude MyPackage/tests/*
```

#### 6.2 Create `.gitignore` file
A `.gitignore` file is used for managing our version control system. It specifies which files and directories should be ignored by Git. This is crucial for preventing unnecessary files (such as temporary files, build artifacts, and sensitive information) from being tracked and included in our version control history.

#### 6.3 Create `CHANGELOG.md` file
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

#### 6.3 Create a README file
A `README.md` file explains how to use our package and provides an overview of the project and serves as the primary documentation for users and developers. It should include
- Project title: The name of our project.
- Description: A brief summary of what our package does and why it’s useful.
- Installation instructions: Step-by-step instructions on how to install the package, including any dependencies.
- Configuration: Instructions on how to configure the package, including any optional settings.
- Usage examples: Code snippets and examples that demonstrate how to use the package.
- Features: A list of key features provided by the package.
- Contributing: Guidelines for contributing to the project, if applicable.


## Step 7: Install and test the package
Install the package locally to ensure everything works as expected. 

1. To install the package locally, we can use the `pip` command. By running the following command in the root directory of the project (where the setup.py file is located), pip will install the package along with all its dependencies specified in requirements.txt:
```bash
pip install .
```

This command installs the package locally on the system, allowing us to use it as if it were installed from PyPI. This is particularly useful for testing before distributing the package.

2. Once installed, we should test the package by either running command-line scripts or importing it in a Python script.

## Step 8: Push the project to a Git repository
After testing the package locally, the next step is to push the project to a Git repository. This allows others to access your code and makes it easier to share, collaborate, and deploy.

Then, to install the package directly from your GitHub repository, you or others can use the following command:
```bash
pip install git+https://github.com/username/repository_name.git@main#egg=customer_churn_predictor&subdirectory=subdirectory_path
```

## Step 9: Versioning and Changelog
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