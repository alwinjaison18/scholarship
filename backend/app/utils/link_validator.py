"""
Link validator utility for validating scholarship URLs.
"""

import asyncio
import aiohttp
import logging
from typing import Dict, Any, List, Optional, Tuple
from urllib.parse import urlparse, urljoin
from dataclasses import dataclass
from datetime import datetime, timedelta
import ssl
import socket

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of URL validation."""
    url: str
    is_valid: bool
    status_code: Optional[int] = None
    response_time: Optional[float] = None
    error_message: Optional[str] = None
    redirect_url: Optional[str] = None
    content_type: Optional[str] = None
    title: Optional[str] = None
    validated_at: datetime = None

    def __post_init__(self):
        if self.validated_at is None:
            self.validated_at = datetime.utcnow()

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'url': self.url,
            'is_valid': self.is_valid,
            'status_code': self.status_code,
            'response_time': self.response_time,
            'error_message': self.error_message,
            'redirect_url': self.redirect_url,
            'content_type': self.content_type,
            'title': self.title,
            'validated_at': self.validated_at.isoformat() if self.validated_at else None
        }


class LinkValidator:
    """Utility class for validating scholarship URLs."""

    def __init__(self, timeout: int = 30, max_redirects: int = 10):
        self.timeout = timeout
        self.max_redirects = max_redirects
        self.session = None
        self.trusted_domains = self._init_trusted_domains()
        self.suspicious_domains = self._init_suspicious_domains()

    def _init_trusted_domains(self) -> List[str]:
        """Initialize list of trusted domains."""
        return [
            'gov.in', 'nic.in', 'ugc.ac.in', 'aicte-india.org',
            'scholarships.gov.in', 'nsp.gov.in', 'pfms.nic.in',
            'minorityaffairs.gov.in', 'tribal.nic.in', 'socialjustice.nic.in',
            'wcd.nic.in', 'education.gov.in', 'dst.gov.in', 'csir.res.in',
            'drdo.gov.in', 'isro.gov.in', 'icmr.gov.in', 'icar.gov.in',
            'universitygrants.gov.in', 'nta.ac.in', 'cbse.gov.in',
            'ncert.nic.in', 'niepa.ac.in', 'ignou.ac.in', 'du.ac.in',
            'jnu.ac.in', 'bhu.ac.in', 'amu.ac.in', 'jadavpuruniversity.in',
            'calcuttauniversity.ac.in', 'tifr.res.in', 'iisc.ac.in',
            'iitd.ac.in', 'iitb.ac.in', 'iitk.ac.in', 'iitm.ac.in',
            'iitkgp.ac.in', 'iitg.ac.in', 'iitr.ac.in', 'iith.ac.in',
            'iitbbs.ac.in', 'iitmandi.ac.in', 'iitgoa.ac.in', 'iitj.ac.in',
            'iitpkd.ac.in', 'iitdh.ac.in', 'iittp.ac.in', 'iitbhilai.ac.in',
            'iitjammu.ac.in', 'nits.ac.in', 'nitc.ac.in', 'nitk.ac.in',
            'nitt.edu', 'nitw.ac.in', 'mnnit.ac.in', 'vnit.ac.in',
            'manit.ac.in', 'svnit.ac.in', 'nitjsr.ac.in', 'nitdgp.ac.in',
            'nitrr.ac.in', 'nitap.ac.in', 'nitmz.ac.in', 'nitm.ac.in',
            'nitpy.ac.in', 'nitsri.ac.in', 'nituk.ac.in', 'nitandhra.ac.in',
            'nitgoa.ac.in', 'nitdelhi.ac.in', 'nitmanipur.ac.in',
            'aiims.edu', 'pgimer.edu.in', 'jipmer.edu.in', 'sgpgi.ac.in',
            'nimhans.ac.in', 'ipgme.ac.in', 'kgmu.edu.in', 'bhu.ac.in'
        ]

    def _init_suspicious_domains(self) -> List[str]:
        """Initialize list of suspicious domains."""
        return [
            '.tk', '.ml', '.ga', '.cf', '.click', '.download', '.stream',
            'bit.ly', 'tinyurl.com', 'short.link', 'rebrand.ly',
            'free-scholarship.com', 'easy-money.com', 'quick-cash.com'
        ]

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            connector=aiohttp.TCPConnector(
                limit=100,
                limit_per_host=30,
                enable_cleanup_closed=True
            )
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def validate_url(self, url: str) -> ValidationResult:
        """
        Validate a single URL.

        Args:
            url: URL to validate

        Returns:
            ValidationResult with validation details
        """
        if not url:
            return ValidationResult(
                url=url,
                is_valid=False,
                error_message="URL is empty"
            )

        # Basic URL format validation
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return ValidationResult(
                url=url,
                is_valid=False,
                error_message="Invalid URL format"
            )

        # Check for suspicious domains
        if any(domain in url.lower() for domain in self.suspicious_domains):
            return ValidationResult(
                url=url,
                is_valid=False,
                error_message="Suspicious domain detected"
            )

        # Try to fetch the URL
        try:
            start_time = datetime.utcnow()

            if not self.session:
                async with aiohttp.ClientSession() as session:
                    result = await self._fetch_url(session, url)
            else:
                result = await self._fetch_url(self.session, url)

            end_time = datetime.utcnow()
            response_time = (end_time - start_time).total_seconds()
            result.response_time = response_time

            return result

        except Exception as e:
            logger.error(f"Error validating URL {url}: {str(e)}")
            return ValidationResult(
                url=url,
                is_valid=False,
                error_message=str(e)
            )

    async def _fetch_url(self, session: aiohttp.ClientSession, url: str) -> ValidationResult:
        """
        Fetch URL and validate response.

        Args:
            session: aiohttp session
            url: URL to fetch

        Returns:
            ValidationResult
        """
        try:
            async with session.get(url, allow_redirects=True) as response:
                # Check status code
                if response.status >= 400:
                    return ValidationResult(
                        url=url,
                        is_valid=False,
                        status_code=response.status,
                        error_message=f"HTTP {response.status}"
                    )

                # Get content type
                content_type = response.headers.get('content-type', '')

                # Check if it's HTML content
                if 'text/html' in content_type:
                    content = await response.text()
                    title = self._extract_title(content)
                else:
                    title = None

                # Check for redirects
                redirect_url = str(response.url) if str(
                    response.url) != url else None

                return ValidationResult(
                    url=url,
                    is_valid=True,
                    status_code=response.status,
                    redirect_url=redirect_url,
                    content_type=content_type,
                    title=title
                )

        except aiohttp.ClientError as e:
            return ValidationResult(
                url=url,
                is_valid=False,
                error_message=f"Client error: {str(e)}"
            )
        except asyncio.TimeoutError:
            return ValidationResult(
                url=url,
                is_valid=False,
                error_message="Request timeout"
            )
        except Exception as e:
            return ValidationResult(
                url=url,
                is_valid=False,
                error_message=f"Unexpected error: {str(e)}"
            )

    def _extract_title(self, html_content: str) -> Optional[str]:
        """Extract title from HTML content."""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                return title_tag.get_text().strip()
        except Exception as e:
            logger.debug(f"Error extracting title: {str(e)}")

        return None

    async def validate_multiple_urls(self, urls: List[str]) -> List[ValidationResult]:
        """
        Validate multiple URLs concurrently.

        Args:
            urls: List of URLs to validate

        Returns:
            List of ValidationResult objects
        """
        if not urls:
            return []

        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            connector=aiohttp.TCPConnector(limit=100, limit_per_host=30)
        ) as session:
            tasks = [self._fetch_url(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Convert exceptions to ValidationResult objects
            validated_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    validated_results.append(ValidationResult(
                        url=urls[i],
                        is_valid=False,
                        error_message=str(result)
                    ))
                else:
                    validated_results.append(result)

            return validated_results

    def is_trusted_domain(self, url: str) -> bool:
        """
        Check if URL is from a trusted domain.

        Args:
            url: URL to check

        Returns:
            True if from trusted domain
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        return any(trusted in domain for trusted in self.trusted_domains)

    def is_suspicious_domain(self, url: str) -> bool:
        """
        Check if URL is from a suspicious domain.

        Args:
            url: URL to check

        Returns:
            True if from suspicious domain
        """
        return any(suspicious in url.lower() for suspicious in self.suspicious_domains)

    def get_domain_trust_score(self, url: str) -> float:
        """
        Get trust score for a domain.

        Args:
            url: URL to score

        Returns:
            Trust score between 0.0 and 1.0
        """
        if self.is_trusted_domain(url):
            return 1.0
        elif self.is_suspicious_domain(url):
            return 0.0
        else:
            # Neutral domains get medium trust
            return 0.5

    def validate_url_format(self, url: str) -> Tuple[bool, List[str]]:
        """
        Validate URL format and structure.

        Args:
            url: URL to validate

        Returns:
            Tuple of (is_valid, issues)
        """
        is_valid = True
        issues = []

        if not url:
            return False, ["URL is empty"]

        # Parse URL
        try:
            parsed = urlparse(url)
        except Exception as e:
            return False, [f"Invalid URL format: {str(e)}"]

        # Check scheme
        if not parsed.scheme:
            is_valid = False
            issues.append("Missing URL scheme (http/https)")
        elif parsed.scheme not in ['http', 'https']:
            is_valid = False
            issues.append(f"Invalid scheme: {parsed.scheme}")

        # Check netloc (domain)
        if not parsed.netloc:
            is_valid = False
            issues.append("Missing domain name")

        # Check for suspicious patterns
        if self.is_suspicious_domain(url):
            is_valid = False
            issues.append("Suspicious domain detected")

        # Check URL length
        if len(url) > 2000:
            is_valid = False
            issues.append("URL too long")

        return is_valid, issues

    async def check_ssl_certificate(self, url: str) -> Dict[str, Any]:
        """
        Check SSL certificate for HTTPS URLs.

        Args:
            url: URL to check

        Returns:
            Dict with SSL certificate details
        """
        parsed = urlparse(url)

        if parsed.scheme != 'https':
            return {
                'valid': False,
                'error': 'Not an HTTPS URL'
            }

        try:
            # Create SSL context
            context = ssl.create_default_context()

            # Connect to server
            with socket.create_connection((parsed.hostname, parsed.port or 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=parsed.hostname) as ssock:
                    cert = ssock.getpeercert()

                    return {
                        'valid': True,
                        'subject': cert.get('subject'),
                        'issuer': cert.get('issuer'),
                        'version': cert.get('version'),
                        'serial_number': cert.get('serialNumber'),
                        'not_before': cert.get('notBefore'),
                        'not_after': cert.get('notAfter')
                    }

        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }

    async def batch_validate(
        self,
        urls: List[str],
        batch_size: int = 50
    ) -> List[ValidationResult]:
        """
        Validate URLs in batches to avoid overwhelming servers.

        Args:
            urls: List of URLs to validate
            batch_size: Number of URLs per batch

        Returns:
            List of ValidationResult objects
        """
        if not urls:
            return []

        all_results = []

        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]
            batch_results = await self.validate_multiple_urls(batch)
            all_results.extend(batch_results)

            # Small delay between batches
            if i + batch_size < len(urls):
                await asyncio.sleep(1)

        return all_results

    def get_validation_summary(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """
        Get summary of validation results.

        Args:
            results: List of ValidationResult objects

        Returns:
            Dict with validation summary
        """
        total = len(results)
        valid = sum(1 for r in results if r.is_valid)
        invalid = total - valid

        status_codes = {}
        error_types = {}

        for result in results:
            if result.status_code:
                status_codes[result.status_code] = status_codes.get(
                    result.status_code, 0) + 1

            if result.error_message:
                error_type = result.error_message.split(':')[0]
                error_types[error_type] = error_types.get(error_type, 0) + 1

        avg_response_time = None
        if results:
            response_times = [
                r.response_time for r in results if r.response_time]
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)

        return {
            'total': total,
            'valid': valid,
            'invalid': invalid,
            'success_rate': (valid / total) * 100 if total > 0 else 0,
            'status_codes': status_codes,
            'error_types': error_types,
            'avg_response_time': avg_response_time
        }
