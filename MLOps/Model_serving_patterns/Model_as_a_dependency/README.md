# Serving a Machine Learning Model as a Dependency in Flask

"Model as a dependency" pattern is the practice of integrating a pre-built machine learning model into a software application so that the model becomes an integral part of that application’s functionality. In this pattern, the model is treated like any other software component (or dependency) that the application relies on to perform its tasks, such as making predictions based on user input.

Key concepts of the "model as a dependency" pattern:
1. **Model integration**: The model is typically loaded into memory when the application starts and can be used throughout the app whenever predictions are needed. This allows the model to be part of the web service, meaning users can interact with the model through a web interface (e.g., by inputting data and receiving predictions).
2. **Reusability**: The model is treated as a reusable component, which means it can be used across different parts of the application or even in different applications. Instead of rewriting the code for loading and using the model in multiple places, it's loaded once and then used as needed, making the code more organized and maintainable.
3. **Separation of concerns**: The application’s core functionality (like handling web requests, rendering HTML, etc.) is kept separate from the model’s logic. The model’s job is to process input data and generate predictions. This separation makes the system easier to maintain and update. For example, if we need to update the model, we can do so without changing the rest of the application.


This guide will walk you through integrating a pre-built machine learning model as a dependency in a Flask application. We'll cover how to set up the Flask project, load the model, and use it to make predictions via a web interface.

## Step 1: Setting up the Flask project

### 1.1 Creating a new project in VS Code
1. Open VS Code and create a new folder for the Flask project.
2. Open the terminal in VS Code by selecting **Terminal** > **New Terminal**.
3. Navigate to the project directory in the terminal (if not already there).

### 1.2 Setting up a virtual environment
A virtual environment helps to keep dependencies required by different projects in separate places, by creating isolated environments for them.
1. In the terminal, run the following command to create a virtual environment named `dependencyenv`:
    ```bash
    python -m venv dependencyenv
    ```
    This creates a folder named `dependencyenv` inside the project directory, which will hold the isolated environment.
2. Activate the virtual environment:
    ```bash
    .\dependencyenv\Scripts\Activate
    ```
    Once activated, we should see the name of the virtual environment (`dependencyenv`) in the terminal prompt, indicating that the environment is active.    

### 1.3 Installing Flask and the model package
1. With the virtual environment activated, install Flask:
    ```bash
    pip install Flask
    ```
2. Install the machine learning model package that we built earlier. If it’s hosted on GitHub and not on PyPI, we can install it using the following command:
    ```bash
    pip install git+https://github.com/username/repository_name.git@main#egg=my_package&subdirectory=package_directory
    ```
    Replace `username`, `repository_name`, and `package_directory` with the actual values.

## Step 2: Creating a simple Flask application

### 2.1 Creating the Flask application file
Create a new file named `app.py` in the project folder and add the following code:
```python
from flask import Flask, render_template, jsonify
from my_model_package import my_model_loader, my_model_predictor  # Example imports

app = Flask(__name__)

# Load the model or initialize any required objects
model = my_model_loader.load_model('path/to/model/file')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def run_predict():
    # Load and preprocess the data
    data = my_model_loader.load_data('path/to/data/file')
    processed_data = my_model_loader.preprocess_data(data)

    # Make predictions using the loaded model
    predictions = my_model_predictor.predict(model, processed_data)

    # Generate and display the plot
    return render_template('predict_results.html', predictions=predictions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```
In this general example, `my_model_package` could be any machine learning package that includes functions for loading the model, running a pipeline, and making predictions. This simple Flask app includes two routes:
- `'/'` for the home page.
- `'/predict'` for making predictions with the model.

The model here is treated as a dependency—it’s loaded once when the application starts and then reused whenever predictions are needed.

We can adapt the code and templates as needed for our specific machine learning model and application.

### 2.2 Adding HTML and CSS for the web interface
To create a user interface for our Flask application, we will need to add HTML and CSS files.
1. Create a folder named `templates` in the project directory. Inside it, create the relevant HTML files, such as `index.html` and `predict_results.html`.
2. Create a `static` directory, and within it, a `styles` directory. Inside it, create the relevant CSS files, such as `styles.css`.

For more detailed examples of HTML and CSS files, check the `templates` and `static/styles` folders in this directory.

### 2.3 Running the flask application
1. Start the Flask application by running the following command in the terminal from the project directory:
    ```bash
    flask run
    ```
2. Open the web browser and navigate to `http://127.0.0.1:5000/` to see the running application.