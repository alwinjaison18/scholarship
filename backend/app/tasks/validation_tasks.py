"""
Background tasks for validating scholarship data and links.
"""

from ..models.models import Scholarship, ValidationResult
from ..services.validation_service import ValidationService, LinkValidationService
from ..core.database import get_db_session
from celery_app import app
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from celery import current_task
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

# Import celery app from parent directory
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)


@app.task(bind=True, retry_backoff=True, retry_kwargs={'max_retries': 3})
def validate_scholarship_links(self, scholarship_ids: List[int]) -> Dict[str, Any]:
    """
    Validate scholarship links in background.

    Args:
        scholarship_ids: List of scholarship IDs to validate

    Returns:
        Dict with validation results
    """
    try:
        with get_db_session() as db:
            validation_service = LinkValidationService(db)
            results = []

            for scholarship_id in scholarship_ids:
                scholarship = db.query(Scholarship).filter(
                    Scholarship.id == scholarship_id
                ).first()

                if not scholarship:
                    logger.warning(f"Scholarship {scholarship_id} not found")
                    continue

                # Validate main URL
                validation_result = asyncio.run(
                    validation_service.validate_url(scholarship.url)
                )

                # Update scholarship with validation result
                scholarship.is_valid = validation_result.is_valid
                scholarship.last_validated = datetime.utcnow()

                # Store validation result
                validation_record = ValidationResult(
                    scholarship_id=scholarship.id,
                    url=scholarship.url,
                    is_valid=validation_result.is_valid,
                    status_code=validation_result.status_code,
                    error_message=validation_result.error_message,
                    validated_at=datetime.utcnow()
                )
                db.add(validation_record)
                results.append(validation_result.dict())

                # Update task progress
                current_task.update_state(
                    state='PROGRESS',
                    meta={'processed': len(
                        results), 'total': len(scholarship_ids)}
                )

            db.commit()

            return {
                'status': 'completed',
                'processed': len(results),
                'total': len(scholarship_ids),
                'results': results
            }

    except Exception as e:
        logger.error(f"Error validating scholarship links: {str(e)}")
        raise self.retry(exc=e, countdown=60)


@app.task(bind=True, retry_backoff=True, retry_kwargs={'max_retries': 3})
def validate_scholarship_data(self, scholarship_id: int) -> Dict[str, Any]:
    """
    Validate scholarship data completeness and accuracy.

    Args:
        scholarship_id: Scholarship ID to validate

    Returns:
        Dict with validation results
    """
    try:
        with get_db_session() as db:
            validation_service = ValidationService(db)

            scholarship = db.query(Scholarship).filter(
                Scholarship.id == scholarship_id
            ).first()

            if not scholarship:
                raise ValueError(f"Scholarship {scholarship_id} not found")

            # Validate data
            validation_result = validation_service.validate_scholarship_data(
                scholarship.dict()
            )

            # Update scholarship quality score
            scholarship.quality_score = validation_result.quality_score
            scholarship.data_completeness = validation_result.completeness_score

            db.commit()

            return {
                'status': 'completed',
                'scholarship_id': scholarship_id,
                'quality_score': validation_result.quality_score,
                'completeness_score': validation_result.completeness_score,
                'issues': validation_result.issues
            }

    except Exception as e:
        logger.error(f"Error validating scholarship data: {str(e)}")
        raise self.retry(exc=e, countdown=60)


@app.task(bind=True, retry_backoff=True, retry_kwargs={'max_retries': 3})
def cleanup_invalid_scholarships(self) -> Dict[str, Any]:
    """
    Clean up invalid or expired scholarships.

    Returns:
        Dict with cleanup results
    """
    try:
        with get_db_session() as db:
            # Remove scholarships with invalid URLs for more than 30 days
            cutoff_date = datetime.utcnow() - timedelta(days=30)

            invalid_scholarships = db.query(Scholarship).filter(
                and_(
                    Scholarship.is_valid == False,
                    Scholarship.last_validated <= cutoff_date
                )
            ).all()

            removed_count = 0
            for scholarship in invalid_scholarships:
                db.delete(scholarship)
                removed_count += 1

            # Mark expired scholarships as inactive
            expired_scholarships = db.query(Scholarship).filter(
                and_(
                    Scholarship.deadline < datetime.utcnow(),
                    Scholarship.is_active == True
                )
            ).all()

            deactivated_count = 0
            for scholarship in expired_scholarships:
                scholarship.is_active = False
                deactivated_count += 1

            db.commit()

            return {
                'status': 'completed',
                'removed_invalid': removed_count,
                'deactivated_expired': deactivated_count
            }

    except Exception as e:
        logger.error(f"Error cleaning up scholarships: {str(e)}")
        raise self.retry(exc=e, countdown=60)


@app.task(bind=True, retry_backoff=True, retry_kwargs={'max_retries': 3})
def batch_validate_scholarships(self, batch_size: int = 100) -> Dict[str, Any]:
    """
    Validate scholarships in batches.

    Args:
        batch_size: Number of scholarships to validate per batch

    Returns:
        Dict with validation results
    """
    try:
        with get_db_session() as db:
            # Get scholarships that need validation
            scholarships_to_validate = db.query(Scholarship).filter(
                or_(
                    Scholarship.last_validated.is_(None),
                    Scholarship.last_validated <= datetime.utcnow() - timedelta(days=7)
                )
            ).limit(batch_size).all()

            if not scholarships_to_validate:
                return {
                    'status': 'completed',
                    'message': 'No scholarships need validation'
                }

            scholarship_ids = [s.id for s in scholarships_to_validate]

            # Queue validation task
            validate_scholarship_links.delay(scholarship_ids)

            return {
                'status': 'queued',
                'batch_size': len(scholarship_ids),
                'scholarship_ids': scholarship_ids
            }

    except Exception as e:
        logger.error(f"Error queuing batch validation: {str(e)}")
        raise self.retry(exc=e, countdown=60)
