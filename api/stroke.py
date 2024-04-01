"""
Outline of the the following code:

- It imports necessary libraries and modules for data manipulation, model building, and API creation.
- Defines a Blueprint named 'stroke_api' that handles API routes related to stroke prediction.
- Defines a class `StrokeModel` responsible for handling the stroke prediction model.
- The `StrokeModel` class contains methods for data cleaning, model training, prediction, and feature weight extraction.
- The `StrokeAPI` class defines routes for the API, particularly a POST endpoint for predicting stroke probabilities.
"""

from flask import Blueprint, jsonify, Flask, request
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from flask_restful import Api, Resource
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import sqlite3
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
import json
import numpy as np

# Define a Blueprint named 'stroke_api' for handling API routes related to stroke prediction
stroke_api = Blueprint('stroke_api', __name__,
                   url_prefix='/api/stroke')

# URL for dataset
url='https://drive.google.com/file/d/1_lvLY-3rlNZoOkJiCVYZIsXF2eT_swf1/view?usp=sharing'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]

class StrokeModel:
    _instance = None
    
    def __init__(self):
        # Initialize model and decision tree attributes
        self.model = None
        self.dt = None
        
        # Define features and target for the model
        self.features = ['gender', 'age', 'hypertension', 'heart_disease', 'Residence_type','avg_glucose_level','bmi','smoking_status']
        self.target = 'stroke'
        
        # Load the stroke dataset
        self.stroke_data = pd.read_csv(url)

    def _clean(self):
        """
        Clean the stroke dataset.
        - Drop unnecessary columns
        - Convert boolean columns to integers
        - Drop rows with missing values
        """
        self.stroke_data.drop(['id', 'ever_married', 'work_type'], axis=1, inplace=True)
        self.stroke_data['gender'] = self.stroke_data['gender'].apply(lambda x: 1 if x == 'Male' else 0)
        self.stroke_data['Residence_type'] = self.stroke_data['Residence_type'].apply(lambda x: 1 if x == 'Urban' else 0)
        self.stroke_data['smoking_status'] = self.stroke_data['smoking_status'].apply(lambda x: 1 if x == 'smoked' else 0)
        self.stroke_data.dropna(inplace=True)

    def _train(self):
        """
        Train the stroke prediction model.
        - Split the data into features and target
        - Perform train-test split
        - Train logistic regression model
        - Train a decision tree classifier to show feature importance
        """
        X = self.stroke_data[self.features]
        y = self.stroke_data[self.target]
        
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X, y)
        
        self.dt = DecisionTreeClassifier()
        self.dt.fit(X, y)
        
    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of the StrokeModel.
        - If instance doesn't exist, create it and clean/train the data
        """
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean()
            cls._instance._train()
        return cls._instance

    def predict(self, individual):
        """
        Predict the stroke probability of an individual.
        - Clean individual data
        - Predict using the model
        - Return probabilities
        """
        individual_df = pd.DataFrame(individual, index=[0])
        individual_df['gender'] = individual_df['gender'].apply(lambda x: 1 if x == 'Male' else 0)
        individual_df['Residence_type'] = individual_df['Residence_type'].apply(lambda x: 1 if x == 'Urban' else 0)
        individual_df['smoking_status'] = individual_df['smoking_status'].apply(lambda x: 1 if x == 'smoked' else 0)
        
        stroke = np.squeeze(self.model.predict_proba(individual_df))
        return {'stroke': stroke}
    
    def feature_weights(self):
        """
        Get the feature weights of the stroke prediction model.
        - Extract feature importances from the decision tree model
        """
        importances = self.dt.feature_importances_
        return {feature: importance for feature, importance in zip(self.features, importances)} 

# Create Flask API
api = Api(stroke_api)

class StrokeAPI:
    class _Predict(Resource):
        """
        Class for predicting stroke probabilities.
        - Handles POST requests for predicting stroke probabilities
        """
        def post(self):
            # Get individual data from request
            individual = request.get_json()
            
            # Get singleton instance of StrokeModel
            strokeModel = StrokeModel.get_instance()            
            
            # Predict stroke probabilities
            response = strokeModel.predict(individual)
            for key, value in response.items():
                if isinstance(value, np.ndarray):
                    response[key] = value.tolist()
            # Return the prediction response as JSON
            return jsonify(response)
            response = json.dumps(response, cls=NumpyEncoder)

            return jsonify(response)

    # Add Predict resource to API
    api.add_resource(_Predict, '/predict')
