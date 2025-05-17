from software_store_app import db, models, login_manager
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aghrghealvn3451'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///software_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Models are now imported from models.py

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
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
        
        flash('Registration successful! Please login.')
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
        return redirect(url_for('index'))
    
    software = Software.query.all()
    users = User.query.all()
    purchases = Purchase.query.all()
    return render_template('admin.html', software=software, users=users, purchases=purchases)

@app.route('/admin/add_software', methods=['POST'])
@login_required
def add_software():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    new_software = Software(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        image_url=data.get('image_url'),
        license_key=data['license_key']
    )
    db.session.add(new_software)
    db.session.commit()
    return jsonify({'message': 'Software added successfully'})

@app.route('/purchase/<int:software_id>')
@login_required
def purchase(software_id):
    software = Software.query.get_or_404(software_id)
    purchase = Purchase(
        user_id=current_user.id,
        software_id=software_id,
        license_key=software.license_key
    )
    db.session.add(purchase)
    db.session.commit()
    flash('Purchase successful! You can find your license key in your account.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
