from configuration import app, db
import json
from faker import Faker
from models import Food,User

fake = Faker()

with open("/Users/markmutugi/Development/code/phase5/project/veninah-server/db.json" , mode='r') as menu_data:
    data = json.load(menu_data)

foods = data['foods']

with app.app_context():
    
    Food.query.delete()
    User.query.delete()
    
    food_list = []
    
    for food_item in foods:

        
        food = Food(
            name = food_item['name'],
            category = food_item['category'],
            image=food_item['image'],
            description= food_item['description'],
            price= food_item['price'],
                 
        )
        
        food_list.append(food) 
         
        db.session.add(food)
    db.session.commit()
        
    for i in range(20):
        user = User(
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            email = fake.email(),
            password = fake.password(),
            
            phone = fake.phone_number(),
        )
        db.session.add(user)
        db.session.commit()

