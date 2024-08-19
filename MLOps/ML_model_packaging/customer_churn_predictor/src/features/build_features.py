from sklearn.preprocessing import PolynomialFeatures
import pandas as pd

def feature_engineering(preprocessed_data):
    try:
        # Feature interaction
        preprocessed_data['Tenure_MonthlyCharges_interaction'] = preprocessed_data['tenure'] * preprocessed_data['MonthlyCharges']

        # Polynomial features
        poly = PolynomialFeatures(degree=2, include_bias=False)
        poly_features = poly.fit_transform(preprocessed_data[['tenure', 'MonthlyCharges']])
        poly_feature_names = poly.get_feature_names_out(['tenure', 'MonthlyCharges'])
        poly_df = pd.DataFrame(poly_features, columns=poly_feature_names)
        preprocessed_data = pd.concat([preprocessed_data, poly_df], axis=1)

        return preprocessed_data
    except ValueError as ve:
        print(f"ValueError occurred during feature engineering: {ve}")
        return None
    except KeyError as ke:
        print(f"KeyError occurred during feature engineering: {ke}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during feature engineering: {e}")
        return None