import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from software_store_app import models
import string
import random

# Create Flask app
editor_app = Flask(__name__)
editor_app.config['SECRET_KEY'] = 'aghrghealvn3451'
editor_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///software_store.db'
editor_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(editor_app)
login_manager.login_view = 'editor_login'

# Initialize SQLAlchemy as a standalone instance
editor_db = SQLAlchemy()

# Initialize the database with the app
editor_db.init_app(editor_app)

# Create models using our local database instance
class LocalUser(editor_db.Model, UserMixin):
    __tablename__ = 'user'
    id = editor_db.Column(editor_db.Integer, primary_key=True)
    username = editor_db.Column(editor_db.String(80), unique=True, nullable=False)
    email = editor_db.Column(editor_db.String(120), unique=True, nullable=False)
    password_hash = editor_db.Column(editor_db.String(128))
    is_admin = editor_db.Column(editor_db.Boolean, default=False)
    purchases = editor_db.relationship('LocalPurchase', backref='user', lazy=True)

class LocalSoftware(editor_db.Model):
    __tablename__ = 'software'
    id = editor_db.Column(editor_db.Integer, primary_key=True)
    name = editor_db.Column(editor_db.String(100), nullable=False)
    description = editor_db.Column(editor_db.Text, nullable=False)
    price = editor_db.Column(editor_db.Float, nullable=False)
    image_url = editor_db.Column(editor_db.String(200))
    license_key = editor_db.Column(editor_db.String(100), unique=True, nullable=False)
    created_at = editor_db.Column(editor_db.DateTime, default=models.datetime.utcnow)
    purchases = editor_db.relationship('LocalPurchase', backref='software', lazy=True)

class LocalPurchase(editor_db.Model):
    __tablename__ = 'purchase'
    id = editor_db.Column(editor_db.Integer, primary_key=True)
    user_id = editor_db.Column(editor_db.Integer, editor_db.ForeignKey('user.id'), nullable=False)
    software_id = editor_db.Column(editor_db.Integer, editor_db.ForeignKey('software.id'), nullable=False)
    purchase_date = editor_db.Column(editor_db.DateTime, default=editor_db.func.current_timestamp())
    license_key = editor_db.Column(editor_db.String(100), nullable=False)

# Function to generate unique license key
def generate_license_key():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(20))

# Initialize the database
with editor_app.app_context():
    editor_db.create_all()

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return LocalUser.query.get(int(user_id))

# Make the Flask app instance available for import
app = editor_app

# Export our local models for use in routes
User = LocalUser
Software = LocalSoftware
Purchase = LocalPurchase

@app.route('/')
@login_required
def editor():
    users = User.query.all()
    software = Software.query.all()
    purchases = Purchase.query.all()
    return render_template('editor/editor.html', 
                         users=users, 
                         software=software, 
                         purchases=purchases)

@app.route('/editor/index')
@login_required
def editor_index():
    return redirect(url_for('editor'))

@app.route('/editor/login', methods=['GET', 'POST'])
def editor_login():
    if current_user.is_authenticated:
        return redirect(url_for('editor'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please fill in all fields')
            return redirect(url_for('editor_login'))
            
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('editor'))
        
        flash('Invalid email or password')
    return render_template('editor/login.html')

@app.route('/editor/register', methods=['GET', 'POST'])
def editor_register():
    if current_user.is_authenticated:
        return redirect(url_for('editor'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            flash('Please fill in all fields')
            return redirect(url_for('editor_register'))
            
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('editor_register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('editor_register'))
            
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('editor_register'))
            
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=False
        )
        editor_db.session.add(new_user)
        try:
            editor_db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('editor_login'))
        except Exception as e:
            editor_db.session.rollback()
            flash('An error occurred during registration')
            return redirect(url_for('editor_register'))
    return render_template('editor/register.html')

@app.route('/editor/logout')
@login_required
def editor_logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('editor_login'))

@app.route('/editor/admin')
@login_required
def editor_admin():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('editor'))
    return render_template('editor/admin.html')

@app.route('/editor/add_software', methods=['GET', 'POST'])
@login_required
def add_software():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('editor'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        image_url = request.form.get('image_url')
        
        if not all([name, description, price]):
            flash('Please fill in all required fields')
            return redirect(url_for('add_software'))
            
        new_software = Software(
            name=name,
            description=description,
            price=price,
            image_url=image_url,
            license_key=generate_license_key()
        )
        
        try:
            editor_db.session.add(new_software)
            editor_db.session.commit()
            flash('Software added successfully')
            return redirect(url_for('editor'))
        except Exception as e:
            editor_db.session.rollback()
            flash('Error adding software')
            return redirect(url_for('add_software'))
    
    return render_template('editor/add_software.html')

@app.route('/editor/edit_user/<int:user_id>')
@login_required
def editor_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('editor/edit_user.html', user=user)

@app.route('/editor/edit_software/<int:software_id>')
@login_required
def editor_edit_software(software_id):
    software = Software.query.get_or_404(software_id)
    return render_template('editor/edit_software.html', software=software)

@app.route('/editor/edit_purchase/<int:purchase_id>')
@login_required
def editor_edit_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    return render_template('editor/edit_purchase.html', purchase=purchase)

@app.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username', user.username)
        user.email = request.form.get('email', user.email)
        if request.form.get('password'):
            user.password_hash = generate_password_hash(request.form.get('password'))
        user.is_admin = bool(request.form.get('is_admin'))
        editor_db.session.commit()
        flash('User updated successfully')
        return redirect(url_for('editor'))
    
    return render_template('editor/edit_user.html', user=user)

@app.route('/software/<int:software_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_software(software_id):
    software = Software.query.get_or_404(software_id)
    
    if request.method == 'POST':
        software.name = request.form.get('name', software.name)
        software.description = request.form.get('description', software.description)
        software.price = float(request.form.get('price', software.price))
        software.image_url = request.form.get('image_url', software.image_url)
        if not software.license_key:
            software.license_key = generate_license_key()
        editor_db.session.commit()
        flash('Software updated successfully')
        return redirect(url_for('editor'))
    
    return render_template('editor/edit_software.html', software=software)

@app.route('/purchase/<int:purchase_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    
    if request.method == 'POST':
        purchase.user_id = request.form.get('user_id', purchase.user_id)
        purchase.software_id = request.form.get('software_id', purchase.software_id)
        purchase.license_key = request.form.get('license_key', purchase.license_key)
        editor_db.session.commit()
        flash('Purchase updated successfully')
        return redirect(url_for('editor'))
    
    return render_template('editor/edit_purchase.html', purchase=purchase)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
