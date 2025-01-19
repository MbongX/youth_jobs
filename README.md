# Youth Jobs Portal

A comprehensive job portal application designed to connect youth with employment opportunities.

## Quick Start (Portable Version)

1. Download `youth_jobs_portable.zip`
2. Extract to your desired location
3. Run `init_db.bat` to initialize the database
4. Run `start.bat` to launch the application
5. Access the application at `http://localhost:5000`

## Documentation

- [Developer Playbook](docs/DEV_PLAYBOOK.md) - Comprehensive guide for developers
- [API Documentation](docs/API.md) - API endpoints and usage
- [Database Schema](docs/DATABASE.md) - Database structure and relationships

## Building from Source

1. Clone the repository
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize database:
   ```bash
   python manage.py
   ```
5. Start the application:
   ```bash
   python app.py
   ```

## Creating Portable Package

Run the build script:
```bash
build.bat
```

This will create `youth_jobs_portable.zip` in the `dist` directory, containing:
- Pre-configured virtual environment
- All dependencies
- Database migrations
- Startup scripts

## Features

- User authentication (login/register)
- Job posting and management
- Resume builder
- Job applications
- Messaging system
- Email notifications
- Profile management

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For detailed information about development, deployment, and troubleshooting, please refer to the [Developer Playbook](docs/DEV_PLAYBOOK.md).
