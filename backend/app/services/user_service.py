"""
User service for handling user operations, authentication, and profile management.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt
import uuid
import logging
from email_validator import validate_email, EmailNotValidError

from ..models.models import User, Application, Bookmark, Review, ActivityLog, Notification
from ..core.config import settings
from ..core.database import get_db_session

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Service for managing user operations and authentication."""

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user with validation."""
        try:
            # Validate email format
            try:
                valid_email = validate_email(user_data["email"])
                email = valid_email.email
            except EmailNotValidError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid email format"
                )

            # Check if user already exists
            existing_user = self.db.query(User).filter(
                or_(User.email == email, User.username ==
                    user_data["username"])
            ).first()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email or username already exists"
                )

            # Hash password
            hashed_password = pwd_context.hash(user_data["password"])

            # Create user
            user = User(
                id=str(uuid.uuid4()),
                username=user_data["username"],
                email=email,
                password_hash=hashed_password,
                full_name=user_data.get("full_name", ""),
                phone=user_data.get("phone"),
                date_of_birth=user_data.get("date_of_birth"),
                gender=user_data.get("gender"),
                category=user_data.get("category"),
                annual_income=user_data.get("annual_income"),
                education_level=user_data.get("education_level"),
                field_of_study=user_data.get("field_of_study"),
                state=user_data.get("state"),
                city=user_data.get("city"),
                is_active=True,
                email_verified=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            # Log user creation
            self._log_activity(user.id, "USER_CREATED",
                               "User account created successfully")

            logger.info(f"User created successfully: {user.email}")
            return user

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user account"
            )

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        try:
            user = self.db.query(User).filter(
                User.email == email,
                User.is_active == True
            ).first()

            if not user or not pwd_context.verify(password, user.password_hash):
                return None

            # Update last login
            user.last_login = datetime.utcnow()
            self.db.commit()

            # Log successful login
            self._log_activity(user.id, "USER_LOGIN",
                               "User logged in successfully")

            return user

        except Exception as e:
            logger.error(f"Error authenticating user: {str(e)}")
            return None

    def create_access_token(self, user: User) -> str:
        """Create JWT access token for user."""
        to_encode = {
            "sub": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        }

        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            return None

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def update_user_profile(self, user_id: str, update_data: Dict[str, Any]) -> User:
        """Update user profile information."""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Update allowed fields
            allowed_fields = [
                "full_name", "phone", "date_of_birth", "gender", "category",
                "annual_income", "education_level", "field_of_study", "state", "city"
            ]

            for field in allowed_fields:
                if field in update_data:
                    setattr(user, field, update_data[field])

            user.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(user)

            # Log profile update
            self._log_activity(user_id, "PROFILE_UPDATED",
                               "User profile updated successfully")

            return user

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating user profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating user profile"
            )

    def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """Change user password."""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Verify current password
            if not pwd_context.verify(current_password, user.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Current password is incorrect"
                )

            # Hash new password
            user.password_hash = pwd_context.hash(new_password)
            user.updated_at = datetime.utcnow()
            self.db.commit()

            # Log password change
            self._log_activity(user_id, "PASSWORD_CHANGED",
                               "User password changed successfully")

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error changing password: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error changing password"
            )

    def verify_email(self, user_id: str, verification_token: str) -> bool:
        """Verify user email with token."""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False

            # In a real implementation, you would verify the token
            # For now, we'll just mark as verified
            user.email_verified = True
            user.updated_at = datetime.utcnow()
            self.db.commit()

            # Log email verification
            self._log_activity(user_id, "EMAIL_VERIFIED",
                               "User email verified successfully")

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error verifying email: {str(e)}")
            return False

    def get_user_applications(self, user_id: str, limit: int = 10, offset: int = 0) -> List[Application]:
        """Get user's scholarship applications."""
        return self.db.query(Application)\
            .filter(Application.user_id == user_id)\
            .order_by(desc(Application.created_at))\
            .limit(limit)\
            .offset(offset)\
            .all()

    def get_user_bookmarks(self, user_id: str, limit: int = 10, offset: int = 0) -> List[Bookmark]:
        """Get user's bookmarked scholarships."""
        return self.db.query(Bookmark)\
            .filter(Bookmark.user_id == user_id)\
            .order_by(desc(Bookmark.created_at))\
            .limit(limit)\
            .offset(offset)\
            .all()

    def get_user_reviews(self, user_id: str, limit: int = 10, offset: int = 0) -> List[Review]:
        """Get user's scholarship reviews."""
        return self.db.query(Review)\
            .filter(Review.user_id == user_id)\
            .order_by(desc(Review.created_at))\
            .limit(limit)\
            .offset(offset)\
            .all()

    def get_user_notifications(self, user_id: str, limit: int = 20, offset: int = 0) -> List[Notification]:
        """Get user's notifications."""
        return self.db.query(Notification)\
            .filter(Notification.user_id == user_id)\
            .order_by(desc(Notification.created_at))\
            .limit(limit)\
            .offset(offset)\
            .all()

    def mark_notification_read(self, user_id: str, notification_id: str) -> bool:
        """Mark a notification as read."""
        try:
            notification = self.db.query(Notification).filter(
                Notification.id == notification_id,
                Notification.user_id == user_id
            ).first()

            if not notification:
                return False

            notification.is_read = True
            notification.read_at = datetime.utcnow()
            self.db.commit()

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error marking notification as read: {str(e)}")
            return False

    def get_user_dashboard_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user dashboard statistics."""
        try:
            # Get application counts by status
            application_stats = self.db.query(
                Application.status,
                func.count(Application.id).label('count')
            ).filter(Application.user_id == user_id)\
             .group_by(Application.status)\
             .all()

            # Get bookmark count
            bookmark_count = self.db.query(func.count(Bookmark.id))\
                .filter(Bookmark.user_id == user_id)\
                .scalar()

            # Get unread notification count
            unread_notifications = self.db.query(func.count(Notification.id))\
                .filter(
                    Notification.user_id == user_id,
                    Notification.is_read == False
            )\
                .scalar()

            # Get recent activity
            recent_activity = self.db.query(ActivityLog)\
                .filter(ActivityLog.user_id == user_id)\
                .order_by(desc(ActivityLog.created_at))\
                .limit(10)\
                .all()

            return {
                "application_stats": {stat.status: stat.count for stat in application_stats},
                "bookmark_count": bookmark_count,
                "unread_notifications": unread_notifications,
                "recent_activity": [
                    {
                        "id": activity.id,
                        "action": activity.action,
                        "description": activity.description,
                        "created_at": activity.created_at.isoformat()
                    }
                    for activity in recent_activity
                ]
            }

        except Exception as e:
            logger.error(f"Error getting user dashboard stats: {str(e)}")
            return {}

    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate user account."""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False

            user.is_active = False
            user.updated_at = datetime.utcnow()
            self.db.commit()

            # Log account deactivation
            self._log_activity(user_id, "ACCOUNT_DEACTIVATED",
                               "User account deactivated")

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deactivating user: {str(e)}")
            return False

    def _log_activity(self, user_id: str, action: str, description: str):
        """Log user activity."""
        try:
            activity = ActivityLog(
                id=str(uuid.uuid4()),
                user_id=user_id,
                action=action,
                description=description,
                ip_address="",  # Will be populated from request
                user_agent="",  # Will be populated from request
                created_at=datetime.utcnow()
            )

            self.db.add(activity)
            self.db.commit()

        except Exception as e:
            logger.error(f"Error logging activity: {str(e)}")
            # Don't raise exception as this is just logging

# Helper function to get user service instance


def get_user_service(db: Session = None) -> UserService:
    """Get user service instance."""
    if db is None:
        db = next(get_db_session())
    return UserService(db)
