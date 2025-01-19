from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask_mail import Mail, Message as MailMessage
import json
from datetime import datetime, timedelta
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youth_jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'employer' or 'applicant'
    company_name = db.Column(db.String(100))  # Only for employers
    
    # Relationships
    jobs = db.relationship('Job', backref='employer', lazy=True)
    applications = db.relationship('JobApplication', backref='applicant', lazy=True, foreign_keys='JobApplication.applicant_id')
    resumes = db.relationship('Resume', backref='applicant', lazy=True)
    sent_messages = db.relationship('Message', backref='sender', lazy=True, foreign_keys='Message.sender_id')
    received_messages = db.relationship('Message', backref='recipient', lazy=True, foreign_keys='Message.recipient_id')
    notifications = db.relationship('Notification', backref='user', lazy=True)
    preferences = db.relationship('JobPreference', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)
    salary_range = db.Column(db.String(50))
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    applications = db.relationship('JobApplication', backref='job', lazy=True)
    skills_required = db.Column(db.Text)
    external_source = db.Column(db.String(50))  # For jobs from external APIs
    external_id = db.Column(db.String(100))     # For jobs from external APIs

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, reviewed, accepted, rejected
    application_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cover_letter = db.Column(db.Text)
    notes = db.Column(db.Text)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False, default='My Resume')
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    summary = db.Column(db.Text)
    education = db.Column(db.JSON)
    experience = db.Column(db.JSON)
    skills = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'summary': self.summary,
            'education': self.education or [],
            'experience': self.experience or [],
            'skills': self.skills or [],
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    # Relationships
    applications = db.relationship('JobApplication', backref='resume', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    subject = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
    notification_type = db.Column(db.String(50), nullable=False)  # 'application_update', 'new_application', 'job_match'
    related_id = db.Column(db.Integer)  # ID of related entity (job, application, etc.)

class JobPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Mock Data Creation
def create_mock_data():
    # Check if mock data already exists
    if User.query.filter_by(email="employer@test.com").first() is not None:
        print("Mock data already exists, skipping creation...")
        return

    # Create test users
    employer = User(
        username="test_employer",
        email="employer@test.com",
        user_type="employer",
        company_name="Test Company"
    )
    employer.set_password("password123")
    
    applicant = User(
        username="test_applicant",
        email="applicant@test.com",
        user_type="applicant"
    )
    applicant.set_password("password123")
    
    db.session.add(employer)
    db.session.add(applicant)
    db.session.commit()
    
    # Create test job
    job = Job(
        employer_id=employer.id,
        title="Software Developer",
        company="Test Company",
        description="Looking for a talented software developer",
        requirements="Python, Flask, SQL",
        location="Remote",
        job_type="Full-time",
        salary_range="$80,000 - $100,000",
        skills_required="Python,Flask,SQL,Git"
    )
    db.session.add(job)
    
    # Create test resume
    resume = Resume(
        user_id=applicant.id,
        title="My Professional Resume",
        full_name="Test Applicant",
        email="applicant@test.com",
        phone="123-456-7890",
        summary="Experienced software developer",
        education=json.dumps([{
            "degree": "Bachelor of Science",
            "institution": "Test University",
            "start_date": "2018",
            "end_date": "2022"
        }]),
        experience=json.dumps([{
            "position": "Junior Developer",
            "company": "Previous Company",
            "start_date": "2022",
            "end_date": "Present",
            "description": "Developed web applications using Python and Flask"
        }]),
        skills="Python,Flask,SQL,Git"
    )
    db.session.add(resume)
    
    try:
        db.session.commit()
        print("Mock data created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating mock data: {str(e)}")
        raise

# Routes
@app.route('/')
def home():
    jobs = Job.query.order_by(Job.posted_date.desc()).limit(10).all()
    return render_template('home.html', jobs=jobs)

@app.route('/jobs')
def jobs():
    jobs = Job.query.order_by(Job.posted_date.desc()).all()
    return render_template('jobs.html', jobs=jobs)

@app.route('/job/<int:job_id>')
def job(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_details.html', job=job)

@app.route('/job/<int:job_id>/apply', methods=['GET', 'POST'])
@login_required
def apply_job(job_id):
    if current_user.user_type != 'applicant':
        flash('Only applicants can apply for jobs.', 'error')
        return redirect(url_for('jobs'))

    job = Job.query.get_or_404(job_id)
    resumes = Resume.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        resume_id = request.form.get('resume_id')
        cover_letter = request.form.get('cover_letter')

        if not resume_id:
            flash('Please select a resume.', 'error')
            return redirect(url_for('apply_job', job_id=job_id))

        application = JobApplication(
            job_id=job_id,
            applicant_id=current_user.id,
            resume_id=resume_id,
            cover_letter=cover_letter,
            status='pending'
        )

        try:
            db.session.add(application)
            db.session.commit()
            
            # Create notification for employer
            notification = Notification(
                user_id=job.employer_id,
                title='New Application Received',
                message=f'New application received for {job.title}',
                notification_type='new_application',
                related_id=application.id
            )
            db.session.add(notification)
            db.session.commit()

            flash('Application submitted successfully!', 'success')
            return redirect(url_for('jobs'))
        except Exception as e:
            db.session.rollback()
            flash('Error submitting application. Please try again.', 'error')
            app.logger.error(f"Application error: {str(e)}")
            return redirect(url_for('apply_job', job_id=job_id))

    return render_template('apply_job.html', job=job, resumes=resumes)

@app.route('/resume-builder')
@login_required
def resume_builder():
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    return render_template('resume_builder.html', resume=resume)

@app.route('/resume/preview/<int:resume_id>')
@login_required
def preview_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash('You do not have permission to view this resume.', 'error')
        return redirect(url_for('resume_builder'))
    return render_template('resume_preview.html', resume=resume)

@app.route('/resume/save', methods=['POST'])
@login_required
def save_resume():
    data = request.json
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    
    if not resume:
        resume = Resume(user_id=current_user.id)
        db.session.add(resume)
    
    # Update resume fields
    resume.title = data.get('title', 'My Resume')
    resume.full_name = data.get('full_name')
    resume.email = data.get('email')
    resume.phone = data.get('phone')
    resume.address = data.get('address')
    resume.summary = data.get('summary')
    resume.education = data.get('education', [])
    resume.experience = data.get('experience', [])
    resume.skills = data.get('skills', [])
    resume.last_updated = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({'status': 'success', 'resume_id': resume.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/profile')
@login_required
def profile():
    if current_user.user_type == 'applicant':
        resumes = Resume.query.filter_by(user_id=current_user.id).all()
        applications = JobApplication.query.filter_by(applicant_id=current_user.id).all()
        return render_template('profile.html', resumes=resumes, applications=applications)
    else:  # employer
        posted_jobs = Job.query.filter_by(employer_id=current_user.id).all()
        return render_template('profile.html', posted_jobs=posted_jobs)

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        current_user.email = request.form['email']
        
        if current_user.user_type == 'employer':
            current_user.company_name = request.form['company_name']
        
        new_password = request.form.get('new_password')
        if new_password:
            current_user.set_password(new_password)
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile. Please try again.', 'error')
            app.logger.error(f"Profile update error: {str(e)}")
        
        return redirect(url_for('profile'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        company_name = request.form.get('company_name') if user_type == 'employer' else None

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))

        user = User(
            username=username,
            email=email,
            user_type=user_type,
            company_name=company_name
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed! Please try again.', 'error')
            app.logger.error(f"Registration error: {str(e)}")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Job Application Tracking
@app.route('/applications')
@login_required
def job_applications():
    if current_user.user_type == 'applicant':
        applications = JobApplication.query.filter_by(applicant_id=current_user.id).all()
    else:
        jobs = Job.query.filter_by(employer_id=current_user.id).all()
        applications = []
        for job in jobs:
            applications.extend(job.applications)
    
    return render_template('applications.html', applications=applications)

# Messaging System
@app.route('/messages')
@login_required
def messages():
    received = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.timestamp.desc()).all()
    sent = Message.query.filter_by(sender_id=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template('messages.html', received=received, sent=sent)

@app.route('/messages/send/<int:recipient_id>', methods=['GET', 'POST'])
@login_required
def send_message(recipient_id):
    if request.method == 'POST':
        message = Message(
            sender_id=current_user.id,
            recipient_id=recipient_id,
            subject=request.form.get('subject'),
            body=request.form.get('body'),
            job_id=request.form.get('job_id')
        )
        db.session.add(message)
        
        # Create notification for recipient
        notification = Notification(
            user_id=recipient_id,
            title='New Message Received',
            message=f"New message from {current_user.username}",
            notification_type='message',
            related_id=message.id
        )
        db.session.add(notification)
        db.session.commit()
        
        flash('Message sent successfully!', 'success')
        return redirect(url_for('messages'))
    
    recipient = User.query.get_or_404(recipient_id)
    return render_template('send_message.html', recipient=recipient)

# Resume Templates
@app.route('/resume/template/<template_name>')
@login_required
def resume_template(template_name):
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    return render_template(f'resume_templates/{template_name}.html', resume=resume)

# Job API Integration
def fetch_external_jobs():
    # Example using Reed API (you'll need to sign up for an API key)
    api_key = os.getenv('REED_API_KEY')
    if not api_key:
        return []
    
    url = 'https://www.reed.co.uk/api/1.0/search'
    headers = {'Authorization': f'Basic {api_key}'}
    
    try:
        response = requests.get(url, headers=headers)
        jobs_data = response.json()
        
        for job_data in jobs_data:
            existing_job = Job.query.filter_by(external_id=str(job_data['jobId'])).first()
            if not existing_job:
                job = Job(
                    title=job_data['jobTitle'],
                    company=job_data['employerName'],
                    description=job_data['description'],
                    location=job_data['locationName'],
                    job_type=job_data['contractType'],
                    external_source='reed',
                    external_id=str(job_data['jobId'])
                )
                db.session.add(job)
        
        db.session.commit()
    except Exception as e:
        app.logger.error(f"Error fetching external jobs: {str(e)}")

# Job Matching and Notifications
def send_job_match_notification(user, job):
    subject = f'New Job Match: {job.title}'
    body = f'''Hello {user.username},

We found a new job that matches your profile:

{job.title}
Company: {job.company}
Location: {job.location}

Click here to view the job: {url_for('job', job_id=job.id, _external=True)}

Best regards,
Youth Jobs Team'''

    msg = MailMessage(
        subject,
        sender=app.config['MAIL_USERNAME'],
        recipients=[user.email]
    )
    msg.body = body
    mail.send(msg)

    notification = Notification(
        user_id=user.id,
        title='New Job Match Found',
        message=f"New job match found: {job.title} at {job.company}",
        notification_type='job_match',
        related_id=job.id
    )
    db.session.add(notification)
    db.session.commit()

@app.route('/notifications')
@login_required
def notifications():
    notifications = Notification.query.filter_by(
        user_id=current_user.id,
        read=False
    ).order_by(Notification.timestamp.desc()).all()
    return render_template('notifications.html', notifications=notifications)

@app.route('/notifications/mark_read/<int:notification_id>')
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id == current_user.id:
        notification.read = True
        db.session.commit()
    return redirect(url_for('notifications'))

# Scheduled task to check for job matches (you'll need to set up a task scheduler)
def check_job_matches():
    recent_jobs = Job.query.filter(
        Job.posted_date >= datetime.utcnow() - timedelta(days=1)
    ).all()
    
    users = User.query.filter_by(user_type='applicant').all()
    for user in users:
        preferences = user.preferences
        if not preferences:
            continue
        
        for job in recent_jobs:
            # Simple matching logic - you can make this more sophisticated
            if any(pref.job_type == job.job_type or 
                  pref.location.lower() in job.location.lower() or
                  pref.industry.lower() in job.title.lower()
                  for pref in preferences):
                send_job_match_notification(user, job)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_mock_data()
        app.run(debug=True)
