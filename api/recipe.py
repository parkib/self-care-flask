import json, jwt
from flask import Blueprint, make_response, request, jsonify, current_app, Response
from flask_restful import Api, Resource, reqparse # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.recipes import Recipe

recipe_api = Blueprint('recipe_api', __name__,
                   url_prefix='/api/recipes')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(recipe_api)

class RecipeAPI:        
    class _Read(Resource):
        def get(self):
            recipes = Recipe.query.all()
            json_ready = [recipe.read() for recipe in recipes]
            re = jsonify(json_ready)
            return re
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            ''' Avoid garbage in, error checking '''
            # validate name
            recipename = body.get('recipename')
            if recipename is None or len(recipename) < 2:
               return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            healthyingredients = body.get('healthyingredients')
            if healthyingredients is None or len(healthyingredients) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password
            recipesteps = body.get('recipesteps')
            difficulty = body.get('difficulty')
            if difficulty is None or len(difficulty) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            recipe = Recipe(recipename=recipename, healthyingredients=healthyingredients, recipesteps=recipesteps, difficulty = difficulty)
            ''' Additional garbage error checking '''
                
            ''' #2: Key Code block to add user to database '''
            # create user in database
            recipe = recipe.create()
            # success returns json of user
            if recipe:
                #return jsonify(user.read())
                return recipe.read()    
            # failure returns error
            return {'message': f'Processed {recipename}, either a format error or '}, 400

        def get(self): # Read Method, the _         indicates current_user is not used
            recipes = Recipe.query.all()    # read/extract all users from database
            json_ready = [recipe.read() for recipe in recipes]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
                
                    
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            recipename = body.get('recipename')
            healthyingredients = body.get('healthyingredients')
            recipesteps = body.get('recipesteps')
            difficulty = body.get('difficulty')
            new_recipe = Recipe(recipename=recipename, healthyingredients=healthyingredients, recipesteps=recipesteps, difficulty=difficulty)
            recipe = new_recipe.create()
            # success returns json of user
            return jsonify(new_recipe.read()) 


            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Read, '/read')
    api.add_resource(_Create, '/make')