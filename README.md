# Youth Jobs Platform

A comprehensive job platform designed specifically for youth employment, built with Flask and SQLAlchemy.

## Features

### For Job Seekers
- Create and manage multiple professional resumes
- Apply to jobs with customized cover letters
- Track application status
- Receive job match notifications
- Message potential employers
- View job recommendations based on skills and preferences

### For Employers
- Post and manage job listings
- Review applications
- Communicate with candidates
- Receive notifications for new applications
- Search candidate profiles

## Technology Stack

- **Backend**: Python 3.12+ with Flask
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: Bootstrap 5, JavaScript
- **Email**: Flask-Mail
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd youth_jobs
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
FLASK_APP=app.py
FLASK_ENV=development
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
REED_API_KEY=your-reed-api-key  # Optional, for job API integration
```

5. Initialize the database:
```bash
python app.py
```

## Project Structure

```
youth_jobs/
├── app.py              # Main application file
├── mock_data.py        # Sample data generation
├── requirements.txt    # Project dependencies
├── static/            # Static files (CSS, JS)
└── templates/         # HTML templates
    ├── base.html
    ├── home.html
    ├── jobs.html
    ├── job_details.html
    ├── messages.html
    ├── notifications.html
    └── resume_templates/
        └── professional.html
```

## Database Models

- **User**: Handles both applicants and employers
- **Job**: Job listings with detailed information
- **Resume**: User resumes with JSON content
- **JobApplication**: Tracks job applications
- **Message**: Internal messaging system
- **Notification**: System notifications
- **JobPreference**: User job preferences

## API Endpoints

### Authentication
- `POST /register`: Register new user
- `POST /login`: User login
- `GET /logout`: User logout

### Jobs
- `GET /jobs`: List all jobs
- `GET /job/<id>`: View job details
- `POST /jobs/create`: Create new job (employers only)
- `POST /job/<id>/apply`: Apply for job

### Profile & Resume
- `GET /resume-builder`: Resume creation interface
- `POST /resume/save`: Save resume
- `GET /applications`: View applications

### Messaging
- `GET /messages`: View messages
- `POST /messages/send`: Send message
- `GET /notifications`: View notifications

## Sample Users

### Employers
- Tech Corp (hr@techcorp.com)
- Innovate Solutions (careers@innovatesolutions.com)
- Digital Dynamics (jobs@digitaldynamics.com)

### Applicants
- John (john@example.com)
- Sarah (sarah@example.com)
- Mike (mike@example.com)

All sample users have password: "password"

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation and community
- SQLAlchemy documentation
- Bootstrap team for the UI framework
