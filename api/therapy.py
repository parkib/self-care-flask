from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.therapy import Therapy

# Change variable name and API name and prefix
therapy_api = Blueprint('therapy_api', __name__,
                   url_prefix='/api/therapy')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(therapy_api)

class TherapyAPI:     
    class _Read(Resource):
        def get(self):
            therapies = Therapy.query.all()
            json_ready = [therapy.read() for therapy in therapies]
            return jsonify(json_ready)

    # building RESTapi endpoint, method distinguishes action
    api.add_resource(_Read, '/')
