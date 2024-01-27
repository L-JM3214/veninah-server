from flask import Flask, make_response, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Food, User, Review, Address
from requests.auth import HTTPBasicAuth
import requests
import base64
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

#Mpesa
consumer_key='7GSlEmZiocYKga9acUBDyIYiuJqOvZvHd6XGzbcVZadPm93f'
consumer_secret='Vh2mvQS4GKyo6seUtpAApN1plTwMDTeqyGZNBEtESYH05sBfRMSddn5vnlJ4zifA'
base_url='https://1115-105-161-25-71.ngrok-free.app'

#Dishes API
@app.route('/dishes', methods=['GET'])
def get_foods():
    foods = []
    for food in Food.query.all():
        response_body = {
            "id": food.id,
            "name": food.name,
            "image": food.image,
            "description": food.description,
            "price": food.price
        }
        foods.append(response_body)

    response = make_response(
        jsonify(foods),
        200
    )
    return response

#register users
@app.route('/user', methods=['POST'])
def register_user():
    data = request.get_json()

    required_fields = ['first_name', 'last_name', 'email', 'phone', 'password']
    if not all(field in data for field in required_fields):
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return make_response(jsonify({"error": "User with this email already exists"}), 409)

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        password=data['password']
    )
    
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "phone": new_user.phone,
        "created_at": new_user.created_at,
    }

    return make_response(jsonify(response_body), 201)

#view users
@app.route('/user/<email>', methods=['GET'])
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    
    if user:
        response_body = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "created_at": user.created_at,
        }
        return make_response(jsonify(response_body), 200)
    else:
        return make_response(jsonify({"error": "User not found"}), 404)

#collect reviews
@app.route('/reviews', methods=['POST'])
def submit_review():
    data = request.get_json()

    required_fields = ['user_email', 'rating']
    if not all(field in data for field in required_fields):
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    user = User.query.filter_by(email=data['user_email']).first()
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    new_review = Review(
        user_id=user.id,
        rating=data['rating'],
        feedback=data.get('feedback', None)
    )

    db.session.add(new_review)
    db.session.commit()

    response_body = {
        "id": new_review.id,
        "user_email": data['user_email'],
        "rating": new_review.rating,
        "feedback": new_review.feedback,
        "created_at": new_review.created_at,
    }

    return make_response(jsonify(response_body), 201)

#collect address
@app.route('/address', methods=['POST'])
def add_address():
    data = request.get_json()

    required_fields = ['user_email', 'city', 'area', 'street', 'building', 'room']
    if not all(field in data for field in required_fields):
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    user = User.query.filter_by(email=data['user_email']).first()
    if not user:
        return make_response(jsonify({"error": "User not found"}), 404)

    new_address = Address(
        user_id=user.id,
        city=data['city'],
        area=data['area'],
        street=data['street'],
        building=data['building'],
        room=data['room'],
        notes=data.get('notes', None)
    )

    db.session.add(new_address)
    db.session.commit()

    response_body = {
        "id": new_address.id,
        "user_email": data['user_email'],
        "city": new_address.city,
        "area": new_address.area,
        "street": new_address.street,
        "building": new_address.building,
        "room": new_address.room,
        "notes": new_address.notes,
    }

    return make_response(jsonify(response_body), 201)

#access_token
@app.route('/access_token')
def token():
    data = ac_token
    return data


def ac_token():
        mpesa_auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        data= (requests.get(mpesa_auth_url, auth = HTTPBasicAuth(consumer_key, consumer_secret))).json()
        return data['access_token']

#register url
@app.route('/register_urls')
def register():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl" 
    headers = {"Authorization": "Bearer %s" % ac_token()}
    req_body = {
            "ShortCode": "174379",
            "ResponseType": "",
            "ConfirmationURL":base_url + "/c2b/confirm",
            "ValidationURL":base_url + "c2b/validation",
        },
    response_data = requests.post(
        mpesa_endpoint, 
        json = req_body,
        headers = headers)
    
    return response_data.json()
    
@app.route('/c2b/confirm')
def confirm():
    data = requests.get_json()
    #write to file
    file = open('./confirm.json', 'a')
    file.write(json.dumps(data))
    file.close()

    return {
        "ResponseCode": "0",
      "ResponseDescription": "Accept the service request successfully."
    }

@app.route('/c2b/validation')
def validate():
    data = requests.get_json()
    #write to file
    file = open('./confirm.json', 'a')
    file.write(json.dumps(data))
    file.close()

    return {
        "ResponseCode": "0",
      "ResponseDescription": "Accept the service request successfully."
    }

@app.route('/simulate')
def simulate():
    mpesa_endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
    access_token = ac_token()

    headers = {"Authorization": "Bearer %s" % ac_token()}
    request_body = {
        "ShortCode": "174379",
        "CommandID": "CustomerPayBillOnline",
        "BillRefNumber": "TestPay",
        "Msisdn":"254708374149",
        "Amount": 50
    }
    simulate_response = requests.post(mpesa_endpoint, json = request_body, headers=headers)

    return simulate_response.json()

if __name__ == '__main__':
    app.run(port=5000, debug=True)

# class FoodClass(Resource):
#     def post(self):
#         data = request.get_json()
#         new_food = Food(
#             id = data['id'],
#             name = data['name'],
#             image = data['image'],
#             description = data['description'],
#             price = data['price']

#         )
#         db.session.add(new_food)
#         db.session.commit()

#         response_data = {
#             "id":new_food.id,
#             "name":new_food.name,
#             "image":new_food.image,
#             "description":new_food.description,
#             "price":new_food.price
#         }

#         if new_food:
#             return make_response(
#                 jsonify(response_data),
#                 200
#             )
#         else:
#             return make_response(
#                 jsonify({
#                     "message": "Not found"
#                 })
#             )
        
# api.add_resource(FoodClass, '/foods')
