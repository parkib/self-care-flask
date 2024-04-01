from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from model.depression import * 

predict_api = Blueprint("predict_api", __name__,
                        url_prefix='/api/predict')
api = Api(predict_api)
# Load the dataset

class Predict(Resource):
    def post(self):
        body = request.get_json()
        age = float(body.get("age"))
        stress_level = float(body.get("stress"))
        daily_exercise_hours = float(body.get("exercise"))
        daily_sleep_hours = float(body.get("sleep"))
        
        depressionModel.train_model('depression_dataset.csv')  # Train the model if not already trained
        chance_of_depression = depressionModel.predict_depression(age, stress_level, daily_exercise_hours, daily_sleep_hours)
        chance_of_depression = max(0, min(chance_of_depression, 1))  # Ensure chance_of_depression is between 0 and 1
        
        return jsonify(f"Based on the provided data, the chance of developing depression is: {chance_of_depression * 100:.2f}%")

api.add_resource(Predict, '/')
