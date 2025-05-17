import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from software_store_app import app, db

with app.app_context():
    print("Initializing database...")
    db.create_all()
    print("Database initialized successfully!")
