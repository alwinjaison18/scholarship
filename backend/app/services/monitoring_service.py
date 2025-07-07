"""
Monitoring service for system health and performance metrics
"""

import psutil
import redis
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Dict, Any
import logging

from app.models.models import ScrapingJob, Scholarship
from app.core.config import settings

logger = logging.getLogger(__name__)


class MonitoringService:
    def __init__(self, db: Session):
        self.db = db
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True
        )

    def check_database_health(self) -> Dict[str, Any]:
        """Check database connectivity and performance"""
        try:
            # Test basic connectivity
            start_time = datetime.utcnow()
            result = self.db.execute("SELECT 1")
            response_time = (datetime.utcnow() -
                             start_time).total_seconds() * 1000

            # Check table counts
            scholarship_count = self.db.query(Scholarship).count()
            job_count = self.db.query(ScrapingJob).count()

            return {
                "status": True,
                "response_time_ms": response_time,
                "scholarship_count": scholarship_count,
                "job_count": job_count,
                "message": "Database is healthy"
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": False,
                "error": str(e),
                "message": "Database connection failed"
            }

    def check_celery_health(self) -> Dict[str, Any]:
        """Check Celery worker and Redis connectivity"""
        try:
            # Check Redis connectivity
            redis_start = datetime.utcnow()
            self.redis_client.ping()
            redis_response_time = (datetime.utcnow() -
                                   redis_start).total_seconds() * 1000

            # Check Celery workers
            from celery_app import app
            inspect = app.control.inspect()
            active_workers = inspect.active()

            worker_count = len(active_workers) if active_workers else 0

            # Check queue sizes
            queue_info = self.redis_client.llen('celery')

            return {
                "status": True,
                "redis_response_time_ms": redis_response_time,
                "active_workers": worker_count,
                "queue_size": queue_info,
                "message": "Celery is healthy"
            }
        except Exception as e:
            logger.error(f"Celery health check failed: {e}")
            return {
                "status": False,
                "error": str(e),
                "message": "Celery connection failed"
            }

    def check_scraping_job_health(self) -> Dict[str, Any]:
        """Check scraping job performance and status"""
        try:
            now = datetime.utcnow()

            # Get recent job statistics
            last_24h = now - timedelta(hours=24)

            total_jobs = self.db.query(ScrapingJob).filter(
                ScrapingJob.created_at >= last_24h
            ).count()

            successful_jobs = self.db.query(ScrapingJob).filter(
                ScrapingJob.created_at >= last_24h,
                ScrapingJob.status == 'completed'
            ).count()

            failed_jobs = self.db.query(ScrapingJob).filter(
                ScrapingJob.created_at >= last_24h,
                ScrapingJob.status == 'failed'
            ).count()

            running_jobs = self.db.query(ScrapingJob).filter(
                ScrapingJob.status == 'running'
            ).count()

            # Check for stuck jobs (running for more than 2 hours)
            stuck_threshold = now - timedelta(hours=2)
            stuck_jobs = self.db.query(ScrapingJob).filter(
                ScrapingJob.status == 'running',
                ScrapingJob.started_at < stuck_threshold
            ).count()

            success_rate = (successful_jobs / total_jobs *
                            100) if total_jobs > 0 else 100

            status = True
            message = "Scraping jobs are healthy"

            if success_rate < 80:
                status = False
                message = "High failure rate detected"
            elif stuck_jobs > 0:
                status = False
                message = f"{stuck_jobs} jobs appear to be stuck"

            return {
                "status": status,
                "total_jobs_24h": total_jobs,
                "successful_jobs": successful_jobs,
                "failed_jobs": failed_jobs,
                "running_jobs": running_jobs,
                "stuck_jobs": stuck_jobs,
                "success_rate": success_rate,
                "message": message
            }
        except Exception as e:
            logger.error(f"Scraping job health check failed: {e}")
            return {
                "status": False,
                "error": str(e),
                "message": "Unable to check scraping job health"
            }

    def get_resource_usage(self) -> Dict[str, Any]:
        """Get system resource usage metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent

            # Network I/O
            network = psutil.net_io_counters()

            return {
                "cpu_usage": cpu_percent,
                "memory_usage": memory_percent,
                "disk_usage": disk_percent,
                "memory_total_gb": round(memory.total / (1024**3), 2),
                "memory_used_gb": round(memory.used / (1024**3), 2),
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "disk_used_gb": round(disk.used / (1024**3), 2),
                "network_bytes_sent": network.bytes_sent,
                "network_bytes_recv": network.bytes_recv
            }
        except Exception as e:
            logger.error(f"Resource usage check failed: {e}")
            return {
                "error": str(e),
                "message": "Unable to get resource usage"
            }

    def get_success_rate(self, days: int = 30) -> float:
        """Get scraping job success rate over the specified period"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)

            total = self.db.query(ScrapingJob).filter(
                ScrapingJob.created_at >= cutoff_date,
                ScrapingJob.status.in_(['completed', 'failed'])
            ).count()

            successful = self.db.query(ScrapingJob).filter(
                ScrapingJob.created_at >= cutoff_date,
                ScrapingJob.status == 'completed'
            ).count()

            return (successful / total * 100) if total > 0 else 0.0
        except Exception as e:
            logger.error(f"Success rate calculation failed: {e}")
            return 0.0

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get detailed performance metrics"""
        try:
            # Average job duration
            avg_duration = self.db.query(func.avg(ScrapingJob.duration)).filter(
                ScrapingJob.status == 'completed',
                ScrapingJob.completed_at >= datetime.utcnow() - timedelta(days=30)
            ).scalar() or 0

            # Jobs per hour
            last_hour = datetime.utcnow() - timedelta(hours=1)
            jobs_per_hour = self.db.query(ScrapingJob).filter(
                ScrapingJob.created_at >= last_hour
            ).count()

            # Average items per job
            avg_items = self.db.query(func.avg(ScrapingJob.items_scraped)).filter(
                ScrapingJob.status == 'completed',
                ScrapingJob.completed_at >= datetime.utcnow() - timedelta(days=7)
            ).scalar() or 0

            return {
                "avg_job_duration_seconds": avg_duration,
                "jobs_per_hour": jobs_per_hour,
                "avg_items_per_job": avg_items,
                "timestamp": datetime.utcnow()
            }
        except Exception as e:
            logger.error(f"Performance metrics calculation failed: {e}")
            return {
                "error": str(e),
                "message": "Unable to calculate performance metrics"
            }
