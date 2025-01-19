from app import app, db, User
from werkzeug.security import generate_password_hash

def create_test_user():
    with app.app_context():
        # Check if test user already exists
        if not User.query.filter_by(email='test@example.com').first():
            test_user = User(
                username='testuser',
                email='test@example.com',
                password=generate_password_hash('testpass123'),
                user_type='applicant'
            )
            db.session.add(test_user)
            db.session.commit()
            print("Test user created successfully!")
            print("Username: testuser")
            print("Password: testpass123")
        else:
            print("Test user already exists!")

if __name__ == '__main__':
    create_test_user()
