from setuptools import setup, find_packages

setup(
    name='customer_churn_package',
    version='0.1.0',
    description='A package for predicting customer churn in telecommunication companies.',
    author='Israel',
    author_email='israel@example.com',
    packages=find_packages(exclude=['tests*']),
    install_requires=open('requirements.txt').readlines(),
    entry_points={
        'console_scripts': [
            'run_pipeline=scripts.run_pipeline:main',
            'run_train=scripts.run_train:main',
        ]
    },
)
