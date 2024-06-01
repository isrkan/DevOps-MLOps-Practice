# Import modules or functions to be directly accessible when importing the package
from .data import load_data, preprocess
from .models import train_model, evaluate_model
from .pipeline import run_pipeline
from .config import config

# Define package version
__version__ = '0.1.0'