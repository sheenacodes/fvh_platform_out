
from flask import jsonify, request
from flask_restful import Resource, Api, reqparse, abort
from datetime import datetime
from app import swagger
from flasgger.utils import swag_from
from app.models import PlatformUser,RevokedTokenModel
from app import db
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

users = {}

def validate_post_user(request):
    # todo check empty strings. enforce min length
        validation_status = True
        result = {}
        try:
            data = request.json
            if not ('username' in data and 'email' in data and 'password' in data):
                result = {'status' : "failure",
                'data': "Insufficient Data: Username, email, password are required"}
                validation_status = False

        except Exception as e:
            print(e)
            result = {'status' : "failure",
            'data': "Invalid Input, Check JSON schema"}
            validation_status = False
        
        response = jsonify(result)
        response.status_code = 400

        return validation_status, response

def db_error_response():
    result = {'status' : "failure",
            'data': "Database error"}
    response = jsonify(result)
    response.status_code = 400
    return response

class UserRegistration(Resource):

    @swag_from('user.yml')
    def post(self):
        """
        Post new user
        """
        validation_status, response = validate_post_user(request)

        if not validation_status:
            return response
        
        data = request.json
        print(data)
        
        try:
            user = PlatformUser.query.filter_by(username=data['username']).first()
        except Exception as e:
            print(e)
            return db_error_response()
        
        print(user)
        if user is not None :            
            result = {'status' : "failure",
            'data': "Username exists. Choose another"}
            return jsonify(result)
        
        try:
            email = PlatformUser.query.filter_by(email=data['email']).first()
        except Exception as e:
            print(e)
            return db_error_response()

        if email is not None :
            result = {'status' : "failure",
            '   data': "email exists. Choose another"}
            return jsonify(result)

        try:
            user = PlatformUser(username=data['username'], email=data['email'], password=data['password']) #,created_at = dt.now())
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()

            del data['password']
            result = {'status' : "success",
                      'data': data}
            response = jsonify(result)
            return jsonify(result)
        
        except Exception as e:
            print(e)

            return db_error_response()



class UserLogin(Resource):

    def post(self):
        print("login")
        # TODO need have only  username and password
        validation_status, response = validate_post_user(request)

        if not validation_status:
            return response

        data = request.json
        print(data)
        
        try:
            user = PlatformUser.query.filter_by(username=data['username']).first()
        except Exception as e:
            print(e)
            return db_error_response()

        if not user:
            result = {'status' : "failure",'data': "username not found"}
            return jsonify(result)

        if user.check_password(data['password']):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'User {} was logged in '.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            result = {'message': 'Wrong credentials'}
        
        return jsonify(result)


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        print(jti)
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            print(1)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      
      
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
    
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
      
      
class AllUsers(Resource):
    def get(self):
        return PlatformUser.return_all()

    def delete(self):
        return PlatformUser.delete_all()
      
      
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
