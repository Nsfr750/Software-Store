from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aghrghealvn3451'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///software_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize the database and models
with app.app_context():
    db.create_all()

# Import models and routes after database initialization
from software_store_app import models, routes
