from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.therapies import Therapy

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
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate location
            location = body.get('location')
            if location is None or len(location) < 2:
                return {'message': f'Location is missing, or is less than 2 characters'}, 400
            # validate location
            special = body.get('special')
            if special is None or len(special) < 2:
                return {'message': f'Specialty is missing, or is less than 2 characters'}, 400
            new_therapy = Therapy(name=name, location=location, special=special)
            therapy = new_therapy.create()
            # success returns json of user
            if therapy:
                    #return jsonify(user.read())
                    return therapy.read()
                # failure returns error
            return {'message': f'Record already exists'}, 400   

    # building RESTapi endpoint, method distinguishes action
    api.add_resource(_Read, '/')
    api.add_resource(_Create, '/create')
