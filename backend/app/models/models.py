"""
Database models for ShikshaSetu scholarship system
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON, ForeignKey, Index, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from app.core.database import Base


class Scholarship(Base):
    """Scholarship model"""
    __tablename__ = "scholarships"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=True, index=True)
    deadline = Column(DateTime, nullable=True, index=True)
    eligibility = Column(JSON, nullable=True)  # List of eligibility criteria
    application_url = Column(String(1000), nullable=True)
    source = Column(String(200), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    level = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False, index=True)
    provider = Column(String(300), nullable=True)
    contact_email = Column(String(200), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    application_process = Column(Text, nullable=True)
    benefits = Column(JSON, nullable=True)  # List of benefits
    # List of selection criteria
    selection_criteria = Column(JSON, nullable=True)
    # List of required documents
    required_documents = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)  # List of tags
    quality_score = Column(Integer, default=0, index=True)
    is_verified = Column(Boolean, default=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    view_count = Column(Integer, default=0)
    application_count = Column(Integer, default=0)
    success_rate = Column(Float, nullable=True)

    # Metadata
    raw_data = Column(JSON, nullable=True)  # Original scraped data
    scraped_at = Column(DateTime, nullable=True)
    last_validated = Column(DateTime, nullable=True)
    validation_status = Column(String(50), default='pending')
    validation_errors = Column(JSON, nullable=True)
    duplicate_of = Column(String, ForeignKey('scholarships.id'), nullable=True)
    priority = Column(String(20), default='medium')

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    applications = relationship("Application", back_populates="scholarship")
    bookmarks = relationship("Bookmark", back_populates="scholarship")
    reviews = relationship("Review", back_populates="scholarship")

    # Indexes for performance
    __table_args__ = (
        Index('idx_scholarship_search', 'title', 'description'),
        Index('idx_scholarship_filters', 'category',
              'level', 'state', 'is_active', 'is_verified'),
        Index('idx_scholarship_deadline', 'deadline', 'is_active'),
        Index('idx_scholarship_quality', 'quality_score', 'is_verified'),
        Index('idx_scholarship_created', 'created_at', 'is_active'),
    )


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(200), unique=True, nullable=False, index=True)
    password_hash = Column(String(200), nullable=False)
    name = Column(String(200), nullable=False)
    avatar = Column(String(500), nullable=True)
    # student, admin, moderator
    role = Column(String(50), default='student', index=True)
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    login_count = Column(Integer, default=0)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)

    # Profile information
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(20), nullable=True)
    address = Column(JSON, nullable=True)  # Address details
    education = Column(JSON, nullable=True)  # Education history
    income = Column(Float, nullable=True)
    category = Column(String(50), nullable=True)  # SC/ST/OBC/General
    is_disabled = Column(Boolean, default=False)
    is_minority = Column(Boolean, default=False)

    # Preferences
    preferences = Column(JSON, nullable=True)  # User preferences
    notification_settings = Column(JSON, nullable=True)
    privacy_settings = Column(JSON, nullable=True)

    # Metadata
    profile_completed = Column(Boolean, default=False)
    verification_status = Column(String(50), default='pending')
    verification_documents = Column(JSON, nullable=True)
    referral_code = Column(String(20), unique=True, nullable=True)
    referred_by = Column(String, ForeignKey('users.id'), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    applications = relationship("Application", back_populates="user")
    bookmarks = relationship("Bookmark", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    activity_logs = relationship("ActivityLog", back_populates="user")


class Application(Base):
    """Scholarship application model"""
    __tablename__ = "applications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'),
                     nullable=False, index=True)
    scholarship_id = Column(String, ForeignKey(
        'scholarships.id'), nullable=False, index=True)
    # draft, submitted, under-review, approved, rejected
    status = Column(String(50), default='draft', index=True)
    tracking_id = Column(String(100), unique=True, nullable=True)

    # Application data
    responses = Column(JSON, nullable=True)  # Form responses
    documents = Column(JSON, nullable=True)  # Uploaded documents
    score = Column(Float, nullable=True)
    rank = Column(Integer, nullable=True)

    # Timeline
    submitted_at = Column(DateTime, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    rejected_at = Column(DateTime, nullable=True)
    disbursed_at = Column(DateTime, nullable=True)

    # Review details
    reviewer_id = Column(String, ForeignKey('users.id'), nullable=True)
    reviewer_notes = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)

    # Disbursement
    amount_approved = Column(Float, nullable=True)
    amount_disbursed = Column(Float, nullable=True)
    disbursement_details = Column(JSON, nullable=True)
    bank_details = Column(JSON, nullable=True)

    # Communication
    communication_history = Column(JSON, nullable=True)
    follow_up_required = Column(Boolean, default=False)
    priority = Column(String(20), default='medium')

    # Metadata
    # How they found the scholarship
    source = Column(String(100), nullable=True)
    reference_number = Column(String(100), nullable=True)
    conditions = Column(JSON, nullable=True)  # Terms and conditions
    acknowledgments = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="applications")
    scholarship = relationship("Scholarship", back_populates="applications")

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'scholarship_id',
                         name='uq_user_scholarship'),
        Index('idx_application_status', 'status', 'created_at'),
        Index('idx_application_timeline', 'submitted_at', 'status'),
    )


class Notification(Base):
    """Notification model"""
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'),
                     nullable=False, index=True)
    type = Column(String(100), nullable=False, index=True)
    title = Column(String(300), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSON, nullable=True)  # Additional data

    # Status
    is_read = Column(Boolean, default=False, index=True)
    is_clicked = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    clicked_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    # Delivery
    channels = Column(JSON, nullable=True)  # email, sms, push, in-app
    delivery_status = Column(JSON, nullable=True)
    delivery_attempts = Column(Integer, default=0)

    # Classification
    category = Column(String(100), nullable=False, index=True)
    priority = Column(String(20), default='medium')
    actions = Column(JSON, nullable=True)  # Available actions

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="notifications")

    # Indexes
    __table_args__ = (
        Index('idx_notification_user_status',
              'user_id', 'is_read', 'created_at'),
        Index('idx_notification_type', 'type', 'category', 'created_at'),
    )


class Bookmark(Base):
    """User bookmark model"""
    __tablename__ = "bookmarks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'),
                     nullable=False, index=True)
    scholarship_id = Column(String, ForeignKey(
        'scholarships.id'), nullable=False, index=True)
    notes = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)
    reminder_date = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="bookmarks")
    scholarship = relationship("Scholarship", back_populates="bookmarks")

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'scholarship_id', name='uq_user_bookmark'),
    )


class Review(Base):
    """Scholarship review model"""
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'),
                     nullable=False, index=True)
    scholarship_id = Column(String, ForeignKey(
        'scholarships.id'), nullable=False, index=True)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=True)

    # Detailed ratings
    application_process_rating = Column(Integer, nullable=True)
    support_quality_rating = Column(Integer, nullable=True)
    disbursement_rating = Column(Integer, nullable=True)
    clarity_rating = Column(Integer, nullable=True)

    # Status
    is_verified = Column(Boolean, default=False)
    is_published = Column(Boolean, default=False)
    # pending, approved, rejected
    status = Column(String(50), default='pending')

    # Engagement
    helpful_count = Column(Integer, default=0)
    unhelpful_count = Column(Integer, default=0)

    # Moderation
    moderated_by = Column(String, ForeignKey('users.id'), nullable=True)
    moderated_at = Column(DateTime, nullable=True)
    moderation_notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="reviews")
    scholarship = relationship("Scholarship", back_populates="reviews")

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'scholarship_id', name='uq_user_review'),
        Index('idx_review_scholarship', 'scholarship_id', 'is_published'),
    )


class ScrapingJob(Base):
    """Scraping job model"""
    __tablename__ = "scraping_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_url = Column(String(1000), nullable=False)
    source_name = Column(String(200), nullable=False, index=True)
    # pending, running, completed, failed
    status = Column(String(50), default='pending', index=True)

    # Job details
    # manual, scheduled, triggered
    job_type = Column(String(50), default='manual')
    priority = Column(String(20), default='medium')
    configuration = Column(JSON, nullable=True)

    # Progress tracking
    items_scraped = Column(Integer, default=0)
    items_validated = Column(Integer, default=0)
    items_saved = Column(Integer, default=0)
    items_rejected = Column(Integer, default=0)

    # Timing
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)  # seconds
    estimated_completion = Column(DateTime, nullable=True)

    # Results
    errors = Column(JSON, nullable=True)  # List of errors
    warnings = Column(JSON, nullable=True)  # List of warnings
    metadata = Column(JSON, nullable=True)

    # Retry logic
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    next_retry_at = Column(DateTime, nullable=True)

    # Performance metrics
    success_rate = Column(Float, nullable=True)
    average_processing_time = Column(Float, nullable=True)
    memory_usage = Column(Integer, nullable=True)
    cpu_usage = Column(Float, nullable=True)

    # Scheduling
    is_recurring = Column(Boolean, default=False)
    schedule_pattern = Column(String(100), nullable=True)  # cron pattern
    last_run_at = Column(DateTime, nullable=True)
    next_run_at = Column(DateTime, nullable=True)

    # Audit
    created_by = Column(String, ForeignKey('users.id'), nullable=True)
    cancelled_by = Column(String, ForeignKey('users.id'), nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    cancellation_reason = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_scraping_job_status', 'status', 'created_at'),
        Index('idx_scraping_job_source', 'source_name', 'status'),
        Index('idx_scraping_job_schedule', 'next_run_at', 'is_recurring'),
    )


class ActivityLog(Base):
    """User activity log model"""
    __tablename__ = "activity_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=True, index=True)
    session_id = Column(String(100), nullable=True, index=True)

    # Activity details
    action = Column(String(100), nullable=False, index=True)
    resource = Column(String(100), nullable=False)
    resource_id = Column(String, nullable=True)
    details = Column(JSON, nullable=True)

    # Request details
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    referer = Column(String(1000), nullable=True)
    location = Column(JSON, nullable=True)  # Geo location
    device = Column(JSON, nullable=True)  # Device information

    # Result
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    response_time = Column(Integer, nullable=True)  # milliseconds

    # Timestamps
    timestamp = Column(DateTime, default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="activity_logs")

    # Indexes
    __table_args__ = (
        Index('idx_activity_user_action', 'user_id', 'action', 'timestamp'),
        Index('idx_activity_resource', 'resource', 'resource_id', 'timestamp'),
        Index('idx_activity_session', 'session_id', 'timestamp'),
    )


class SystemConfig(Base):
    """System configuration model"""
    __tablename__ = "system_config"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    key = Column(String(200), unique=True, nullable=False, index=True)
    value = Column(JSON, nullable=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False, index=True)
    # string, integer, float, boolean, json
    data_type = Column(String(50), default='string')
    is_public = Column(Boolean, default=False)
    is_editable = Column(Boolean, default=True)

    # Validation
    validation_rules = Column(JSON, nullable=True)
    default_value = Column(JSON, nullable=True)

    # Audit
    updated_by = Column(String, ForeignKey('users.id'), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Cache(Base):
    """Cache model for storing computed results"""
    __tablename__ = "cache"

    key = Column(String(500), primary_key=True)
    value = Column(JSON, nullable=False)
    expires_at = Column(DateTime, nullable=True, index=True)
    tags = Column(JSON, nullable=True)  # For cache invalidation

    # Metadata
    size = Column(Integer, nullable=True)  # Size in bytes
    hit_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    last_accessed = Column(DateTime, default=func.now())


class Analytics(Base):
    """Analytics and metrics model"""
    __tablename__ = "analytics"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    metric_name = Column(String(200), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    dimensions = Column(JSON, nullable=True)  # Additional dimensions

    # Time series
    date = Column(DateTime, nullable=False, index=True)
    hour = Column(Integer, nullable=True, index=True)
    day_of_week = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)
    year = Column(Integer, nullable=True)

    # Aggregation level
    # hourly, daily, weekly, monthly
    granularity = Column(String(20), default='daily')

    # Metadata
    source = Column(String(100), nullable=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=True)
    session_id = Column(String(100), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_analytics_metric_date', 'metric_name', 'date'),
        Index('idx_analytics_time_series', 'date', 'granularity'),
        Index('idx_analytics_user_metrics', 'user_id', 'metric_name', 'date'),
    )

# Additional models for specific features


class ScholarshipCategory(Base):
    """Scholarship category master data"""
    __tablename__ = "scholarship_categories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(100), nullable=True)
    color = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    # SEO
    slug = Column(String(200), unique=True, nullable=False)
    meta_title = Column(String(200), nullable=True)
    meta_description = Column(Text, nullable=True)

    # Statistics
    scholarship_count = Column(Integer, default=0)
    application_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class FAQ(Base):
    """Frequently Asked Questions"""
    __tablename__ = "faqs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    tags = Column(JSON, nullable=True)

    # Display
    is_published = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)

    # SEO
    slug = Column(String(300), unique=True, nullable=False)

    # Audit
    created_by = Column(String, ForeignKey('users.id'), nullable=True)
    updated_by = Column(String, ForeignKey('users.id'), nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Testimonial(Base):
    """Success stories and testimonials"""
    __tablename__ = "testimonials"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=True)
    scholarship_id = Column(String, ForeignKey(
        'scholarships.id'), nullable=True)

    # Testimonial content
    student_name = Column(String(200), nullable=False)
    student_photo = Column(String(500), nullable=True)
    quote = Column(Text, nullable=False)
    amount_received = Column(Float, nullable=True)
    year = Column(String(10), nullable=True)
    university = Column(String(300), nullable=True)
    course = Column(String(300), nullable=True)

    # Verification
    is_verified = Column(Boolean, default=False)
    verification_method = Column(String(100), nullable=True)
    verification_date = Column(DateTime, nullable=True)

    # Display
    is_featured = Column(Boolean, default=False)
    is_published = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)

    # Engagement
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)

    # Audit
    approved_by = Column(String, ForeignKey('users.id'), nullable=True)
    approved_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
