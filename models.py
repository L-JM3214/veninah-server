from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData()

db = SQLAlchemy()

class Food(db.Model):

    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    image = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    price = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Food(id={self.id}, name='{self.name}', image='{self.image}', description='{self.description}', price={self.price})"
 