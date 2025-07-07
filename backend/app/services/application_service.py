"""
Application service for handling scholarship applications and related operations.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func, text
from fastapi import HTTPException, status
import uuid
import logging
from enum import Enum

from ..models.models import Application, Scholarship, User, Notification, ActivityLog
from ..core.database import get_db_session

logger = logging.getLogger(__name__)


class ApplicationStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class ApplicationService:
    """Service for managing scholarship applications."""

    def __init__(self, db: Session):
        self.db = db

    def create_application(self, user_id: str, scholarship_id: str, application_data: Dict[str, Any]) -> Application:
        """Create a new scholarship application."""
        try:
            # Validate user exists
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Validate scholarship exists and is active
            scholarship = self.db.query(Scholarship).filter(
                Scholarship.id == scholarship_id,
                Scholarship.is_active == True
            ).first()
            if not scholarship:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Scholarship not found or inactive"
                )

            # Check if user already applied
            existing_application = self.db.query(Application).filter(
                Application.user_id == user_id,
                Application.scholarship_id == scholarship_id
            ).first()

            if existing_application:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You have already applied for this scholarship"
                )

            # Check application deadline
            if scholarship.application_deadline and datetime.utcnow() > scholarship.application_deadline:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Application deadline has passed"
                )

            # Create application
            application = Application(
                id=str(uuid.uuid4()),
                user_id=user_id,
                scholarship_id=scholarship_id,
                status=ApplicationStatus.DRAFT,
                application_data=application_data,
                submitted_at=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            self.db.add(application)
            self.db.commit()
            self.db.refresh(application)

            # Log application creation
            self._log_activity(
                user_id,
                "APPLICATION_CREATED",
                f"Created application for scholarship: {scholarship.title}"
            )

            logger.info(
                f"Application created: {application.id} for user: {user_id}")
            return application

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating application: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating application"
            )

    def update_application(self, application_id: str, user_id: str, update_data: Dict[str, Any]) -> Application:
        """Update application data."""
        try:
            application = self.db.query(Application).filter(
                Application.id == application_id,
                Application.user_id == user_id
            ).first()

            if not application:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Application not found"
                )

            # Check if application can be updated
            if application.status not in [ApplicationStatus.DRAFT, ApplicationStatus.SUBMITTED]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Application cannot be updated in current status"
                )

            # Update application data
            if "application_data" in update_data:
                application.application_data = update_data["application_data"]

            if "notes" in update_data:
                application.notes = update_data["notes"]

            application.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(application)

            # Log application update
            self._log_activity(
                user_id,
                "APPLICATION_UPDATED",
                f"Updated application: {application.id}"
            )

            return application

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating application: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating application"
            )

    def submit_application(self, application_id: str, user_id: str) -> Application:
        """Submit application for review."""
        try:
            application = self.db.query(Application).filter(
                Application.id == application_id,
                Application.user_id == user_id
            ).first()

            if not application:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Application not found"
                )

            # Check if application is in draft status
            if application.status != ApplicationStatus.DRAFT:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Application is not in draft status"
                )

            # Validate required fields
            if not application.application_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Application data is required"
                )

            # Check scholarship deadline
            scholarship = self.db.query(Scholarship).filter(
                Scholarship.id == application.scholarship_id
            ).first()

            if scholarship and scholarship.application_deadline and datetime.utcnow() > scholarship.application_deadline:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Application deadline has passed"
                )

            # Submit application
            application.status = ApplicationStatus.SUBMITTED
            application.submitted_at = datetime.utcnow()
            application.updated_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(application)

            # Create notification
            self._create_notification(
                user_id,
                "APPLICATION_SUBMITTED",
                f"Your application for {scholarship.title} has been submitted successfully",
                {"application_id": application.id,
                    "scholarship_id": scholarship.id}
            )

            # Log application submission
            self._log_activity(
                user_id,
                "APPLICATION_SUBMITTED",
                f"Submitted application: {application.id}"
            )

            return application

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error submitting application: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error submitting application"
            )

    def withdraw_application(self, application_id: str, user_id: str, reason: str = "") -> Application:
        """Withdraw application."""
        try:
            application = self.db.query(Application).filter(
                Application.id == application_id,
                Application.user_id == user_id
            ).first()

            if not application:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Application not found"
                )

            # Check if application can be withdrawn
            if application.status not in [ApplicationStatus.SUBMITTED, ApplicationStatus.UNDER_REVIEW]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Application cannot be withdrawn in current status"
                )

            # Withdraw application
            application.status = ApplicationStatus.WITHDRAWN
            application.notes = f"Withdrawn by user. Reason: {reason}" if reason else "Withdrawn by user"
            application.updated_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(application)

            # Create notification
            scholarship = self.db.query(Scholarship).filter(
                Scholarship.id == application.scholarship_id
            ).first()

            self._create_notification(
                user_id,
                "APPLICATION_WITHDRAWN",
                f"Your application for {scholarship.title} has been withdrawn",
                {"application_id": application.id,
                    "scholarship_id": scholarship.id}
            )

            # Log application withdrawal
            self._log_activity(
                user_id,
                "APPLICATION_WITHDRAWN",
                f"Withdrew application: {application.id}"
            )

            return application

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error withdrawing application: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error withdrawing application"
            )

    def get_application(self, application_id: str, user_id: str = None) -> Optional[Application]:
        """Get application by ID."""
        query = self.db.query(Application).filter(
            Application.id == application_id)

        if user_id:
            query = query.filter(Application.user_id == user_id)

        return query.first()

    def get_user_applications(self, user_id: str, status: str = None, limit: int = 10, offset: int = 0) -> List[Application]:
        """Get user's applications with optional status filter."""
        query = self.db.query(Application).filter(
            Application.user_id == user_id)

        if status:
            query = query.filter(Application.status == status)

        return query.order_by(desc(Application.created_at))\
            .limit(limit)\
            .offset(offset)\
            .all()

    def get_scholarship_applications(self, scholarship_id: str, status: str = None, limit: int = 10, offset: int = 0) -> List[Application]:
        """Get applications for a specific scholarship."""
        query = self.db.query(Application).filter(
            Application.scholarship_id == scholarship_id)

        if status:
            query = query.filter(Application.status == status)

        return query.order_by(desc(Application.created_at))\
            .limit(limit)\
            .offset(offset)\
            .all()

    def get_application_statistics(self, user_id: str = None, scholarship_id: str = None) -> Dict[str, Any]:
        """Get application statistics."""
        try:
            base_query = self.db.query(Application)

            if user_id:
                base_query = base_query.filter(Application.user_id == user_id)

            if scholarship_id:
                base_query = base_query.filter(
                    Application.scholarship_id == scholarship_id)

            # Get status counts
            status_counts = base_query.with_entities(
                Application.status,
                func.count(Application.id).label('count')
            ).group_by(Application.status).all()

            # Get monthly application counts (last 12 months)
            monthly_counts = base_query.with_entities(
                func.date_trunc(
                    'month', Application.created_at).label('month'),
                func.count(Application.id).label('count')
            ).filter(
                Application.created_at >= datetime.utcnow() - timedelta(days=365)
            ).group_by(
                func.date_trunc('month', Application.created_at)
            ).order_by(
                func.date_trunc('month', Application.created_at)
            ).all()

            # Get total applications
            total_count = base_query.count()

            return {
                "total_applications": total_count,
                "status_counts": {status: count for status, count in status_counts},
                "monthly_counts": [
                    {
                        "month": month.strftime("%Y-%m"),
                        "count": count
                    } for month, count in monthly_counts
                ]
            }

        except Exception as e:
            logger.error(f"Error getting application statistics: {str(e)}")
            return {}

    def update_application_status(self, application_id: str, new_status: str, admin_notes: str = "") -> Application:
        """Update application status (admin only)."""
        try:
            application = self.db.query(Application).filter(
                Application.id == application_id
            ).first()

            if not application:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Application not found"
                )

            old_status = application.status
            application.status = new_status
            application.admin_notes = admin_notes
            application.updated_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(application)

            # Create notification to user
            scholarship = self.db.query(Scholarship).filter(
                Scholarship.id == application.scholarship_id
            ).first()

            status_messages = {
                ApplicationStatus.UNDER_REVIEW: f"Your application for {scholarship.title} is now under review",
                ApplicationStatus.APPROVED: f"Congratulations! Your application for {scholarship.title} has been approved",
                ApplicationStatus.REJECTED: f"Your application for {scholarship.title} has been rejected"
            }

            if new_status in status_messages:
                self._create_notification(
                    application.user_id,
                    f"APPLICATION_{new_status.upper()}",
                    status_messages[new_status],
                    {"application_id": application.id,
                        "scholarship_id": scholarship.id}
                )

            # Log status change
            self._log_activity(
                application.user_id,
                "APPLICATION_STATUS_CHANGED",
                f"Application status changed from {old_status} to {new_status}"
            )

            return application

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating application status: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating application status"
            )

    def search_applications(self, query: str, filters: Dict[str, Any] = None, limit: int = 10, offset: int = 0) -> List[Application]:
        """Search applications with filters."""
        try:
            # Build base query
            base_query = self.db.query(Application)\
                .join(Scholarship, Application.scholarship_id == Scholarship.id)\
                .join(User, Application.user_id == User.id)

            # Apply text search
            if query:
                base_query = base_query.filter(
                    or_(
                        Scholarship.title.ilike(f"%{query}%"),
                        User.full_name.ilike(f"%{query}%"),
                        User.email.ilike(f"%{query}%")
                    )
                )

            # Apply filters
            if filters:
                if "status" in filters:
                    base_query = base_query.filter(
                        Application.status == filters["status"])

                if "scholarship_id" in filters:
                    base_query = base_query.filter(
                        Application.scholarship_id == filters["scholarship_id"])

                if "user_id" in filters:
                    base_query = base_query.filter(
                        Application.user_id == filters["user_id"])

                if "date_from" in filters:
                    base_query = base_query.filter(
                        Application.created_at >= filters["date_from"])

                if "date_to" in filters:
                    base_query = base_query.filter(
                        Application.created_at <= filters["date_to"])

            return base_query.order_by(desc(Application.created_at))\
                .limit(limit)\
                .offset(offset)\
                .all()

        except Exception as e:
            logger.error(f"Error searching applications: {str(e)}")
            return []

    def _create_notification(self, user_id: str, notification_type: str, message: str, metadata: Dict[str, Any] = None):
        """Create notification for user."""
        try:
            notification = Notification(
                id=str(uuid.uuid4()),
                user_id=user_id,
                type=notification_type,
                title=notification_type.replace("_", " ").title(),
                message=message,
                metadata=metadata or {},
                is_read=False,
                created_at=datetime.utcnow()
            )

            self.db.add(notification)
            self.db.commit()

        except Exception as e:
            logger.error(f"Error creating notification: {str(e)}")

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

# Helper function to get application service instance


def get_application_service(db: Session = None) -> ApplicationService:
    """Get application service instance."""
    if db is None:
        db = next(get_db_session())
    return ApplicationService(db)
