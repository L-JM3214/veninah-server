from flask import Flask
# from flask_bcrypt import Bcrypt
# from flask_marshmallow import Marshmallow, schema
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# from flask_session import Session
# from flask_admin import Admin

app = Flask(__name__)

db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE']='sqlalchemy'
app.config['SESSION_SQLALCHEMY']=db
app.config['SECRET_KEY'] = 'no_key'

migrate = Migrate(app, db)
CORS(app)

# Session(app)
# bcrypt = Bcrypt(app)
# mash = Marshmallow(app)
db.init_app(app)
