import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

def calculate_feature_importance(trained_model, feature_names, save_path=None):
    """
    Calculate and plot feature importance for a trained model.

    Args:
    - trained_model (model): The trained machine learning model.
    - feature_names (list): List of feature names corresponding to the training data.
    - save_path (str, optional): Path to save the feature importance plot. Defaults to None.

    Returns:
    - None: Displays the plot and optionally saves it, and prints/logs the top 5 important features.
    """
    try:
        if not hasattr(trained_model, 'feature_importances_'):
            logging.warning(f"The trained model does not have a feature_importances_ attribute.")
            print(f"The trained model does not have a feature_importances_ attribute.")
            return None, None

        # Feature importances
        feature_importances = trained_model.feature_importances_

        # Create DataFrame of feature importances
        feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})

        # Sort feature importances in descending order
        feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

        # Plot feature importances
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Importance', y='Feature', data=feature_importance_df)
        plt.title('Feature importances')
        plt.xlabel('Importance')
        plt.ylabel('Feature')

        # Save the plot if save_path is provided
        if save_path:
            plt.savefig(save_path)
            logging.info(f"Feature importance plot saved at: {save_path}")
            print(f"Feature importance plot saved at: {save_path}")
        # Display the plot
        plt.show()

        # Print top 5 most important features
        print("Top 5 most important features:")
        logging.info("Top 5 most important features:\n%s", feature_importance_df.head())
        print(feature_importance_df.head())

        return plt.gcf(), feature_importance_df
    except AttributeError as ae:
        logging.error(f"AttributeError occurred: {ae}")
        print(f"AttributeError occurred: {ae}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")