# Software Store Application

A web-based software store application with a main store interface and an editor interface for managing the store's database. Built with Flask and SQLAlchemy.

## Features

### Main Store Interface
- Browse available software products with detailed descriptions
- View software prices and purchase history
- Secure user authentication and registration system
- User-friendly purchase process with unique license keys
- Admin panel for managing the store
- Responsive design for all devices

### Editor Interface
- Comprehensive user management:
  - Create, edit, and delete users
  - Manage user roles and permissions
  - View detailed user information
  - Track user purchase history

- Software product management:
  - Add new software products with descriptions
  - Edit existing product details
  - Manage product pricing and availability
  - Generate unique license keys

- Purchase management:
  - View all purchase transactions
  - Track license key assignments
  - Manage purchase history
  - Generate reports

- Enhanced admin controls:
  - Detailed database management
  - User activity tracking
  - System logs and monitoring
  - Backup and restore capabilities

## Project Structure

```
software_store/
├── software_store_app/           # Main application directory
│   ├── __init__.py             # Application initialization
│   ├── app.py                  # Main application routes
│   ├── editor.py               # Editor interface routes
│   ├── models.py               # Database models
│   ├── routes.py               # Main application routes
│   ├── init_db.py              # Database initialization
│   ├── static/
│   │   └── style.css          # CSS styles
│   └── templates/
│       ├── base.html          # Main application base template
│       ├── editor/            # Editor interface templates
│       │   ├── base.html     # Editor base template
│       │   ├── editor.html   # Main editor interface
│       │   ├── login.html    # Editor login page
│       │   ├── register.html # Editor registration page
│       │   ├── admin.html    # Editor admin panel
│       │   ├── add_software.html # Add software form
│       │   ├── edit_user.html   # Edit user form
│       │   ├── edit_software.html # Edit software form
│       │   └── edit_purchase.html # Edit purchase form
│       ├── admin.html         # Main admin dashboard
│       ├── index.html         # Home page
│       ├── login.html         # User login page
│       └── register.html      # User registration page
├── run.py                     # Main application runner
├── run_editor.py              # Editor interface runner
├── requirements.txt           # Project dependencies
└── README.md                 # Project documentation
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd software_store
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python -m software_store_app.init_db
   ```

## Running the Application

### Main Store Interface

Run the main application on port 5000:
```bash
python run.py
```

Access the store at: http://127.0.0.1:5000/

### Editor Interface

Run the editor interface on port 5001:
```bash
python run_editor.py
```

Access the editor at: http://127.0.0.1:5001/

## Usage

### Main Store Interface

1. Register a new user or login with existing credentials
2. Browse available software products
3. View detailed product information
4. Make purchases with unique license keys
5. View purchase history and license keys
6. Access the admin panel with admin credentials

### Editor Interface (Admin Only)

1. User Management:
   - Create new user accounts
   - Edit existing user information
   - Delete user accounts
   - Manage user roles and permissions
   - View user activity logs
   - Track purchase history

2. Software Product Management:
   - Add new software products
   - Edit existing product details
   - Manage product pricing
   - Generate unique license keys
   - Track product availability
   - View product statistics

3. Purchase Management:
   - View all purchase transactions
   - Track license key assignments
   - Manage purchase history
   - Generate purchase reports
   - Handle refunds and cancellations

4. Admin Controls:
   - System configuration
   - Database management
   - Backup and restore
   - Activity monitoring
   - System logs

## Database Structure

The application uses SQLite as its database with the following models:

- User: Stores user information and authentication details
  - username
  - email
  - password_hash
  - is_admin
  - purchases

- Software: Stores software products and license keys
  - name
  - description
  - price
  - image_url
  - license_key
  - created_at
  - purchases

- Purchase: Stores purchase transactions and license key assignments
  - user_id
  - software_id
  - purchase_date
  - license_key

## Security

- Passwords are hashed using Werkzeug's security utilities
- User authentication is handled by Flask-Login
- Admin privileges are restricted to authorized users
- Secure session management
- Protection against common web vulnerabilities
- Regular security updates and patches

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the maintainers directly.
   - Delete products
   - Manage licenses

3. Manage purchases:
   - View all purchases
   - Edit purchase details
   - Generate new licenses
   - Track purchase history

## Database

The application uses SQLite as its database. The database file will be created automatically when you run `init_db.py`.

## Configuration

The application uses environment variables for configuration. You can create a `.env` file in the root directory to set custom configurations.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Technical Details

- Flask 3.0.0
- SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- SQLite database
- Bootstrap 5.3.0 for frontend
- Separate editor interface for administrative tasks
- RESTful API endpoints for data management
- Secure admin authentication
- Error handling and logging
- Responsive design
- CSRF protection
- Session management
