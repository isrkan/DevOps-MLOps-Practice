import mlflow

parameters={
    "learning_rate":0.3,
    "epochs":3
}

mlflow.projects.run(
    uri=".",
    entry_point="main",
    parameters=parameters,
    experiment_name="My Iris Classification Experiment"
)