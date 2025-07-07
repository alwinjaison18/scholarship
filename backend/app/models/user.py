"""
User model definitions.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Dict, Any, Optional

Base = declarative_base()


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    date_of_birth = Column(DateTime)

    # Profile information
    profile = Column(JSON)  # Store flexible profile data

    # Preferences
    notification_preferences = Column(JSON)
    search_preferences = Column(JSON)

    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    email_notifications_enabled = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    last_login = Column(DateTime)

    # Relationships
    applications = relationship("Application", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'profile': self.profile,
            'notification_preferences': self.notification_preferences,
            'search_preferences': self.search_preferences,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'email_notifications_enabled': self.email_notifications_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class Application(Base):
    """Application model."""
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scholarship_id = Column(Integer, ForeignKey(
        "scholarships.id"), nullable=False)

    # applied, under_review, accepted, rejected
    status = Column(String(50), default="applied")
    application_data = Column(JSON)
    submitted_documents = Column(JSON)
    notes = Column(Text)

    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="applications")
    scholarship = relationship("Scholarship", back_populates="applications")


class Notification(Base):
    """Notification model."""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scholarship_id = Column(Integer, ForeignKey("scholarships.id"))

    # new_scholarship, deadline_reminder, status_update
    type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSON)

    is_read = Column(Boolean, default=False)
    sent_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="notifications")
    scholarship = relationship("Scholarship", back_populates="notifications")
