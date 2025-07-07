"""
Notification service for handling user notifications and communication.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from fastapi import HTTPException, status
import uuid
import logging
from enum import Enum

from ..models.models import Notification, User
from ..core.database import get_db_session

logger = logging.getLogger(__name__)


class NotificationType(str, Enum):
    APPLICATION_SUBMITTED = "APPLICATION_SUBMITTED"
    APPLICATION_APPROVED = "APPLICATION_APPROVED"
    APPLICATION_REJECTED = "APPLICATION_REJECTED"
    APPLICATION_WITHDRAWN = "APPLICATION_WITHDRAWN"
    APPLICATION_UNDER_REVIEW = "APPLICATION_UNDER_REVIEW"
    SCHOLARSHIP_DEADLINE_REMINDER = "SCHOLARSHIP_DEADLINE_REMINDER"
    SCHOLARSHIP_NEW_MATCH = "SCHOLARSHIP_NEW_MATCH"
    SCHOLARSHIP_UPDATED = "SCHOLARSHIP_UPDATED"
    SYSTEM_ANNOUNCEMENT = "SYSTEM_ANNOUNCEMENT"
    ACCOUNT_VERIFICATION = "ACCOUNT_VERIFICATION"
    PASSWORD_RESET = "PASSWORD_RESET"


class NotificationService:
    """Service for managing user notifications."""

    def __init__(self, db: Session):
        self.db = db

    def create_notification(self, user_id: str, notification_type: str, title: str, message: str,
                            metadata: Dict[str, Any] = None, priority: str = "normal") -> Notification:
        """Create a new notification."""
        try:
            # Validate user exists
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Create notification
            notification = Notification(
                id=str(uuid.uuid4()),
                user_id=user_id,
                type=notification_type,
                title=title,
                message=message,
                metadata=metadata or {},
                priority=priority,
                is_read=False,
                created_at=datetime.utcnow()
            )

            self.db.add(notification)
            self.db.commit()
            self.db.refresh(notification)

            logger.info(
                f"Notification created: {notification.id} for user: {user_id}")
            return notification

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating notification: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating notification"
            )

    def get_user_notifications(self, user_id: str, is_read: bool = None, notification_type: str = None,
                               limit: int = 20, offset: int = 0) -> List[Notification]:
        """Get user's notifications with optional filters."""
        try:
            query = self.db.query(Notification).filter(
                Notification.user_id == user_id)

            if is_read is not None:
                query = query.filter(Notification.is_read == is_read)

            if notification_type:
                query = query.filter(Notification.type == notification_type)

            return query.order_by(desc(Notification.created_at))\
                .limit(limit)\
                .offset(offset)\
                .all()

        except Exception as e:
            logger.error(f"Error getting user notifications: {str(e)}")
            return []

    def mark_notification_read(self, notification_id: str, user_id: str) -> bool:
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

    def mark_all_notifications_read(self, user_id: str) -> bool:
        """Mark all notifications as read for a user."""
        try:
            self.db.query(Notification).filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            ).update({
                "is_read": True,
                "read_at": datetime.utcnow()
            })

            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error marking all notifications as read: {str(e)}")
            return False

    def delete_notification(self, notification_id: str, user_id: str) -> bool:
        """Delete a notification."""
        try:
            notification = self.db.query(Notification).filter(
                Notification.id == notification_id,
                Notification.user_id == user_id
            ).first()

            if not notification:
                return False

            self.db.delete(notification)
            self.db.commit()

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting notification: {str(e)}")
            return False

    def get_notification_counts(self, user_id: str) -> Dict[str, int]:
        """Get notification counts for a user."""
        try:
            total_count = self.db.query(func.count(Notification.id))\
                .filter(Notification.user_id == user_id)\
                .scalar()

            unread_count = self.db.query(func.count(Notification.id))\
                .filter(
                    Notification.user_id == user_id,
                    Notification.is_read == False
            )\
                .scalar()

            # Get counts by type
            type_counts = self.db.query(
                Notification.type,
                func.count(Notification.id).label('count')
            ).filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            ).group_by(Notification.type).all()

            return {
                "total": total_count,
                "unread": unread_count,
                "by_type": {notification_type: count for notification_type, count in type_counts}
            }

        except Exception as e:
            logger.error(f"Error getting notification counts: {str(e)}")
            return {"total": 0, "unread": 0, "by_type": {}}

    def create_bulk_notifications(self, user_ids: List[str], notification_type: str,
                                  title: str, message: str, metadata: Dict[str, Any] = None) -> List[Notification]:
        """Create notifications for multiple users."""
        try:
            notifications = []

            for user_id in user_ids:
                notification = Notification(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    type=notification_type,
                    title=title,
                    message=message,
                    metadata=metadata or {},
                    is_read=False,
                    created_at=datetime.utcnow()
                )
                notifications.append(notification)

            self.db.add_all(notifications)
            self.db.commit()

            logger.info(f"Created {len(notifications)} bulk notifications")
            return notifications

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating bulk notifications: {str(e)}")
            return []

    def send_deadline_reminders(self, days_before: int = 7) -> int:
        """Send deadline reminders for scholarships."""
        try:
            # This would typically query scholarships with upcoming deadlines
            # and send notifications to users who have bookmarked them
            # For now, we'll return a placeholder

            # Get scholarships with deadlines in the next X days
            from ..models.models import Scholarship, Bookmark

            upcoming_deadline = datetime.utcnow() + timedelta(days=days_before)

            scholarships = self.db.query(Scholarship).filter(
                Scholarship.application_deadline <= upcoming_deadline,
                Scholarship.application_deadline > datetime.utcnow(),
                Scholarship.is_active == True
            ).all()

            notification_count = 0

            for scholarship in scholarships:
                # Get users who bookmarked this scholarship
                bookmarked_users = self.db.query(Bookmark.user_id).filter(
                    Bookmark.scholarship_id == scholarship.id
                ).all()

                user_ids = [user.user_id for user in bookmarked_users]

                if user_ids:
                    days_left = (scholarship.application_deadline -
                                 datetime.utcnow()).days

                    self.create_bulk_notifications(
                        user_ids,
                        NotificationType.SCHOLARSHIP_DEADLINE_REMINDER,
                        "Scholarship Deadline Reminder",
                        f"The deadline for '{scholarship.title}' is in {days_left} days. Don't miss out!",
                        {"scholarship_id": scholarship.id, "days_left": days_left}
                    )

                    notification_count += len(user_ids)

            return notification_count

        except Exception as e:
            logger.error(f"Error sending deadline reminders: {str(e)}")
            return 0

    def cleanup_old_notifications(self, days_old: int = 30) -> int:
        """Delete old read notifications."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)

            deleted_count = self.db.query(Notification).filter(
                Notification.is_read == True,
                Notification.created_at < cutoff_date
            ).delete()

            self.db.commit()

            logger.info(f"Cleaned up {deleted_count} old notifications")
            return deleted_count

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error cleaning up old notifications: {str(e)}")
            return 0

    def get_notification_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user's notification preferences."""
        try:
            # This would typically query a user preferences table
            # For now, return default preferences
            return {
                "email_enabled": True,
                "push_enabled": True,
                "application_updates": True,
                "scholarship_reminders": True,
                "new_scholarships": True,
                "system_announcements": True
            }

        except Exception as e:
            logger.error(f"Error getting notification preferences: {str(e)}")
            return {}

    def update_notification_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Update user's notification preferences."""
        try:
            # This would typically update a user preferences table
            # For now, just return success
            logger.info(
                f"Updated notification preferences for user: {user_id}")
            return True

        except Exception as e:
            logger.error(f"Error updating notification preferences: {str(e)}")
            return False

    def get_system_announcements(self, limit: int = 10) -> List[Notification]:
        """Get system-wide announcements."""
        try:
            return self.db.query(Notification).filter(
                Notification.type == NotificationType.SYSTEM_ANNOUNCEMENT
            ).order_by(desc(Notification.created_at))\
             .limit(limit)\
             .all()

        except Exception as e:
            logger.error(f"Error getting system announcements: {str(e)}")
            return []

    def create_system_announcement(self, title: str, message: str, metadata: Dict[str, Any] = None) -> List[Notification]:
        """Create a system announcement for all active users."""
        try:
            # Get all active users
            active_users = self.db.query(User.id).filter(
                User.is_active == True).all()
            user_ids = [user.id for user in active_users]

            return self.create_bulk_notifications(
                user_ids,
                NotificationType.SYSTEM_ANNOUNCEMENT,
                title,
                message,
                metadata
            )

        except Exception as e:
            logger.error(f"Error creating system announcement: {str(e)}")
            return []

# Helper function to get notification service instance


def get_notification_service(db: Session = None) -> NotificationService:
    """Get notification service instance."""
    if db is None:
        db = next(get_db_session())
    return NotificationService(db)
