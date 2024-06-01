import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_feature_importance(trained_model, feature_names):
    try:
        if not hasattr(trained_model, 'feature_importances_'):
            raise AttributeError("The trained model does not have a feature_importances_ attribute.")

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
        plt.show()

        # Print top 5 most important features
        print("Top 5 most important features:")
        print(feature_importance_df.head())

    except AttributeError as ae:
        print(f"AttributeError occurred: {ae}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")