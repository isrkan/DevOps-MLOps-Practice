import mlflow
import mlflow.sklearn
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import argparse

def main():
    # These values will be passed from the MLproject file or command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--learning_rate", type=float, default=0.01)
    parser.add_argument("--epochs", type=int, default=10)
    args = parser.parse_args()

    # Set the tracking URI to the MLflow server
    mlflow.set_tracking_uri(uri="")

    # Start a new MLflow run
    with mlflow.start_run() as run:
        # Load the Iris dataset
        iris = datasets.load_iris()
        X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)

        # Create and train the model
        model = RandomForestClassifier(n_estimators=int(args.epochs), max_depth=5, random_state=42)
        model.fit(X_train, y_train)

        # Predict on test data
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)

        # Log parameters, metrics, and the model to MLflow
        mlflow.log_param("learning_rate", args.learning_rate)
        mlflow.log_param("epochs", args.epochs)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "model")

        print(f"Model trained with accuracy: {accuracy}")
        print(f"Run ID: {run.info.run_id}")

if __name__ == "__main__":
    main()