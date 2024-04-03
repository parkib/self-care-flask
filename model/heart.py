import pandas as pd  # Pandas is a data manipulation and analysis library in Python
import numpy as np  # NumPy is a library for numerical computing in Python
from sklearn.model_selection import train_test_split  # This function splits arrays or matrices into random train and test subsets
from sklearn.tree import DecisionTreeClassifier  # DecisionTreeClassifier is a class capable of performing multi-class classification on a dataset
from sklearn.linear_model import LogisticRegression  # LogisticRegression is a linear model for binary classification
from sklearn.metrics import accuracy_score  # Accuracy_score is a function to measure the accuracy of classification models
from sklearn.naive_bayes import GaussianNB  # GaussianNB is a class for Gaussian Naive Bayes classification

class HeartModel:
    """
    A class representing the Heart Disease Prediction Model.
    
    Attributes:
        _instance (HeartModel): A singleton instance of the HeartModel class.
        model (LogisticRegression): The logistic regression model for heart disease prediction.
        dt (DecisionTreeClassifier): The decision tree classifier for feature importance analysis.
        gnb (GaussianNB): The Gaussian Naive Bayes classifier for heart disease prediction.
        features (list): A list of feature names used in the model.
        target (str): The target variable name.
        heart_data (DataFrame): The dataset containing heart disease data.
    """
    
    _instance = None
    
    def __init__(self):
        """Constructor method for HeartModel."""
        self.model = None
        self.dt = None
        self.gnb = None
        self.features = ['sex', 'age', 'cp', 'trtbps', 'chol', 'exng']
        self.target = 'output'
        self.heart_data = None

    def _clean(self, url):
        """Clean the dataset and prepare it for training.
        
        Args:
            url (str): The URL to the heart disease dataset.
        """
        # Load the dataset
        self.heart_data = pd.read_csv(url)
        
        # Drop unnecessary columns
        self.heart_data.drop(['fbs', 'restecg', 'thalachh', 'oldpeak'], axis=1, inplace=True)

        # Convert boolean columns to integers
        self.heart_data['sex'] = self.heart_data['sex'].apply(lambda x: 1 if x == 'male' else 0)
        self.heart_data['exng'] = self.heart_data['exng'].apply(lambda x: 1 if x == 'Yes' else 0)
    
        # Drop rows with missing values
        self.heart_data.dropna(inplace=True)

    def _train(self):
        """Train the logistic regression, decision tree, and Gaussian Naive Bayes models."""
        # Split the data into features and target
        X = self.heart_data[self.features]
        y = self.heart_data[self.target]
        
        # Perform train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Train the logistic regression model
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X_train, y_train)
        
        # Train a decision tree classifier
        self.dt = DecisionTreeClassifier()
        self.dt.fit(X_train, y_train)
        
        # Train Gaussian Naive Bayes
        self.gnb = GaussianNB()
        self.gnb.fit(X_train, y_train)
        
    @classmethod
    def get_instance(cls, url):
        """Get the singleton instance of the HeartModel.
        
        Args:
            url (str): The URL to the heart disease dataset.
        
        Returns:
            HeartModel: The singleton instance of the HeartModel.
        """
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean(url)
            cls._instance._train()
        return cls._instance

    def predict(self, individual):
        """Predict the probability of heart disease for an individual.
        
        Args:
            individual (dict): A dictionary representing the individual's features.
        
        Returns:
            dict: A dictionary containing the probability of heart disease.
        """
        individual_df = pd.DataFrame(individual, index=[0])
        individual_df['sex'] = individual_df['sex'].apply(lambda x: 1 if x == 'Male' else 0)
        individual_df['exng'] = individual_df['exng'].apply(lambda x: 1 if x == 'Yes' else 0)
        heart_attack = np.squeeze(self.model.predict_proba(individual_df))
        return {'heart': heart_attack}

    def feature_weights(self):
        """Get the feature importance weights from the decision tree model.
        
        Returns:
            dict: A dictionary containing feature names and their importance weights.
        """
        importances = self.dt.feature_importances_
        return {feature: importance for feature, importance in zip(self.features, importances)}

def initHeart():
    """Initialize the HeartModel instance."""
    url = 'https://drive.google.com/file/d/1kJcitXtlysIg1pCPQxV-lMSVTFsLWOkv'
    HeartModel.get_instance(url)
    
def testHeart():
    """Test the HeartModel by predicting heart disease probability and feature importance."""
    HeartModel_instance = HeartModel.get_instance(url)
    
    individual = {
        'sex': 14,
        'age': 'Male',
        'cp': 2,
        'trtbps': 130,
        'chol': 204,
        'exng': 0,
    }
    
    # Predict the heart disease probability for the individual
    probability = HeartModel_instance.predict(individual)
    print('Heart probability:', probability.get('heart_attack'))
    print()
    
    # Get the feature importance weights
    importances = HeartModel_instance.feature_weights()
    for feature, importance in importances.items():
        print(feature, 'importance:', importance)

if __name__ == "__main__":
    url = 'https://drive.google.com/file/d/1kJcitXtlysIg1pCPQxV-lMSVTFsLWOkv'
    initHeart()
    testHeart()