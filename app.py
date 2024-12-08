#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from flask import Flask, abort, jsonify, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
from werkzeug.utils import secure_filename
from forms import LoginForm, RegisterForm, PropertyForm, SearchForm
from models import db, User, Property

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///realestate.db'
app.config['SECRET_KEY'] = 'secretkey'
app.config['UPLOAD_FOLDER'] = 'static/images'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Page Route
@app.route('/')
def index():
    properties = Property.query.all()
    # form = SearchForm()
    # return render_template('index.html', properties=properties, form=form)
    return render_template('index.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            if user.user_type=='owner':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('user'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data,full_name=form.full_name.data,user_type=form.user_type.data)
        # user.set_admin(true)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Admin Page
@app.route('/admin')
@login_required
def admin():
    if not current_user.user_type=='owner':
        return redirect(url_for('index'))
    properties = Property.query.all()
    users = User.query.all()
    return render_template('admin.html', properties=properties, users=users)

# User Page
@app.route('/user')
@login_required
def user():
    properties = Property.query.all()
    return render_template('user.html', properties=properties)

from flask import send_from_directory

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/images/', filename)
# Add Property (User Side)
@app.route('/add_property', methods=['GET', 'POST'])
@login_required
def add_property():
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        price = request.form.get('price')
        location = request.form.get('location')
        description = request.form.get('description')
        
        # Handle file upload
        file = request.files.get('image')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_path = f'uploads/{filename}'  # Save relative path
        else:
            flash("Please upload a valid image file", "error")
            return redirect(url_for('add_property'))

        # Save property to database
        try:
            new_property = Property(
                title=title,
                price=float(price),
                location=location,
                description=description,
                images=filename,
                owner_id=current_user.id  # Assuming properties are linked to users
            )
            db.session.add(new_property)
            db.session.commit()
            flash("Property added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding property: {str(e)}", "error")
            return redirect(url_for('add_property'))

        return redirect(url_for('user'))  # Redirect to dashboard to view properties

    return render_template('add_property.html')
# Search and Filter Properties
@app.route('/search', methods=['GET','POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query = Property.query
        if form.location.data:
            query = query.filter(Property.location.contains(form.location.data))
        if form.min_price.data:
            query = query.filter(Property.price >= form.min_price.data)
        if form.max_price.data:
            query = query.filter(Property.price <= form.max_price.data)
        if form.amenities.data:
            query = query.filter(Property.amenities.contains(form.amenities.data))
        
        properties = query.all()
        return render_template('search.html', properties=properties, form=form)
    return render_template('search.html', form=form)
@app.route('/property/<int:property_id>')
def property_details(property_id):
    property = Property.query.get_or_404(property_id)  # Fetch property or return 404 if not found
    return render_template('property_details.html', property=property)
# @app.route('/add_to_favorites/<int:property_id>', methods=['POST'])
# @login_required
# def add_to_favorites(property_id):
#     property = Property.query.get_or_404(property_id)
#     if property not in current_user.favorites:
#         current_user.favorites.append(property)  # Add to user's favorites
#         db.session.commit()
#         flash("Property added to favorites!", "success")
#     else:
#         flash("Property is already in your favorites!", "info")
#     return redirect(request.referrer or url_for('favorities'))
@app.route('/add_to_favorites/<int:property_id>', methods=['POST'])
@login_required
def add_to_favorites(property_id):
    property = Property.query.get_or_404(property_id)
    if property not in current_user.favorites:
        current_user.favorites.append(property)
        db.session.commit()
        return jsonify({'message': 'Property added to favorites!'}), 200
    return jsonify({'message': 'Property is already in favorites!'}), 400


# @app.route('/add_to_favorites/<int:property_id>', methods=['POST'])
# @login_required
# def add_to_favorites(property_id):
#     property = Property.query.get_or_404(property_id)
#     if property not in current_user.favorites:
#         current_user.favorites.append(property)
#         db.session.commit()
#         return jsonify({'message': 'Property added to favorites!'}), 200
#     return jsonify({'message': 'Property already in favorites!'}), 400

@app.route('/favorites', methods=['GET'])
@login_required
def view_favorites():
    favorites = current_user.favorites  # Fetch user's favorites
    return render_template('favorites.html', favorites=favorites)
@app.route('/remove_from_favorites/<int:property_id>', methods=['POST'])
@login_required
def remove_from_favorites(property_id):
    property = Property.query.get_or_404(property_id)
    if property in current_user.favorites:
        current_user.favorites.remove(property)
        db.session.commit()
        flash("Property removed from favorites.", "success")
    return redirect(url_for('view_favorites'))
from flask import session

@app.route('/buy_property/<int:property_id>', methods=['POST'])
@login_required
def buy_property(property_id):
    property = Property.query.get_or_404(property_id)

    # Delete the property from the database
    db.session.delete(property)
    db.session.commit()

    flash('Property bought successfully!', 'success')

    # Store property details in the session
    session['property'] = {
        'title': property.title,
        'location': property.location,
        'price': property.price,
        'image': property.images
    }

    return redirect(url_for('success'))

# @app.route('/buy_property/<int:property_id>', methods=['POST'])
# @login_required
# def buy_property(property_id):
#     property = Property.query.get_or_404(property_id)  # Get property or 404 error
#     db.session.delete(property)  # Delete property
#     db.session.commit()  # Save changes to the database
#     flash("Property bought successfully and removed from the listing.", "success")
#     return redirect(url_for('success',  title=property.title, 
#                             location=property.location, 
#                             price=property.price, 
#                             image=property.images))  # Redirect back to the dashboard
# # Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
@app.route('/success')
@login_required
def success():
    property = session.pop('property', None)  # Remove property data from session after use
    if not property:
        abort(404)  # Redirect if no data in session
    return render_template('success.html', **property)


@app.route('/normalsearch', methods=['GET', 'POST'] ,endpoint="normalsearch")
@login_required
def search_properties():
    properties = None
    query = None
    if request.method == 'POST':
        query = request.form.get('query', '').strip()  # Get the search query
        if query:
            properties = Property.query.filter(Property.title.ilike(f'%{query}%')).all() 
    # return redirect(url_for('success'))
     # Case-insensitive search
    return render_template('normalsearch.html', query=query, properties=properties)

@app.route('/dashboard')
@login_required  # Ensure only logged-in users can access this route
def dashboard():
    # Fetch all properties from the database
    properties = Property.query.all()

    # Pass the properties to the template
    return render_template('dashboard.html', properties=properties)

if __name__ == '__main__':
    app.run(debug=True)

