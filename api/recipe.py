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
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            recipename = body.get('recipename')
            healthyingredients = body.get('healthyingredients')
            recipesteps = body.get('recipesteps')
            difficulty = body.get('difficulty')
            tags = body.get('tags')
            new_recipe = Recipe(recipename=recipename, healthyingredients=healthyingredients, recipesteps=recipesteps, difficulty=difficulty, tags = tags)
            recipe = new_recipe.create()
            # success returns json of user
            return jsonify(new_recipe.read()) 
        
    class _Filter(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            tags = body.get('tags')
            # Split tags string into a list of tags
            tags_list = tags.split(',') if tags else []
            # Query recipes that have any of the specified tags
            recipes = Recipe.query.all()
            # Filter recipes based on tags
            if len(tags_list) == 1:
                filtered_recipes = [recipe.read() for recipe in recipes if tags_list[0] in recipe.tags.split(',')]
            else:
                filtered_recipes = [recipe.read() for recipe in recipes if all(tag in recipe.tags.split(',') for tag in tags_list)]
            return jsonify(filtered_recipes)




        
            
    api.add_resource(_Read, '/read')
    api.add_resource(_Create, '/make')
    api.add_resource(_Filter, '/search')
    
