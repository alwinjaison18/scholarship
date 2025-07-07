"""
Enhanced Celery Task for Dynamic Scholarship Discovery and Scraping
Integrates dynamic crawler with existing scraping infrastructure
"""

from celery import current_task
from celery_app import app
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from ..models.models import ScrapingJob, Scholarship, ScrapingSource
from ..services.dynamic_crawler import DynamicScholarshipCrawler
from ..services.scraping_service import ScrapingService
from ..core.database import get_db_session
from ..core.config import settings

logger = logging.getLogger(__name__)


@app.task(bind=True, name="app.tasks.scraping_tasks.discover_new_scholarship_sources")
def discover_new_scholarship_sources(self, max_depth: int = 2, max_pages_per_source: int = 30):
    """
    Dynamically discover new scholarship sources using AI-powered crawling
    """
    try:
        # Create discovery job record
        with get_db_session() as db:
            job = ScrapingJob(
                id=self.request.id,
                source="DYNAMIC_DISCOVERY",
                status="running",
                started_at=datetime.utcnow(),
                metadata={
                    "max_depth": max_depth,
                    "max_pages_per_source": max_pages_per_source,
                    "job_type": "discovery"
                }
            )
            db.add(job)
            db.commit()

            # Initialize dynamic crawler
            crawler = DynamicScholarshipCrawler()

            # Seed URLs for discovery
            seed_urls = [
                'https://scholarships.gov.in/',
                'https://www.buddy4study.com/',
                'https://www.aicte-india.org/schemes',
                'https://www.ugc.ac.in/schemes',
                'https://www.education.gov.in/',
                'https://www.tribal.nic.in/',
                'https://socialjustice.nic.in/',
                'https://minorityaffairs.gov.in/',
                'https://www.nta.ac.in/',
                'https://www.dst.gov.in/scientific-programmes/science-and-technology-programmes-scholarships',
                'https://www.ncbc.nic.in/',
                'https://nstfdc.nic.in/en/loan-schemes-scholarship'
            ]

            logger.info(f"Starting dynamic discovery with {len(seed_urls)} seed URLs")

            # Start discovery process
            discovered_pages = asyncio.run(
                crawler.discover_scholarship_sources(
                    seed_urls=seed_urls,
                    max_depth=max_depth,
                    max_pages_per_source=max_pages_per_source
                )
            )

            # Save discovered sources to database
            new_sources_count = 0
            high_priority_sources = []

            for page in discovered_pages:
                # Check if source already exists
                existing_source = db.query(ScrapingSource).filter(
                    ScrapingSource.url == page.url
                ).first()

                if not existing_source:
                    # Create new source record
                    new_source = ScrapingSource(
                        url=page.url,
                        name=page.title,
                        domain=page.source_domain,
                        source_type=page.page_type,
                        relevance_score=page.relevance_score,
                        estimated_scholarships=page.estimated_scholarships,
                        status="discovered",
                        metadata=page.metadata,
                        discovered_at=datetime.utcnow(),
                        last_scraped=None
                    )
                    db.add(new_source)
                    new_sources_count += 1

                    # Track high-priority sources for immediate scraping
                    if page.relevance_score >= 0.7:
                        high_priority_sources.append(page)

            db.commit()

            # Save discovery results to file
            crawler.save_discovered_sources(
                f'discovery_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            )

            # Update job status
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.total_urls = len(discovered_pages)
            job.new_scholarships = new_sources_count
            job.metadata.update({
                "discovered_sources": len(discovered_pages),
                "new_sources": new_sources_count,
                "high_priority_sources": len(high_priority_sources)
            })
            db.commit()

            logger.info(f"Discovery completed. Found {len(discovered_pages)} sources, {new_sources_count} new")

            # Trigger immediate scraping of high-priority sources
            if high_priority_sources:
                logger.info(f"Triggering immediate scraping of {len(high_priority_sources)} high-priority sources")
                for source in high_priority_sources[:5]:  # Limit to top 5 to avoid overload
                    scrape_discovered_source.delay(
                        source_url=source.url,
                        source_name=source.title,
                        priority="high"
                    )

            return {
                "status": "success",
                "job_id": job.id,
                "discovered_sources": len(discovered_pages),
                "new_sources": new_sources_count,
                "high_priority_sources": len(high_priority_sources)
            }

    except Exception as e:
        logger.error(f"Error in discovery task: {str(e)}")

        # Update job status to failed
        try:
            with get_db_session() as db:
                job = db.query(ScrapingJob).filter(
                    ScrapingJob.id == self.request.id
                ).first()
                if job:
                    job.status = "failed"
                    job.completed_at = datetime.utcnow()
                    job.errors = [str(e)]
                    db.commit()
        except:
            pass

        raise self.retry(exc=e, countdown=600, max_retries=2)


@app.task(bind=True, name="app.tasks.scraping_tasks.scrape_discovered_source")
def scrape_discovered_source(self, source_url: str, source_name: str, priority: str = "normal"):
    """
    Scrape a dynamically discovered scholarship source
    """
    try:
        # Create scraping job record
        with get_db_session() as db:
            job = ScrapingJob(
                id=self.request.id,
                source=f"DISCOVERED_{source_name}",
                status="running",
                started_at=datetime.utcnow(),
                metadata={
                    "source_url": source_url,
                    "source_name": source_name,
                    "priority": priority,
                    "job_type": "discovered_source_scraping"
                }
            )
            db.add(job)
            db.commit()

            # Initialize scraping service
            scraping_service = ScrapingService()

            logger.info(f"Starting scraping of discovered source: {source_name}")

            # Extract domain name for configuration
            from urllib.parse import urlparse
            domain = urlparse(source_url).netloc

            # Scrape the source
            scraped_scholarships = asyncio.run(
                scraping_service.scrape_scholarships(
                    source_url=source_url,
                    source_name=domain,
                    max_pages=10 if priority == "high" else 5
                )
            )

            # Process and save scholarships
            new_scholarships = 0
            updated_scholarships = 0

            for scraped_scholarship in scraped_scholarships:
                try:
                    # Check if scholarship already exists
                    existing_scholarship = db.query(Scholarship).filter(
                        Scholarship.title == scraped_scholarship.title,
                        Scholarship.provider == scraped_scholarship.provider
                    ).first()

                    if existing_scholarship:
                        # Update existing scholarship
                        existing_scholarship.description = scraped_scholarship.description
                        existing_scholarship.amount = scraped_scholarship.amount
                        existing_scholarship.deadline = scraped_scholarship.deadline
                        existing_scholarship.updated_at = datetime.utcnow()
                        updated_scholarships += 1
                    else:
                        # Create new scholarship
                        new_scholarship = Scholarship(
                            title=scraped_scholarship.title,
                            description=scraped_scholarship.description,
                            amount=scraped_scholarship.amount,
                            deadline=scraped_scholarship.deadline,
                            eligibility=", ".join(scraped_scholarship.eligibility),
                            application_url=scraped_scholarship.application_url,
                            source=scraped_scholarship.source,
                            category=scraped_scholarship.category,
                            level=scraped_scholarship.level,
                            state=scraped_scholarship.state,
                            provider=scraped_scholarship.provider,
                            verified=False,  # Newly discovered sources start as unverified
                            trending=False,
                            views=0,
                            applications=0,
                            tags=scraped_scholarship.tags,
                            created_at=datetime.utcnow(),
                            updated_at=datetime.utcnow()
                        )
                        db.add(new_scholarship)
                        new_scholarships += 1

                except Exception as e:
                    logger.error(f"Error processing scholarship: {str(e)}")
                    continue

            db.commit()

            # Update source record
            source_record = db.query(ScrapingSource).filter(
                ScrapingSource.url == source_url
            ).first()
            
            if source_record:
                source_record.last_scraped = datetime.utcnow()
                source_record.total_scholarships = new_scholarships + updated_scholarships
                source_record.status = "active" if new_scholarships > 0 else "low_activity"
                db.commit()

            # Update job status
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.total_urls = 1
            job.processed_urls = 1
            job.successful_urls = 1 if scraped_scholarships else 0
            job.new_scholarships = new_scholarships
            job.updated_scholarships = updated_scholarships
            job.metadata.update({
                "scraped_count": len(scraped_scholarships),
                "source_quality": "high" if new_scholarships > 5 else "medium" if new_scholarships > 0 else "low"
            })
            db.commit()

            logger.info(f"Scraping completed for {source_name}. New: {new_scholarships}, Updated: {updated_scholarships}")

            return {
                "status": "success",
                "job_id": job.id,
                "source_name": source_name,
                "new_scholarships": new_scholarships,
                "updated_scholarships": updated_scholarships,
                "total_scraped": len(scraped_scholarships)
            }

    except Exception as e:
        logger.error(f"Error scraping discovered source {source_name}: {str(e)}")

        # Update job status to failed
        try:
            with get_db_session() as db:
                job = db.query(ScrapingJob).filter(
                    ScrapingJob.id == self.request.id
                ).first()
                if job:
                    job.status = "failed"
                    job.completed_at = datetime.utcnow()
                    job.errors = [str(e)]
                    db.commit()
        except:
            pass

        raise self.retry(exc=e, countdown=300, max_retries=2)


@app.task(bind=True, name="app.tasks.scraping_tasks.intelligent_discovery_scheduler")
def intelligent_discovery_scheduler(self):
    """
    Intelligent scheduler that triggers discovery based on data freshness and patterns
    """
    try:
        with get_db_session() as db:
            # Check when last discovery was run
            last_discovery = db.query(ScrapingJob).filter(
                ScrapingJob.source == "DYNAMIC_DISCOVERY",
                ScrapingJob.status == "completed"
            ).order_by(ScrapingJob.completed_at.desc()).first()

            # Determine if discovery should run
            should_run_discovery = False
            discovery_reason = ""

            if not last_discovery:
                should_run_discovery = True
                discovery_reason = "No previous discovery found"
            elif (datetime.utcnow() - last_discovery.completed_at).days >= 7:
                should_run_discovery = True
                discovery_reason = "Weekly discovery schedule"
            else:
                # Check if current sources are performing poorly
                recent_jobs = db.query(ScrapingJob).filter(
                    ScrapingJob.completed_at >= datetime.utcnow() - timedelta(days=3),
                    ScrapingJob.status == "completed"
                ).all()

                if recent_jobs:
                    avg_new_scholarships = sum(job.new_scholarships or 0 for job in recent_jobs) / len(recent_jobs)
                    if avg_new_scholarships < 5:  # Low productivity threshold
                        should_run_discovery = True
                        discovery_reason = "Low productivity from existing sources"

            if should_run_discovery:
                logger.info(f"Triggering discovery: {discovery_reason}")
                discover_new_scholarship_sources.delay(max_depth=2, max_pages_per_source=25)
                
                return {
                    "status": "discovery_triggered",
                    "reason": discovery_reason
                }
            else:
                logger.info("Discovery not needed at this time")
                return {
                    "status": "discovery_skipped",
                    "reason": "Recent discovery still fresh"
                }

    except Exception as e:
        logger.error(f"Error in intelligent discovery scheduler: {str(e)}")
        raise


@app.task(bind=True, name="app.tasks.scraping_tasks.validate_discovered_sources")
def validate_discovered_sources(self):
    """
    Validate and clean up discovered sources periodically
    """
    try:
        with get_db_session() as db:
            # Get sources that haven't been validated recently
            sources_to_validate = db.query(ScrapingSource).filter(
                ScrapingSource.status == "discovered",
                ScrapingSource.last_scraped.is_(None)
            ).limit(10).all()  # Validate 10 sources per run

            validated_count = 0
            for source in sources_to_validate:
                try:
                    # Trigger scraping for validation
                    scrape_discovered_source.delay(
                        source_url=source.url,
                        source_name=source.name,
                        priority="validation"
                    )
                    validated_count += 1
                    
                except Exception as e:
                    logger.error(f"Error validating source {source.url}: {str(e)}")
                    # Mark source as problematic
                    source.status = "validation_failed"
                    source.metadata = source.metadata or {}
                    source.metadata["validation_error"] = str(e)

            db.commit()

            logger.info(f"Triggered validation for {validated_count} sources")

            return {
                "status": "success",
                "validated_sources": validated_count
            }

    except Exception as e:
        logger.error(f"Error in source validation: {str(e)}")
        raise
