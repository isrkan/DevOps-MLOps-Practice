from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def define_models():
    try:
        models = {
            'Logistic regression': LogisticRegression(),
            'Decision tree': DecisionTreeClassifier(),
            'Random forest': RandomForestClassifier()
        }
        return models
    except Exception as e:
        print(f"An unexpected error occurred while defining models: {e}")
        return None