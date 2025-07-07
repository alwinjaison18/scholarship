# FastAPI Backend for ShikshaSetu

from app.api.test_scraping import router as test_scraping_router
from app.api.admin.admin_routes import router as admin_router
from app.tasks.validation_tasks import start_validation_scheduler
from app.tasks.notification_tasks import start_notification_scheduler
from app.tasks.scraping_tasks import start_scraping_scheduler
from app.services.analytics_service import AnalyticsService
from app.services.application_service import ApplicationService
from app.services.user_service import UserService
from app.services.notification_service import NotificationService
from app.services.scraping_service import ScrapingService
from app.services.scholarship_service import ScholarshipService
from app.schemas import schemas
from app.models import models
from app.core.logging import setup_logging
from app.core.cache import redis_client
from app.core.auth import get_current_user, get_current_admin
from app.core.database import get_db, engine
from app.core.config import settings
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import uvicorn
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import custom modules
# Import admin routes
# Import test scraping routes

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting ShikshaSetu API...")

    # Initialize services
    try:
        # Start background schedulers
        start_scraping_scheduler()
        start_notification_scheduler()
        start_validation_scheduler()

        logger.info("Background schedulers started successfully")
    except Exception as e:
        logger.error(f"Failed to start background schedulers: {e}")

    yield

    # Shutdown
    logger.info("Shutting down ShikshaSetu API...")

# Create FastAPI app
app = FastAPI(
    title="ShikshaSetu API",
    description="Production-grade Indian scholarship portal API with real-time scraping and validation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Initialize services
scholarship_service = ScholarshipService()
scraping_service = ScrapingService()
notification_service = NotificationService()
user_service = UserService()
application_service = ApplicationService()
analytics_service = AnalyticsService()

# Health check endpoint


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_status = "healthy"
        try:
            with engine.connect() as conn:
                conn.execute("SELECT 1")
        except Exception as e:
            db_status = f"unhealthy: {str(e)}"

        # Check Redis connection
        redis_status = "healthy"
        try:
            await redis_client.ping()
        except Exception as e:
            redis_status = f"unhealthy: {str(e)}"

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "database": db_status,
                "redis": redis_status,
                "api": "healthy"
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "unhealthy", "error": str(e)}
        )

# Scholarship endpoints


@app.get("/api/scholarships", response_model=schemas.ScholarshipSearchResult)
async def get_scholarships(
    skip: int = Query(0, ge=0, description="Number of scholarships to skip"),
    limit: int = Query(
        20, ge=1, le=100, description="Number of scholarships to return"),
    search: Optional[str] = Query(None, description="Search term"),
    category: Optional[str] = Query(None, description="Category filter"),
    state: Optional[str] = Query(None, description="State filter"),
    level: Optional[str] = Query(None, description="Education level filter"),
    min_amount: Optional[float] = Query(
        None, ge=0, description="Minimum scholarship amount"),
    max_amount: Optional[float] = Query(
        None, ge=0, description="Maximum scholarship amount"),
    is_active: Optional[bool] = Query(
        None, description="Filter by active scholarships"),
    is_verified: Optional[bool] = Query(
        None, description="Filter by verified scholarships"),
    sort_by: Optional[str] = Query("created_at", description="Sort field"),
    sort_order: Optional[str] = Query("desc", description="Sort order"),
    db: Session = Depends(get_db)
):
    """Get scholarships with filtering, sorting, and pagination"""
    try:
        filters = schemas.ScholarshipFilter(
            search=search,
            category=category,
            state=state,
            level=level,
            min_amount=min_amount,
            max_amount=max_amount,
            is_active=is_active,
            is_verified=is_verified,
            sort_by=sort_by,
            sort_order=sort_order,
            skip=skip,
            limit=limit
        )

        result = await scholarship_service.get_scholarships(db, filters)
        return result
    except Exception as e:
        logger.error(f"Error getting scholarships: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve scholarships")


@app.get("/api/scholarships/{scholarship_id}", response_model=schemas.ScholarshipDetail)
async def get_scholarship(
    scholarship_id: str,
    db: Session = Depends(get_db)
):
    """Get scholarship details by ID"""
    try:
        scholarship = await scholarship_service.get_scholarship_by_id(db, scholarship_id)
        if not scholarship:
            raise HTTPException(
                status_code=404, detail="Scholarship not found")

        # Increment view count
        await scholarship_service.increment_view_count(db, scholarship_id)

        return scholarship
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting scholarship {scholarship_id}: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve scholarship")


@app.get("/api/scholarships/featured", response_model=List[schemas.ScholarshipSummary])
async def get_featured_scholarships(
    limit: int = Query(
        6, ge=1, le=20, description="Number of featured scholarships"),
    db: Session = Depends(get_db)
):
    """Get featured scholarships"""
    try:
        scholarships = await scholarship_service.get_featured_scholarships(db, limit)
        return scholarships
    except Exception as e:
        logger.error(f"Error getting featured scholarships: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve featured scholarships")


@app.get("/api/scholarships/categories", response_model=List[schemas.CategoryStats])
async def get_scholarship_categories(db: Session = Depends(get_db)):
    """Get scholarship categories with counts"""
    try:
        categories = await scholarship_service.get_categories_with_counts(db)
        return categories
    except Exception as e:
        logger.error(f"Error getting scholarship categories: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve categories")


@app.get("/api/scholarships/stats", response_model=schemas.ScholarshipStats)
async def get_scholarship_stats(db: Session = Depends(get_db)):
    """Get scholarship statistics"""
    try:
        stats = await scholarship_service.get_scholarship_stats(db)
        return stats
    except Exception as e:
        logger.error(f"Error getting scholarship stats: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve statistics")

# User endpoints


@app.post("/api/users/register", response_model=schemas.UserResponse)
async def register_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    try:
        user = await user_service.create_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Failed to register user")


@app.post("/api/users/login", response_model=schemas.TokenResponse)
async def login_user(
    credentials: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    """User login"""
    try:
        token_data = await user_service.authenticate_user(db, credentials)
        return token_data
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        raise HTTPException(status_code=500, detail="Failed to login")


@app.get("/api/users/profile", response_model=schemas.UserProfile)
async def get_user_profile(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user profile"""
    try:
        profile = await user_service.get_user_profile(db, current_user.id)
        return profile
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve profile")


@app.put("/api/users/profile", response_model=schemas.UserProfile)
async def update_user_profile(
    profile_data: schemas.UserProfileUpdate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    try:
        profile = await user_service.update_user_profile(db, current_user.id, profile_data)
        return profile
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to update profile")

# Application endpoints


@app.post("/api/applications", response_model=schemas.ApplicationResponse)
async def create_application(
    application_data: schemas.ApplicationCreate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new scholarship application"""
    try:
        application = await application_service.create_application(
            db, current_user.id, application_data
        )
        return application
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating application: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to create application")


@app.get("/api/applications", response_model=List[schemas.ApplicationSummary])
async def get_user_applications(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's scholarship applications"""
    try:
        applications = await application_service.get_user_applications(db, current_user.id)
        return applications
    except Exception as e:
        logger.error(f"Error getting user applications: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve applications")


@app.get("/api/applications/{application_id}", response_model=schemas.ApplicationDetail)
async def get_application(
    application_id: str,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get application details"""
    try:
        application = await application_service.get_application_by_id(
            db, application_id, current_user.id
        )
        if not application:
            raise HTTPException(
                status_code=404, detail="Application not found")
        return application
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting application {application_id}: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve application")

# Admin endpoints


@app.get("/api/admin/dashboard", response_model=schemas.AdminDashboardStats)
async def get_admin_dashboard(
    current_admin: schemas.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get admin dashboard statistics"""
    try:
        stats = await analytics_service.get_admin_dashboard_stats(db)
        return stats
    except Exception as e:
        logger.error(f"Error getting admin dashboard: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve dashboard")


@app.get("/api/admin/scholarships", response_model=schemas.ScholarshipSearchResult)
async def get_admin_scholarships(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    current_admin: schemas.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get scholarships for admin management"""
    try:
        filters = schemas.AdminScholarshipFilter(
            search=search,
            status=status,
            source=source,
            skip=skip,
            limit=limit
        )
        result = await scholarship_service.get_admin_scholarships(db, filters)
        return result
    except Exception as e:
        logger.error(f"Error getting admin scholarships: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve scholarships")


@app.put("/api/admin/scholarships/{scholarship_id}/verify")
async def verify_scholarship(
    scholarship_id: str,
    current_admin: schemas.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Verify a scholarship"""
    try:
        await scholarship_service.verify_scholarship(db, scholarship_id, current_admin.id)
        return {"message": "Scholarship verified successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error verifying scholarship {scholarship_id}: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to verify scholarship")


@app.post("/api/admin/scraping/trigger")
async def trigger_scraping(
    scraping_request: schemas.ScrapingRequest,
    background_tasks: BackgroundTasks,
    current_admin: schemas.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Trigger manual scraping job"""
    try:
        job = await scraping_service.create_scraping_job(db, scraping_request, current_admin.id)
        background_tasks.add_task(
            scraping_service.execute_scraping_job, job.id)
        return {"message": "Scraping job triggered successfully", "job_id": job.id}
    except Exception as e:
        logger.error(f"Error triggering scraping: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to trigger scraping")


@app.get("/api/admin/scraping/jobs", response_model=List[schemas.ScrapingJobSummary])
async def get_scraping_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    current_admin: schemas.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get scraping jobs"""
    try:
        jobs = await scraping_service.get_scraping_jobs(db, skip, limit, status)
        return jobs
    except Exception as e:
        logger.error(f"Error getting scraping jobs: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve scraping jobs")

# Notification endpoints


@app.get("/api/notifications", response_model=List[schemas.NotificationSummary])
async def get_user_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    unread_only: bool = Query(False),
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user notifications"""
    try:
        notifications = await notification_service.get_user_notifications(
            db, current_user.id, skip, limit, unread_only
        )
        return notifications
    except Exception as e:
        logger.error(f"Error getting user notifications: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve notifications")


@app.put("/api/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark notification as read"""
    try:
        await notification_service.mark_notification_read(db, notification_id, current_user.id)
        return {"message": "Notification marked as read"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error marking notification read: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to mark notification as read")

# Analytics endpoints


@app.get("/api/analytics/trends", response_model=schemas.AnalyticsTrends)
async def get_analytics_trends(
    period: str = Query("7d", description="Time period (7d, 30d, 90d, 1y)"),
    db: Session = Depends(get_db)
):
    """Get analytics trends"""
    try:
        trends = await analytics_service.get_trends(db, period)
        return trends
    except Exception as e:
        logger.error(f"Error getting analytics trends: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve trends")

# Search endpoints


@app.get("/api/search/suggestions")
async def get_search_suggestions(
    query: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(10, ge=1, le=20, description="Number of suggestions"),
    db: Session = Depends(get_db)
):
    """Get search suggestions"""
    try:
        suggestions = await scholarship_service.get_search_suggestions(db, query, limit)
        return {"suggestions": suggestions}
    except Exception as e:
        logger.error(f"Error getting search suggestions: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve suggestions")

# Bookmark endpoints


@app.post("/api/bookmarks/{scholarship_id}")
async def add_bookmark(
    scholarship_id: str,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add scholarship to bookmarks"""
    try:
        await user_service.add_bookmark(db, current_user.id, scholarship_id)
        return {"message": "Scholarship bookmarked successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error adding bookmark: {e}")
        raise HTTPException(status_code=500, detail="Failed to add bookmark")


@app.delete("/api/bookmarks/{scholarship_id}")
async def remove_bookmark(
    scholarship_id: str,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove scholarship from bookmarks"""
    try:
        await user_service.remove_bookmark(db, current_user.id, scholarship_id)
        return {"message": "Bookmark removed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error removing bookmark: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to remove bookmark")


@app.get("/api/bookmarks", response_model=List[schemas.ScholarshipSummary])
async def get_bookmarks(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's bookmarked scholarships"""
    try:
        bookmarks = await user_service.get_bookmarks(db, current_user.id, skip, limit)
        return bookmarks
    except Exception as e:
        logger.error(f"Error getting bookmarks: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to retrieve bookmarks")

# Include admin routes
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
# Include test scraping routes (remove in production)
app.include_router(test_scraping_router, prefix="/api/test", tags=["testing"])

# Error handlers


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS if not settings.DEBUG else 1,
        access_log=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )
