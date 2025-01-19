# Youth Jobs Portal - Developer Playbook

## Table of Contents
1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Development Environment](#development-environment)
4. [Database Management](#database-management)
5. [Code Structure](#code-structure)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git (for version control)
- SQLite (included with Python)

### Quick Start (Portable Version)
1. Download `youth_jobs_portable.zip`
2. Extract to desired location
3. Run `init_db.bat` to initialize the database
4. Run `start.bat` to launch the application
5. Access the application at `http://localhost:5000`

## Installation

### From Source
```bash
# Clone the repository
git clone [repository-url]
cd youth_jobs

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python manage.py

# Start the application
python app.py
```

### Portable Installation
1. Extract `youth_jobs_portable.zip`
2. The package includes:
   - Pre-configured virtual environment
   - All dependencies
   - Database migrations
   - Startup scripts

## Development Environment

### IDE Setup
Recommended VS Code extensions:
- Python
- SQLite Viewer
- Git Lens
- Python Test Explorer

### Environment Variables
Create a `.env` file in the root directory:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions small and focused

## Database Management

### Database Structure
The application uses SQLite with Flask-Migrate for database management.

Key models:
- User
- Job
- Resume
- JobApplication
- Message
- Notification

### Migrations
```bash
# Generate new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

### Backup and Restore
```bash
# Backup database
copy youth_jobs.db youth_jobs_backup.db

# Restore database
copy youth_jobs_backup.db youth_jobs.db
```

## Code Structure

### Project Layout
```
youth_jobs/
├── app.py              # Main application file
├── manage.py           # Database management script
├── requirements.txt    # Python dependencies
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── migrations/        # Database migrations
├── docs/             # Documentation
└── tests/            # Unit tests
```

### Key Components
1. **Routes** (`app.py`):
   - Authentication
   - Job management
   - Resume management
   - Messaging system
   - Profile management

2. **Models** (`app.py`):
   - Database models and relationships
   - Data validation
   - Helper methods

3. **Templates** (`templates/`):
   - Base template
   - Authentication forms
   - Job listings
   - Resume builder
   - Profile pages

## Deployment

### Building Portable Package
```bash
# Run build script
build.bat

# Output: dist/youth_jobs_portable.zip
```

### Production Setup
1. Update `.env` for production:
   ```env
   FLASK_ENV=production
   SECRET_KEY=[secure-key]
   ```

2. Configure email settings:
   - Use production SMTP server
   - Set up proper email credentials

3. Security considerations:
   - Enable HTTPS
   - Set secure cookie settings
   - Configure proper logging

## Troubleshooting

### Common Issues

1. **Database Errors**
   ```bash
   # Reset database
   python manage.py
   ```

2. **Missing Dependencies**
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt
   ```

3. **Email Configuration**
   - Check SMTP settings
   - Verify email credentials
   - Test email connection

### Debug Mode
```python
# Enable debug mode in app.py
app.debug = True
```

### Logs
- Application logs: `logs/app.log`
- Error logs: `logs/error.log`
- Access logs: `logs/access.log`

### Support
For additional support:
1. Check the documentation in `docs/`
2. Review error logs
3. Contact the development team

## Best Practices

### Code Quality
- Write unit tests for new features
- Run tests before committing
- Follow the existing code style
- Document significant changes

### Git Workflow
1. Create feature branch
2. Make changes
3. Run tests
4. Create pull request
5. Code review
6. Merge to main

### Security
- Never commit sensitive data
- Use environment variables
- Validate all user inputs
- Follow security best practices

## Contributing
1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request
5. Wait for review

Remember to update this playbook when making significant changes to the application architecture or development process.
