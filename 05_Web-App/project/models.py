from flask_login import UserMixin

from . import db

# Create a user model with attributes

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    weight = db.Column(db.String(1000))
    height = db.Column(db.String(1000))
    age = db.Column(db.String(1000))