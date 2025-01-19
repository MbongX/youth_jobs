from app import app, db, create_mock_data
from flask_migrate import upgrade

def init_db():
    with app.app_context():
        # Upgrade the database to the latest revision
        upgrade()
        
        # Check if we need to create mock data
        from app import User
        if not User.query.first():
            print("Creating mock data...")
            create_mock_data(app, db)
            print("Mock data created successfully!")
        else:
            print("Database already contains data, skipping mock data creation.")

if __name__ == '__main__':
    init_db()
