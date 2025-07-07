"""
Admin API endpoints for managing scraping jobs and monitoring system health
"""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, desc, asc

from app.core.database import get_db
from app.core.auth import get_current_admin_user
from app.models.models import ScrapingJob, Scholarship, User
from app.schemas import ScrapingJobResponse, ScrapingJobCreate, SystemStatsResponse
from app.tasks.scraping_tasks import (
    scrape_nsp_scholarships,
    scrape_ugc_scholarships,
    scrape_aicte_scholarships,
    validate_scholarships
)
from app.services.monitoring_service import MonitoringService

router = APIRouter()


@router.get("/dashboard/stats", response_model=SystemStatsResponse)
async def get_system_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get system statistics for admin dashboard"""

    monitoring_service = MonitoringService(db)

    # Get basic counts
    total_scholarships = db.query(Scholarship).count()
    active_scholarships = db.query(Scholarship).filter(
        Scholarship.is_active == True).count()
    verified_scholarships = db.query(Scholarship).filter(
        Scholarship.is_verified == True).count()
    total_users = db.query(User).count()

    # Get scraping job stats
    today = datetime.utcnow().date()
    jobs_today = db.query(ScrapingJob).filter(
        func.date(ScrapingJob.created_at) == today
    ).count()

    running_jobs = db.query(ScrapingJob).filter(
        ScrapingJob.status == 'running'
    ).count()

    failed_jobs_today = db.query(ScrapingJob).filter(
        func.date(ScrapingJob.created_at) == today,
        ScrapingJob.status == 'failed'
    ).count()

    # Get recent activity
    recent_scholarships = db.query(Scholarship).filter(
        Scholarship.created_at >= datetime.utcnow() - timedelta(days=7)
    ).count()

    # Get performance metrics
    avg_job_duration = db.query(func.avg(ScrapingJob.duration)).filter(
        ScrapingJob.status == 'completed',
        ScrapingJob.completed_at >= datetime.utcnow() - timedelta(days=30)
    ).scalar() or 0

    success_rate = monitoring_service.get_success_rate(days=30)

    return SystemStatsResponse(
        total_scholarships=total_scholarships,
        active_scholarships=active_scholarships,
        verified_scholarships=verified_scholarships,
        total_users=total_users,
        jobs_today=jobs_today,
        running_jobs=running_jobs,
        failed_jobs_today=failed_jobs_today,
        recent_scholarships=recent_scholarships,
        avg_job_duration=avg_job_duration,
        success_rate=success_rate
    )


@router.get("/scraping-jobs", response_model=List[ScrapingJobResponse])
async def get_scraping_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get paginated list of scraping jobs with filters"""

    query = db.query(ScrapingJob)

    # Apply filters
    if status:
        query = query.filter(ScrapingJob.status == status)

    if source:
        query = query.filter(ScrapingJob.source_name.ilike(f"%{source}%"))

    if start_date:
        query = query.filter(ScrapingJob.created_at >= start_date)

    if end_date:
        query = query.filter(ScrapingJob.created_at <= end_date)

    # Order by most recent first
    query = query.order_by(desc(ScrapingJob.created_at))

    # Apply pagination
    jobs = query.offset(skip).limit(limit).all()

    return jobs


@router.get("/scraping-jobs/{job_id}", response_model=ScrapingJobResponse)
async def get_scraping_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get detailed information about a specific scraping job"""

    job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Scraping job not found")

    return job


@router.post("/scraping-jobs/start", response_model=dict)
async def start_scraping_job(
    job_data: ScrapingJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Start a new scraping job"""

    # Create job record
    job = ScrapingJob(
        source_url=job_data.source_url,
        source_name=job_data.source_name,
        job_type="manual",
        priority=job_data.priority or "medium",
        configuration=job_data.configuration or {},
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Start appropriate scraping task based on source
    if job_data.source_name.lower() == "nsp":
        task = scrape_nsp_scholarships.delay(
            force_update=job_data.force_update)
    elif job_data.source_name.lower() == "ugc":
        task = scrape_ugc_scholarships.delay(
            force_update=job_data.force_update)
    elif job_data.source_name.lower() == "aicte":
        task = scrape_aicte_scholarships.delay(
            force_update=job_data.force_update)
    else:
        raise HTTPException(status_code=400, detail="Unknown source name")

    # Update job with task ID
    job.id = task.id
    db.commit()

    return {
        "job_id": job.id,
        "status": "started",
        "message": f"Scraping job started for {job_data.source_name}"
    }


@router.post("/scraping-jobs/{job_id}/cancel")
async def cancel_scraping_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Cancel a running scraping job"""

    job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Scraping job not found")

    if job.status != "running":
        raise HTTPException(status_code=400, detail="Job is not running")

    # Cancel the celery task
    from celery_app import app
    app.control.revoke(job_id, terminate=True)

    # Update job status
    job.status = "cancelled"
    job.completed_at = datetime.utcnow()
    db.commit()

    return {"message": "Job cancelled successfully"}


@router.post("/scraping-jobs/{job_id}/retry")
async def retry_scraping_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Retry a failed scraping job"""

    job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Scraping job not found")

    if job.status != "failed":
        raise HTTPException(
            status_code=400, detail="Job is not in failed state")

    if job.retry_count >= job.max_retries:
        raise HTTPException(
            status_code=400, detail="Maximum retry attempts reached")

    # Reset job status
    job.status = "pending"
    job.retry_count += 1
    job.started_at = None
    job.completed_at = None
    job.next_retry_at = datetime.utcnow() + timedelta(minutes=5)

    db.commit()

    # Restart the task
    if job.source_name.lower() == "nsp":
        task = scrape_nsp_scholarships.delay(force_update=True)
    elif job.source_name.lower() == "ugc":
        task = scrape_ugc_scholarships.delay(force_update=True)
    elif job.source_name.lower() == "aicte":
        task = scrape_aicte_scholarships.delay(force_update=True)

    return {"message": "Job retry initiated"}


@router.get("/system-health")
async def get_system_health(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get system health metrics"""

    monitoring_service = MonitoringService(db)

    # Check database health
    db_health = monitoring_service.check_database_health()

    # Check Redis/Celery health
    celery_health = monitoring_service.check_celery_health()

    # Check scraping job health
    job_health = monitoring_service.check_scraping_job_health()

    # Check memory and CPU usage
    resource_usage = monitoring_service.get_resource_usage()

    overall_status = "healthy"
    if not db_health["status"] or not celery_health["status"] or not job_health["status"]:
        overall_status = "unhealthy"
    elif resource_usage["memory_usage"] > 80 or resource_usage["cpu_usage"] > 80:
        overall_status = "warning"

    return {
        "overall_status": overall_status,
        "database": db_health,
        "celery": celery_health,
        "scraping_jobs": job_health,
        "resources": resource_usage,
        "timestamp": datetime.utcnow()
    }


@router.post("/validate-scholarships")
async def trigger_scholarship_validation(
    force_revalidate: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Trigger scholarship validation process"""

    task = validate_scholarships.delay(force_revalidate=force_revalidate)

    return {
        "task_id": task.id,
        "status": "started",
        "message": "Scholarship validation process started"
    }


@router.get("/sources")
async def get_scraping_sources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get available scraping sources and their status"""

    sources = [
        {
            "name": "NSP",
            "full_name": "National Scholarship Portal",
            "url": "https://scholarships.gov.in/",
            "enabled": True,
            "last_scraped": db.query(func.max(ScrapingJob.completed_at)).filter(
                ScrapingJob.source_name == "NSP",
                ScrapingJob.status == "completed"
            ).scalar(),
            "success_rate": 0.95
        },
        {
            "name": "UGC",
            "full_name": "University Grants Commission",
            "url": "https://www.ugc.ac.in/",
            "enabled": True,
            "last_scraped": db.query(func.max(ScrapingJob.completed_at)).filter(
                ScrapingJob.source_name == "UGC",
                ScrapingJob.status == "completed"
            ).scalar(),
            "success_rate": 0.88
        },
        {
            "name": "AICTE",
            "full_name": "All India Council for Technical Education",
            "url": "https://www.aicte-india.org/",
            "enabled": True,
            "last_scraped": db.query(func.max(ScrapingJob.completed_at)).filter(
                ScrapingJob.source_name == "AICTE",
                ScrapingJob.status == "completed"
            ).scalar(),
            "success_rate": 0.82
        }
    ]

    return sources


@router.get("/logs")
async def get_system_logs(
    level: Optional[str] = Query("INFO"),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get system logs"""

    # This would typically read from a log file or logging service
    # For now, return recent scraping job logs

    jobs = db.query(ScrapingJob).order_by(
        desc(ScrapingJob.created_at)).limit(limit).all()

    logs = []
    for job in jobs:
        logs.append({
            "timestamp": job.created_at,
            "level": "ERROR" if job.status == "failed" else "INFO",
            "message": f"Scraping job {job.id} for {job.source_name}: {job.status}",
            "source": "scraping_service",
            "job_id": job.id
        })

        if job.errors:
            for error in job.errors:
                logs.append({
                    "timestamp": job.completed_at or job.created_at,
                    "level": "ERROR",
                    "message": error,
                    "source": "scraping_service",
                    "job_id": job.id
                })

    return {"logs": logs}
