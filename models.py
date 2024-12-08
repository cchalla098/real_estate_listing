#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///realestate.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)

# User Model
user_favorites = Table(
    'user_favorites',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('property_id', Integer, ForeignKey('property.id'), primary_key=True)
)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    full_name=db.Column(db.String(100), unique=False, nullable=False)
    email=db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    user_type =  db.Column(db.String(200), nullable=False)
    properties = db.relationship('Property', backref='owner', lazy=True)
    favorites = relationship('Property', secondary=user_favorites, backref='liked_by')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
   


# Property Model
class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    amenities = db.Column(db.String(200))
    images = db.Column(db.String(500))  # stores image file paths, comma-separated
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

