from flask import Blueprint, jsonify, Flask, request
from flask_cors import CORS  # Import CORS
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from flask_restful import Api, Resource
import numpy as np
import json
# Define a blueprint for the heart disease prediction API
heart_api = Blueprint('heart_api', __name__, url_prefix='/api/heart')
api = Api(heart_api)
CORS(heart_api)

class HeartModel:
    """A class representing the Heart Disease Prediction Model."""
    
    # Singleton instance for HeartModel
    _instance = None

    def __init__(self):
        """Constructor method for HeartModel."""
        self.model = None
        self.dt = None
        self.features = ['sex', 'age', 'cp', 'trtbps', 'chol', 'exng']
        self.target = 'output'
        # Load the heart disease dataset from a Google Drive link
        url = 'https://drive.google.com/file/d/1kJcitXtlysIg1pCPQxV-lMSVTFsLWOkv/view'
        url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
        self.heart_data = pd.read_csv(url)

    def _clean(self):
        """Clean the dataset and prepare it for training."""
        # Drop unnecessary columns from the dataset
        self.heart_data.drop(['fbs', 'restecg', 'thalachh', 'oldpeak'], axis=1, inplace=True)
        # Drop rows with missing values
        self.heart_data.dropna(inplace=True)

    def _train(self):
        """Train the logistic regression and decision tree models."""
        # Split the dataset into features (X) and target (y)
        X = self.heart_data[self.features]
        y = self.heart_data[self.target]
        
        # Initialize and train the logistic regression model
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X, y)
        
        # Initialize and train the decision tree classifier
        self.dt = DecisionTreeClassifier()
        self.dt.fit(X, y)
        
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the HeartModel."""
        # If the instance doesn't exist, create it, clean the dataset, and train the model
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean()
            cls._instance._train()
        return cls._instance

    def predict(self, disease):
        """Predict the probability of heart disease for an individual."""
        # Convert the individual's features into a DataFrame
        heart_df = pd.DataFrame(disease, index=[0])
        # Convert gender values to binary (0 for Female, 1 for Male)
        heart_df['sex'] = heart_df['sex'].apply(lambda x: 1 if x == 'Male' else 0)
        # Predict the probability of heart disease using the logistic regression model
        heart_attack = np.squeeze(self.model.predict_proba(heart_df))
        return {'heart probability': heart_attack}

    def feature_weights(self):
        """Get the feature importance weights from the decision tree model."""
        # Extract feature importances from the decision tree model
        importances = self.dt.feature_importances_
        # Return feature importances as a dictionary
        return {feature: importance for feature, importance in zip(self.features, importances)} 
    
import json
import numpy as np

class HeartAPI:
    class _Predict(Resource):
        def post(self):
            """Handle POST requests."""
            # Extract heart data from the POST request
            patient = request.get_json()
            # Get the singleton instance of the HeartModel
            HeartModel_instance = HeartModel.get_instance()
            
            # Predict the probability of heart disease for the individual
            response = HeartModel_instance.predict(patient)
            # Convert any numpy arrays to lists
            for key, value in response.items():
                if isinstance(value, np.ndarray):
                    response[key] = value.tolist()
            # Return the prediction response as JSON
            return jsonify(response)
    # Add the _Predict resource to the heart_api with the '/predict' endpoint
    api.add_resource(_Predict, '/predict')

if __name__ == "__main__":
    # Create a Flask application
    app = Flask(__name__)
    # Register the heart_api blueprint with the Flask application
    app.register_blueprint(heart_api)
    # Run the application in debug mode if executed directly
    app.run(debug=True)
