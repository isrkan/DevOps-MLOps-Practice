# Serving a Machine Learning Model as a Service with FastAPI and Flask

"Model as a service" pattern is a practice in which a machine learning model is exposed as a standalone service that other applications or systems can interact with via HTTP requests. This approach allows us to decouple the model from the main application, enabling scalability, reusability, and easier maintenance. 

Key concepts of the "model as a service" pattern:
1. **Decoupling**: Separating the machine learning model from the main application allows the model to be updated, scaled, or replaced independently. This flexibility reduces the risk of changes in the model affecting the rest of the system and vice versa.
2. **Reusability**: The model service can be reused across different applications or services, allowing for consistent and centralized model predictions.
3. **Scalability**: The model service can be scaled independently of the main application, allowing it to handle high volumes of prediction requests more effectively, without affecting the rest of the application.

This guide will walk you through the process of setting up a FastAPI service to expose a machine learning model and then building a Flask application that interacts with this service to generate predictions.

## Step 1: Setting up the FastAPI service for the model

### 1.1 Creating a new FastAPI project in VS Code

1. **Create a new folder**: Create a new folder for the FastAPI project.
2. **Open VS Code**: Open the folder in VS Code.
3. **Open the terminal**: In VS Code, open the terminal by selecting **Terminal** > **New Terminal**.

### 1.2 Setting up a virtual environment for FastAPI

1. **Create the virtual environment**: Run the following command to create a virtual environment named `fastapienv`:
    ```bash
    python -m venv fastapienv
    ```
2. **Activate the virtual environment**:
    ```bash
    .\fastapienv\Scripts\Activate
    ```

### 1.3 Installing FastAPI, Uvicorn and the model package

1. **Install FastAPI**:
    ```bash
    pip install fastapi
    ```
2. **Install Uvicorn** (an ASGI server for FastAPI):
    ```bash
    pip install uvicorn
    ```
3. Install the machine learning model package that we built earlier. If it’s hosted on GitHub and not on PyPI, we can install it using the following command:
    ```bash
    pip install git+https://github.com/username/repository_name.git@main#egg=my_package&subdirectory=package_directory
    ```
    Replace `username`, `repository_name`, and `package_directory` with the actual values.

### 1.4 Creating the FastAPI application

1. **Create the main application file**: Create a new file named `main.py` in the project folder and add the following code:

    ```python
    from fastapi import FastAPI
    from pydantic import BaseModel
    from my_model_package import my_model_loader, my_model_predictor  # Example imports

    app = FastAPI()

    # Load the model when the service starts
    model = my_model_loader.load_model('path/to/model/file')
    # Class to define the structure of the data that the API endpoints expect
    class PredictRequest(BaseModel):
        data: dict  # Adjust this to match the data schema

    @app.get("/predict")
    def get_predict():
        # Load and preprocess the data
        data = load_data(data_path)
        preprocessed_data = preprocess_data(data)
        processed_data = feature_engineering(preprocessed_data)

        # Make a prediction using the loaded model
        prediction = my_model_predictor.predict(model, processed_data)
        
        return {"prediction": prediction}

    @app.post("/predict")
    def post_predict(request: PredictRequest):
        # Extract and preprocess the data from the request
        data = request.data
        preprocessed_data = my_model_loader.preprocess_data(data)
        processed_data = my_model_loader.feature_engineering(preprocessed_data)

        # Make a prediction using the loaded model
        prediction = my_model_predictor.predict(model, processed_data)
        
        return {"prediction": prediction}
    ```

    - **GET request**: The GET request can be used to trigger predictions using predefined data or configuration. This method is useful for testing or when we want to use static data.
    - **POST request**: The POST request allows for sending data to the FastAPI service for prediction. This method is useful for interactive applications where users can provide input data dynamically.

2. **Running the FastAPI application**: Run the FastAPI server using Uvicorn:
    ```bash
    uvicorn main:app --reload
    ```
    This will start the server on `http://127.0.0.1:8000/`.

3. **Testing the FastAPI model service**: We can test the FastAPI service by navigating to `http://127.0.0.1:8000/docs` in our browser. FastAPI automatically generates a Swagger UI, where we can test the endpoints we created (such as the `/predict` endpoint). For `POST` requests need to provide JSON input.

## Step 2: Setting up the Flask application

### 2.1 Creating a new Flask project in VS Code

1. **Create a new folder**: Create a new folder for the Flask project.
2. **Open VS Code**: Open the folder in VS Code.
3. **Open the terminal**: In VS Code, open the terminal by selecting **Terminal** > **New Terminal**.

### 2.2 Setting up a virtual environment for Flask

1. **Create the virtual environment**: Run the following command to create a virtual environment named `flaskenv`:
    ```bash
    python -m venv flaskenv
    ```
2. **Activate the virtual environment**:
    ```bash
    .\flaskenv\Scripts\Activate
    ```

### 2.3 Installing Flask and required dependencies

1. **Install Flask**:
    ```bash
    pip install Flask
    ```
2. Install additional necessary dependencies that support various functionalities in Flask, such as `requests` for making HTTP requests and `matplotlib` for generating plots.

### 2.4 Creating the Flask application

1. **Create the main application file**: Create a new file named `app.py` in the Flask project folder and add the following code:

    ```python
    from flask import Flask, render_template, jsonify, request
    import requests

    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/predict', methods=['GET','POST'])
    def predict():
        # Handle GET request
        if request.method == 'GET':
            # Send a GET request to the FastAPI model service
            response = requests.get('http://127.0.0.1:8000/predict')

        # Handle POST request
        if request.method == 'POST':
            # Extract data from the form and converting the form data into a dictionary
            input_data = request.form.to_dict()
            # Send a POST request to the FastAPI model service with user input data
            response = requests.post('http://127.0.0.1:8000/predict', json={"data": input_data})
            
        # Get the prediction from the response
        prediction = response.json().get('prediction')
        
        return render_template('predict_results.html', prediction=prediction)

    if __name__ == '__main__':
        app.run(debug=True, port=5000)
    ```

    - **GET request handling**: When a `GET` request is made to the `/predict` endpoint, the Flask app sends a `GET` request to the FastAPI service. This is typically used to get predictions based on a fixed data set or default values. The predictions are then rendered using a template.
    - **POST request handling**: When a `POST` request is made to the `/predict` endpoint, the Flask app extracts form data from the user input and sends this data as a JSON payload to the FastAPI service. This method is used if the application needs to process user-provided input and get predictions based on that data. The result is then rendered using a template.

2. Adding HTML and CSS for the Flask web interface
To create a user interface for our Flask application, we will need to add HTML and CSS files.
    1. Create a folder named `templates` in the project directory. Inside it, create the relevant HTML files, such as `index.html` and `predict_results.html`.
    2. Create a `static` directory, and within it, a `styles` directory. Inside it, create the relevant CSS files, such as `styles.css`.

    For more detailed examples of HTML and CSS files, check the templates and static/styles folders in this directory.

3. Running the Flask application
    1. **Start the Flask application**:
        ```bash
        flask run
        ```
        This will start the Flask server on `http://127.0.0.1:5000/`.
    2. **Access the Flask application**: Open the web browser and navigate to `http://127.0.0.1:5000/` to see the running application.

### Step 3: Testing the end-to-end system
1. **Start the FastAPI model service**: Ensure the FastAPI service is running at `http://127.0.0.1:8000/` by executing:
    ```bash
    uvicorn main:app --reload
    ```
2. **Start the Flask application**: Ensure the the Flask app is accessed at `http://127.0.0.1:5000/` by running:
    ```bash
    flask run
    ```
3. **Perform tests**:
    - **GET Request**: Visit `http://127.0.0.1:5000/predict` in the browser to trigger a GET request.
    - **POST Request**: Fill out any forms provided on the main page, submit, and observe the prediction results.
4. **Review Logs**: Check the terminal outputs for both the Flask and FastAPI servers to ensure there are no errors, and that requests and responses are being handled as expected.