"""
Celery configuration for background tasks.
"""

import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Create Celery app
app = Celery(
    "shiksha_setu",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "app.tasks.scraping_tasks",
        "app.tasks.notification_tasks",
        "app.tasks.validation_tasks",
        "app.tasks.analytics_tasks",
        "app.tasks.cleanup_tasks"
    ]
)

# Celery configuration
app.conf.update(
    # Task routing
    task_routes={
        "app.tasks.scraping_tasks.*": {"queue": "scraping"},
        "app.tasks.notification_tasks.*": {"queue": "notifications"},
        "app.tasks.validation_tasks.*": {"queue": "validation"},
        "app.tasks.analytics_tasks.*": {"queue": "analytics"},
        "app.tasks.cleanup_tasks.*": {"queue": "cleanup"},
    },

    # Task serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,

    # Task execution
    task_always_eager=False,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_disable_rate_limits=False,

    # Task retry settings
    task_retry_delay=60,
    task_max_retries=3,

    # Task expiration
    task_soft_time_limit=300,  # 5 minutes
    task_time_limit=600,       # 10 minutes
    result_expires=3600,       # 1 hour

    # Beat schedule for periodic tasks
    beat_schedule={
        "scrape-nsp-scholarships": {
            "task": "app.tasks.scraping_tasks.scrape_nsp_scholarships",
            "schedule": 3600.0,  # Every hour
            "options": {"queue": "scraping"}
        },
        "scrape-ugc-scholarships": {
            "task": "app.tasks.scraping_tasks.scrape_ugc_scholarships",
            "schedule": 7200.0,  # Every 2 hours
            "options": {"queue": "scraping"}
        },
        "scrape-government-scholarships": {
            "task": "app.tasks.scraping_tasks.scrape_government_scholarships",
            "schedule": 14400.0,  # Every 4 hours
            "options": {"queue": "scraping"}
        },
        "validate-scholarship-links": {
            "task": "app.tasks.validation_tasks.validate_all_scholarship_links",
            "schedule": 21600.0,  # Every 6 hours
            "options": {"queue": "validation"}
        },
        "send-deadline-reminders": {
            "task": "app.tasks.notification_tasks.send_deadline_reminders",
            "schedule": 86400.0,  # Daily
            "options": {"queue": "notifications"}
        },
        "cleanup-old-data": {
            "task": "app.tasks.cleanup_tasks.cleanup_old_data",
            "schedule": 86400.0,  # Daily
            "options": {"queue": "cleanup"}
        },
        "generate-analytics-reports": {
            "task": "app.tasks.analytics_tasks.generate_daily_analytics",
            "schedule": 86400.0,  # Daily
            "options": {"queue": "analytics"}
        }
    },

    # Worker configuration
    worker_concurrency=4,
    worker_max_tasks_per_child=1000,
    worker_log_level="INFO",

    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,

    # Security
    worker_hijack_root_logger=False,
    worker_log_color=True,

    # Database settings
    database_url=os.getenv("DATABASE_URL")
)

# Task annotations for better monitoring
app.conf.task_annotations = {
    "app.tasks.scraping_tasks.*": {
        "rate_limit": "10/m",
        "time_limit": 300,
        "soft_time_limit": 240
    },
    "app.tasks.validation_tasks.*": {
        "rate_limit": "20/m",
        "time_limit": 180,
        "soft_time_limit": 150
    },
    "app.tasks.notification_tasks.*": {
        "rate_limit": "50/m",
        "time_limit": 60,
        "soft_time_limit": 45
    }
}

if __name__ == "__main__":
    app.start()
