"""
Pydantic schemas for API request/response models.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from decimal import Decimal

# Base schemas


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

# User schemas


class UserBase(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    full_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    category: Optional[str] = None
    annual_income: Optional[Decimal] = None
    education_level: Optional[str] = None
    field_of_study: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseSchema):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    category: Optional[str] = None
    annual_income: Optional[Decimal] = None
    education_level: Optional[str] = None
    field_of_study: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None


class UserResponse(UserBase):
    id: str
    role: str
    is_active: bool
    email_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseSchema):
    email: str
    password: str


class Token(BaseSchema):
    access_token: str
    token_type: str

# Scholarship schemas


class ScholarshipBase(BaseSchema):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    url: str = Field(..., min_length=1, max_length=2000)
    amount: Optional[float] = None
    deadline: Optional[datetime] = None
    category: Optional[str] = None
    eligibility: Optional[str] = None
    location: Optional[str] = None
    provider: Optional[str] = None
    application_process: Optional[str] = None
    required_documents: Optional[Dict[str, Any]] = None


class ScholarshipCreate(ScholarshipBase):
    pass


class ScholarshipUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    amount: Optional[float] = None
    deadline: Optional[datetime] = None
    category: Optional[str] = None
    eligibility: Optional[str] = None
    location: Optional[str] = None
    provider: Optional[str] = None
    application_process: Optional[str] = None
    required_documents: Optional[Dict[str, Any]] = None


class ScholarshipResponse(ScholarshipBase):
    id: int
    is_active: bool
    is_valid: bool
    quality_score: float
    data_completeness: float
    view_count: int
    application_count: int
    created_at: datetime
    updated_at: datetime
    last_validated: Optional[datetime] = None

# Application schemas


class ApplicationBase(BaseSchema):
    scholarship_id: str
    application_data: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseSchema):
    application_data: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class ApplicationResponse(ApplicationBase):
    id: str
    user_id: str
    status: str
    admin_notes: Optional[str] = None
    submitted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class ApplicationStatusUpdate(BaseSchema):
    status: str = Field(...,
                        regex=r'^(draft|submitted|under_review|approved|rejected|withdrawn)$')
    admin_notes: Optional[str] = None

# Notification schemas


class NotificationBase(BaseSchema):
    type: str
    title: str
    message: str
    metadata: Optional[Dict[str, Any]] = None
    priority: str = "normal"


class NotificationCreate(NotificationBase):
    user_id: str


class NotificationResponse(NotificationBase):
    id: str
    user_id: str
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime

# Bookmark schemas


class BookmarkCreate(BaseSchema):
    scholarship_id: str
    notes: Optional[str] = None


class BookmarkResponse(BaseSchema):
    id: str
    user_id: str
    scholarship_id: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# Review schemas


class ReviewBase(BaseSchema):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    scholarship_id: str


class ReviewResponse(ReviewBase):
    id: str
    user_id: str
    scholarship_id: str
    is_verified: bool
    is_helpful: bool
    created_at: datetime
    updated_at: datetime

# Analytics schemas


class AnalyticsEvent(BaseSchema):
    event_type: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AnalyticsResponse(BaseSchema):
    total_users: int
    active_users: int
    total_scholarships: int
    total_applications: int
    popular_categories: List[Dict[str, Any]]
    recent_activity: List[Dict[str, Any]]

# Scraping schemas


class ScrapingJobCreate(BaseSchema):
    source: str
    force_update: bool = False


class ScrapingJobResponse(BaseSchema):
    id: str
    source: str
    status: str
    total_urls: int
    processed_urls: int
    successful_urls: int
    failed_urls: int
    duplicate_urls: int
    new_scholarships: int
    updated_scholarships: int
    errors: List[str]
    metadata: Dict[str, Any]
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

# Response schemas


class PaginatedResponse(BaseSchema):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int


class SuccessResponse(BaseSchema):
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseSchema):
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None

# Health check schema


class HealthResponse(BaseSchema):
    status: str
    timestamp: datetime
    version: str
    environment: str
    database: str
    cache: str

# Admin schemas


class ScrapingJobCreate(BaseSchema):
    source_url: str
    source_name: str
    force_update: bool = False
    priority: Optional[str] = "medium"
    configuration: Optional[Dict[str, Any]] = None


class ScrapingJobResponse(BaseSchema):
    id: str
    source_url: str
    source_name: str
    status: str
    job_type: str
    priority: str
    items_scraped: int
    items_validated: int
    items_saved: int
    items_rejected: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration: Optional[int] = None
    errors: Optional[List[str]] = None
    warnings: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    retry_count: int
    created_at: datetime
    updated_at: datetime


class SystemStatsResponse(BaseSchema):
    total_scholarships: int
    active_scholarships: int
    verified_scholarships: int
    total_users: int
    jobs_today: int
    running_jobs: int
    failed_jobs_today: int
    recent_scholarships: int
    avg_job_duration: float
    success_rate: float
