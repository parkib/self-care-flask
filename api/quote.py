import json, jwt
from flask import Blueprint, make_response, request, jsonify, current_app, Response
from flask_restful import Api, Resource, reqparse
from datetime import datetime
from auth_middleware import token_required
from flask_cors import CORS

from model.quotes import Quote

quote_api = Blueprint('quote_api', __name__,
                   url_prefix='/api/quotes')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(quote_api)
CORS(quote_api)

class QuoteAPI:
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()
            quotename = body.get('quotename')
            quoteauthor = body.get('quoteauthor')
            opinion = body.get('opinion')
            quote = Quote(quotename=quotename, quoteauthor=quoteauthor, opinion=opinion)
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
            new_quote = Quote(quotename=quotename, quoteauthor=quoteauthor, opinion=opinion)
            quote = new_quote.create()
            return jsonify(quote.read())
            # return jsonify({
            #     "id": 1,
            #     "quotename": "c1",
            #     "quoteauthor": "c1",
            #     "opinion": "c1"
            #     })

    class _Read(Resource):
        def get(self):
            quotes = Quote.query.all()
            json_ready = [quote.read() for quote in quotes]
            return jsonify(json_ready)
            # return jsonify({
            #     "id": 1,
            #     "quotename": "c1",
            #     "quoteauthor": "c1",
            #     "opinion": "c1"
            #     })

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Read, '/read')
    api.add_resource(_Create, '/build')