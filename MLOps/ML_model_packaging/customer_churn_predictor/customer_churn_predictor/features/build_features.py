from sklearn.preprocessing import PolynomialFeatures
import pandas as pd
import logging

def feature_engineering(preprocessed_data):
    try:
        logging.info("Starting feature engineering.")

        # Feature interaction
        preprocessed_data['Tenure_MonthlyCharges_interaction'] = preprocessed_data['tenure'] * preprocessed_data['MonthlyCharges']
        logging.info("Feature interaction created.")

        # Polynomial features
        poly = PolynomialFeatures(degree=2, include_bias=False)
        poly_features = poly.fit_transform(preprocessed_data[['tenure', 'MonthlyCharges']])
        poly_feature_names = poly.get_feature_names_out(['tenure', 'MonthlyCharges'])
        poly_df = pd.DataFrame(poly_features, columns=poly_feature_names)
        # Concatenate the polynomial features with the preprocessed data
        preprocessed_data = pd.concat([preprocessed_data, poly_df], axis=1)
        logging.info("Polynomial features created and concatenated.")

        # Remove duplicate columns, if any
        preprocessed_data = preprocessed_data.loc[:, ~preprocessed_data.columns.duplicated()]
        logging.info("Duplicate columns removed, if any.")

        logging.info("Feature engineering completed successfully.")
        return preprocessed_data
    except ValueError as ve:
        logging.error(f"ValueError occurred during feature engineering: {ve}")
        print(f"ValueError occurred during feature engineering: {ve}")
        return None
    except KeyError as ke:
        logging.error(f"KeyError occurred during feature engineering: {ke}")
        print(f"KeyError occurred during feature engineering: {ke}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during feature engineering: {e}")
        print(f"An unexpected error occurred during feature engineering: {e}")
        return None