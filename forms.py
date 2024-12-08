#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, FileField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    full_name=StringField('Username', validators=[DataRequired()])
    email=StringField('Username', validators=[DataRequired()])
    user_type=StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Register')

class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    amenities = StringField('Amenities')
    images = FileField('Upload Images')
    submit = SubmitField('Add Property')

class SearchForm(FlaskForm):
    location = StringField('Location')
    min_price = FloatField('Min Price')
    max_price = FloatField('Max Price')
    amenities = StringField('Amenities')
    submit = SubmitField('Search')

