import json, jwt
from flask import Blueprint, make_response, request, jsonify, current_app, Response
from flask_restful import Api, Resource, reqparse # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.quotes import Quote

quote_api = Blueprint('quote_api', __name__,
                   url_prefix='/api/quotes')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(quote_api)

class QuoteAPI:        
    class _Read(Resource):
        def get(self):
            quotes = Quote.query.all()
            json_ready = [quote.read() for quote in quotes]
            re = jsonify(json_ready)
            return re
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            ''' Avoid garbage in, error checking '''
            # validate name
            quotename = body.get('quote')
            #if recipename is None or len(recipename) < 2:
             #   return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            quoteauthor = body.get('quote_author')
            #if healthyingredients is None or len(healthyingredients) < 2:
               # return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password
            opinion = body.get('opinion')
            #if difficulty is None or len(difficulty) < 2:
             #   return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            quote = Quote(quotename=quote, quoteauthor=quoteauthor, opinion=opinion)
            ''' Additional garbage error checking '''
                
            ''' #2: Key Code block to add user to database '''
            # create user in database
            quote = quote.create()
            # success returns json of user
            if quote:
                #return jsonify(user.read())
                return quote.read()    
            # failure returns error
            return {'message': f'Processed {quotename}, either a format error or '}, 400

        def get(self): # Read Method, the _         indicates current_user is not used
            quotes = Quote.query.all()    # read/extract all users from database
            json_ready = [quote.read() for quote in quotes]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
                
                    
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            quotename = body.get('quotename')
            quoteauthor = body.get('quoteauthor')
            opinion = body.get('opinion')
            new_quote = Quote(quotename=quotename, quoteauthor=quoteauthor, opinion=opinion)
            quote = new_quote.create()
            # success returns json of user
            return jsonify(quote.read()) 


            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Read, '/look')
    api.add_resource(_Create, '/write')