# When we import modules or functions from a package,
# Python looks for the __init__.py file in that package directory.
# By including the import statement in __init__.py,
# we're effectively exposing the feature_engineering function at the package level.
from .build_features import feature_engineering