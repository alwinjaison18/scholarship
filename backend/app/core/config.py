"""
Core configuration for ShikshaSetu API
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator
from functools import lru_cache


class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "ShikshaSetu API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/shikshasetu"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    DATABASE_POOL_TIMEOUT: int = 30

    # Redis settings
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    REDIS_MAX_CONNECTIONS: int = 20

    # JWT settings
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    REFRESH_TOKEN_EXPIRATION_DAYS: int = 7

    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000", "http://localhost:3001"]

    # API settings
    API_V1_PREFIX: str = "/api/v1"
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIRECTORY: str = "uploads"
    ALLOWED_FILE_EXTENSIONS: List[str] = [
        ".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png", ".gif"
    ]

    # Email settings
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None
    EMAIL_USE_TLS: bool = True
    EMAIL_FROM: str = "noreply@shikshasetu.com"
    EMAIL_FROM_NAME: str = "ShikshaSetu"

    # SMS settings
    SMS_PROVIDER: str = "twilio"  # twilio, msg91, textlocal
    SMS_API_KEY: Optional[str] = None
    SMS_API_SECRET: Optional[str] = None
    SMS_FROM: str = "ShikshaSetu"

    # Scraping settings
    SCRAPING_ENABLED: bool = True
    SCRAPING_INTERVAL_HOURS: int = 6
    SCRAPING_MAX_CONCURRENT_JOBS: int = 5
    SCRAPING_TIMEOUT_SECONDS: int = 300
    SCRAPING_RETRY_ATTEMPTS: int = 3
    SCRAPING_DELAY_SECONDS: int = 2
    SCRAPING_USER_AGENT: str = "ShikshaSetu-Bot/1.0"
    SCRAPING_RESPECT_ROBOTS_TXT: bool = True

    # Validation settings
    VALIDATION_ENABLED: bool = True
    VALIDATION_INTERVAL_HOURS: int = 24
    VALIDATION_TIMEOUT_SECONDS: int = 30
    VALIDATION_MIN_QUALITY_SCORE: int = 70
    VALIDATION_MAX_FAILURES: int = 3

    # Notification settings
    NOTIFICATION_ENABLED: bool = True
    NOTIFICATION_BATCH_SIZE: int = 100
    NOTIFICATION_RETRY_ATTEMPTS: int = 3
    NOTIFICATION_DELAY_SECONDS: int = 1

    # Analytics settings
    ANALYTICS_ENABLED: bool = True
    ANALYTICS_RETENTION_DAYS: int = 365
    ANALYTICS_BATCH_SIZE: int = 1000

    # Caching settings
    CACHE_ENABLED: bool = True
    CACHE_DEFAULT_TTL: int = 300  # 5 minutes
    CACHE_MAX_ENTRIES: int = 10000

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "logs/shikshasetu.log"
    LOG_MAX_SIZE: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5

    # Security settings
    SECURITY_PASSWORD_MIN_LENGTH: int = 8
    SECURITY_PASSWORD_REQUIRE_UPPERCASE: bool = True
    SECURITY_PASSWORD_REQUIRE_LOWERCASE: bool = True
    SECURITY_PASSWORD_REQUIRE_NUMBERS: bool = True
    SECURITY_PASSWORD_REQUIRE_SPECIAL: bool = True
    SECURITY_MAX_LOGIN_ATTEMPTS: int = 5
    SECURITY_LOCKOUT_DURATION_MINUTES: int = 30

    # Monitoring settings
    MONITORING_ENABLED: bool = True
    MONITORING_HEALTH_CHECK_INTERVAL: int = 60
    MONITORING_ALERT_EMAIL: Optional[str] = None
    MONITORING_ALERT_WEBHOOK: Optional[str] = None

    # External API settings
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    GOOGLE_ANALYTICS_ID: Optional[str] = None
    FACEBOOK_APP_ID: Optional[str] = None
    TWITTER_API_KEY: Optional[str] = None

    # Celery settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: List[str] = ["json"]
    CELERY_TIMEZONE: str = "Asia/Kolkata"
    CELERY_ENABLE_UTC: bool = True

    # Scholarship specific settings
    SCHOLARSHIP_SOURCES: List[str] = [
        "scholarships.gov.in",
        "buddy4study.com",
        "scholarshipsindia.com",
        "aicte-india.org",
        "ugc.ac.in",
        "scholarship.up.gov.in",
        "ekalyan.cgg.gov.in",
        "scholarship.rajasthan.gov.in",
        "scholarship.mp.gov.in",
        "scholarship.kerala.gov.in"
    ]

    SCHOLARSHIP_CATEGORIES: List[str] = [
        "merit", "need-based", "minority", "women", "disabled", "sports", "arts",
        "science", "technology", "medical", "engineering", "law", "management",
        "agriculture", "research", "international", "state-specific",
        "central-government", "private", "corporate", "ngo", "other"
    ]

    EDUCATION_LEVELS: List[str] = [
        "pre-matric", "post-matric", "graduation", "post-graduation", "doctorate",
        "diploma", "certificate", "skill-development", "research", "professional",
        "vocational", "all-levels"
    ]

    INDIAN_STATES: List[str] = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
        "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
        "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
        "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
        "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
        "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
    ]

    @validator('CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(',')]
        return v

    @validator('ALLOWED_FILE_EXTENSIONS', pre=True)
    def assemble_file_extensions(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(',')]
        return v

    @validator('DATABASE_URL', pre=True)
    def assemble_database_url(cls, v):
        if v and not v.startswith('postgresql://'):
            # For development, use SQLite if PostgreSQL URL not provided
            return f"sqlite:///./shikshasetu.db"
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings():
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()

# Environment-specific configurations


class DevelopmentSettings(Settings):
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    DATABASE_URL: str = "sqlite:///./shikshasetu_dev.db"
    CORS_ORIGINS: List[str] = ["*"]


class ProductionSettings(Settings):
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    WORKERS: int = 8
    SECURITY_PASSWORD_MIN_LENGTH: int = 10
    SECURITY_MAX_LOGIN_ATTEMPTS: int = 3
    MONITORING_ENABLED: bool = True


class TestingSettings(Settings):
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test_shikshasetu.db"
    TESTING: bool = True
    CACHE_ENABLED: bool = False
    NOTIFICATION_ENABLED: bool = False
    SCRAPING_ENABLED: bool = False


def get_environment_settings():
    """Get settings based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()

    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()

# Feature flags


class FeatureFlags:
    ENABLE_AI_RECOMMENDATIONS: bool = True
    ENABLE_PERSONALIZED_FEED: bool = True
    ENABLE_SOCIAL_LOGIN: bool = True
    ENABLE_MOBILE_APP: bool = True
    ENABLE_OFFLINE_MODE: bool = False
    ENABLE_DARK_MODE: bool = True
    ENABLE_MULTI_LANGUAGE: bool = False
    ENABLE_ACCESSIBILITY: bool = True
    ENABLE_ANALYTICS: bool = True
    ENABLE_FEEDBACK: bool = True
    ENABLE_CHAT: bool = False
    ENABLE_FORUM: bool = False
    ENABLE_BLOG: bool = True
    ENABLE_NEWSLETTER: bool = True
    ENABLE_REFERRAL_PROGRAM: bool = False
    ENABLE_GAMIFICATION: bool = False


feature_flags = FeatureFlags()

# API versioning


class APIVersion:
    V1: str = "v1"
    V2: str = "v2"
    CURRENT: str = V1

# Response codes


class ResponseCodes:
    SUCCESS: int = 200
    CREATED: int = 201
    NO_CONTENT: int = 204
    BAD_REQUEST: int = 400
    UNAUTHORIZED: int = 401
    FORBIDDEN: int = 403
    NOT_FOUND: int = 404
    CONFLICT: int = 409
    VALIDATION_ERROR: int = 422
    INTERNAL_SERVER_ERROR: int = 500
    SERVICE_UNAVAILABLE: int = 503

# Cache keys


class CacheKeys:
    SCHOLARSHIPS_LIST: str = "scholarships:list"
    SCHOLARSHIP_DETAIL: str = "scholarship:detail"
    CATEGORIES: str = "categories"
    STATS: str = "stats"
    USER_PROFILE: str = "user:profile"
    SEARCH_SUGGESTIONS: str = "search:suggestions"
    FEATURED_SCHOLARSHIPS: str = "featured:scholarships"
    TRENDING_SCHOLARSHIPS: str = "trending:scholarships"

# Queue names


class QueueNames:
    SCRAPING: str = "scraping"
    VALIDATION: str = "validation"
    NOTIFICATIONS: str = "notifications"
    ANALYTICS: str = "analytics"
    EMAIL: str = "email"
    SMS: str = "sms"
    CLEANUP: str = "cleanup"

# Default values


class Defaults:
    PAGINATION_LIMIT: int = 20
    PAGINATION_MAX_LIMIT: int = 100
    SEARCH_LIMIT: int = 50
    FEATURED_LIMIT: int = 6
    TRENDING_LIMIT: int = 10
    RECENT_LIMIT: int = 20
    CACHE_TTL: int = 300
    RATE_LIMIT: int = 100
    QUALITY_SCORE_THRESHOLD: int = 70
    DEADLINE_WARNING_DAYS: int = 7
    VALIDATION_INTERVAL_HOURS: int = 24
    SCRAPING_INTERVAL_HOURS: int = 6
