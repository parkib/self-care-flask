import seaborn as sns  # Import seaborn for visualization
import pandas as pd  # Import pandas for data manipulation
from sklearn.model_selection import train_test_split  # Import train_test_split for splitting data
from sklearn.tree import DecisionTreeClassifier  # Import DecisionTreeClassifier for decision tree model
from sklearn.metrics import accuracy_score  # Import accuracy_score for model evaluation
from sklearn.preprocessing import OneHotEncoder  # Import OneHotEncoder for data preprocessing
import sqlite3  # Import sqlite3 for database operations
import numpy as np  # Import numpy for numerical computations
from sklearn.datasets import load_iris  # Import load_iris for iris dataset
from sklearn.model_selection import train_test_split  # Redundant import; should be removed
from sklearn.linear_model import LogisticRegression  # Import LogisticRegression for logistic regression model
from sklearn.model_selection import train_test_split  # Redundant import; should be removed
from sklearn.naive_bayes import GaussianNB  # Import GaussianNB for Naive Bayes model

# Data source URL
url = 'https://drive.google.com/file/d/1_lvLY-3rlNZoOkJiCVYZIsXF2eT_swf1/view?usp=sharing'
url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]

class StrokeModel:
    """A class used to represent the Stroke Model for patient survival prediction."""
    
    _instance = None  # Singleton instance of StrokeModel
    
    def __init__(self):
        """Constructor for StrokeModel."""
        self.model = None
        self.dt = None
        self.features = ['gender','age', 'hypertension', 'heart_disease', 'Residence_type','avg_glucose_level','bmi','smoking_status']
        self.target = 'stroke'
        self.stroke_data = pd.read_csv(url)  # Load dataset

    def _clean(self):
        """Clean the Stroke dataset."""
        # Drop unnecessary columns
        self.stroke_data.drop(['id', 'ever_married', 'work_type'], axis=1, inplace=True)
        # Convert categorical columns to numerical
        self.stroke_data['gender'] = self.stroke_data['gender'].apply(lambda x: 1 if x == 'male' else 0)
        self.stroke_data['Residence_type'] = self.stroke_data['Residence_type'].apply(lambda x: 1 if x == 'Urban' else 0)
        self.stroke_data['smoking_status'] = self.stroke_data['smoking_status'].apply(lambda x: 1 if x == 'smoked' else 0)
        # Drop rows with missing values
        self.stroke_data.dropna(inplace=True)

    def _train(self):
        """Train the Stroke prediction model."""
        X = self.stroke_data[self.features]
        y = self.stroke_data[self.target]
        # Initialize and train logistic regression model
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X, y)
        # Initialize and train decision tree classifier to show feature importance
        self.dt = DecisionTreeClassifier()
        self.dt.fit(X, y)

    @classmethod
    def get_instance(cls):
        """Get the singleton instance of StrokeModel."""
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean()
            cls._instance._train()
        return cls._instance

    def predict(self, individual):
        """Predict the survival probability of a patient."""
        # Prepare individual data for prediction
        individual_df = pd.DataFrame(individual, index=[0])
        individual_df['gender'] = individual_df['gender'].apply(lambda x: 1 if x == 'Male' else 0)
        individual_df['Residence_type'] = individual_df['Residence_type'].apply(lambda x: 1 if x == 'Urban' else 0)
        individual_df['smoking_status'] = individual_df['smoking_status'].apply(lambda x: 1 if x == 'smoked' else 0)
        # Predict survival probability
        stroke = np.squeeze(self.model.predict_proba(individual_df))
        return {'stroke': stroke}
    
    def feature_weights(self):
        """Get the feature weights of the Stroke prediction model."""
        # Extract feature importances from decision tree model
        importances = self.dt.feature_importances_
        return {feature: importance for feature, importance in zip(self.features, importances)} 
    
def initStroke():
    """Initialize the Stroke Model."""
    StrokeModel.get_instance()
    
def testStroke():
    """Test the Stroke Model."""
    print(" Step 1:  Define theoretical patient data for prediction: ")
    # Define patient data for prediction
    individual = {
        'gender': ['Male'],
        'age': [2],
        'hypertension': [1],
        'heart_disease': [1],
        'Residence_type': ['Urban'],
        'avg_glucose_level': [1],
        'bmi': [16],
        'smoking_status': ['smoked'],
    }
    print("\t", individual)
    print()
    StrokeModel = StrokeModel.get_instance()
    print(" Step 2:", StrokeModel.get_instance.__doc__)
    print(" Step 3:", StrokeModel.predict.__doc__)
    probability = StrokeModel.predict(individual)
    print('\t stroke: {:.2%}'.format(probability.get('stroke')))  
    print()
    print(" Step 4:", StrokeModel.feature_weights.__doc__)
    importances = StrokeModel.feature_weights()
    for feature, importance in importances.items():
        print("\t\t", feature, f"{importance:.2%}") 

if __name__ == "__main__":
    print(" Begin:", testStroke.__doc__)
    testStroke()
