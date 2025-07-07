"""
Scholarship model definitions.
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Dict, Any, Optional

Base = declarative_base()


class Scholarship(Base):
    """Scholarship model."""
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text)
    url = Column(String(2000), nullable=False)
    amount = Column(Float)
    deadline = Column(DateTime)
    category = Column(String(100), index=True)
    eligibility = Column(Text)
    location = Column(String(200))
    provider = Column(String(200))
    application_process = Column(Text)
    required_documents = Column(JSON)

    # Metadata
    is_active = Column(Boolean, default=True, index=True)
    is_valid = Column(Boolean, default=True, index=True)
    quality_score = Column(Float, default=0.0)
    data_completeness = Column(Float, default=0.0)

    # Counters
    view_count = Column(Integer, default=0)
    application_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    last_validated = Column(DateTime)
    deleted_at = Column(DateTime)

    # Relationships
    scraping_source_id = Column(Integer, ForeignKey("scraping_sources.id"))
    scraping_source = relationship(
        "ScrapingSource", back_populates="scholarships")

    applications = relationship("Application", back_populates="scholarship")
    notifications = relationship("Notification", back_populates="scholarship")
    validation_results = relationship(
        "ValidationResult", back_populates="scholarship")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'amount': self.amount,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'category': self.category,
            'eligibility': self.eligibility,
            'location': self.location,
            'provider': self.provider,
            'application_process': self.application_process,
            'required_documents': self.required_documents,
            'is_active': self.is_active,
            'is_valid': self.is_valid,
            'quality_score': self.quality_score,
            'data_completeness': self.data_completeness,
            'view_count': self.view_count,
            'application_count': self.application_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_validated': self.last_validated.isoformat() if self.last_validated else None
        }


class ScrapingSource(Base):
    """Scraping source model."""
    __tablename__ = "scraping_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    url = Column(String(2000), nullable=False)
    selector_config = Column(JSON)
    is_active = Column(Boolean, default=True)
    last_scraped = Column(DateTime)
    success_rate = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    # Relationships
    scholarships = relationship(
        "Scholarship", back_populates="scraping_source")
    scraping_jobs = relationship("ScrapingJob", back_populates="source")


class ScrapingJob(Base):
    """Scraping job model."""
    __tablename__ = "scraping_jobs"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("scraping_sources.id"))
    # pending, running, completed, failed
    status = Column(String(50), default="pending")
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    scholarships_found = Column(Integer, default=0)
    scholarships_new = Column(Integer, default=0)
    scholarships_updated = Column(Integer, default=0)
    error_message = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    source = relationship("ScrapingSource", back_populates="scraping_jobs")


class ValidationResult(Base):
    """Validation result model."""
    __tablename__ = "validation_results"

    id = Column(Integer, primary_key=True, index=True)
    scholarship_id = Column(Integer, ForeignKey("scholarships.id"))
    url = Column(String(2000), nullable=False)
    is_valid = Column(Boolean, default=False)
    status_code = Column(Integer)
    response_time = Column(Float)
    error_message = Column(Text)
    redirect_url = Column(String(2000))
    content_type = Column(String(100))
    title = Column(String(500))

    validated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    scholarship = relationship(
        "Scholarship", back_populates="validation_results")
