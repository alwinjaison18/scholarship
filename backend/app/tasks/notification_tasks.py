"""
Background tasks for sending notifications to users.
"""

from ..models.models import User, Notification, Scholarship
from ..services.notification_service import NotificationService
from ..core.database import get_db_session
from celery_app import app
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from celery import current_task
from sqlalchemy.orm import Session

# Import celery app from parent directory
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)


@app.task(bind=True, retry_backoff=True, retry_kwargs={'max_retries': 3})
def send_email_notification(self, user_id: int, notification_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send email notification to user.

    Args:
        user_id: User ID to send notification to
        notification_type: Type of notification
        data: Notification data

    Returns:
        Dict with send result
    """
    try:
        with get_db_session() as db:
            notification_service = NotificationService(db)

            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User {user_id} not found")

            # Send notification
            result = notification_service.send_email_notification(
                user=user,
                notification_type=notification_type,
                data=data
            )

            return {
                'status': 'sent' if result else 'failed',
                'user_id': user_id,
                'notification_type': notification_type,
                'timestamp': datetime.utcnow().isoformat()
            }

    except Exception as e:
        logger.error(f"Error sending email notification: {str(e)}")
        raise self.retry(exc=e, countdown=60)


@app.task(bind=True, retry_backoff=True, retry_kwargs={'max_retries': 3})
def send_bulk_notifications(self, notification_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Send bulk notifications to multiple users.

    Args:
        notification_data: List of notification data

    Returns:
        Dict with send results
    """
    try:
        with get_db_session() as db:
            notification_service = NotificationService(db)

            results = []
            for data in notification_data:
                user_id = data.get('user_id')
                notification_type = data.get('notification_type')
                content = data.get('content', {})

                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    logger.warning(f"User {user_id} not found")
                    continue

                result = notification_service.send_email_notification(
                    user=user,
                    notification_type=notification_type,
                    data=content
                )

                results.append({
                    'user_id': user_id,
                    'notification_type': notification_type,
                    'sent': result,
                    'timestamp': datetime.utcnow().isoformat()
                })

                # Update task progress
                current_task.update_state(
                    state='PROGRESS',
                    meta={'processed': len(
                        results), 'total': len(notification_data)}
                )

            return {
                'status': 'completed',
                'processed': len(results),
                'total': len(notification_data),
                'results': results
            }

    except Exception as e:
        logger.error(f"Error sending bulk notifications: {str(e)}")
        raise self.retry(exc=e, countdown=60)


@app.task(bind=True, retry_backoff=True, retry_kwargs={'max_retries': 3})
def send_deadline_reminders(self) -> Dict[str, Any]:
    """
    Send deadline reminders for scholarships.

    Returns:
        Dict with reminder results
    """
    try:
        with get_db_session() as db:
            notification_service = NotificationService(db)

            # Get scholarships with deadlines in the next 7 days
            deadline_threshold = datetime.utcnow() + timedelta(days=7)
            upcoming_scholarships = db.query(Scholarship).filter(
                Scholarship.deadline <= deadline_threshold,
                Scholarship.deadline > datetime.utcnow(),
                Scholarship.is_active == True
            ).all()

            if not upcoming_scholarships:
                return {
                    'status': 'completed',
                    'message': 'No upcoming deadlines'
                }

            # Get users interested in these scholarships
            notifications_sent = 0
            for scholarship in upcoming_scholarships:
                # Find users who have shown interest or applied
                interested_users = db.query(User).filter(
                    User.is_active == True,
                    User.email_notifications_enabled == True
                ).all()

                for user in interested_users:
                    # Check if user matches scholarship criteria
                    if notification_service.should_notify_user(user, scholarship):
                        result = notification_service.send_email_notification(
                            user=user,
                            notification_type='deadline_reminder',
                            data={
                                'scholarship': scholarship.to_dict(),
                                'days_remaining': (scholarship.deadline - datetime.utcnow()).days
                            }
                        )

                        if result:
                            notifications_sent += 1

            return {
                'status': 'completed',
                'scholarships_processed': len(upcoming_scholarships),
                'notifications_sent': notifications_sent
            }

    except Exception as e:
        logger.error(f"Error sending deadline reminders: {str(e)}")
        raise self.retry(exc=e, countdown=60)


@app.task(bind=True, retry_backoff=True, retry_kwargs={'max_retries': 3})
def send_new_scholarship_alerts(self, scholarship_id: int) -> Dict[str, Any]:
    """
    Send alerts for new scholarships to matching users.

    Args:
        scholarship_id: ID of the new scholarship

    Returns:
        Dict with alert results
    """
    try:
        with get_db_session() as db:
            notification_service = NotificationService(db)

            scholarship = db.query(Scholarship).filter(
                Scholarship.id == scholarship_id
            ).first()

            if not scholarship:
                raise ValueError(f"Scholarship {scholarship_id} not found")

            # Find users who match the scholarship criteria
            matching_users = notification_service.find_matching_users(
                scholarship)

            notifications_sent = 0
            for user in matching_users:
                result = notification_service.send_email_notification(
                    user=user,
                    notification_type='new_scholarship',
                    data={
                        'scholarship': scholarship.to_dict(),
                        'match_reasons': notification_service.get_match_reasons(user, scholarship)
                    }
                )

                if result:
                    notifications_sent += 1

            return {
                'status': 'completed',
                'scholarship_id': scholarship_id,
                'matching_users': len(matching_users),
                'notifications_sent': notifications_sent
            }

    except Exception as e:
        logger.error(f"Error sending new scholarship alerts: {str(e)}")
        raise self.retry(exc=e, countdown=60)


@app.task(bind=True, retry_backoff=True, retry_kwargs={'max_retries': 3})
def cleanup_old_notifications(self) -> Dict[str, Any]:
    """
    Clean up old notifications.

    Returns:
        Dict with cleanup results
    """
    try:
        with get_db_session() as db:
            # Delete notifications older than 30 days
            cutoff_date = datetime.utcnow() - timedelta(days=30)

            old_notifications = db.query(Notification).filter(
                Notification.created_at <= cutoff_date
            ).all()

            deleted_count = 0
            for notification in old_notifications:
                db.delete(notification)
                deleted_count += 1

            db.commit()

            return {
                'status': 'completed',
                'deleted_notifications': deleted_count
            }

    except Exception as e:
        logger.error(f"Error cleaning up notifications: {str(e)}")
        raise self.retry(exc=e, countdown=60)
