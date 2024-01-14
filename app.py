from flask import Flask, make_response, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from models import db, Food
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/dishes', methods = ['GET'])
def get_foods():

        foods = []
        for food in Food.query.all():
            response_body = {
                "id":food.id,
                "name": food.name,
                "image": food.image,
                "description": food.description,
                "price":food.price
            }
            foods.append(response_body)
        response = make_response(
            jsonify(foods),
            200
        )
        return response

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
