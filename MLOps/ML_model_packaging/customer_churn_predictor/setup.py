from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
def read_version():
    with open(os.path.join('customer_churn_predictor', '__init__.py')) as f:
        content = f.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")

# Read requirements from the requirements.txt file with explicit error handling
with open('requirements.txt', 'rb') as f:
    content = f.read()
    # Remove BOM if present and decode
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]
    required = content.decode('utf-8').splitlines()


setup(
    name='customer_churn_predictor',
    version=read_version(),
    description='A package for predicting customer churn in telecommunication companies.',
    author='Israel',
    author_email='israel@example.com',
    packages=find_packages(where='.'),  # Root directory of the package
    package_dir={'customer_churn_predictor': 'customer_churn_predictor'},  # Correct mapping
    include_package_data=True,
    install_requires=required,
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'run_pipeline=scripts.run_pipeline:main',
            'run_train=scripts.run_train:main',
        ]
    },
)
