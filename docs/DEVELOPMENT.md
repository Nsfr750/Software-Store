# Development Guide

## Project Setup

### Prerequisites
- Python 3.8+
- pip
- virtualenv
- SQLite

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
venv\Scripts\activate     # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize database:
```bash
python -m software_store_app.init_db
```

## Running the Application

### Main Application
```bash
python run.py
```
Access at: http://127.0.0.1:5000/

### Editor Interface
```bash
python run_editor.py
```
Access at: http://127.0.0.1:5001/

## Project Structure

```
software_store/
├── software_store_app/
│   ├── __init__.py          # Application initialization
│   ├── app.py              # Main application routes
│   ├── editor.py           # Editor interface routes
│   ├── models.py          # Database models
│   ├── routes.py          # Main application routes
│   ├── static/
│   │   └── style.css     # CSS styles
│   └── templates/
│       ├── base.html     # Base template
│       ├── editor/       # Editor interface templates
│       └── main/         # Main application templates
├── run.py                 # Main application runner
├── run_editor.py         # Editor interface runner
├── requirements.txt      # Project dependencies
└── docs/                 # Documentation
```

## Database Models

### User Model
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    purchases = db.relationship('Purchase', backref='user', lazy=True)
```

### Software Model
```python
class Software(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))
    license_key = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    purchases = db.relationship('Purchase', backref='software', lazy=True)
```

### Purchase Model
```python
class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    software_id = db.Column(db.Integer, db.ForeignKey('software.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    license_key = db.Column(db.String(100), nullable=False)
```

## Security

### Authentication
- Uses Flask-Login for user sessions
- Passwords are hashed using Werkzeug's security utilities
- Admin privileges are restricted to authorized users
- Secure session management

### Authorization
- Role-based access control
- Admin-only routes
- Protected editor interface
- Secure license key generation

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing

### Unit Tests
```bash
python -m pytest tests/
```

### Integration Tests
```bash
python -m pytest tests/integration/
```

## Deployment

### Production Setup
1. Create production environment:
```bash
python -m venv prod_env
source prod_env/bin/activate
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
export FLASK_APP=run.py
export FLASK_ENV=production
```

3. Run application:
```bash
gunicorn run:app
```

## Troubleshooting

### Common Issues

#### Database Connection
- Ensure SQLite is installed
- Verify database file permissions
- Check database initialization

#### Authentication
- Clear browser cookies
- Verify session configuration
- Check password hashing

#### Routing
- Verify endpoint names
- Check template inheritance
- Review URL building

## License

This project is licensed under the MIT License - see the LICENSE file for details.
