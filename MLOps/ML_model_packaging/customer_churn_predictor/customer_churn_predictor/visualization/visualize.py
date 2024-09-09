import matplotlib.pyplot as plt
import seaborn as sns
import logging

def visualize_categorical_distribution(data, feature, save_path=None):
    """
    Visualize distribution of a categorical feature.

    Args:
    - data (pd.DataFrame): Input DataFrame containing the dataset.
    - feature (str): Name of the categorical feature to visualize.
    - save_path (str, optional): Path to save the plot. If None, the plot will not be saved.

    Returns:
    - fig (matplotlib.figure.Figure): The matplotlib figure object of the plot.
    """
    plt.figure(figsize=(10, 6))
    sns.countplot(x=feature, hue='Churn', data=data)
    plt.title(f'Distribution of {feature} by Churn')
    plt.xlabel(feature)
    plt.ylabel('Count')
    plt.legend(title='Churn', loc='upper right')
    plt.xticks(rotation=45)
    fig = plt.gcf()  # Get the current figure
    # Save the plot if save_path is provided
    if save_path:
        plt.savefig(save_path)
        logging.info(f"Categorical distribution plot saved at: {save_path}")
        print(f"Categorical distribution plot saved at: {save_path}")
    # Display the plot
    plt.show()
    plt.close()  # Close the plot to free memory

    return fig

def visualize_numerical_distribution(data, feature, save_path=None):
    """
    Visualize distribution of a numerical feature.

    Args:
    - data (pd.DataFrame): Input DataFrame containing the dataset.
    - feature (str): Name of the numerical feature to visualize.
    - save_path (str, optional): Path to save the plot. If None, the plot will not be saved.

    Returns:
    - fig (matplotlib.figure.Figure): The matplotlib figure object of the plot.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x=feature, hue='Churn', kde=True, bins=30)
    plt.title(f'Distribution of {feature} by Churn')
    plt.xlabel(feature)
    plt.ylabel('Count')
    plt.legend(title='Churn', loc='upper right')
    fig = plt.gcf()  # Get the current figure
    # Save the plot if save_path is provided
    if save_path:
        plt.savefig(save_path)
        logging.info(f"Numerical distribution plot saved at: {save_path}")
        print(f"Numerical distribution plot saved at: {save_path}")
    # Display the plot
    plt.show()
    plt.close()  # Close the plot to free memory

    return fig