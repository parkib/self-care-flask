import json, jwt
from flask import Blueprint, make_response, request, jsonify, current_app, Response
from flask_restful import Api, Resource, reqparse
from datetime import datetime
from flask_cors import CORS

from model.quotes import Quote

quote_api = Blueprint('quote_api', __name__, url_prefix='/api/quotes')
api = Api(quote_api)
#CORS(quote_api)

class QuoteAPI:
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()
            quotename = body.get('quote')
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

    class _Read(Resource):
        def get(self):
            quotes = Quote.query.all()
            json_ready = [quote.read() for quote in quotes]
            return jsonify(json_ready)

api.add_resource(QuoteAPI._CRUD, '/write')
api.add_resource(QuoteAPI._Create, '/create')
api.add_resource(QuoteAPI._Read, '/read')