"""
Simple test API endpoints for scraping functions
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.tasks.scraping_tasks import scrape_nsp_scholarships, scrape_ugc_scholarships
from app.models.models import ScrapingJob
from datetime import datetime

router = APIRouter()


@router.post("/test-scraping")
async def test_scraping(
    source: str = "nsp",
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    """Test scraping functionality"""

    # Create a test job record
    job = ScrapingJob(
        source_url=f"https://test-{source}.com",
        source_name=source.upper(),
        status="pending",
        job_type="manual",
        created_at=datetime.utcnow()
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Start appropriate scraping task
    if source.lower() == "nsp":
        task = scrape_nsp_scholarships.delay(force_update=True)
    elif source.lower() == "ugc":
        task = scrape_ugc_scholarships.delay(force_update=True)
    else:
        raise HTTPException(status_code=400, detail="Invalid source")

    # Update job with task ID
    job.id = task.id
    db.commit()

    return {
        "message": f"Scraping job started for {source.upper()}",
        "job_id": job.id,
        "task_id": task.id,
        "status": "started"
    }


@router.get("/scraping-status/{job_id}")
async def get_scraping_status(
    job_id: str,
    db: Session = Depends(get_db)
):
    """Get scraping job status"""

    job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job.id,
        "source": job.source_name,
        "status": job.status,
        "items_scraped": job.items_scraped,
        "items_saved": job.items_saved,
        "items_rejected": job.items_rejected,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
        "errors": job.errors,
        "created_at": job.created_at
    }


@router.get("/recent-jobs")
async def get_recent_jobs(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recent scraping jobs"""

    jobs = db.query(ScrapingJob).order_by(
        ScrapingJob.created_at.desc()).limit(limit).all()

    return [
        {
            "job_id": job.id,
            "source": job.source_name,
            "status": job.status,
            "items_scraped": job.items_scraped,
            "items_saved": job.items_saved,
            "started_at": job.started_at,
            "completed_at": job.completed_at,
            "created_at": job.created_at
        }
        for job in jobs
    ]
