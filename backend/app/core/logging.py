"""
Logging configuration for the application.
"""

import logging
import structlog
from datetime import datetime
import os
from typing import Any, Dict

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log")
        ]
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a logger instance."""
    return structlog.get_logger(name)


def log_api_request(method: str, path: str, status_code: int, duration: float, user_id: str = None):
    """Log API request."""
    logger = get_logger("api")
    logger.info(
        "API Request",
        method=method,
        path=path,
        status_code=status_code,
        duration=duration,
        user_id=user_id
    )


def log_error(error: Exception, context: Dict[str, Any] = None):
    """Log error with context."""
    logger = get_logger("error")
    logger.error(
        "Error occurred",
        error=str(error),
        error_type=type(error).__name__,
        context=context or {}
    )
