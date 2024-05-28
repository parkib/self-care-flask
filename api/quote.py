import json, jwt
from flask import Blueprint, make_response, request, jsonify, current_app, Response
from flask_restful import Api, Resource, reqparse
from datetime import datetime
from auth_middleware import token_required
from flask_cors import CORS


from model.quotes import Quote


quote_api = Blueprint('quote_api', __name__, url_prefix='/api/quotes')
api = Api(quote_api)
CORS(quote_api)


class QuoteAPI:
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()
            quotename = body.get('quotename')
            quoteauthor = body.get('quoteauthor')
            opinion = body.get('opinion')
            rating = body.get('rating')
            quote = Quote(quotename=quotename, quoteauthor=quoteauthor, opinion=opinion, rating=rating)
            quote = quote.create()
            if quote:
                return quote.read()
            return {'message': f'Processed {quotename}, either a format error or '}, 400


        def get(self):
            quotes = Quote.query.all()
            json_ready = [quote.read() for quote in quotes]
            return jsonify(json_ready)


    class _Create(Resource):
        def post(self):
            body = request.get_json()
            quotename = body.get('quotename')
            quoteauthor = body.get('quoteauthor')
            opinion = body.get('opinion')
            rating = body.get('rating')
            new_quote = Quote(quotename=quotename, quoteauthor=quoteauthor, opinion=opinion, rating=rating)
            quote = new_quote.create()
            return jsonify(quote.read())


    class _Read(Resource):
        def get(self):
            quotes = Quote.query.all()
            json_ready = [quote.read() for quote in quotes]
            return jsonify(json_ready)


    class _FilterByRating(Resource):
        def get(self, rating):
            quotes = Quote.query.filter_by(rating=rating).all()
            json_ready = [quote.read() for quote in quotes]
            return jsonify(json_ready)


    api.add_resource(_CRUD, '/')
    api.add_resource(_Read, '/read')
    api.add_resource(_Create, '/make')
    api.add_resource(_FilterByRating, '/filter/<int:rating>')