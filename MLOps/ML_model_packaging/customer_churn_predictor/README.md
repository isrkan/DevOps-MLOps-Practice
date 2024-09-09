# Customer Churn Prediction Package

This Python package predicts customer churn for subscription-based businesses, with a focus on the telecommunications industry. It includes tools for data preprocessing, model training, evaluation, and visualization, making it a versatile solution for tackling churn prediction challenges.

### Problem statement
Customer churn is a critical issue in the telecommunications industry, where businesses lose significant revenue when customers decide to leave their services. Identifying the factors that contribute to customer churn and predicting which customers are likely to churn can help businesses take proactive measures to retain these customers, improve customer satisfaction, and increase profitability.

The goal of this project is to accurately predict customer churn by using machine learning models. The package helps businesses develop targeted strategies to retain at-risk customers, by identifying key factors that contribute to churn.

### Data
The data used in this project is the Telco Customer Churn dataset and comes from a public dataset provided by IBM, which contains information about a telecom company's customers. The dataset includes various features such as customer demographics, account information, and services used.

**Source**: [Kaggle Telco Customer Churn Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

## Installation
We have two options for installing the package from the GitHub repository:

#### Option 1: Clone the specific project directory
1. Clone only the specific project directory from the repository:
```
git clone --no-checkout https://github.com/isrkan/DevOps-MLOps-Practice.git
cd DevOps-MLOps-Practice
git sparse-checkout init --cone
git sparse-checkout set "MLOps/ML_model_packaging/customer_churn_predictor"
git fetch
git pull
git read-tree -mu HEAD
```

2. Navigate to the root directory:
```
cd "MLOps/ML_model_packaging/customer_churn_predictor"
```

3. Build the package as a wheel first:
```
python setup.py sdist bdist_wheel
```

This will create two types of distributions in the `dist/` folder:
- Source distribution (`.tar.gz`)
- Built wheel (`.whl`)

4. After generating the wheel, install the package using `pip`:
```
pip install dist/customer_churn_predictor-0.1.0-py3-none-any.whl
```

This will install the `customer_churn_predictor` package along with all required dependencies.

#### Option 2: Install directly from GitHub with pip
Alternatively, we can install the package directly from the GitHub repository using `pip`.
```
pip install "git+https://github.com/isrkan/DevOps-MLOps-Practice.git#subdirectory=MLOps/ML_model_packaging/customer_churn_predictor"
```

To verify that the package has been installed correctly, use the following command:
```
pip show customer-churn-predictor
```

## Usage

#### Importing and using the package
To use the churn predictor in the Python code, import it as follows:
```python
from customer_churn_predictor import customer_churn_predictor, pipeline

# Initialize the churn predictor
churn_predictor = customer_churn_predictor.CustomerChurnPredictor()

# Run the pipeline with the data
pipeline.run_pipeline(churn_predictor.config, data_path='<path_to_csv_data_file>')
```

#### Creating predictions

##### Option 1: Using a loaded model
If we already have a trained model and want to generate predictions directly without retraining the model, we can do so as follows:
```python
from customer_churn_predictor import load_saved_model, predict_model

# Load the trained model
trained_models = load_saved_model.load_model('<path_to_trained_model_file>')

# Use the trained model to make predictions on new data
predictions = predict_model.predict_models(trained_models, new_data)
```

##### Option 2: Using a served model via MLflow REST API
If we have a model served through MLflow, we can generate predictions by making a REST API call. To do this, ensure that the model is served on the required port and then run the following code:
```python
from customer_churn_predictor.models import predict_via_api

# Generate predictions using the served model via the REST API
predictions = predict_via_api.predict_via_api(new_data, "http://127.0.0.1:<port>/invocations")
```

#### Using command line
After installing the package, we can run the pipeline directly from the command line. The pipeline will load the data, preprocess it, train models, evaluate them, and save the results.

```bash
python scripts/run_pipeline.py --data_path <path_to_csv_data_file>
```

It takes the following command-line arguments:
- `--data_path`: Path to the CSV data file (required).
- `--config_path`: Optional path to a custom configuration file.

Alternatively, if we want to focus on training and saving the models separately, we can run the training script:

```bash
python scripts/run_train.py --data_path <path_to_csv_data_file> --models_dir <directory_to_save_models>
```

It takes the following command-line arguments:
- `--data_path`: Path to the CSV data file (required).
- `--config_path`: Optional path to a custom configuration file.
- `--models_dir`: Directory to save the trained models (required).

## Features

- **Data loading and preprocessing**: Load and preprocess customer data with customizable pipelines.
- **Model training and evaluation**: Train various machine learning models and evaluate their performance.
- **Feature importance visualization**: Visualize the importance of different features in the models.
- **Prediction**: Generate predictions using trained models.
- **Model saving and loading**: Save and load models using a standard format for later use.
- **Command-line interface**: Run the entire pipeline or train models via command-line scripts.