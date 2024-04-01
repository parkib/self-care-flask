from flask import Blueprint, jsonify, Flask, request
from flask_cors import CORS  # Import CORS
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from flask_restful import Api, Resource
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
import sqlite3
from flask import Blueprint, jsonify, Flask, request
from flask_restful import Api, Resource
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
import numpy as np


heart_api = Blueprint('heart_api', __name__,
                   url_prefix='/api/heart')

heart_api = Blueprint('heart_api', __name__, url_prefix='/api/heart')
api = Api(heart_api)
CORS(heart_api)

class HeartModel:
    """A class used to represent the Titanic Model for passenger survival prediction.
    """
    # a singleton instance of TitanicModel, created to train the model only once, while using it for prediction multiple times
    ## underbar in Python means that it is not for general use - you need to use another accessor to get to it (it will be assigned something if you use the system appropriately)
    _instance = None


    ## creating + cleaning + training of the instance
    
    # constructor, used to initialize the TitanicModel
    '''

    '''
    def __init__(self):
        # the titanic ML model
        self.model = None
        self.dt = None
        # define ML features and target
        self.features = ['age', 'sex', 'cp', 'trtpbs', 'chol', 'exng' ]
        self.target = 'heart'
        # load the titanic dataset
        url='https://drive.google.com/file/d/1_lvLY-3rlNZoOkJiCVYZIsXF2eT_swf1/view?usp=sharing'    
        url='https://drive.google.com/uc?id=' + url.split('/')[-2]
        self.heart_data = pd.read_csv(url)
        #self.titanic_data = sns.load_dataset('titanic')
        # one-hot encoder used to encode 'embarked' column
        #self.encoder = OneHotEncoder(handle_unknown='ignore')

    # clean the titanic dataset, prepare it for training
    def _clean(self):
        # Drop unnecessary columns
        self.heart_data.drop(['fbs', 'restecg', 'thalachh', 'oldpeak'], axis=1, inplace=True)
        #self.stroke_data['gender'] = self.stroke_data['gender'].apply(lambda x: 1 if x == 'Male' else 0)
        #self.stroke_data['alone'] = self.stroke_data['alone'].apply(lambda x: 1 if x == True else 0)
        #self.stroke_data['Residence_type'] = self.stroke_data['Residence_type'].apply(lambda x: 1 if x == 'Urban' else 0)
        #self.stroke_data['smoking_status'] = self.stroke_data['smoking_status'].apply(lambda x: 1 if x == 'smoked' else 0)
        #self.stroke_data.dropna(subset=['embarked'], inplace=True)
        self.heart_data.dropna(inplace=True)

    # train the titanic model, using logistic regression as key model, and decision tree to show feature importance
    def _train(self):
        # split the data into features and target
        X = self.heart_data[self.features]
        y = self.heart_data[self.target]
        
        # perform train-test split
        self.model = LogisticRegression(max_iter=1000)
        
        # train the model
        self.model.fit(X, y)
        
        # train a decision tree classifier
        self.dt = DecisionTreeClassifier()
        self.dt.fit(X, y)
        
    @classmethod
    def get_instance(cls):
        """ Gets, and conditionaly cleans and builds, the singleton instance of the TitanicModel.
        The model is used for analysis on titanic data and predictions on the survival of theoritical passengers.
        
        Returns:
            TitanicModel: the singleton _instance of the TitanicModel, which contains data and methods for prediction.
        """        
        # check for instance, if it doesn't exist, create it
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean()
            cls._instance._train()
        # return the instance, to be used for prediction
        return cls._instance

    def predict(self, heart):
        """ Predict the survival probability of a passenger.

        Args:
            passenger (dict): A dictionary representing a passenger. The dictionary should contain the following keys:
                'pclass': The passenger's class (1, 2, or 3)
                'sex': The passenger's sex ('male' or 'female')
                'age': The passenger's age
                'sibsp': The number of siblings/spouses the passenger has aboard
                'parch': The number of parents/children the passenger has aboard
                'fare': The fare the passenger paid
                'embarked': The port at which the passenger embarked ('C', 'Q', or 'S')
                'alone': Whether the passenger is alone (True or False)

        Returns:
           dictionary : contains die and survive probabilities 
        """
        # clean the passenger data
        heart_df = pd.DataFrame(heart, index=[0])
        heart_df['gender'] = heart_df['gender'].apply(lambda x: 1 if x == 'Male' else 0)
        #self.stroke_data['Residence_type'] = self.stroke_data['Residence_type'].apply(lambda x: 1 if x == 'Urban' else 0)
        #self.stroke_data['smoking_status'] = self.stroke_data['smoking_status'].apply(lambda x: 1 if x == 'smoked' else 0)
        #individual_df['alone'] = individual_df['alone'].apply(lambda x: 1 if x == True else 0)
        #onehot = self.encoder.transform(passenger_df[['embarked']]).toarray()
        #cols = ['embarked_' + str(val) for val in self.encoder.categories_[0]]
        #onehot_df = pd.DataFrame(onehot, columns=cols)
        #passenger_df = pd.concat([passenger_df, onehot_df], axis=1)
        #passenger_df.drop(['embarked'], axis=1, inplace=True)
        
        # predict the survival probability and extract the probabilities from numpy array
        heart = np.squeeze(self.model.predict_proba(heart_df))
        # return the survival probabilities as a dictionary
        return {'heart percentage': heart}
    
    def feature_weights(self):
        """Get the feature weights
        The weights represent the relative importance of each feature in the prediction model.

        Returns:
            dictionary: contains each feature as a key and its weight of importance as a value
        """
        # extract the feature importances from the decision tree model
        importances = self.dt.feature_importances_
        # return the feature importances as a dictionary, using dictionary comprehension
        return {feature: importance for feature, importance in zip(self.features, importances)} 
    
api = Api(heart_api)

class HeartAPI:
    class _Predict(Resource):
        def options(self):
            """Handle preflight requests."""
            resp = make_response()
            resp.headers.add("Access-Control-Allow-Origin", "*")
            resp.headers.add("Access-Control-Allow-Methods", "POST")
            resp.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            return resp

api = Api(heart_api)
class HeartAPI:
    class _Predict(Resource):
        
        def post(self):
            """ Semantics: In HTTP, POST requests are used to send data to the server for processing.
            Sending passenger data to the server to get a prediction fits the semantics of a POST request.
            
            POST requests send data in the body of the request...
            1. which can handle much larger amounts of data and data types, than URL parameters
            2. using an HTTPS request, the data is encrypted, making it more secure
            3. a JSON formated body is easy to read and write between JavaScript and Python, great for Postman testing
            """     
            # Get the passenger data from the request
            heart = request.get_json()

            # Get the singleton instance of the TitanicModel
            HeartModel = HeartModel.get_instance()
            # Predict the survival probability of the passenger
            response = HeartModel.predict(heart)

            # Return the response as JSON
            return jsonify(response)

    api.add_resource(_Predict, '/predict')