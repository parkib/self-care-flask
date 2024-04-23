from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
# Change variable name and API name and prefix

from model.hotlines import Hotline
hotline_api = Blueprint('hotline_api', __name__,
                   url_prefix='/api/hotlines')
# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(hotline_api)
class HotlineAPI:
    class _Read(Resource):
        def get(self):
            hotlines = Hotline.query.all()
            json_ready = [hotline.read() for hotline in hotlines]
            return jsonify(json_ready)
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate location
            number = body.get('number')
            if number is None or len(number) < 2:
                return {'message': f'Number is missing, or is less than 2 characters'}, 400
            # success returns json of user
            if number:
                    #return jsonify(user.read())
                    return number.read()
                # failure returns error
            return {'message': f'Record already exists'}, 400
    # building RESTapi endpoint, method distinguishes action
    api.add_resource(_Read, '/')
    api.add_resource(_Create, '/create')