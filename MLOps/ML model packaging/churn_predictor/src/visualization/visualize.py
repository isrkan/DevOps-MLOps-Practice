import matplotlib.pyplot as plt
import seaborn as sns

def visualize_categorical_distribution(data, feature):
    """
    Visualize distribution of a categorical feature.

    Args:
    - data (pd.DataFrame): Input DataFrame containing the dataset.
    - feature (str): Name of the categorical feature to visualize.
    """
    plt.figure(figsize=(10, 6))
    sns.countplot(x=feature, hue='Churn', data=data)
    plt.title(f'Distribution of {feature} by Churn')
    plt.xlabel(feature)
    plt.ylabel('Count')
    plt.legend(title='Churn', loc='upper right')
    plt.xticks(rotation=45)
    plt.show()

def visualize_numerical_distribution(data, feature):
    """
    Visualize distribution of a numerical feature.

    Args:
    - data (pd.DataFrame): Input DataFrame containing the dataset.
    - feature (str): Name of the numerical feature to visualize.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x=feature, hue='Churn', kde=True, bins=30)
    plt.title(f'Distribution of {feature} by Churn')
    plt.xlabel(feature)
    plt.ylabel('Count')
    plt.legend(title='Churn', loc='upper right')
    plt.show()