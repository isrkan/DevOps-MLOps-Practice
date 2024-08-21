from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler, LabelEncoder
import pandas as pd
import logging

def preprocess_data(data):
    """
    Preprocess the input data for machine learning.

    This includes encoding categorical variables, scaling numerical features,
    and encoding the target variable.

    Args:
    - data (DataFrame): The raw data to be preprocessed.

    Returns:
    - preprocessed_data (DataFrame): The preprocessed data ready for modeling.
    """
    try:
        logging.info("Starting data preprocessing.")
        # Encoding categorical variables
        binary_categorical_features = ['gender', 'Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']
        ordinal_categorical_features = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                                        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                                        'Contract', 'PaymentMethod']

        # Perform one-hot encoding for binary features
        binary_encoder = OneHotEncoder(drop='first')
        binary_encoded_data = binary_encoder.fit_transform(data[binary_categorical_features])
        binary_encoded_columns = binary_encoder.get_feature_names_out(binary_categorical_features)
        logging.info("Binary categorical features encoded.")

        # Perform ordinal encoding for ordinal features
        ordinal_encoder = OrdinalEncoder()
        ordinal_encoded_data = ordinal_encoder.fit_transform(data[ordinal_categorical_features])
        ordinal_encoded_columns = [f'{feature}_encoded' for feature in ordinal_categorical_features]
        logging.info("Ordinal categorical features encoded.")

        # Concatenate encoded binary and ordinal categorical features
        encoded_data = pd.concat([pd.DataFrame(binary_encoded_data.toarray(), columns=binary_encoded_columns),
                                  pd.DataFrame(ordinal_encoded_data, columns=ordinal_encoded_columns)], axis=1)

        # Scale numerical features
        numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges']

        # Ensure numerical features are numeric
        data[numerical_features] = data[numerical_features].apply(pd.to_numeric, errors='coerce')

        # Handle missing values in numerical features
        data[numerical_features] = data[numerical_features].fillna(data[numerical_features].median())

        scaler = StandardScaler()
        scaled_numerical_features = scaler.fit_transform(data[numerical_features])

        # Replace original numerical features with scaled ones
        for i, feature in enumerate(numerical_features):
            data[feature] = scaled_numerical_features[:, i]
        logging.info("Numerical features scaled.")

        # Encoding the target variable 'Churn'
        label_encoder = LabelEncoder()
        data['Churn_encoded'] = label_encoder.fit_transform(data['Churn'])
        logging.info("Target variable 'Churn' encoded.")

        # Concatenate encoded categorical features and numerical features
        preprocessed_data = pd.concat([encoded_data, data[numerical_features], data['Churn_encoded']], axis=1)
        logging.info("Data preprocessing completed successfully.")

        return preprocessed_data
    except ValueError as ve:
        logging.error(f"ValueError occurred during preprocessing: {ve}")
        print(f"ValueError occurred: {ve}")
        return None
    except KeyError as ke:
        logging.error(f"KeyError occurred during preprocessing: {ke}")
        print(f"KeyError occurred: {ke}")
        return None
    except TypeError as te:
        logging.error(f"TypeError occurred during preprocessing: {te}")
        print(f"TypeError occurred: {te}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during preprocessing: {e}")
        print(f"An unexpected error occurred: {e}")
        return None