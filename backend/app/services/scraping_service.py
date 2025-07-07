"""
Real-time scholarship scraping service with AI-powered extraction
"""

import asyncio
import aiohttp
import json
import re
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from dataclasses import dataclass, asdict
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.core.config import settings
from app.core.database import db_transaction
from app.models.scholarship import Scholarship, ScrapingJob, ScrapingSource
from app.models.user import User
from app.schemas import ScholarshipCreate, ScrapingJobCreate
from app.services.validation_service import ValidationService
from app.services.ai_service import AIService
from app.utils.text_processing import TextProcessor
from app.utils.date_parser import DateParser
from app.utils.amount_parser import AmountParser
from app.utils.link_validator import LinkValidator
from app.utils.deduplication import DuplicationDetector

logger = logging.getLogger(__name__)


@dataclass
class ScrapedScholarship:
    """Data class for scraped scholarship data"""
    title: str
    description: str
    amount: Optional[float]
    deadline: Optional[str]
    eligibility: List[str]
    application_url: str
    source: str
    category: str
    level: str
    state: str
    provider: str
    contact_email: Optional[str]
    contact_phone: Optional[str]
    application_process: str
    benefits: List[str]
    selection_criteria: List[str]
    required_documents: List[str]
    tags: List[str]
    raw_data: Dict[str, Any]
    scraped_at: datetime
    quality_score: int = 0


class ScrapingService:
    """Advanced scholarship scraping service with AI-powered extraction"""

    def __init__(self):
        self.validation_service = ValidationService()
        self.ai_service = AIService()
        self.text_processor = TextProcessor()
        self.date_parser = DateParser()
        self.amount_parser = AmountParser()
        self.link_validator = LinkValidator()
        self.duplication_detector = DuplicationDetector()

        # Scraping configuration
        self.config = {
            'timeout': settings.SCRAPING_TIMEOUT_SECONDS,
            'delay': settings.SCRAPING_DELAY_SECONDS,
            'max_retries': settings.SCRAPING_RETRY_ATTEMPTS,
            'user_agent': settings.SCRAPING_USER_AGENT,
            'respect_robots_txt': settings.SCRAPING_RESPECT_ROBOTS_TXT,
            'max_concurrent': settings.SCRAPING_MAX_CONCURRENT_JOBS,
            'headless': True,
            'viewport': {'width': 1920, 'height': 1080}
        }

        # Source-specific configurations
        self.source_configs = {
            'scholarships.gov.in': {
                'selectors': {
                    'title': '.scheme-title, .scholarship-title, h1, h2.title',
                    'description': '.scheme-description, .scholarship-description, .content-desc',
                    'amount': '.amount, .scholarship-amount, .benefit-amount',
                    'deadline': '.deadline, .last-date, .closing-date',
                    'eligibility': '.eligibility, .eligible-criteria, .criteria',
                    'application_url': '.apply-link, .application-link, a[href*="apply"]',
                    'documents': '.documents-required, .required-documents',
                    'benefits': '.benefits, .scheme-benefits',
                    'contact': '.contact-info, .helpdesk'
                },
                'pagination': {
                    'enabled': True,
                    'next_page_selector': '.next-page, .pagination-next, a[rel="next"]',
                    'max_pages': 50
                },
                'wait_for': '.scholarship-list, .scheme-list, .results-container'
            },
            'buddy4study.com': {
                'selectors': {
                    'title': '.scholarship-title, h1.title, .card-title',
                    'description': '.scholarship-description, .card-description',
                    'amount': '.amount, .scholarship-amount, .prize-amount',
                    'deadline': '.deadline, .last-date, .expiry-date',
                    'eligibility': '.eligibility, .criteria, .eligible-for',
                    'application_url': '.apply-button, .application-link',
                    'provider': '.provider, .sponsor, .organization',
                    'category': '.category, .scholarship-type',
                    'level': '.level, .education-level'
                },
                'pagination': {
                    'enabled': True,
                    'next_page_selector': '.next, .pagination-next',
                    'max_pages': 30
                },
                'wait_for': '.scholarship-card, .scholarship-item'
            },
            'aicte-india.org': {
                'selectors': {
                    'title': '.scheme-title, h1, .title',
                    'description': '.scheme-details, .description',
                    'amount': '.amount, .scholarship-amount',
                    'deadline': '.deadline, .last-date',
                    'eligibility': '.eligibility, .criteria',
                    'application_url': '.apply-link, a[href*="apply"]',
                    'documents': '.documents, .required-docs'
                },
                'wait_for': '.content, .scheme-content'
            },
            'ugc.ac.in': {
                'selectors': {
                    'title': '.scheme-title, h1, .announcement-title',
                    'description': '.scheme-description, .announcement-content',
                    'amount': '.amount, .fellowship-amount',
                    'deadline': '.deadline, .last-date',
                    'eligibility': '.eligibility, .criteria',
                    'application_url': '.apply-link, .application-link'
                },
                'wait_for': '.content, .announcement-content'
            }
        }

    async def scrape_scholarships(self, source_url: str, source_name: str,
                                  max_pages: int = 10) -> List[ScrapedScholarship]:
        """
        Scrape scholarships from a source with AI-powered extraction
        """
        scholarships = []

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=self.config['headless'],
                    args=['--no-sandbox', '--disable-dev-shm-usage']
                )

                context = await browser.new_context(
                    user_agent=self.config['user_agent'],
                    viewport=self.config['viewport']
                )

                page = await context.new_page()

                # Get source-specific configuration
                source_config = self.source_configs.get(source_name, {})

                # Navigate to source
                await page.goto(source_url, timeout=self.config['timeout'] * 1000)

                # Wait for content to load
                if 'wait_for' in source_config:
                    try:
                        await page.wait_for_selector(
                            source_config['wait_for'],
                            timeout=30000
                        )
                    except:
                        logger.warning(
                            f"Wait selector not found for {source_name}")

                # Extract scholarships from current page
                page_scholarships = await self._extract_scholarships_from_page(
                    page, source_name, source_config
                )
                scholarships.extend(page_scholarships)

                # Handle pagination if enabled
                if source_config.get('pagination', {}).get('enabled', False):
                    current_page = 1
                    max_pages_config = source_config['pagination'].get(
                        'max_pages', max_pages)

                    while current_page < min(max_pages, max_pages_config):
                        next_page_selector = source_config['pagination'].get(
                            'next_page_selector')

                        if not next_page_selector:
                            break

                        try:
                            # Check if next page button exists
                            next_button = await page.query_selector(next_page_selector)
                            if not next_button:
                                break

                            # Click next page
                            await next_button.click()
                            await page.wait_for_load_state('networkidle', timeout=30000)

                            # Extract scholarships from new page
                            page_scholarships = await self._extract_scholarships_from_page(
                                page, source_name, source_config
                            )
                            scholarships.extend(page_scholarships)

                            current_page += 1

                            # Delay between pages
                            await asyncio.sleep(self.config['delay'])

                        except Exception as e:
                            logger.error(f"Error navigating to next page: {e}")
                            break

                await browser.close()

        except Exception as e:
            logger.error(f"Error scraping {source_name}: {e}")
            raise

        logger.info(
            f"Scraped {len(scholarships)} scholarships from {source_name}")
        return scholarships

    async def _extract_scholarships_from_page(self, page, source_name: str,
                                              source_config: Dict) -> List[ScrapedScholarship]:
        """
        Extract scholarships from a single page using AI-powered extraction
        """
        scholarships = []

        try:
            # Get page content
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')

            # Use AI to identify scholarship entries
            scholarship_elements = await self._identify_scholarship_elements(soup, source_config)

            for element in scholarship_elements:
                try:
                    # Extract scholarship data using AI
                    scholarship_data = await self._extract_scholarship_data(
                        element, source_name, source_config
                    )

                    if scholarship_data:
                        scholarships.append(scholarship_data)

                except Exception as e:
                    logger.error(f"Error extracting scholarship data: {e}")
                    continue

            # If no scholarships found with AI, try fallback extraction
            if not scholarships:
                scholarships = await self._fallback_extraction(soup, source_name, source_config)

        except Exception as e:
            logger.error(f"Error extracting scholarships from page: {e}")
            raise

        return scholarships

    async def _identify_scholarship_elements(self, soup: BeautifulSoup,
                                             source_config: Dict) -> List:
        """
        Use AI to identify scholarship elements on the page
        """
        # Try common selectors first
        common_selectors = [
            '.scholarship-item', '.scholarship-card', '.scheme-item',
            '.scholarship-entry', '.scheme-entry', '.result-item',
            '.card', '.item', '.entry', '.row', '.listing'
        ]

        elements = []

        for selector in common_selectors:
            found_elements = soup.select(selector)
            if found_elements:
                # Use AI to validate if these are actually scholarship elements
                validated_elements = await self._validate_scholarship_elements(found_elements)
                elements.extend(validated_elements)
                break

        # If no elements found, use AI to analyze the entire page
        if not elements:
            elements = await self._ai_identify_scholarships(soup)

        return elements

    async def _validate_scholarship_elements(self, elements: List) -> List:
        """
        Use AI to validate if elements contain scholarship information
        """
        validated = []

        for element in elements:
            text_content = element.get_text(strip=True)

            # Basic validation - check for scholarship-related keywords
            scholarship_keywords = [
                'scholarship', 'fellowship', 'grant', 'award', 'stipend',
                'financial aid', 'education', 'student', 'apply', 'deadline',
                'eligibility', 'amount', 'prize', 'benefit'
            ]

            if any(keyword in text_content.lower() for keyword in scholarship_keywords):
                validated.append(element)

        return validated[:50]  # Limit to prevent overload

    async def _ai_identify_scholarships(self, soup: BeautifulSoup) -> List:
        """
        Use AI to identify scholarship content when standard selectors fail
        """
        try:
            # Extract text content for AI analysis
            text_content = soup.get_text(strip=True)

            # Use AI service to identify scholarship sections
            scholarship_sections = await self.ai_service.identify_scholarship_sections(text_content)

            # Convert AI-identified sections back to soup elements
            elements = []
            for section in scholarship_sections:
                # Find elements containing the identified text
                for element in soup.find_all(text=re.compile(re.escape(section['text'][:50]))):
                    parent = element.parent
                    if parent and parent not in elements:
                        elements.append(parent)

            return elements

        except Exception as e:
            logger.error(f"AI scholarship identification failed: {e}")
            return []

    async def _extract_scholarship_data(self, element, source_name: str,
                                        source_config: Dict) -> Optional[ScrapedScholarship]:
        """
        Extract scholarship data from an element using AI-powered extraction
        """
        try:
            # Get element text content
            text_content = element.get_text(strip=True)
            html_content = str(element)

            # Use AI to extract structured data
            ai_extracted = await self.ai_service.extract_scholarship_data(
                text_content, html_content, source_name
            )

            # Use traditional extraction as fallback
            traditional_extracted = await self._traditional_extraction(element, source_config)

            # Merge AI and traditional extraction results
            merged_data = self._merge_extraction_results(
                ai_extracted, traditional_extracted)

            # Validate and clean extracted data
            cleaned_data = await self._clean_and_validate_data(merged_data, source_name)

            if not cleaned_data:
                return None

            # Create ScrapedScholarship object
            scholarship = ScrapedScholarship(
                title=cleaned_data.get('title', ''),
                description=cleaned_data.get('description', ''),
                amount=cleaned_data.get('amount'),
                deadline=cleaned_data.get('deadline'),
                eligibility=cleaned_data.get('eligibility', []),
                application_url=cleaned_data.get('application_url', ''),
                source=source_name,
                category=cleaned_data.get('category', 'general'),
                level=cleaned_data.get('level', 'all-levels'),
                state=cleaned_data.get('state', 'All India'),
                provider=cleaned_data.get('provider', ''),
                contact_email=cleaned_data.get('contact_email'),
                contact_phone=cleaned_data.get('contact_phone'),
                application_process=cleaned_data.get(
                    'application_process', ''),
                benefits=cleaned_data.get('benefits', []),
                selection_criteria=cleaned_data.get('selection_criteria', []),
                required_documents=cleaned_data.get('required_documents', []),
                tags=cleaned_data.get('tags', []),
                raw_data=cleaned_data,
                scraped_at=datetime.utcnow()
            )

            # Calculate quality score
            scholarship.quality_score = self._calculate_quality_score(
                scholarship)

            return scholarship

        except Exception as e:
            logger.error(f"Error extracting scholarship data: {e}")
            return None

    async def _traditional_extraction(self, element, source_config: Dict) -> Dict[str, Any]:
        """
        Traditional extraction using CSS selectors
        """
        selectors = source_config.get('selectors', {})
        extracted = {}

        try:
            # Extract title
            title_selector = selectors.get('title', 'h1, h2, h3, .title')
            title_elem = element.select_one(title_selector)
            if title_elem:
                extracted['title'] = title_elem.get_text(strip=True)

            # Extract description
            desc_selector = selectors.get(
                'description', '.description, .content, p')
            desc_elem = element.select_one(desc_selector)
            if desc_elem:
                extracted['description'] = desc_elem.get_text(strip=True)

            # Extract amount
            amount_selector = selectors.get(
                'amount', '.amount, .prize, .benefit')
            amount_elem = element.select_one(amount_selector)
            if amount_elem:
                amount_text = amount_elem.get_text(strip=True)
                extracted['amount'] = self.amount_parser.parse_amount(
                    amount_text)

            # Extract deadline
            deadline_selector = selectors.get(
                'deadline', '.deadline, .last-date, .closing-date')
            deadline_elem = element.select_one(deadline_selector)
            if deadline_elem:
                deadline_text = deadline_elem.get_text(strip=True)
                extracted['deadline'] = self.date_parser.parse_date(
                    deadline_text)

            # Extract eligibility
            eligibility_selector = selectors.get(
                'eligibility', '.eligibility, .criteria')
            eligibility_elems = element.select(eligibility_selector)
            if eligibility_elems:
                eligibility_list = []
                for elem in eligibility_elems:
                    eligibility_list.append(elem.get_text(strip=True))
                extracted['eligibility'] = eligibility_list

            # Extract application URL
            url_selector = selectors.get(
                'application_url', 'a[href*="apply"], .apply-link')
            url_elem = element.select_one(url_selector)
            if url_elem:
                extracted['application_url'] = url_elem.get('href', '')

            # Extract other fields
            for field, selector in selectors.items():
                if field not in extracted:
                    elem = element.select_one(selector)
                    if elem:
                        extracted[field] = elem.get_text(strip=True)

        except Exception as e:
            logger.error(f"Traditional extraction error: {e}")

        return extracted

    def _merge_extraction_results(self, ai_data: Dict, traditional_data: Dict) -> Dict[str, Any]:
        """
        Merge AI and traditional extraction results, prioritizing AI results
        """
        merged = {}

        # Start with traditional data as base
        merged.update(traditional_data)

        # Override with AI data where available and more accurate
        for key, value in ai_data.items():
            if value and (key not in merged or not merged[key]):
                merged[key] = value
            elif value and key in merged:
                # Use AI data if it's more comprehensive
                if isinstance(value, str) and len(value) > len(str(merged[key])):
                    merged[key] = value
                elif isinstance(value, list) and len(value) > len(merged.get(key, [])):
                    merged[key] = value

        return merged

    async def _clean_and_validate_data(self, data: Dict[str, Any], source_name: str) -> Optional[Dict[str, Any]]:
        """
        Clean and validate extracted scholarship data
        """
        try:
            # Clean title
            title = data.get('title', '').strip()
            if not title or len(title) < 10:
                return None

            # Clean description
            description = data.get('description', '').strip()
            if not description or len(description) < 20:
                return None

            # Validate amount
            amount = data.get('amount')
            if amount is not None:
                try:
                    amount = float(amount)
                    if amount <= 0:
                        amount = None
                except (ValueError, TypeError):
                    amount = None

            # Validate deadline
            deadline = data.get('deadline')
            if deadline:
                try:
                    if isinstance(deadline, str):
                        deadline = self.date_parser.parse_date(deadline)

                    # Check if deadline is in the future
                    if deadline and deadline < datetime.now().date():
                        return None  # Skip expired scholarships

                except Exception:
                    deadline = None

            # Clean and validate application URL
            application_url = data.get('application_url', '').strip()
            if application_url:
                if not application_url.startswith(('http://', 'https://')):
                    # Try to construct full URL
                    base_url = f"https://{source_name}"
                    application_url = urljoin(base_url, application_url)

                # Validate URL
                if not self.link_validator.validate_url(application_url):
                    application_url = ''

            # Clean eligibility list
            eligibility = data.get('eligibility', [])
            if isinstance(eligibility, str):
                eligibility = [eligibility]
            eligibility = [e.strip() for e in eligibility if e.strip()]

            # Process text fields
            title = self.text_processor.clean_text(title)
            description = self.text_processor.clean_text(description)

            # Extract category from title/description
            category = self._extract_category(title, description)

            # Extract education level
            level = self._extract_education_level(
                title, description, eligibility)

            # Extract state
            state = self._extract_state(title, description, eligibility)

            # Generate tags
            tags = self._generate_tags(title, description, eligibility)

            cleaned_data = {
                'title': title,
                'description': description,
                'amount': amount,
                'deadline': deadline.isoformat() if deadline else None,
                'eligibility': eligibility,
                'application_url': application_url,
                'category': category,
                'level': level,
                'state': state,
                'provider': data.get('provider', ''),
                'contact_email': data.get('contact_email'),
                'contact_phone': data.get('contact_phone'),
                'application_process': data.get('application_process', ''),
                'benefits': data.get('benefits', []),
                'selection_criteria': data.get('selection_criteria', []),
                'required_documents': data.get('required_documents', []),
                'tags': tags
            }

            return cleaned_data

        except Exception as e:
            logger.error(f"Error cleaning and validating data: {e}")
            return None

    def _calculate_quality_score(self, scholarship: ScrapedScholarship) -> int:
        """
        Calculate quality score for scraped scholarship
        """
        score = 0

        # Title quality (0-20)
        if scholarship.title and len(scholarship.title) > 10:
            score += 20
        elif scholarship.title and len(scholarship.title) > 5:
            score += 15
        else:
            score += 10

        # Description quality (0-20)
        if scholarship.description and len(scholarship.description) > 200:
            score += 20
        elif scholarship.description and len(scholarship.description) > 100:
            score += 15
        elif scholarship.description and len(scholarship.description) > 50:
            score += 10
        else:
            score += 5

        # Application URL quality (0-20)
        if scholarship.application_url and self.link_validator.validate_url(scholarship.application_url):
            score += 20
        else:
            score += 5

        # Deadline validity (0-15)
        if scholarship.deadline:
            try:
                deadline_date = datetime.fromisoformat(
                    scholarship.deadline).date()
                if deadline_date > datetime.now().date():
                    score += 15
                else:
                    score += 5
            except:
                score += 5
        else:
            score += 5

        # Amount specification (0-15)
        if scholarship.amount and scholarship.amount > 0:
            score += 15
        else:
            score += 5

        # Eligibility details (0-10)
        if scholarship.eligibility and len(scholarship.eligibility) > 0:
            score += 10
        else:
            score += 3

        return min(score, 100)

    def _extract_category(self, title: str, description: str) -> str:
        """
        Extract scholarship category from title and description
        """
        text = f"{title} {description}".lower()

        category_keywords = {
            'merit': ['merit', 'toppers', 'academic excellence', 'outstanding'],
            'need-based': ['need based', 'financial aid', 'economically weaker', 'poor'],
            'minority': ['minority', 'muslim', 'christian', 'sikh', 'buddhist', 'jain'],
            'women': ['women', 'girl', 'female', 'lady', 'mother'],
            'disabled': ['disabled', 'handicapped', 'divyang', 'differently abled'],
            'sc': ['sc', 'scheduled caste', 'dalit'],
            'st': ['st', 'scheduled tribe', 'tribal'],
            'obc': ['obc', 'other backward class', 'backward'],
            'sports': ['sports', 'athlete', 'games', 'physical education'],
            'arts': ['arts', 'cultural', 'music', 'dance', 'painting'],
            'science': ['science', 'research', 'scientific', 'innovation'],
            'technology': ['technology', 'technical', 'engineering', 'it'],
            'medical': ['medical', 'medicine', 'healthcare', 'doctor', 'nurse'],
            'engineering': ['engineering', 'engineer', 'technical'],
            'law': ['law', 'legal', 'advocate', 'lawyer'],
            'management': ['management', 'mba', 'business', 'commerce'],
            'agriculture': ['agriculture', 'farming', 'agricultural'],
            'international': ['international', 'foreign', 'abroad', 'overseas']
        }

        for category, keywords in category_keywords.items():
            if any(keyword in text for keyword in keywords):
                return category

        return 'general'

    def _extract_education_level(self, title: str, description: str, eligibility: List[str]) -> str:
        """
        Extract education level from scholarship information
        """
        text = f"{title} {description} {' '.join(eligibility)}".lower()

        level_keywords = {
            'pre-matric': ['pre matric', 'class 9', 'class 10', '9th', '10th'],
            'post-matric': ['post matric', 'class 11', 'class 12', '11th', '12th'],
            'graduation': ['graduation', 'bachelor', 'ba', 'bsc', 'bcom', 'be', 'btech', 'undergraduate'],
            'post-graduation': ['post graduation', 'masters', 'ma', 'msc', 'mcom', 'mba', 'mtech', 'postgraduate'],
            'doctorate': ['doctorate', 'phd', 'doctoral', 'research'],
            'diploma': ['diploma', 'polytechnic'],
            'certificate': ['certificate', 'certification'],
            'professional': ['professional', 'ca', 'cs', 'cma', 'medical', 'law'],
            'vocational': ['vocational', 'skill', 'training', 'iti']
        }

        for level, keywords in level_keywords.items():
            if any(keyword in text for keyword in keywords):
                return level

        return 'all-levels'

    def _extract_state(self, title: str, description: str, eligibility: List[str]) -> str:
        """
        Extract state from scholarship information
        """
        text = f"{title} {description} {' '.join(eligibility)}".lower()

        for state in settings.INDIAN_STATES:
            if state.lower() in text:
                return state

        # Check for common state abbreviations
        state_abbr = {
            'up': 'Uttar Pradesh',
            'mp': 'Madhya Pradesh',
            'hp': 'Himachal Pradesh',
            'ap': 'Andhra Pradesh',
            'tn': 'Tamil Nadu',
            'wb': 'West Bengal',
            'rj': 'Rajasthan',
            'gj': 'Gujarat',
            'mh': 'Maharashtra',
            'ka': 'Karnataka',
            'kl': 'Kerala',
            'od': 'Odisha',
            'as': 'Assam',
            'jh': 'Jharkhand',
            'ch': 'Chhattisgarh',
            'hr': 'Haryana',
            'pb': 'Punjab',
            'br': 'Bihar',
            'uk': 'Uttarakhand',
            'ga': 'Goa',
            'sk': 'Sikkim',
            'mn': 'Manipur',
            'mg': 'Meghalaya',
            'mz': 'Mizoram',
            'nl': 'Nagaland',
            'tr': 'Tripura',
            'ar': 'Arunachal Pradesh'
        }

        for abbr, full_name in state_abbr.items():
            if abbr in text:
                return full_name

        return 'All India'

    def _generate_tags(self, title: str, description: str, eligibility: List[str]) -> List[str]:
        """
        Generate tags for scholarship
        """
        text = f"{title} {description} {' '.join(eligibility)}".lower()

        tags = []

        # Extract keywords
        keywords = [
            'scholarship', 'fellowship', 'grant', 'award', 'stipend',
            'merit', 'need', 'minority', 'women', 'disabled', 'sports',
            'arts', 'science', 'technology', 'medical', 'engineering',
            'government', 'private', 'international', 'research'
        ]

        for keyword in keywords:
            if keyword in text:
                tags.append(keyword)

        # Extract institution types
        institution_types = ['university', 'college',
                             'school', 'institute', 'iit', 'nit', 'iiit', 'aiims']
        for inst_type in institution_types:
            if inst_type in text:
                tags.append(inst_type)

        return list(set(tags))  # Remove duplicates

    async def _fallback_extraction(self, soup: BeautifulSoup, source_name: str,
                                   source_config: Dict) -> List[ScrapedScholarship]:
        """
        Fallback extraction when AI and standard methods fail
        """
        scholarships = []

        try:
            # Look for any links or sections that might contain scholarships
            potential_elements = soup.find_all(['div', 'section', 'article', 'li'],
                                               class_=re.compile(r'scholarship|scheme|grant|award|fellowship', re.I))

            for element in potential_elements:
                try:
                    text_content = element.get_text(strip=True)
                    if len(text_content) > 100:  # Minimum content length
                        # Try to extract basic information
                        basic_data = {
                            'title': self._extract_title_from_text(text_content),
                            # First 500 chars
                            'description': text_content[:500],
                            'source': source_name
                        }

                        cleaned_data = await self._clean_and_validate_data(basic_data, source_name)
                        if cleaned_data:
                            scholarship = ScrapedScholarship(**cleaned_data,
                                                             raw_data=basic_data,
                                                             scraped_at=datetime.utcnow())
                            scholarship.quality_score = self._calculate_quality_score(
                                scholarship)
                            scholarships.append(scholarship)

                except Exception as e:
                    logger.debug(f"Error in fallback extraction: {e}")
                    continue

        except Exception as e:
            logger.error(f"Fallback extraction failed: {e}")

        return scholarships

    def _extract_title_from_text(self, text: str) -> str:
        """
        Extract title from text content
        """
        # Split by common separators and take the first meaningful line
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) > 10 and len(line) < 200:
                return line

        # If no good line found, take first 100 characters
        return text[:100].strip()

    async def save_scraped_scholarships(self, db: Session, scholarships: List[ScrapedScholarship]) -> int:
        """
        Save scraped scholarships to database with deduplication
        """
        saved_count = 0

        try:
            for scholarship in scholarships:
                try:
                    # Check for duplicates
                    is_duplicate = await self.duplication_detector.is_duplicate(
                        db, scholarship.title, scholarship.description, scholarship.source
                    )

                    if is_duplicate:
                        logger.debug(
                            f"Duplicate scholarship found: {scholarship.title}")
                        continue

                    # Validate scholarship data
                    if not await self.validation_service.validate_scholarship_data(scholarship):
                        logger.warning(
                            f"Scholarship validation failed: {scholarship.title}")
                        continue

                    # Create scholarship record
                    scholarship_data = ScholarshipCreate(
                        title=scholarship.title,
                        description=scholarship.description,
                        amount=scholarship.amount,
                        deadline=scholarship.deadline,
                        eligibility=scholarship.eligibility,
                        application_url=scholarship.application_url,
                        source=scholarship.source,
                        category=scholarship.category,
                        level=scholarship.level,
                        state=scholarship.state,
                        provider=scholarship.provider,
                        contact_email=scholarship.contact_email,
                        contact_phone=scholarship.contact_phone,
                        application_process=scholarship.application_process,
                        benefits=scholarship.benefits,
                        selection_criteria=scholarship.selection_criteria,
                        required_documents=scholarship.required_documents,
                        tags=scholarship.tags,
                        quality_score=scholarship.quality_score,
                        is_verified=False,  # Needs manual verification
                        is_active=True,
                        raw_data=scholarship.raw_data,
                        scraped_at=scholarship.scraped_at
                    )

                    # Save to database
                    db_scholarship = Scholarship(**scholarship_data.dict())
                    db.add(db_scholarship)
                    db.commit()

                    saved_count += 1
                    logger.info(f"Saved scholarship: {scholarship.title}")

                except Exception as e:
                    logger.error(
                        f"Error saving scholarship {scholarship.title}: {e}")
                    db.rollback()
                    continue

        except Exception as e:
            logger.error(f"Error saving scraped scholarships: {e}")
            db.rollback()
            raise

        logger.info(
            f"Saved {saved_count} scholarships out of {len(scholarships)} scraped")
        return saved_count

    async def create_scraping_job(self, db: Session, source_url: str,
                                  source_name: str, user_id: str) -> ScrapingJob:
        """
        Create a new scraping job
        """
        try:
            job_data = ScrapingJobCreate(
                source_url=source_url,
                source_name=source_name,
                status='pending',
                created_by=user_id,
                started_at=None,
                completed_at=None,
                items_scraped=0,
                items_saved=0,
                errors=[],
                configuration=self.source_configs.get(source_name, {})
            )

            db_job = ScrapingJob(**job_data.dict())
            db.add(db_job)
            db.commit()
            db.refresh(db_job)

            return db_job

        except Exception as e:
            logger.error(f"Error creating scraping job: {e}")
            db.rollback()
            raise

    async def execute_scraping_job(self, job_id: str):
        """
        Execute a scraping job
        """
        with db_transaction() as db:
            try:
                # Get job
                job = db.query(ScrapingJob).filter(
                    ScrapingJob.id == job_id).first()
                if not job:
                    logger.error(f"Scraping job {job_id} not found")
                    return

                # Update job status
                job.status = 'running'
                job.started_at = datetime.utcnow()
                db.commit()

                # Execute scraping
                scholarships = await self.scrape_scholarships(
                    job.source_url, job.source_name, max_pages=10
                )

                # Save scholarships
                saved_count = await self.save_scraped_scholarships(db, scholarships)

                # Update job completion
                job.status = 'completed'
                job.completed_at = datetime.utcnow()
                job.items_scraped = len(scholarships)
                job.items_saved = saved_count
                db.commit()

                logger.info(f"Scraping job {job_id} completed successfully")

            except Exception as e:
                logger.error(f"Error executing scraping job {job_id}: {e}")

                # Update job with error
                job.status = 'failed'
                job.completed_at = datetime.utcnow()
                job.errors.append(str(e))
                db.commit()

                raise

    async def get_scraping_sources(self) -> List[Dict[str, Any]]:
        """
        Get list of available scraping sources
        """
        sources = []

        for source_name, config in self.source_configs.items():
            sources.append({
                'name': source_name,
                'url': f"https://{source_name}",
                'description': f"Scholarships from {source_name}",
                'supported_features': {
                    'pagination': config.get('pagination', {}).get('enabled', False),
                    'ai_extraction': True,
                    'link_validation': True
                },
                'last_scraped': None,  # This would be fetched from database
                'status': 'active'
            })

        return sources

    async def get_scraping_stats(self, db: Session) -> Dict[str, Any]:
        """
        Get scraping statistics
        """
        try:
            total_jobs = db.query(ScrapingJob).count()
            completed_jobs = db.query(ScrapingJob).filter(
                ScrapingJob.status == 'completed').count()
            failed_jobs = db.query(ScrapingJob).filter(
                ScrapingJob.status == 'failed').count()
            running_jobs = db.query(ScrapingJob).filter(
                ScrapingJob.status == 'running').count()

            total_scholarships = db.query(Scholarship).count()
            active_scholarships = db.query(Scholarship).filter(
                Scholarship.is_active == True).count()
            verified_scholarships = db.query(Scholarship).filter(
                Scholarship.is_verified == True).count()

            return {
                'total_jobs': total_jobs,
                'completed_jobs': completed_jobs,
                'failed_jobs': failed_jobs,
                'running_jobs': running_jobs,
                'success_rate': (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0,
                'total_scholarships': total_scholarships,
                'active_scholarships': active_scholarships,
                'verified_scholarships': verified_scholarships,
                'verification_rate': (verified_scholarships / total_scholarships * 100) if total_scholarships > 0 else 0
            }

        except Exception as e:
            logger.error(f"Error getting scraping stats: {e}")
            raise
