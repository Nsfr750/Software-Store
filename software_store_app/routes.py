from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from software_store_app import app, db
import string
import random
from software_store_app.models import User, Software, Purchase

@app.route('/')
def index():
    software = Software.query.all()
    return render_template('index.html', software=software)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        
        flash('Invalid email or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
            
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    users = User.query.all()
    software = Software.query.all()
    purchases = Purchase.query.all()
    return render_template('admin.html', users=users, software=software, purchases=purchases)

@app.route('/add_software', methods=['POST'])
@login_required
def add_software():
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    name = request.form.get('name')
    description = request.form.get('description')
    price = float(request.form.get('price'))
    image_url = request.form.get('image_url')
    license_key = request.form.get('license_key')
    
    new_software = Software(
        name=name,
        description=description,
        price=price,
        image_url=image_url,
        license_key=license_key
    )
    db.session.add(new_software)
    db.session.commit()
    
    return jsonify({'message': 'Software added successfully'})

@app.route('/purchase/<int:software_id>')
@login_required
def purchase(software_id):
    software = Software.query.get_or_404(software_id)
    
    def generate_license_key():
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(20))
    
    new_purchase = Purchase(
        user_id=current_user.id,
        software_id=software_id,
        license_key=generate_license_key()
    )
    db.session.add(new_purchase)
    db.session.commit()
    
    return redirect(url_for('index'))
