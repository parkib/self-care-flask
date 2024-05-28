import json, jwt
from flask import Blueprint, make_response, request, jsonify, current_app, Response
from flask_restful import Api, Resource, reqparse # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password
            password = body.get('password')
            uo = User(name=name, #user name
                        uid=uid, diary = "", sleep="", exercise="", profile="", image_path = "")
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            # if dob is not None:
            #     try:
            #         uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
            #     except:
            #         return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            # if tracking is not None:
            #     uo.tracking = tracking
            
            # if exercise is not None:
            #     uo.exercise = exercise
                
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                #return jsonify(user.read())
                return user.read()
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        def get(self): # Read Method, the _ indicates current_user is not used
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
   
        def delete(self): # Delete Method
            body = request.get_json()
            uid = body.get('uid')
            user = User.query.filter_by(_uid=uid).first()
            if user is None:
                return {'message': f'User {uid} not found'}, 404
            json = user.read()
            user.delete() 
            # 204 is the status code for delete with no json response
            return f"Deleted user: {json}", 204 # use 200 to test with Postman
         
    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                ''' Get Data '''
                uid = body.get('uid')
                if uid is None:
                    return {'message': f'User ID is missing'}, 401
                password = body.get('password')

                ''' Find user '''
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 401
                if user:
                    try:
                        token = jwt.encode(
                            {"_uid": user._uid},
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        resp_data = {
                        "message": "Authentication for %s successful" % (user._uid),
                        "name": user.name,
                        "id": user.id
                        }
                        resp = jsonify(resp_data)
                        resp.set_cookie(current_app.config["JWT_TOKEN_NAME"],
                                token,
                                max_age=3600,
                                secure=True,
                                httponly=True,
                                path='/',
                                samesite='None'
                        )
                        return resp
                    except Exception as e:
                        return {
                            "error": "Something went wrong guys",
                            "message": str(e)
                        }, 500
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404
            except Exception as e:
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 500
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            name = body.get('name')
            uid = body.get('uid')
            password = body.get('password')
            new_user = User(name=name, uid=uid, password=password, diary = '', exercise='', sleep='', profile='', image_path = '')
            user = new_user.create()
            # success returns json of user
            if user:
                    #return jsonify(user.read())
                    return user.read()
                # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400   
    class _Logout(Resource):
        def post(self):
            # Create a response to remove the JWT cookie
            resp = make_response(jsonify({"message": "Logout successful"}))
            resp.set_cookie("jwt", "", expires=0)  # Clear the JWT cookie
            return resp
    
    class _UD(Resource):        
        def put(self, user_id):
            body = request.get_json()
            user_id = body.get('id')
            if user_id is None:
                return {'message': 'Id not found.'}, 400
            user = User.query.filter_by(id=user_id).first()  # Use filter_by to query by UID
            if user:
                updated_fields = False

                if 'exercise' in body:
                    user.exercise = body['exercise']
                    updated_fields = True

                if 'sleep' in body:
                    user.sleep = body['sleep']
                    updated_fields = True

                if 'profile' in body:
                    user.profile = body['profile']
                    updated_fields = True

                if 'image_path' in body:
                    user.image_path = body['image_path']
                    updated_fields = True

                if 'diary' in body:
                    diary = body.get('diary')
                    user.update("", "", "", user._diary + "||" + diary, "", "", "", "")
                    updated_fields = True

                if updated_fields:
                    user.update()
                    return user.read()
                else:
                    return {'message': 'No valid fields to update.'}, 400

            return {'message': 'User not found.'}, 404
        def get(self, user_id):
            user = User.query.filter_by(id=user_id).first()
            if user:
                return user.read()  # Assuming you have a 'read' method in your User model
            return {'message': 'User not found.'}, 404
        def patch(self, user_id):    
            user = User.query.get(user_id)
            if not user:
                return {'message': 'User not found'}, 404
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, required=True, help='New name is required')
            args = parser.parse_args()
            try:
                user.updatename(new_name=args['name'])
                return user.read(), 200
            except Exception as e:
                # Handle the exception (e.g., log the error or return an error response)
                return {'message': f'Error updating name: {str(e)}'}, 500
    class _Diary(Resource):
        #retrieving data for all users in database
        def get(self, user_id):
            body = request.get_json()
            user_id = body.get("id")
            if user_id is None:
                return {'message': 'Id not found.'}, 400
            users = User.query.all()
            for user in users:
                if user.uid == user_id:    
                    jsonData = user.diary
                    print(jsonData)
                    return user.diary
            return jsonify(jsonData)
                
        #Diary api code
        def put(self, user_id):
            body = request.get_json()
            user_id = body.get("id")
            if user_id is None:
                return {'message': 'Id not found.'}, 400
            diary = body.get('diary')
            users = User.query.all()
            for user in users:
                if user.uid == user_id:    
                    user.update("", "", "", user._diary + "||" + diary, "", "")
                    return user.read()

        #Posting diary data
        def post(self):
            token = request.cookies.get("jwt")
            data = jwt.decode(token, 
                            current_app.config["SECRET_KEY"], 
                            algorithms=["HS256"])
            users = User.query.all()
            for user in users:
                if user.uid == data["_uid"]:    
                    return user.diary
    class _Bio(Resource):
        #retrieving data for all users in database
        def get(self):
            token = request.cookies.get("jwt")
            data = jwt.decode(token, 
                            current_app.config["SECRET_KEY"], 
                            algorithms=["HS256"])
            users = User.query.all()
            for user in users:
                if user.uid == data["_uid"]:    
                    jsonData = user.profile
                    print(jsonData)
                    return user.profile
            return jsonify(jsonData)

            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Create, '/create')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(_Diary, '/diary/<int:user_id>')
    api.add_resource(_UD, '/<int:user_id>') 
    api.add_resource(_Logout, '/logout') 
