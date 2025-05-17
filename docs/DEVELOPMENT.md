# Development Guide

## Project Overview

### Purpose
The Software Store is a web application for managing software licenses and purchases. It provides both a user interface for customers and an administrative interface for managing the store.

### Key Features
- User management system
- Software catalog management
- License key generation and tracking
- Purchase tracking and reporting
- Admin interface
- Editor interface

## Technical Requirements

### Prerequisites
- Python 3.8+ (recommended: 3.10+)
- pip (Python package manager)
- virtualenv (for isolated environments)
- SQLite (database)
- Git (version control)

### System Requirements
- Minimum 2GB RAM
- Minimum 1GB free disk space
- Modern web browser (Chrome, Firefox, Safari)
- Internet connection for development dependencies

## Project Setup

### Development Environment

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On Unix/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize database:
```bash
python -m software_store_app.init_db
```

### Environment Variables

Create a `.env` file with the following variables:
```bash
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///software_store.db
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

### Development Server Options
```bash
# Run with debug mode
FLASK_ENV=development python run.py

# Run with specific port
FLASK_RUN_PORT=8080 python run.py

# Run with specific host
FLASK_RUN_HOST=0.0.0.0 python run.py
```

## Project Structure

```
software_store/
├── software_store_app/           # Main application package
│   ├── __init__.py              # Application initialization
│   ├── app.py                  # Main application routes
│   ├── editor.py               # Editor interface routes
│   ├── models.py              # Database models
│   ├── routes.py              # Main application routes
│   ├── static/                # Static files
│   │   ├── css/              # CSS styles
│   │   ├── js/               # JavaScript files
│   │   └── images/           # Image assets
│   └── templates/            # HTML templates
│       ├── base.html        # Base template
│       ├── editor/          # Editor interface templates
│       └── main/            # Main application templates
├── config.py                 # Configuration settings
├── run.py                   # Main application runner
├── run_editor.py           # Editor interface runner
├── requirements.txt        # Project dependencies
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_models.py     # Database model tests
│   ├── test_routes.py     # Route tests
│   └── test_security.py   # Security tests
├── docs/                   # Documentation
│   ├── ADMIN_GUIDE.md     # Administrator documentation
│   └── DEVELOPMENT.md     # Developer documentation
└── .env                   # Environment variables
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
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
    category = db.Column(db.String(50))
    tags = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
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
    status = db.Column(db.String(20), default='active')
    expires_at = db.Column(db.DateTime)
```

## Security Implementation

### Authentication
- Flask-Login for user sessions
- Werkzeug security utilities for password hashing
- JWT for API authentication
- CSRF protection
- Secure session management

### Authorization
- Role-based access control (RBAC)
- Permission system
- Protected routes
- Secure API endpoints

### Security Features
- Two-factor authentication
- Password complexity requirements
- Session timeout
- Rate limiting
- Input validation
- XSS protection
- CSRF protection

## Development Workflow

### Branching Strategy
```
main (production)
├── develop (development)
    ├── feature/* (feature branches)
    ├── hotfix/* (hotfix branches)
    └── release/* (release branches)
```

### Commit Guidelines
1. Use descriptive commit messages
2. Follow conventional commits format
3. Include issue numbers when applicable
4. Keep commits atomic

### Code Style
- Follow PEP 8 guidelines
- Use black for code formatting
- Use isort for import sorting
- Use pylint for code analysis

## Testing

### Test Suite
- Unit tests
- Integration tests
- End-to-end tests
- Security tests

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_models.py

# Run with coverage
python -m pytest --cov=software_store_app

# Run with verbose output
python -m pytest -v
```

### Test Coverage
- Minimum 80% coverage required
- Critical paths must be 100% covered
- Security features must be 100% covered

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
export SECRET_KEY=your-production-secret
export DATABASE_URL=sqlite:///software_store_prod.db
```

3. Run application:
```bash
gunicorn run:app --bind 0.0.0.0:5000 --workers 4
```

### Deployment Checklist
- Update dependencies
- Run database migrations
- Clear caches
- Verify environment variables
- Test application
- Monitor logs

## Performance Optimization

### Database
- Index optimization
- Query optimization
- Connection pooling
- Caching strategy

### Application
- Template caching
- Asset compression
- Browser caching
- CDN integration

### Monitoring
- Performance metrics
- Error tracking
- Log monitoring
- Resource usage

## Troubleshooting

### Common Issues

#### Database Connection
- Verify SQLite is installed
- Check database file permissions
- Ensure database file exists
- Review database logs

#### Authentication
- Clear browser cookies
- Verify session configuration
- Check password hashing
- Review login logs

#### Routing
- Verify endpoint names
- Check template inheritance
- Review URL building
- Clear browser cache

#### Performance
- Monitor server resources
- Check database queries
- Review page load times
- Enable caching

### Debugging Tools
- Flask debug toolbar
- Python debugger (pdb)
- Performance profiler
- Log analyzer

## Documentation Standards

### Code Documentation
- Docstrings for all functions
- Type hints
- API documentation
- Configuration documentation

### API Documentation
- Swagger/OpenAPI specification
- API endpoints
- Request/response examples
- Authentication documentation

### User Documentation
- Installation guide
- User guide
- Administrator guide
- FAQ

## Version Control

### Git Workflow
1. Create feature branch
2. Implement changes
3. Write tests
4. Review code
5. Merge to develop
6. Deploy to staging
7. Merge to main
8. Deploy to production

### Release Process
1. Create release branch
2. Update version number
3. Update changelog
4. Run tests
5. Create release tag
6. Deploy to production

## Contributing

### Guidelines
1. Follow coding standards
2. Write tests
3. Document code
4. Review PRs
5. Follow security guidelines

### Pull Request Process
1. Create feature branch
2. Implement changes
3. Write tests
4. Update documentation
5. Submit PR
6. Get review
7. Address feedback
8. Merge PR

## Security Policy

### Reporting Security Issues
1. Do not disclose publicly
2. Contact security@software-store.com
3. Include detailed information
4. Follow up regularly

### Security Updates
- Regular security audits
- Dependency updates
- Security patches
- Security testing

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Open source contributors
- Community support
- Partners
- Advisors

## Disclaimer

This documentation is provided "as is" without warranty of any kind, express or implied. Users are advised to verify the information independently.
