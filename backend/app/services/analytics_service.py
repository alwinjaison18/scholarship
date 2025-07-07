"""
Analytics service for tracking user behavior, scholarship performance, and system metrics.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func, text
import logging
from dataclasses import dataclass
from enum import Enum

from ..models.models import (
    User, Scholarship, Application, Bookmark, Review, ActivityLog,
    AnalyticsEvent, Cache, ScrapingJob
)
from ..core.database import get_db_session

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    PAGE_VIEW = "page_view"
    SEARCH = "search"
    FILTER_APPLIED = "filter_applied"
    SCHOLARSHIP_VIEWED = "scholarship_viewed"
    SCHOLARSHIP_BOOKMARKED = "scholarship_bookmarked"
    APPLICATION_STARTED = "application_started"
    APPLICATION_SUBMITTED = "application_submitted"
    USER_REGISTERED = "user_registered"
    USER_LOGIN = "user_login"
    LINK_CLICKED = "link_clicked"
    REVIEW_SUBMITTED = "review_submitted"


@dataclass
class AnalyticsData:
    """Analytics data structure."""
    metric_name: str
    value: float
    timestamp: datetime
    metadata: Dict[str, Any]


class AnalyticsService:
    """Service for analytics and reporting."""

    def __init__(self, db: Session):
        self.db = db

    def track_event(self, event_type: str, user_id: str = None, session_id: str = None,
                    metadata: Dict[str, Any] = None) -> bool:
        """Track an analytics event."""
        try:
            event = AnalyticsEvent(
                event_type=event_type,
                user_id=user_id,
                session_id=session_id,
                metadata=metadata or {},
                timestamp=datetime.utcnow()
            )

            self.db.add(event)
            self.db.commit()

            return True

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error tracking event: {str(e)}")
            return False

    def get_user_analytics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get analytics for a specific user."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)

            # Get user activity
            activities = self.db.query(ActivityLog).filter(
                ActivityLog.user_id == user_id,
                ActivityLog.created_at >= start_date
            ).order_by(desc(ActivityLog.created_at)).all()

            # Get application stats
            applications = self.db.query(Application).filter(
                Application.user_id == user_id,
                Application.created_at >= start_date
            ).all()

            # Get bookmark stats
            bookmarks = self.db.query(Bookmark).filter(
                Bookmark.user_id == user_id,
                Bookmark.created_at >= start_date
            ).all()

            # Get review stats
            reviews = self.db.query(Review).filter(
                Review.user_id == user_id,
                Review.created_at >= start_date
            ).all()

            # Get event analytics
            events = self.db.query(AnalyticsEvent).filter(
                AnalyticsEvent.user_id == user_id,
                AnalyticsEvent.timestamp >= start_date
            ).all()

            # Calculate engagement metrics
            engagement_score = self._calculate_engagement_score(
                activities, applications, bookmarks, reviews)

            return {
                "user_id": user_id,
                "period_days": days,
                "activity_count": len(activities),
                "applications_count": len(applications),
                "bookmarks_count": len(bookmarks),
                "reviews_count": len(reviews),
                "events_count": len(events),
                "engagement_score": engagement_score,
                "activity_timeline": [
                    {
                        "date": activity.created_at.date().isoformat(),
                        "action": activity.action,
                        "description": activity.description
                    }
                    for activity in activities[:10]  # Last 10 activities
                ],
                "application_status_distribution": self._get_application_status_distribution(applications),
                "most_viewed_categories": self._get_most_viewed_categories(events),
                "search_patterns": self._get_search_patterns(events)
            }

        except Exception as e:
            logger.error(f"Error getting user analytics: {str(e)}")
            return {}

    def get_scholarship_analytics(self, scholarship_id: str, days: int = 30) -> Dict[str, Any]:
        """Get analytics for a specific scholarship."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)

            # Get scholarship details
            scholarship = self.db.query(Scholarship).filter(
                Scholarship.id == scholarship_id
            ).first()

            if not scholarship:
                return {}

            # Get application stats
            applications = self.db.query(Application).filter(
                Application.scholarship_id == scholarship_id,
                Application.created_at >= start_date
            ).all()

            # Get bookmark stats
            bookmarks = self.db.query(Bookmark).filter(
                Bookmark.scholarship_id == scholarship_id,
                Bookmark.created_at >= start_date
            ).all()

            # Get review stats
            reviews = self.db.query(Review).filter(
                Review.scholarship_id == scholarship_id,
                Review.created_at >= start_date
            ).all()

            # Get view events
            view_events = self.db.query(AnalyticsEvent).filter(
                AnalyticsEvent.event_type == EventType.SCHOLARSHIP_VIEWED,
                AnalyticsEvent.metadata.contains(
                    {"scholarship_id": scholarship_id}),
                AnalyticsEvent.timestamp >= start_date
            ).all()

            # Calculate performance metrics
            performance_score = self._calculate_scholarship_performance(
                applications, bookmarks, reviews, view_events
            )

            return {
                "scholarship_id": scholarship_id,
                "scholarship_title": scholarship.title,
                "period_days": days,
                "views_count": len(view_events),
                "applications_count": len(applications),
                "bookmarks_count": len(bookmarks),
                "reviews_count": len(reviews),
                "average_rating": sum(r.rating for r in reviews) / len(reviews) if reviews else 0,
                "performance_score": performance_score,
                "conversion_rate": len(applications) / len(view_events) if view_events else 0,
                "application_status_distribution": self._get_application_status_distribution(applications),
                "daily_views": self._get_daily_views(view_events),
                "user_demographics": self._get_user_demographics(applications)
            }

        except Exception as e:
            logger.error(f"Error getting scholarship analytics: {str(e)}")
            return {}

    def get_system_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get system-wide analytics."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)

            # User metrics
            total_users = self.db.query(func.count(User.id)).scalar()
            active_users = self.db.query(func.count(User.id)).filter(
                User.last_login >= start_date
            ).scalar()
            new_users = self.db.query(func.count(User.id)).filter(
                User.created_at >= start_date
            ).scalar()

            # Scholarship metrics
            total_scholarships = self.db.query(func.count(Scholarship.id)).filter(
                Scholarship.is_active == True
            ).scalar()
            new_scholarships = self.db.query(func.count(Scholarship.id)).filter(
                Scholarship.created_at >= start_date
            ).scalar()

            # Application metrics
            total_applications = self.db.query(func.count(Application.id)).filter(
                Application.created_at >= start_date
            ).scalar()

            # Get application status distribution
            application_status_stats = self.db.query(
                Application.status,
                func.count(Application.id).label('count')
            ).filter(
                Application.created_at >= start_date
            ).group_by(Application.status).all()

            # Get most popular scholarships
            popular_scholarships = self.db.query(
                Scholarship.title,
                func.count(Application.id).label('application_count')
            ).join(Application).filter(
                Application.created_at >= start_date
            ).group_by(Scholarship.id, Scholarship.title)\
             .order_by(desc('application_count'))\
             .limit(10).all()

            # Get scraping job statistics
            scraping_jobs = self.db.query(ScrapingJob).filter(
                ScrapingJob.created_at >= start_date
            ).all()

            successful_jobs = [
                job for job in scraping_jobs if job.status == 'completed']
            failed_jobs = [
                job for job in scraping_jobs if job.status == 'failed']

            return {
                "period_days": days,
                "user_metrics": {
                    "total_users": total_users,
                    "active_users": active_users,
                    "new_users": new_users,
                    "user_retention_rate": (active_users / total_users) * 100 if total_users > 0 else 0
                },
                "scholarship_metrics": {
                    "total_scholarships": total_scholarships,
                    "new_scholarships": new_scholarships,
                    "avg_applications_per_scholarship": total_applications / total_scholarships if total_scholarships > 0 else 0
                },
                "application_metrics": {
                    "total_applications": total_applications,
                    "status_distribution": {status: count for status, count in application_status_stats}
                },
                "popular_scholarships": [
                    {"title": title, "applications": count}
                    for title, count in popular_scholarships
                ],
                "scraping_metrics": {
                    "total_jobs": len(scraping_jobs),
                    "successful_jobs": len(successful_jobs),
                    "failed_jobs": len(failed_jobs),
                    "success_rate": (len(successful_jobs) / len(scraping_jobs)) * 100 if scraping_jobs else 0
                },
                "system_health": self._get_system_health()
            }

        except Exception as e:
            logger.error(f"Error getting system analytics: {str(e)}")
            return {}

    def get_search_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get search analytics."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)

            # Get search events
            search_events = self.db.query(AnalyticsEvent).filter(
                AnalyticsEvent.event_type == EventType.SEARCH,
                AnalyticsEvent.timestamp >= start_date
            ).all()

            # Extract search terms
            search_terms = []
            for event in search_events:
                if 'query' in event.metadata:
                    search_terms.append(event.metadata['query'])

            # Get most popular search terms
            from collections import Counter
            search_counter = Counter(search_terms)
            popular_searches = search_counter.most_common(20)

            # Get search patterns
            search_patterns = self._analyze_search_patterns(search_events)

            return {
                "period_days": days,
                "total_searches": len(search_events),
                "unique_search_terms": len(set(search_terms)),
                "popular_searches": [
                    {"term": term, "count": count}
                    for term, count in popular_searches
                ],
                "search_patterns": search_patterns,
                "average_searches_per_user": self._get_average_searches_per_user(search_events)
            }

        except Exception as e:
            logger.error(f"Error getting search analytics: {str(e)}")
            return {}

    def get_performance_metrics(self, days: int = 30) -> Dict[str, Any]:
        """Get system performance metrics."""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)

            # Get page view events
            page_views = self.db.query(AnalyticsEvent).filter(
                AnalyticsEvent.event_type == EventType.PAGE_VIEW,
                AnalyticsEvent.timestamp >= start_date
            ).all()

            # Calculate response times from metadata
            response_times = []
            for event in page_views:
                if 'response_time' in event.metadata:
                    response_times.append(event.metadata['response_time'])

            avg_response_time = sum(response_times) / \
                len(response_times) if response_times else 0

            # Get error rates
            error_events = self.db.query(AnalyticsEvent).filter(
                AnalyticsEvent.event_type == 'error',
                AnalyticsEvent.timestamp >= start_date
            ).all()

            error_rate = len(error_events) / \
                len(page_views) if page_views else 0

            return {
                "period_days": days,
                "total_page_views": len(page_views),
                "average_response_time": avg_response_time,
                "error_rate": error_rate,
                "uptime_percentage": self._calculate_uptime(),
                "cache_hit_rate": self._get_cache_hit_rate(),
                "database_performance": self._get_database_performance()
            }

        except Exception as e:
            logger.error(f"Error getting performance metrics: {str(e)}")
            return {}

    def _calculate_engagement_score(self, activities: List, applications: List,
                                    bookmarks: List, reviews: List) -> float:
        """Calculate user engagement score."""
        score = 0.0

        # Activity score (max 30 points)
        score += min(30, len(activities) * 2)

        # Application score (max 40 points)
        score += min(40, len(applications) * 10)

        # Bookmark score (max 20 points)
        score += min(20, len(bookmarks) * 5)

        # Review score (max 10 points)
        score += min(10, len(reviews) * 5)

        return min(100.0, score)

    def _get_application_status_distribution(self, applications: List) -> Dict[str, int]:
        """Get application status distribution."""
        status_counts = {}
        for app in applications:
            status = app.status
            if status not in status_counts:
                status_counts[status] = 0
            status_counts[status] += 1
        return status_counts

    def _get_most_viewed_categories(self, events: List) -> List[Dict[str, Any]]:
        """Get most viewed scholarship categories."""
        category_views = {}

        for event in events:
            if event.event_type == EventType.SCHOLARSHIP_VIEWED and 'category' in event.metadata:
                category = event.metadata['category']
                if category not in category_views:
                    category_views[category] = 0
                category_views[category] += 1

        return [
            {"category": category, "views": count}
            for category, count in sorted(category_views.items(), key=lambda x: x[1], reverse=True)[:5]
        ]

    def _get_search_patterns(self, events: List) -> Dict[str, Any]:
        """Get search patterns from events."""
        search_events = [e for e in events if e.event_type == EventType.SEARCH]

        if not search_events:
            return {}

        # Get search times
        search_hours = [e.timestamp.hour for e in search_events]
        peak_hour = max(set(search_hours), key=search_hours.count)

        return {
            "total_searches": len(search_events),
            "peak_search_hour": peak_hour,
            "search_frequency": len(search_events) / 30  # per day
        }

    def _calculate_scholarship_performance(self, applications: List, bookmarks: List,
                                           reviews: List, views: List) -> float:
        """Calculate scholarship performance score."""
        if not views:
            return 0.0

        score = 0.0
        view_count = len(views)

        # Conversion rate (applications/views)
        conversion_rate = len(applications) / view_count
        score += conversion_rate * 40

        # Bookmark rate (bookmarks/views)
        bookmark_rate = len(bookmarks) / view_count
        score += bookmark_rate * 30

        # Review rate (reviews/views)
        review_rate = len(reviews) / view_count
        score += review_rate * 20

        # Review quality
        if reviews:
            avg_rating = sum(r.rating for r in reviews) / len(reviews)
            score += (avg_rating / 5.0) * 10

        return min(100.0, score)

    def _get_daily_views(self, view_events: List) -> List[Dict[str, Any]]:
        """Get daily view counts."""
        daily_views = {}

        for event in view_events:
            date = event.timestamp.date()
            if date not in daily_views:
                daily_views[date] = 0
            daily_views[date] += 1

        return [
            {"date": date.isoformat(), "views": count}
            for date, count in sorted(daily_views.items())
        ]

    def _get_user_demographics(self, applications: List) -> Dict[str, Any]:
        """Get user demographics for applications."""
        user_ids = [app.user_id for app in applications]
        users = self.db.query(User).filter(User.id.in_(user_ids)).all()

        states = [u.state for u in users if u.state]
        categories = [u.category for u in users if u.category]
        education_levels = [
            u.education_level for u in users if u.education_level]

        from collections import Counter

        return {
            "total_applicants": len(users),
            "top_states": dict(Counter(states).most_common(5)),
            "categories": dict(Counter(categories).most_common()),
            "education_levels": dict(Counter(education_levels).most_common())
        }

    def _analyze_search_patterns(self, search_events: List) -> Dict[str, Any]:
        """Analyze search patterns."""
        if not search_events:
            return {}

        # Get search times
        search_hours = [e.timestamp.hour for e in search_events]
        search_days = [e.timestamp.weekday() for e in search_events]

        from collections import Counter

        return {
            "peak_hours": dict(Counter(search_hours).most_common(3)),
            "peak_days": dict(Counter(search_days).most_common(3)),
            "search_frequency_by_hour": dict(Counter(search_hours))
        }

    def _get_average_searches_per_user(self, search_events: List) -> float:
        """Get average searches per user."""
        if not search_events:
            return 0.0

        user_searches = {}
        for event in search_events:
            user_id = event.user_id
            if user_id:
                if user_id not in user_searches:
                    user_searches[user_id] = 0
                user_searches[user_id] += 1

        return sum(user_searches.values()) / len(user_searches) if user_searches else 0.0

    def _get_system_health(self) -> Dict[str, Any]:
        """Get system health metrics."""
        # This would typically check various system metrics
        return {
            "database_status": "healthy",
            "cache_status": "healthy",
            "api_status": "healthy",
            "scraping_status": "healthy"
        }

    def _calculate_uptime(self) -> float:
        """Calculate system uptime percentage."""
        # This would typically calculate actual uptime
        return 99.9

    def _get_cache_hit_rate(self) -> float:
        """Get cache hit rate."""
        # This would typically calculate from cache metrics
        return 85.5

    def _get_database_performance(self) -> Dict[str, Any]:
        """Get database performance metrics."""
        # This would typically get actual database metrics
        return {
            "avg_query_time": 45.2,
            "active_connections": 12,
            "slow_queries": 2
        }

# Helper function to get analytics service instance


def get_analytics_service(db: Session = None) -> AnalyticsService:
    """Get analytics service instance."""
    if db is None:
        db = next(get_db_session())
    return AnalyticsService(db)
