from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def create_mock_data(app, db, User, Job, Resume, JobApplication, Message, Notification):
    """Create mock data for the application"""
    with app.app_context():
        # Only create mock data if the database is empty
        if User.query.first():
            return

        print("Creating mock data...")

        # Create employers
        employers = [
            {
                'username': 'tech_corp',
                'email': 'hr@techcorp.com',
                'password': generate_password_hash('password'),
                'user_type': 'employer',
                'company_name': 'Tech Corp'
            },
            {
                'username': 'innovate_solutions',
                'email': 'careers@innovatesolutions.com',
                'password': generate_password_hash('password'),
                'user_type': 'employer',
                'company_name': 'Innovate Solutions'
            },
            {
                'username': 'digital_dynamics',
                'email': 'jobs@digitaldynamics.com',
                'password': generate_password_hash('password'),
                'user_type': 'employer',
                'company_name': 'Digital Dynamics'
            }
        ]

        employer_objects = []
        for employer_data in employers:
            employer = User(**employer_data)
            db.session.add(employer)
            employer_objects.append(employer)
        db.session.commit()

        # Create applicants
        applicants = [
            {
                'username': 'john_dev',
                'email': 'john@example.com',
                'password': generate_password_hash('password'),
                'user_type': 'applicant'
            },
            {
                'username': 'sarah_designer',
                'email': 'sarah@example.com',
                'password': generate_password_hash('password'),
                'user_type': 'applicant'
            },
            {
                'username': 'mike_analyst',
                'email': 'mike@example.com',
                'password': generate_password_hash('password'),
                'user_type': 'applicant'
            }
        ]

        applicant_objects = []
        for applicant_data in applicants:
            applicant = User(**applicant_data)
            db.session.add(applicant)
            applicant_objects.append(applicant)
        db.session.commit()

        # Create jobs
        jobs_data = [
            {
                'employer_id': employer_objects[0].id,
                'title': 'Senior Python Developer',
                'company': 'Tech Corp',
                'description': 'We are looking for an experienced Python developer to lead our backend team. The ideal candidate will have strong experience with Flask/Django and microservices architecture.',
                'requirements': 'Python, Flask/Django, SQL, AWS, 5+ years experience',
                'location': 'New York, NY',
                'job_type': 'Full-time',
                'salary_range': '$120,000 - $150,000',
                'skills_required': 'Python, Flask, Django, AWS, SQL, Docker',
                'posted_date': datetime.now() - timedelta(days=2)
            },
            {
                'employer_id': employer_objects[1].id,
                'title': 'UI/UX Designer',
                'company': 'Innovate Solutions',
                'description': 'Join our creative team as a UI/UX Designer. You will be responsible for creating beautiful and intuitive user interfaces for our web and mobile applications.',
                'requirements': 'Figma, Adobe XD, 3+ years experience in UI/UX design',
                'location': 'Remote',
                'job_type': 'Full-time',
                'salary_range': '$90,000 - $120,000',
                'skills_required': 'Figma, Adobe XD, HTML, CSS, JavaScript',
                'posted_date': datetime.now() - timedelta(days=5)
            },
            {
                'employer_id': employer_objects[2].id,
                'title': 'Data Analyst Intern',
                'company': 'Digital Dynamics',
                'description': 'Looking for a motivated intern to join our data analytics team. You will work with senior analysts on real-world data projects.',
                'requirements': 'Currently pursuing degree in Data Science, Statistics, or related field',
                'location': 'Chicago, IL',
                'job_type': 'Internship',
                'salary_range': '$25/hour',
                'skills_required': 'Python, SQL, Excel, Data Visualization',
                'posted_date': datetime.now() - timedelta(days=1)
            },
            {
                'employer_id': employer_objects[0].id,
                'title': 'Frontend Developer',
                'company': 'Tech Corp',
                'description': 'We need a talented frontend developer to create responsive and interactive web applications using modern JavaScript frameworks.',
                'requirements': 'React/Vue.js, 2+ years experience',
                'location': 'Boston, MA',
                'job_type': 'Full-time',
                'salary_range': '$90,000 - $120,000',
                'skills_required': 'React, Vue.js, HTML5, CSS3, JavaScript',
                'posted_date': datetime.now() - timedelta(days=3)
            }
        ]

        job_objects = []
        for job_data in jobs_data:
            job = Job(**job_data)
            db.session.add(job)
            job_objects.append(job)
        db.session.commit()

        # Create resumes
        resume_data = {
            'user_id': applicant_objects[0].id,
            'title': 'Software Developer Resume',
            'full_name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1 234-567-8900',
            'address': '123 Tech Street, Silicon Valley, CA',
            'summary': 'Experienced software developer with expertise in Python and web development.',
            'education': [
                {
                    'school': 'Tech University',
                    'degree': 'Bachelor of Science',
                    'field': 'Computer Science',
                    'start_date': '2018',
                    'end_date': '2022'
                }
            ],
            'experience': [
                {
                    'company': 'Tech Corp',
                    'position': 'Junior Developer',
                    'description': 'Developed and maintained web applications using Python and Flask.',
                    'start_date': '2022',
                    'end_date': 'Present'
                }
            ],
            'skills': ['Python', 'Flask', 'SQL', 'JavaScript', 'Git']
        }
        
        resume2_data = {
            'user_id': applicant_objects[1].id,
            'title': 'Marketing Specialist Resume',
            'full_name': 'Jane Smith',
            'email': 'jane.smith@example.com',
            'phone': '+1 234-567-8901',
            'address': '456 Marketing Ave, Digital City, CA',
            'summary': 'Creative marketing specialist with experience in digital marketing and social media management.',
            'education': [
                {
                    'school': 'Marketing College',
                    'degree': 'Bachelor of Arts',
                    'field': 'Marketing',
                    'start_date': '2019',
                    'end_date': '2023'
                }
            ],
            'experience': [
                {
                    'company': 'Digital Marketing Agency',
                    'position': 'Marketing Intern',
                    'description': 'Assisted in social media campaigns and content creation.',
                    'start_date': '2023',
                    'end_date': 'Present'
                }
            ],
            'skills': ['Social Media Marketing', 'Content Creation', 'Analytics', 'SEO', 'Email Marketing']
        }

        resume = Resume(**resume_data)
        resume2 = Resume(**resume2_data)
        db.session.add(resume)
        db.session.add(resume2)
        db.session.commit()

        # Create job applications
        applications_data = [
            {
                'job_id': job_objects[0].id,
                'applicant_id': applicant_objects[0].id,
                'resume_id': Resume.query.filter_by(user_id=applicant_objects[0].id).first().id,
                'status': 'pending',
                'application_date': datetime.now() - timedelta(days=1),
                'cover_letter': 'I am excited to apply for the Senior Python Developer position at Tech Corp...'
            },
            {
                'job_id': job_objects[1].id,
                'applicant_id': applicant_objects[1].id,
                'resume_id': Resume.query.filter_by(user_id=applicant_objects[1].id).first().id,
                'status': 'under_review',
                'application_date': datetime.now() - timedelta(days=2),
                'cover_letter': 'With my background in UI/UX design, I believe I would be a great fit for...'
            }
        ]

        for application_data in applications_data:
            application = JobApplication(**application_data)
            db.session.add(application)
        db.session.commit()

        # Create messages
        messages_data = [
            {
                'sender_id': applicant_objects[0].id,
                'recipient_id': employer_objects[0].id,
                'subject': 'Question about the Python Developer position',
                'body': 'I would like to know more about the development team and tech stack...',
                'timestamp': datetime.now() - timedelta(days=1),
                'job_id': job_objects[0].id
            },
            {
                'sender_id': employer_objects[0].id,
                'recipient_id': applicant_objects[0].id,
                'subject': 'Re: Question about the Python Developer position',
                'body': 'Thank you for your interest! Our tech stack includes...',
                'timestamp': datetime.now() - timedelta(hours=12),
                'job_id': job_objects[0].id
            }
        ]

        for message_data in messages_data:
            message = Message(**message_data)
            db.session.add(message)
        db.session.commit()

        # Create notifications
        notifications_data = [
            {
                'user_id': applicant_objects[0].id,
                'title': 'Application Status Update',
                'message': 'Your application for Senior Python Developer is under review',
                'timestamp': datetime.now() - timedelta(hours=6),
                'read': False,
                'notification_type': 'application_update',
                'related_id': job_objects[0].id
            },
            {
                'user_id': employer_objects[0].id,
                'title': 'New Application',
                'message': 'New application received for Senior Python Developer position',
                'timestamp': datetime.now() - timedelta(days=1),
                'read': True,
                'notification_type': 'new_application',
                'related_id': job_objects[0].id
            }
        ]

        for notification_data in notifications_data:
            notification = Notification(**notification_data)
            db.session.add(notification)
        db.session.commit()

        print("Mock data creation completed!")
