from sklearn.model_selection import train_test_split

def perform_train_test_split(data, test_size=0.2, random_state=42):
    try:
        # Split the dataset into features (X) and target variable (y)
        X = data.drop(columns=['Churn_encoded'])  # Features
        y = data['Churn_encoded']  # Target variable
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        return X_train, X_test, y_train, y_test
    except ValueError as ve:
        print(f"ValueError occurred during train-test split: {ve}")
        return None, None, None, None
    except Exception as e:
        print(f"An unexpected error occurred during train-test split: {e}")
        return None, None, None, None