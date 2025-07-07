"""
Create admin user script for ShikshaSetu
Run this script to create default admin and test users
"""

import asyncio
from sqlalchemy.orm import Session
from app.core.database import get_db, engine
from app.models.models import User
from app.core.auth import AuthService
import uuid


def create_default_users():
    """Create default admin and test users"""

    # Create database session
    db = Session(engine)

    try:
        # Check if admin user already exists
        admin_exists = db.query(User).filter(
            User.email == "admin@shikshasetu.com").first()
        if not admin_exists:
            # Create admin user
            admin_user = User(
                id=str(uuid.uuid4()),
                email="admin@shikshasetu.com",
                password_hash=AuthService.get_password_hash("admin123"),
                name="Admin User",
                role="admin",
                is_active=True,
                is_verified=True
            )
            db.add(admin_user)
            print("✅ Created admin user: admin@shikshasetu.com / admin123")
        else:
            print("ℹ️  Admin user already exists")

        # Check if test user already exists
        test_exists = db.query(User).filter(
            User.email == "test@shikshasetu.com").first()
        if not test_exists:
            # Create test user
            test_user = User(
                id=str(uuid.uuid4()),
                email="test@shikshasetu.com",
                password_hash=AuthService.get_password_hash("test123"),
                name="Test User",
                role="student",
                is_active=True,
                is_verified=True
            )
            db.add(test_user)
            print("✅ Created test user: test@shikshasetu.com / test123")
        else:
            print("ℹ️  Test user already exists")

        # Commit changes
        db.commit()
        print("\n🎉 Default users created successfully!")
        print("\nAdmin Credentials:")
        print("Email: admin@shikshasetu.com")
        print("Password: admin123")
        print("Role: admin")
        print("\nTest User Credentials:")
        print("Email: test@shikshasetu.com")
        print("Password: test123")
        print("Role: student")

    except Exception as e:
        print(f"❌ Error creating users: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_default_users()
