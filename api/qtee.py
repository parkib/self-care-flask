import json, jwt
from flask import Blueprint, make_response, request, jsonify, current_app, Response
from flask_restful import Api, Resource, reqparse # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.qtees import Qt1

qt1_api = Blueprint('qt1_api', __name__,
                   url_prefix='/api/qt1')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(qt1_api)

class qt1API:        
    class _Read(Resource):
        def get(self):
            qt1 = qt1.query.all()
            json_ready = [qt1.read() for qt1 in qt1]
            re = jsonify(json_ready)
            return re
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            ''' Avoid garbage in, error checking '''
            # validate name
            qt1name = body.get('qt1name')
            #if difficulty is None or len(difficulty) < 2:
             #   return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            qt11 = Qt1(qt1name=qt1name)
            ''' Additional garbage error checking '''
                
            ''' #2: Key Code block to add user to database '''
            # create user in database
            qt1 = qt11.create()
            # success returns json of user
            if qt1:
                #return jsonify(user.read())
                return qt1.read()    
            # failure returns error
            return {'message': 'Processed'}, 400

        def get(self): # Read Method, the _         indicates current_user is not used
            qt1 = qt1.query.all()    # read/extract all users from database
            json_ready = [qt1.read() for qt1 in qt1]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
                
                    
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            qt1name = body.get('qt1name')
            new_qt1 = qt1(qt1name=qt1name)
            qt1 = new_qt1.create()
            # success returns json of user
            return jsonify(qt1.read())
            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Read, '/read')
    api.add_resource(_Create, '/make')