from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import uuid

metadata = MetaData()
db = SQLAlchemy()

def get_uuid():
    return str(uuid.uuid4())

class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Food(id={self.id}, name='{self.name}', image='{self.image}', description='{self.description}', price={self.price})"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String, primary_key=True, default=get_uuid)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-Many relationship with Review model
    reviews = db.relationship('Review', backref='user', lazy=True)

    # One-to-Many relationship with Address model
    addresses = db.relationship('Address', backref='user', lazy=True)

    def __repr__(self):
        return f'User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, phone={self.phone}, created_at={self.created_at})'

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.String, primary_key=True, default=get_uuid)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Review(id={self.id}, user_id={self.user_id}, rating={self.rating}, feedback='{self.feedback}', created_at={self.created_at})"

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    city = db.Column(db.String, nullable=False)
    area = db.Column(db.String, nullable=False)
    street = db.Column(db.String, nullable=False)
    building = db.Column(db.String, nullable=False)
    room = db.Column(db.String, nullable=False)
    notes = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"Address(id={self.id}, user_id={self.user_id}, city='{self.city}', area='{self.area}', street='{self.street}', building='{self.building}', room='{self.room}', notes='{self.notes}')"
