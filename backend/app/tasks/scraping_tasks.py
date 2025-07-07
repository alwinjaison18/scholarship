"""
Background tasks for scraping scholarship data.
"""

from ..models.models import ScrapingJob, Scholarship
from ..services.validation_service import LinkValidationService
from ..services.scraping_service import ScrapingService
from ..core.database import get_db_session
from celery_app import app
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
from celery import current_task
from sqlalchemy.orm import Session

# Import celery app from parent directory
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


logger = logging.getLogger(__name__)


@app.task(bind=True, name="app.tasks.scraping_tasks.scrape_nsp_scholarships")
def scrape_nsp_scholarships(self, force_update: bool = False):
    """Scrape scholarships from NSP (National Scholarship Portal)."""
    try:
        # Create scraping job record
        with get_db_session() as db:
            job = ScrapingJob(
                id=self.request.id,
                source="NSP",
                status="running",
                started_at=datetime.utcnow(),
                metadata={"force_update": force_update}
            )
            db.add(job)
            db.commit()

            # Initialize services
            scraping_service = ScrapingService(db)

            # Start scraping
            logger.info("Starting NSP scholarship scraping...")
            result = asyncio.run(scraping_service.scrape_nsp_scholarships())

            # Update job status
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.total_urls = result.get("total_urls", 0)
            job.processed_urls = result.get("processed_urls", 0)
            job.successful_urls = result.get("successful_urls", 0)
            job.failed_urls = result.get("failed_urls", 0)
            job.new_scholarships = result.get("new_scholarships", 0)
            job.updated_scholarships = result.get("updated_scholarships", 0)
            job.metadata = result.get("metadata", {})

            db.commit()

            logger.info(
                f"NSP scraping completed. New: {job.new_scholarships}, Updated: {job.updated_scholarships}")

            return {
                "status": "success",
                "job_id": job.id,
                "new_scholarships": job.new_scholarships,
                "updated_scholarships": job.updated_scholarships,
                "total_processed": job.processed_urls
            }

    except Exception as e:
        logger.error(f"Error in NSP scraping task: {str(e)}")

        # Update job status to failed
        try:
            with get_db_session() as db:
                job = db.query(ScrapingJob).filter(
                    ScrapingJob.id == self.request.id).first()
                if job:
                    job.status = "failed"
                    job.completed_at = datetime.utcnow()
                    job.errors = [str(e)]
                    db.commit()
        except:
            pass

        raise self.retry(exc=e, countdown=300, max_retries=3)


@app.task(bind=True, name="app.tasks.scraping_tasks.scrape_ugc_scholarships")
def scrape_ugc_scholarships(self, force_update: bool = False):
    """Scrape scholarships from UGC sources."""
    try:
        with get_db_session() as db:
            job = ScrapingJob(
                id=self.request.id,
                source="UGC",
                status="running",
                started_at=datetime.utcnow(),
                metadata={"force_update": force_update}
            )
            db.add(job)
            db.commit()

            scraping_service = ScrapingService(db)

            logger.info("Starting UGC scholarship scraping...")
            result = asyncio.run(scraping_service.scrape_ugc_scholarships())

            # Update job status
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.total_urls = result.get("total_urls", 0)
            job.processed_urls = result.get("processed_urls", 0)
            job.successful_urls = result.get("successful_urls", 0)
            job.failed_urls = result.get("failed_urls", 0)
            job.new_scholarships = result.get("new_scholarships", 0)
            job.updated_scholarships = result.get("updated_scholarships", 0)
            job.metadata = result.get("metadata", {})

            db.commit()

            logger.info(
                f"UGC scraping completed. New: {job.new_scholarships}, Updated: {job.updated_scholarships}")

            return {
                "status": "success",
                "job_id": job.id,
                "new_scholarships": job.new_scholarships,
                "updated_scholarships": job.updated_scholarships,
                "total_processed": job.processed_urls
            }

    except Exception as e:
        logger.error(f"Error in UGC scraping task: {str(e)}")

        try:
            with get_db_session() as db:
                job = db.query(ScrapingJob).filter(
                    ScrapingJob.id == self.request.id).first()
                if job:
                    job.status = "failed"
                    job.completed_at = datetime.utcnow()
                    job.errors = [str(e)]
                    db.commit()
        except:
            pass

        raise self.retry(exc=e, countdown=300, max_retries=3)


@app.task(bind=True, name="app.tasks.scraping_tasks.scrape_government_scholarships")
def scrape_government_scholarships(self, force_update: bool = False):
    """Scrape scholarships from various government sources."""
    try:
        with get_db_session() as db:
            job = ScrapingJob(
                id=self.request.id,
                source="GOVERNMENT",
                status="running",
                started_at=datetime.utcnow(),
                metadata={"force_update": force_update}
            )
            db.add(job)
            db.commit()

            scraping_service = ScrapingService(db)

            logger.info("Starting government scholarship scraping...")
            result = asyncio.run(
                scraping_service.scrape_government_scholarships())

            # Update job status
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.total_urls = result.get("total_urls", 0)
            job.processed_urls = result.get("processed_urls", 0)
            job.successful_urls = result.get("successful_urls", 0)
            job.failed_urls = result.get("failed_urls", 0)
            job.new_scholarships = result.get("new_scholarships", 0)
            job.updated_scholarships = result.get("updated_scholarships", 0)
            job.metadata = result.get("metadata", {})

            db.commit()

            logger.info(
                f"Government scraping completed. New: {job.new_scholarships}, Updated: {job.updated_scholarships}")

            return {
                "status": "success",
                "job_id": job.id,
                "new_scholarships": job.new_scholarships,
                "updated_scholarships": job.updated_scholarships,
                "total_processed": job.processed_urls
            }

    except Exception as e:
        logger.error(f"Error in government scraping task: {str(e)}")

        try:
            with get_db_session() as db:
                job = db.query(ScrapingJob).filter(
                    ScrapingJob.id == self.request.id).first()
                if job:
                    job.status = "failed"
                    job.completed_at = datetime.utcnow()
                    job.errors = [str(e)]
                    db.commit()
        except:
            pass

        raise self.retry(exc=e, countdown=300, max_retries=3)


@app.task(bind=True, name="app.tasks.scraping_tasks.scrape_single_source")
def scrape_single_source(self, source_url: str, source_name: str):
    """Scrape a single scholarship source."""
    try:
        with get_db_session() as db:
            job = ScrapingJob(
                id=self.request.id,
                source=source_name,
                status="running",
                started_at=datetime.utcnow(),
                metadata={"source_url": source_url}
            )
            db.add(job)
            db.commit()

            scraping_service = ScrapingService(db)

            logger.info(f"Starting scraping for {source_name}: {source_url}")
            result = asyncio.run(
                scraping_service.scrape_single_source(source_url))

            # Update job status
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.total_urls = result.get("total_urls", 0)
            job.processed_urls = result.get("processed_urls", 0)
            job.successful_urls = result.get("successful_urls", 0)
            job.failed_urls = result.get("failed_urls", 0)
            job.new_scholarships = result.get("new_scholarships", 0)
            job.updated_scholarships = result.get("updated_scholarships", 0)
            job.metadata = result.get("metadata", {})

            db.commit()

            logger.info(
                f"{source_name} scraping completed. New: {job.new_scholarships}, Updated: {job.updated_scholarships}")

            return {
                "status": "success",
                "job_id": job.id,
                "source": source_name,
                "new_scholarships": job.new_scholarships,
                "updated_scholarships": job.updated_scholarships,
                "total_processed": job.processed_urls
            }

    except Exception as e:
        logger.error(f"Error in single source scraping task: {str(e)}")

        try:
            with get_db_session() as db:
                job = db.query(ScrapingJob).filter(
                    ScrapingJob.id == self.request.id).first()
                if job:
                    job.status = "failed"
                    job.completed_at = datetime.utcnow()
                    job.errors = [str(e)]
                    db.commit()
        except:
            pass

        raise self.retry(exc=e, countdown=300, max_retries=3)


@app.task(bind=True, name="app.tasks.scraping_tasks.update_scholarship_quality_scores")
def update_scholarship_quality_scores(self):
    """Update quality scores for all scholarships."""
    try:
        with get_db_session() as db:
            # Get all active scholarships
            scholarships = db.query(Scholarship).filter(
                Scholarship.is_active == True
            ).all()

            validation_service = LinkValidationService()
            updated_count = 0

            for scholarship in scholarships:
                try:
                    # Validate the official URL
                    if scholarship.official_url:
                        result = asyncio.run(
                            validation_service.validate_url(scholarship.official_url))

                        # Update quality score and validation status
                        scholarship.quality_score = result.quality_score
                        scholarship.link_validated = result.status == "valid"
                        scholarship.last_validated = datetime.utcnow()

                        updated_count += 1

                        # Update progress
                        current_task.update_state(
                            state="PROGRESS",
                            meta={
                                "current": updated_count,
                                "total": len(scholarships),
                                "status": f"Updated {updated_count}/{len(scholarships)} scholarships"
                            }
                        )

                except Exception as e:
                    logger.error(
                        f"Error updating scholarship {scholarship.id}: {str(e)}")
                    continue

            db.commit()

            logger.info(
                f"Updated quality scores for {updated_count} scholarships")

            return {
                "status": "success",
                "updated_count": updated_count,
                "total_scholarships": len(scholarships)
            }

    except Exception as e:
        logger.error(f"Error in quality score update task: {str(e)}")
        raise self.retry(exc=e, countdown=300, max_retries=3)


@app.task(bind=True, name="app.tasks.scraping_tasks.cleanup_failed_jobs")
def cleanup_failed_jobs(self):
    """Clean up old failed scraping jobs."""
    try:
        with get_db_session() as db:
            # Delete failed jobs older than 7 days
            cutoff_date = datetime.utcnow() - timedelta(days=7)

            deleted_count = db.query(ScrapingJob).filter(
                ScrapingJob.status == "failed",
                ScrapingJob.created_at < cutoff_date
            ).delete()

            db.commit()

            logger.info(f"Cleaned up {deleted_count} failed scraping jobs")

            return {
                "status": "success",
                "deleted_count": deleted_count
            }

    except Exception as e:
        logger.error(f"Error in cleanup task: {str(e)}")
        raise self.retry(exc=e, countdown=300, max_retries=3)
