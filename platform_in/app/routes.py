from flask import Flask,request
from flask_restful import Resource, Api
from app import app
from app.resources.user import UserRegistration, UserLogin, UserLogoutAccess, UserLogoutRefresh, TokenRefresh, AllUsers, SecretResource
from app.resources.observations import Observation


api = Api(app)
api.add_resource(Observation, '/observation')

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(AllUsers, '/users')
api.add_resource(SecretResource, '/secret')