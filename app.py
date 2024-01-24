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

consumer_key='7GSlEmZiocYKga9acUBDyIYiuJqOvZvHd6XGzbcVZadPm93f'
consumer_secret='Vh2mvQS4GKyo6seUtpAApN1plTwMDTeqyGZNBEtESYH05sBfRMSddn5vnlJ4zifA'

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

@app.route('/user/id/<email>', methods=['GET'])
def get_user_id_by_email(email):
    user = User.query.filter_by(email=email).first()

    if user:
        response_body = {
            "user_id": user.id
        }
        return make_response(jsonify(response_body), 200)
    else:
        return make_response(jsonify({"error": "User not found"}), 404)

def generate_access_token():
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(mpesa_auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = response.json()
    return data.get('access_token', '')


@app.route('/access_token')
def token():
    return jsonify({"access_token": generate_access_token()})


@app.route('/stk_push', methods=['POST'])
def initiate_stk_push():
    token = generate_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortCode = "174379"  # vevinah paybill here
    passkey = "7a6d95bf0a510e19e08c9881e8b48a03"  # vevinah passkey here
    stk_password = base64.b64encode((shortCode + passkey + timestamp).encode('utf-8')).decode('utf-8')

 
    # sandbox
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    # live
    # url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    data = request.get_json()

    requestBody = {
        "BusinessShortCode": shortCode,
        "Password": stk_password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",  # or "CustomerBuyGoodsOnline"
        "Amount": data.get('amount', ''),  
        "PartyA": data.get('phone_number', ''),  
        "PartyB": shortCode,
        "PhoneNumber": data.get('phone_number', 'name'),  
        "CallBackURL": "http://127.0.0.1:5000/callback",
        "AccountReference": "account",
        "TransactionDesc": "test"
    }

    try:
        response = requests.post(url, json=requestBody, headers=headers)
        print(response.json())
        return response.json()
    except Exception as e:
        print('Error:', str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/mpesa_transaction', methods=['POST'])
def mpesa_transaction():

    data = request.get_json()

    user_email = data.get('user_email', '')
    user = User.query.filter_by(email=user_email).first()

    if user:
        user.mpesa_access_token = data.get('access_token', '')
        user.mpesa_transaction_code = data.get('transaction_code', '')
        db.session.commit()

        return jsonify({"message": "M-Pesa transaction information saved successfully"})
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/get_mpesa_transaction/<email>', methods=['GET'])
def get_mpesa_transaction(email):
    # M-Pesa transaction - one user
    user = User.query.filter_by(email=email).first()

    if user:
        response_body = {
            "user_email": user.email,
            "mpesa_access_token": user.mpesa_access_token,
            "mpesa_transaction_code": user.mpesa_transaction_code,
        }
        return make_response(jsonify(response_body), 200)
    else:
        return make_response(jsonify({"error": "User not found"}), 404)

@app.route('/all_mpesa_transactions', methods=['GET'])
def get_all_mpesa_transactions():
    all_transactions = User.query.filter(User.mpesa_transaction_code.isnot(None)).all()

    transactions_data = []
    for user in all_transactions:
        transaction_data = {
            "user_email": user.email,
            "mpesa_access_token": user.mpesa_access_token,
            "mpesa_transaction_code": user.mpesa_transaction_code,
        }
        transactions_data.append(transaction_data)

    return make_response(jsonify(transactions_data), 200)

@app.route('/callback', methods=['POST'])
def handle_callback():
    callback_data = request.json

    result_code = callback_data['Body']['stkCallback']['ResultCode']
    if result_code != 0:
        error_message = callback_data['Body']['stkCallback']['ResultDesc']
        response_data = {'ResultCode': result_code, 'ResultDesc': error_message}
        return jsonify(response_data)

    callback_metadata = callback_data['Body']['stkCallback']['CallbackMetadata']
    transaction_data = {}
    for item in callback_metadata['Item']:
        transaction_data[item['Name']] = item['Value']

    save_transaction_to_json(transaction_data) #saved to json 

    response_data = {'ResultCode': result_code, 'ResultDesc': 'Success'}
    return jsonify(response_data)

def save_transaction_to_json(data):
    try:
        with open('mpesa_transactions.json', 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    existing_data.append(data)

    with open('mpesa_transactions.json', 'w') as file:
        json.dump(existing_data, file, indent=2)


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
