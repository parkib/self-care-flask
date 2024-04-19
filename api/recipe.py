from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.recipes import Recipe

# Change variable name and API name and prefix
recipe_api = Blueprint('recipe_api', __name__,
                   url_prefix='/api/recipe')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(recipe_api)

class RecipeAPI:     
    class _Read(Resource):
        def get(self):
            recipes = Recipe.query.all()
            json_ready = [recipe.read() for recipe in recipes]
            return jsonify(json_ready)
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            recipename = body.get('recipename')
            if recipename is None or len(recipename) < 2:
                return {'message': f'Recipe name is missing, or is less than 2 characters'}, 400
            # validate location
            healthyingredients = body.get('healthyingredients')
            if healthyingredients is None or len(healthyingredients) < 2:
                return {'message': f'Healthy Ingredients are missing, or is less than 2 characters'}, 400
            # validate location
            difficulty = body.get('difficulty')
            if difficulty is None or len(difficulty) < 2:
                return {'message': f'Difficulty of recipe is missing, or is less than 2 characters'}, 400
            new_recipe = Recipe(recipename=recipename, healthyingredients=healthyingredients, difficulty=difficulty)
            recipe = new_recipe.create()
            # success returns json of user
            if recipe:
                    #return jsonify(user.read())
                    return recipe.read()
                # failure returns error
            return {'message': f'Record already exists'}, 400   

    # building RESTapi endpoint, method distinguishes action
    api.add_resource(_Read, '/')
    api.add_resource(_Create, '/create')
