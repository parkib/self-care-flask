from contextlib import nullcontext
from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import time
from flask import Blueprint, request, jsonify
import json
import requests
import random
from flask import request

kpop_api = Blueprint('kpop_api', __name__,
                  url_prefix='/api/kpop')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(kpop_api)

def beautify_json_data(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        beautified_data = []
        for item in data.get('items', []):
            beautified_item = {
                "id": item.get("id", 0),
                "song": item.get("song", ""),
                "album": item.get("album", ""),
                "artist": item.get("artist", ""),
                "genre": item.get("genre", ""),
                "time": item.get("time", 0),
            }
            
            medium_icon_url = item.get("iconUrls", {}).get("icon", "")
            if medium_icon_url:
                beautified_item["icon"] = medium_icon_url

            medium_audio_url = item.get("audioUrls", {}).get("audio", "")
            if medium_audio_url:
                beautified_item["audio"] = medium_audio_url

            beautified_data.append(beautified_item)

        return beautified_data  # Return the processed data as a list

    except FileNotFoundError:
        return {"error": "File not found"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in the file"}


beautify_json_data("kpop.json")


# getJokes()
class _Read(Resource):
    def get(self):
        json_list = []
        json_list.append(beautify_json_data('model/kpop.json'))
        return jsonify(json_list)

class _ReadRandom(Resource):
    def get(self):
        beautified_data = beautify_json_data('model/kpop.json')
        random_item = random.choice(beautified_data)
        return jsonify(random_item)
    
class _Search(Resource):
    def get(self):
        query = request.args.get('query')  # Get the query parameter
        if not query:
            return {"error": "No query provided"}, 400

        beautified_data = beautify_json_data('model/kpop.json')
        results = [item for item in beautified_data if query.lower() in item['name'].lower()]

        return jsonify(results)

class _Count(Resource):
    def get(self):
        beautified_data = beautify_json_data('model/kpop.json')
        count = len(beautified_data)
        return {"count": count}

api.add_resource(_Read, '/')
api.add_resource(_ReadRandom, '/random')
api.add_resource(_Search, '/search')
api.add_resource(_Count, '/count')