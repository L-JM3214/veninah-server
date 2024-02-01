from flask import Flask, make_response, jsonify, request, json, session
from configuration import db, mash,api,app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import Address, Food, User, Review, Location, Reservation, Order, OrderItem
from requests.auth import HTTPBasicAuth
from flask_restful import Api, Resource, reqparse
import requests
# import base64
from datetime import datetime



class Index(Resource):
    def get(self):
        return make_response(
            "Venina API", 200
        )
        
api.add_resource(Index, '/')

        
def User_details(user):
    return make_response(
        {"id": user.id,
        "first_name":user.first_name,
        "last_name":user.last_name,
        "email":user.email,
        "phone":user.phone,
        "password":user.password},200
    )        
  
class Login(Resource):
    def post(self):
        user_signIn = request.get_json()
        password = user_signIn['password']
        user = User.query.filter_by(email=user_signIn['email']).first()

        if user:
            if user.authenticate(password):
                session['user'] = user.email
                return User_details(user)

            return "Enter Correct Username or Password" , 400
        return "No such user exists" , 404       

api.add_resource(Login, '/login')

class CheckSession(Resource):
    def get(self):
        user = session.get('user')
        user_info = User.query.filter_by(email=user).first()
    
        if user:
            return User_details(user_info)

        return "Please signIn to continue", 404

api.add_resource(CheckSession, '/checksession')

class Logout(Resource):
    def delete(self):
        user = session.get('user')

        if user:
            session['user'] = None

            return "LogOut Successful", 200
        return make_response("Method not allowed", 404)

api.add_resource(Logout, '/logout')

class UserSchema(mash.SQLAlchemySchema):

    class Meta:
        model=User
        
    id= mash.auto_field()
    first_name=mash.auto_field()
    last_name=mash.auto_field()
    email=mash.auto_field()
    phone=mash.auto_field()
    first_name=mash.auto_field()
    
    url = mash.Hyperlinks(
        {
        "self":mash.URLFor(
            "userbyid",
            values=dict(id="<id>")),
        "collection":mash.URLFor("users")
        }
)   
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Users(Resource):
    def get(self):
        users = User.query.all()
        
        return make_response(
            users_schema.dump(users), 200
        )

api.add_resource(Users, '/users')

if __name__ == '__main__':
    app.run(port=5000, debug=True)