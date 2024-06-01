# When we import modules or functions from a package,
# Python looks for the __init__.py file in that package directory.
# By including the import statement in __init__.py,
# we're effectively exposing the load_data, preprocess_data and perform_train_test_split functions at the package level
from .load_data import load_data
from .preprocess import preprocess_data
from .split_data import perform_train_test_split