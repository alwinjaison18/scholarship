"""
Scholarship service for managing scholarship data and operations.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc

from ..core.database import db_transaction
from ..models.models import Scholarship, User, Application, ScrapingSource
from ..utils.text_processing import TextProcessor
from ..utils.deduplication import DuplicationDetector

logger = logging.getLogger(__name__)


class ScholarshipService:
    """Service for managing scholarship operations."""

    def __init__(self, db: Session):
        self.db = db
        self.text_processor = TextProcessor()
        self.deduplication_detector = DuplicationDetector()

    def get_scholarship_by_id(self, scholarship_id: int) -> Optional[Scholarship]:
        """Get scholarship by ID."""
        return self.db.query(Scholarship).filter(
            Scholarship.id == scholarship_id
        ).first()

    def get_scholarships_by_criteria(
        self,
        category: Optional[str] = None,
        eligibility: Optional[str] = None,
        amount_min: Optional[float] = None,
        amount_max: Optional[float] = None,
        deadline_start: Optional[datetime] = None,
        deadline_end: Optional[datetime] = None,
        is_active: bool = True,
        limit: int = 100,
        offset: int = 0
    ) -> List[Scholarship]:
        """Get scholarships by various criteria."""
        query = self.db.query(Scholarship)

        if is_active:
            query = query.filter(Scholarship.is_active == True)

        if category:
            query = query.filter(Scholarship.category.ilike(f'%{category}%'))

        if eligibility:
            query = query.filter(
                Scholarship.eligibility.ilike(f'%{eligibility}%'))

        if amount_min is not None:
            query = query.filter(Scholarship.amount >= amount_min)

        if amount_max is not None:
            query = query.filter(Scholarship.amount <= amount_max)

        if deadline_start:
            query = query.filter(Scholarship.deadline >= deadline_start)

        if deadline_end:
            query = query.filter(Scholarship.deadline <= deadline_end)

        return query.order_by(desc(Scholarship.created_at)).offset(offset).limit(limit).all()

    def search_scholarships(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Scholarship]:
        """Search scholarships by text query."""
        base_query = self.db.query(Scholarship).filter(
            Scholarship.is_active == True
        )

        if query:
            # Search in title, description, category, and eligibility
            search_filter = or_(
                Scholarship.title.ilike(f'%{query}%'),
                Scholarship.description.ilike(f'%{query}%'),
                Scholarship.category.ilike(f'%{query}%'),
                Scholarship.eligibility.ilike(f'%{query}%')
            )
            base_query = base_query.filter(search_filter)

        if filters:
            if filters.get('category'):
                base_query = base_query.filter(
                    Scholarship.category.ilike(f'%{filters["category"]}%')
                )

            if filters.get('amount_min'):
                base_query = base_query.filter(
                    Scholarship.amount >= filters['amount_min']
                )

            if filters.get('amount_max'):
                base_query = base_query.filter(
                    Scholarship.amount <= filters['amount_max']
                )

            if filters.get('deadline_start'):
                base_query = base_query.filter(
                    Scholarship.deadline >= filters['deadline_start']
                )

            if filters.get('deadline_end'):
                base_query = base_query.filter(
                    Scholarship.deadline <= filters['deadline_end']
                )

        return base_query.order_by(desc(Scholarship.quality_score)).offset(offset).limit(limit).all()

    def get_trending_scholarships(self, limit: int = 10) -> List[Scholarship]:
        """Get trending scholarships based on views and applications."""
        return self.db.query(Scholarship).filter(
            Scholarship.is_active == True,
            Scholarship.deadline > datetime.utcnow()
        ).order_by(
            desc(Scholarship.view_count),
            desc(Scholarship.application_count)
        ).limit(limit).all()

    def get_scholarships_by_deadline(
        self,
        days_ahead: int = 30,
        limit: int = 100
    ) -> List[Scholarship]:
        """Get scholarships with upcoming deadlines."""
        deadline_threshold = datetime.utcnow() + timedelta(days=days_ahead)

        return self.db.query(Scholarship).filter(
            Scholarship.is_active == True,
            Scholarship.deadline <= deadline_threshold,
            Scholarship.deadline > datetime.utcnow()
        ).order_by(Scholarship.deadline).limit(limit).all()

    def get_recommended_scholarships(
        self,
        user: User,
        limit: int = 20
    ) -> List[Scholarship]:
        """Get recommended scholarships for a user."""
        # Get user's application history
        user_applications = self.db.query(Application).filter(
            Application.user_id == user.id
        ).all()

        applied_categories = [
            app.scholarship.category for app in user_applications if app.scholarship]

        # Get scholarships in similar categories
        query = self.db.query(Scholarship).filter(
            Scholarship.is_active == True,
            Scholarship.deadline > datetime.utcnow()
        )

        if applied_categories:
            query = query.filter(
                Scholarship.category.in_(applied_categories)
            )

        # Filter by user profile if available
        if user.profile:
            profile = user.profile
            if profile.get('education_level'):
                query = query.filter(
                    Scholarship.eligibility.ilike(
                        f'%{profile["education_level"]}%')
                )

            if profile.get('field_of_study'):
                query = query.filter(
                    or_(
                        Scholarship.category.ilike(
                            f'%{profile["field_of_study"]}%'),
                        Scholarship.eligibility.ilike(
                            f'%{profile["field_of_study"]}%')
                    )
                )

        return query.order_by(desc(Scholarship.quality_score)).limit(limit).all()

    def create_scholarship(self, scholarship_data: Dict[str, Any]) -> Scholarship:
        """Create a new scholarship."""
        # Check for duplicates
        existing_scholarship = self.find_duplicate_scholarship(
            scholarship_data)
        if existing_scholarship:
            logger.info(
                f"Duplicate scholarship found: {existing_scholarship.id}")
            return existing_scholarship

        # Process text data
        processed_data = self.text_processor.process_scholarship_data(
            scholarship_data)

        scholarship = Scholarship(**processed_data)
        self.db.add(scholarship)
        self.db.commit()
        self.db.refresh(scholarship)

        logger.info(f"Created new scholarship: {scholarship.id}")
        return scholarship

    def update_scholarship(
        self,
        scholarship_id: int,
        update_data: Dict[str, Any]
    ) -> Optional[Scholarship]:
        """Update an existing scholarship."""
        scholarship = self.get_scholarship_by_id(scholarship_id)
        if not scholarship:
            return None

        # Process text data
        processed_data = self.text_processor.process_scholarship_data(
            update_data)

        for key, value in processed_data.items():
            if hasattr(scholarship, key):
                setattr(scholarship, key, value)

        scholarship.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(scholarship)

        logger.info(f"Updated scholarship: {scholarship.id}")
        return scholarship

    def delete_scholarship(self, scholarship_id: int) -> bool:
        """Delete a scholarship."""
        scholarship = self.get_scholarship_by_id(scholarship_id)
        if not scholarship:
            return False

        # Soft delete
        scholarship.is_active = False
        scholarship.deleted_at = datetime.utcnow()
        self.db.commit()

        logger.info(f"Deleted scholarship: {scholarship.id}")
        return True

    def find_duplicate_scholarship(self, scholarship_data: Dict[str, Any]) -> Optional[Scholarship]:
        """Find potential duplicate scholarships."""
        title = scholarship_data.get('title', '')
        url = scholarship_data.get('url', '')

        if not title and not url:
            return None

        # Check for exact URL match
        if url:
            existing = self.db.query(Scholarship).filter(
                Scholarship.url == url
            ).first()
            if existing:
                return existing

        # Check for similar titles
        if title:
            similar_scholarships = self.db.query(Scholarship).filter(
                Scholarship.title.ilike(f'%{title}%')
            ).all()

            for scholarship in similar_scholarships:
                if self.deduplication_detector.are_duplicates(
                    scholarship_data, scholarship.to_dict()
                ):
                    return scholarship

        return None

    def increment_view_count(self, scholarship_id: int) -> bool:
        """Increment view count for a scholarship."""
        scholarship = self.get_scholarship_by_id(scholarship_id)
        if not scholarship:
            return False

        scholarship.view_count = (scholarship.view_count or 0) + 1
        self.db.commit()
        return True

    def increment_application_count(self, scholarship_id: int) -> bool:
        """Increment application count for a scholarship."""
        scholarship = self.get_scholarship_by_id(scholarship_id)
        if not scholarship:
            return False

        scholarship.application_count = (
            scholarship.application_count or 0) + 1
        self.db.commit()
        return True

    def get_scholarship_statistics(self) -> Dict[str, Any]:
        """Get overall scholarship statistics."""
        total_scholarships = self.db.query(Scholarship).count()
        active_scholarships = self.db.query(Scholarship).filter(
            Scholarship.is_active == True
        ).count()

        upcoming_deadlines = self.db.query(Scholarship).filter(
            Scholarship.is_active == True,
            Scholarship.deadline > datetime.utcnow(),
            Scholarship.deadline <= datetime.utcnow() + timedelta(days=30)
        ).count()

        total_amount = self.db.query(func.sum(Scholarship.amount)).filter(
            Scholarship.is_active == True,
            Scholarship.amount.isnot(None)
        ).scalar() or 0

        categories = self.db.query(
            Scholarship.category,
            func.count(Scholarship.id).label('count')
        ).filter(
            Scholarship.is_active == True
        ).group_by(Scholarship.category).all()

        return {
            'total_scholarships': total_scholarships,
            'active_scholarships': active_scholarships,
            'upcoming_deadlines': upcoming_deadlines,
            'total_amount': total_amount,
            'categories': [{'name': cat, 'count': count} for cat, count in categories]
        }

    def get_category_statistics(self) -> Dict[str, int]:
        """Get scholarship count by category."""
        categories = self.db.query(
            Scholarship.category,
            func.count(Scholarship.id).label('count')
        ).filter(
            Scholarship.is_active == True
        ).group_by(Scholarship.category).all()

        return {category: count for category, count in categories}

    def bulk_update_scholarships(
        self,
        scholarship_ids: List[int],
        update_data: Dict[str, Any]
    ) -> int:
        """Bulk update multiple scholarships."""
        updated_count = self.db.query(Scholarship).filter(
            Scholarship.id.in_(scholarship_ids)
        ).update(update_data, synchronize_session=False)

        self.db.commit()
        return updated_count
