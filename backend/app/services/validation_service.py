"""
Validation service for link validation, quality scoring, and content verification.
"""

from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta
import asyncio
import aiohttp
import logging
from urllib.parse import urlparse, urljoin
from dataclasses import dataclass
import re
from enum import Enum

logger = logging.getLogger(__name__)


class LinkStatus(str, Enum):
    VALID = "valid"
    INVALID = "invalid"
    BROKEN = "broken"
    SUSPICIOUS = "suspicious"
    REDIRECT = "redirect"
    SLOW = "slow"
    BLOCKED = "blocked"


@dataclass
class ValidationResult:
    """Result of link validation."""
    url: str
    status: LinkStatus
    response_code: int
    response_time: float
    final_url: str
    content_type: str
    content_length: int
    quality_score: float
    issues: List[str]
    metadata: Dict[str, Any]
    validated_at: datetime


class LinkValidationService:
    """Service for validating links and scoring content quality."""

    def __init__(self):
        self.timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.headers = {
            'User-Agent': 'ShikshaSetu-Bot/1.0 (Scholarship Portal Link Validator)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        # Trusted domains for scholarship sources
        self.trusted_domains = {
            'scholarships.gov.in',
            'nsp.gov.in',
            'ugc.ac.in',
            'aicte-india.org',
            'dst.gov.in',
            'csir.res.in',
            'icmr.gov.in',
            'dbt.gov.in',
            'icar.org.in',
            'indianrailways.gov.in',
            'pfms.nic.in',
            'aiims.edu',
            'iit.ac.in',
            'iisc.ac.in',
            'bits-pilani.ac.in',
            'gov.in',
            'nic.in',
            'edu'
        }

        # Suspicious patterns
        self.suspicious_patterns = [
            r'bit\.ly',
            r'tinyurl\.com',
            r'goo\.gl',
            r't\.co',
            r'shorturl\.at',
            r'click\.here',
            r'download\.now',
            r'free\.money',
            r'guaranteed\.scholarship',
            r'100%\.scholarship',
            r'no\.application\.fee',
            r'instant\.approval'
        ]

    async def validate_url(self, url: str) -> ValidationResult:
        """Validate a single URL and return validation result."""
        start_time = datetime.utcnow()

        try:
            # Basic URL validation
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                return ValidationResult(
                    url=url,
                    status=LinkStatus.INVALID,
                    response_code=0,
                    response_time=0.0,
                    final_url=url,
                    content_type="",
                    content_length=0,
                    quality_score=0.0,
                    issues=["Invalid URL format"],
                    metadata={},
                    validated_at=start_time
                )

            # Check for suspicious patterns
            issues = []
            for pattern in self.suspicious_patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    issues.append(f"Suspicious pattern detected: {pattern}")

            async with aiohttp.ClientSession(
                timeout=self.timeout,
                headers=self.headers
            ) as session:
                try:
                    async with session.get(url, allow_redirects=True) as response:
                        response_time = (datetime.utcnow() -
                                         start_time).total_seconds()

                        # Get response details
                        content_type = response.headers.get('content-type', '')
                        content_length = int(
                            response.headers.get('content-length', 0))
                        final_url = str(response.url)

                        # Read content for analysis
                        content = await response.text()

                        # Determine status
                        status = self._determine_status(
                            response.status, response_time, final_url, content)

                        # Calculate quality score
                        quality_score = self._calculate_quality_score(
                            url, final_url, content, content_type, response.status, response_time
                        )

                        # Additional checks
                        if response.status >= 400:
                            issues.append(f"HTTP error: {response.status}")

                        if response_time > 10:
                            issues.append("Slow response time")

                        if final_url != url:
                            issues.append("URL redirected")

                        # Check content quality
                        content_issues = self._check_content_quality(content)
                        issues.extend(content_issues)

                        return ValidationResult(
                            url=url,
                            status=status,
                            response_code=response.status,
                            response_time=response_time,
                            final_url=final_url,
                            content_type=content_type,
                            content_length=content_length,
                            quality_score=quality_score,
                            issues=issues,
                            metadata={
                                'server': response.headers.get('server', ''),
                                'last_modified': response.headers.get('last-modified', ''),
                                'content_encoding': response.headers.get('content-encoding', ''),
                                'cache_control': response.headers.get('cache-control', ''),
                                'redirects': len(response.history) if hasattr(response, 'history') else 0
                            },
                            validated_at=start_time
                        )

                except aiohttp.ClientError as e:
                    logger.error(
                        f"Client error validating URL {url}: {str(e)}")
                    return ValidationResult(
                        url=url,
                        status=LinkStatus.BROKEN,
                        response_code=0,
                        response_time=(datetime.utcnow() -
                                       start_time).total_seconds(),
                        final_url=url,
                        content_type="",
                        content_length=0,
                        quality_score=0.0,
                        issues=[f"Connection error: {str(e)}"],
                        metadata={},
                        validated_at=start_time
                    )

                except asyncio.TimeoutError:
                    logger.error(f"Timeout validating URL {url}")
                    return ValidationResult(
                        url=url,
                        status=LinkStatus.SLOW,
                        response_code=0,
                        response_time=(datetime.utcnow() -
                                       start_time).total_seconds(),
                        final_url=url,
                        content_type="",
                        content_length=0,
                        quality_score=0.0,
                        issues=["Request timeout"],
                        metadata={},
                        validated_at=start_time
                    )

        except Exception as e:
            logger.error(f"Unexpected error validating URL {url}: {str(e)}")
            return ValidationResult(
                url=url,
                status=LinkStatus.INVALID,
                response_code=0,
                response_time=(datetime.utcnow() - start_time).total_seconds(),
                final_url=url,
                content_type="",
                content_length=0,
                quality_score=0.0,
                issues=[f"Validation error: {str(e)}"],
                metadata={},
                validated_at=start_time
            )

    async def validate_urls_batch(self, urls: List[str], batch_size: int = 10) -> List[ValidationResult]:
        """Validate multiple URLs in batches."""
        results = []

        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]
            batch_results = await asyncio.gather(
                *[self.validate_url(url) for url in batch],
                return_exceptions=True
            )

            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"Error in batch validation: {str(result)}")
                else:
                    results.append(result)

        return results

    def _determine_status(self, status_code: int, response_time: float, final_url: str, content: str) -> LinkStatus:
        """Determine the link status based on response."""
        if status_code >= 400:
            return LinkStatus.BROKEN

        if response_time > 10:
            return LinkStatus.SLOW

        if self._is_suspicious_content(content):
            return LinkStatus.SUSPICIOUS

        if status_code in [301, 302, 303, 307, 308]:
            return LinkStatus.REDIRECT

        return LinkStatus.VALID

    def _calculate_quality_score(self, original_url: str, final_url: str, content: str,
                                 content_type: str, status_code: int, response_time: float) -> float:
        """Calculate quality score for the link."""
        score = 100.0

        # Domain trust score
        domain_score = self._get_domain_trust_score(final_url)
        score = score * (domain_score / 100.0)

        # HTTP status penalty
        if status_code >= 400:
            score *= 0.0
        elif status_code >= 300:
            score *= 0.8

        # Response time penalty
        if response_time > 10:
            score *= 0.5
        elif response_time > 5:
            score *= 0.8

        # Content quality score
        content_score = self._get_content_quality_score(content)
        score = score * (content_score / 100.0)

        # Content type bonus
        if 'text/html' in content_type:
            score *= 1.1
        elif 'application/pdf' in content_type:
            score *= 1.05

        # Redirect penalty
        if original_url != final_url:
            score *= 0.9

        return min(100.0, max(0.0, score))

    def _get_domain_trust_score(self, url: str) -> float:
        """Get trust score for domain."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            # Check for exact matches
            if domain in self.trusted_domains:
                return 100.0

            # Check for subdomain matches
            for trusted_domain in self.trusted_domains:
                if domain.endswith(f".{trusted_domain}"):
                    return 95.0

            # Government domains
            if domain.endswith('.gov.in') or domain.endswith('.gov'):
                return 90.0

            # Educational domains
            if domain.endswith('.edu') or domain.endswith('.ac.in'):
                return 85.0

            # Organization domains
            if domain.endswith('.org'):
                return 75.0

            # Commercial domains
            if domain.endswith('.com') or domain.endswith('.in'):
                return 60.0

            return 40.0

        except Exception:
            return 30.0

    def _get_content_quality_score(self, content: str) -> float:
        """Get content quality score."""
        if not content:
            return 0.0

        score = 50.0

        # Check for scholarship-related keywords
        scholarship_keywords = [
            'scholarship', 'fellowship', 'grant', 'financial aid', 'education',
            'student', 'application', 'eligibility', 'criteria', 'deadline'
        ]

        keyword_count = sum(1 for keyword in scholarship_keywords
                            if keyword.lower() in content.lower())
        score += min(30.0, keyword_count * 3.0)

        # Check for application process information
        process_keywords = [
            'apply', 'application form', 'submit', 'documents', 'requirements',
            'how to apply', 'selection process', 'merit', 'interview'
        ]

        process_count = sum(1 for keyword in process_keywords
                            if keyword.lower() in content.lower())
        score += min(20.0, process_count * 2.0)

        # Penalty for spam indicators
        spam_keywords = [
            'click here', 'act now', 'limited time', 'guaranteed', 'instant',
            'free money', 'no fee', 'easy money', 'work from home'
        ]

        spam_count = sum(1 for keyword in spam_keywords
                         if keyword.lower() in content.lower())
        score -= min(40.0, spam_count * 10.0)

        # Content length bonus
        if len(content) > 1000:
            score += 10.0
        elif len(content) > 500:
            score += 5.0

        return min(100.0, max(0.0, score))

    def _check_content_quality(self, content: str) -> List[str]:
        """Check content for quality issues."""
        issues = []

        if not content:
            issues.append("Empty content")
            return issues

        # Check for minimal content
        if len(content) < 100:
            issues.append("Very short content")

        # Check for suspicious patterns
        suspicious_content = [
            'click here to download',
            'guaranteed scholarship',
            'no application fee',
            'instant approval',
            'limited time offer'
        ]

        for pattern in suspicious_content:
            if pattern.lower() in content.lower():
                issues.append(f"Suspicious content: {pattern}")

        # Check for missing important information
        if 'eligibility' not in content.lower():
            issues.append("Missing eligibility criteria")

        if 'deadline' not in content.lower() and 'last date' not in content.lower():
            issues.append("Missing deadline information")

        return issues

    def _is_suspicious_content(self, content: str) -> bool:
        """Check if content appears suspicious."""
        if not content:
            return True

        # Check for excessive promotional language
        promotional_words = ['guaranteed', 'instant',
                             'free money', 'no fee', 'easy money']
        promotional_count = sum(1 for word in promotional_words
                                if word.lower() in content.lower())

        if promotional_count > 3:
            return True

        # Check for lack of official information
        if len(content) < 200:
            return True

        return False

    def get_validation_summary(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Get summary of validation results."""
        if not results:
            return {}

        total_count = len(results)
        status_counts = {}

        for result in results:
            status = result.status
            if status not in status_counts:
                status_counts[status] = 0
            status_counts[status] += 1

        avg_response_time = sum(
            result.response_time for result in results) / total_count
        avg_quality_score = sum(
            result.quality_score for result in results) / total_count

        return {
            "total_urls": total_count,
            "status_distribution": status_counts,
            "average_response_time": avg_response_time,
            "average_quality_score": avg_quality_score,
            "validation_timestamp": datetime.utcnow().isoformat()
        }

# Helper function to get validation service instance


def get_validation_service() -> LinkValidationService:
    """Get validation service instance."""
    return LinkValidationService()
