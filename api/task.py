import json
import jwt
from flask import Blueprint, make_response, request, jsonify, current_app, Response
from flask_restful import Api, Resource, reqparse  # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.tasks import Task

task_api = Blueprint('task_api', __name__,
                     url_prefix='/api/tasks')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(task_api)


def bubble_sort_by_deadline(tasks, sortOrder):
    n = len(tasks)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            date1 = datetime.strptime(tasks[j]['taskdeadline'], '%m/%d/%Y')
            date2 = datetime.strptime(tasks[j + 1]['taskdeadline'], '%m/%d/%Y')
            if sortOrder == 'asc':
                if date1 > date2:
                    tasks[j], tasks[j + 1] = tasks[j + 1], tasks[j]
            else:
                if date1 < date2:
                    tasks[j], tasks[j + 1] = tasks[j + 1], tasks[j]
    return tasks


class TaskAPI:
    class _Read(Resource):
        def get(self):
            tasks = Task.query.all()
            json_ready = [task.read() for task in tasks]
            re = jsonify(json_ready)
            return re

    class _Create(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            taskname = body.get('taskname')
            if taskname is None or len(taskname) < 2:
                return {'message': f'Task name is missing, or is less than 2 characters'}, 400
            taskdeadline = body.get('taskdeadline')
            if taskdeadline is None or len(taskdeadline) < 2:
                return {'message': f'Task deadline is missing, or is less than 2 characters'}, 400
            taskdescription = body.get('taskdescription')
            if taskdescription is None or len(taskdescription) < 2:
                return {'message': f'Task description is missing, or is less than 2 characters'}, 400
            taskpriority = body.get('taskpriority')
            if taskpriority is None or len(taskpriority) < 2:
                return {'message': f'Priority of task is missing, or is less than 2 characters'}, 400
            new_task = Task(taskname=taskname, taskdeadline=taskdeadline, taskdescription=taskdescription,
                            taskpriority=taskpriority)
            task = new_task.create()
            # success returns json of user
            return jsonify(new_task.read())

    class _Sort(Resource):
        def post(self):
            body = request.get_json()
            if body:
                sortBy = body.get('sortBy')
                sortOrder = body.get('sortOrder')
                priority = body.get('priority')
                if sortBy and sortOrder:  # Check if sortBy and sortOrder are not None
                    tasks = Task.query.all()
                    json_ready = [task.read() for task in tasks]
                    if sortBy == 'priority':
                        if priority == 'high':
                            json_ready = [task for task in json_ready if task['taskpriority'] == 'high']
                        elif priority == 'medium':
                            json_ready = [task for task in json_ready if task['taskpriority'] == 'medium']
                        elif priority == 'low':
                            json_ready = [task for task in json_ready if task['taskpriority'] == 'low']
                    elif sortBy == 'deadline':
                        json_ready = bubble_sort_by_deadline(json_ready, sortOrder)  # using bubble sort to sort the deadlines
                    return json_ready
                else:
                    return {"error": "sortBy and sortOrder are required in the request body."}, 400
            else:
                return {"error": "Request body is empty or not in JSON format."}, 400


# building RESTapi endpoint
# api.add_resource(_CRUD, '/')
api.add_resource(TaskAPI._Read, '/read')
api.add_resource(TaskAPI._Create, '/create')
api.add_resource(TaskAPI._Sort, '/sort')
