"""
Enhanced Dynamic Crawler for Scholarship Discovery
Automatically discovers new scholarship pages and sources
"""

import asyncio
import aiohttp
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse, parse_qs
from typing import List, Dict, Set, Optional, Tuple
import logging
from datetime import datetime
from dataclasses import dataclass
import json
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class DiscoveredPage:
    """Data class for discovered scholarship pages"""
    url: str
    title: str
    content_preview: str
    relevance_score: float
    page_type: str  # 'list', 'detail', 'category'
    estimated_scholarships: int
    last_updated: Optional[datetime]
    source_domain: str
    metadata: Dict


class DynamicScholarshipCrawler:
    """
    Advanced crawler that dynamically discovers scholarship pages
    """

    def __init__(self):
        self.visited_urls: Set[str] = set()
        self.discovered_pages: List[DiscoveredPage] = []

        # Scholarship-related keywords for relevance scoring
        self.scholarship_keywords = {
            'high_relevance': [
                'scholarship', 'fellowship', 'bursary', 'grant', 'award',
                'financial aid', 'educational support', 'student aid',
                'merit scholarship', 'need based', 'विद्यार्थी वृत्ति',
                'छात्रवृत्ति', 'scholarship scheme', 'fellowship program'
            ],
            'medium_relevance': [
                'education', 'student', 'academic', 'university', 'college',
                'study', 'learning', 'tuition', 'fee waiver', 'admission',
                'eligibility', 'application', 'deadline', 'form'
            ],
            'context_keywords': [
                'apply now', 'last date', 'eligible', 'benefits', 'amount',
                'criteria', 'documents required', 'selection process',
                'how to apply', 'application process'
            ]
        }

        # Indian education domains to prioritize
        self.trusted_domains = [
            'scholarships.gov.in', 'buddy4study.com', 'aicte-india.org',
            'ugc.ac.in', 'nta.ac.in', 'csab.nic.in', 'nic.in',
            'education.gov.in', 'mhrd.gov.in', 'dst.gov.in',
            'meity.gov.in', 'minorityaffairs.gov.in', 'tribal.nic.in',
            'socialjustice.nic.in', 'ncbc.nic.in', 'nstfdc.nic.in'
        ]

        # URL patterns that likely contain scholarships
        self.scholarship_url_patterns = [
            r'scholarship',
            r'fellowship',
            r'grant',
            r'financial.?aid',
            r'student.?aid',
            r'bursary',
            r'award',
            r'scheme',
            r'yojana',
            r'vrithi',
            r'chhatravritti'
        ]

    async def discover_scholarship_sources(self,
                                           seed_urls: List[str],
                                           max_depth: int = 3,
                                           max_pages_per_source: int = 50) -> List[DiscoveredPage]:
        """
        Dynamically discover scholarship pages starting from seed URLs
        """
        logger.info(
            f"Starting dynamic discovery from {len(seed_urls)} seed URLs")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )

            # Process seed URLs
            for seed_url in seed_urls:
                await self._crawl_source(context, seed_url, max_depth, max_pages_per_source)

            await browser.close()

        # Sort by relevance score
        self.discovered_pages.sort(
            key=lambda x: x.relevance_score, reverse=True)

        logger.info(
            f"Discovery completed. Found {len(self.discovered_pages)} relevant pages")
        return self.discovered_pages

    async def _crawl_source(self,
                            context,
                            base_url: str,
                            max_depth: int,
                            max_pages: int):
        """
        Crawl a specific source to find scholarship pages
        """
        if len(self.visited_urls) >= max_pages:
            return

        page = await context.new_page()

        try:
            await page.goto(base_url, timeout=30000)
            await page.wait_for_load_state('networkidle', timeout=10000)

            # Extract page content and analyze
            content = await page.content()
            page_info = await self._analyze_page(page, base_url, content)

            if page_info and page_info.relevance_score > 0.3:
                self.discovered_pages.append(page_info)

            self.visited_urls.add(base_url)

            # Find links to explore further
            if max_depth > 0:
                links = await self._extract_relevant_links(page, base_url)

                for link in links[:10]:  # Limit concurrent processing
                    if link not in self.visited_urls and len(self.visited_urls) < max_pages:
                        await asyncio.sleep(1)  # Rate limiting
                        await self._crawl_source(context, link, max_depth - 1, max_pages)

        except Exception as e:
            logger.warning(f"Error crawling {base_url}: {str(e)}")
        finally:
            await page.close()

    async def _analyze_page(self, page, url: str, content: str) -> Optional[DiscoveredPage]:
        """
        Analyze a page to determine if it contains scholarship information
        """
        try:
            # Get page title
            title = await page.title()

            # Extract text content
            text_content = await page.evaluate('''
                () => {
                    // Remove script and style elements
                    const scripts = document.querySelectorAll('script, style');
                    scripts.forEach(el => el.remove());
                    return document.body.innerText;
                }
            ''')

            # Calculate relevance score
            relevance_score = self._calculate_relevance_score(
                title, text_content, url)

            if relevance_score < 0.2:
                return None

            # Determine page type
            page_type = self._determine_page_type(content, text_content)

            # Estimate number of scholarships
            estimated_scholarships = self._estimate_scholarship_count(
                content, text_content)

            # Extract metadata
            metadata = await self._extract_page_metadata(page)

            return DiscoveredPage(
                url=url,
                title=title,
                content_preview=text_content[:500],
                relevance_score=relevance_score,
                page_type=page_type,
                estimated_scholarships=estimated_scholarships,
                last_updated=datetime.now(),
                source_domain=urlparse(url).netloc,
                metadata=metadata
            )

        except Exception as e:
            logger.error(f"Error analyzing page {url}: {str(e)}")
            return None

    def _calculate_relevance_score(self, title: str, content: str, url: str) -> float:
        """
        Calculate relevance score based on content analysis
        """
        score = 0.0
        content_lower = content.lower()
        title_lower = title.lower()
        url_lower = url.lower()

        # High relevance keywords
        for keyword in self.scholarship_keywords['high_relevance']:
            if keyword in title_lower:
                score += 0.3
            if keyword in url_lower:
                score += 0.2
            score += content_lower.count(keyword) * 0.05

        # Medium relevance keywords
        for keyword in self.scholarship_keywords['medium_relevance']:
            if keyword in title_lower:
                score += 0.1
            score += content_lower.count(keyword) * 0.02

        # Context keywords
        for keyword in self.scholarship_keywords['context_keywords']:
            score += content_lower.count(keyword) * 0.03

        # Domain trust score
        domain = urlparse(url).netloc
        if any(trusted in domain for trusted in self.trusted_domains):
            score += 0.4

        # URL pattern matching
        for pattern in self.scholarship_url_patterns:
            if re.search(pattern, url_lower):
                score += 0.2
                break

        # Presence of forms (likely application pages)
        if '<form' in content and ('apply' in content_lower or 'application' in content_lower):
            score += 0.3

        # Presence of amount/money keywords
        money_patterns = [r'₹\s*\d+', r'rs\.?\s*\d+',
                          r'\d+\s*lakhs?', r'\d+\s*crores?']
        for pattern in money_patterns:
            if re.search(pattern, content_lower):
                score += 0.1
                break

        return min(score, 1.0)  # Cap at 1.0

    def _determine_page_type(self, html_content: str, text_content: str) -> str:
        """
        Determine the type of scholarship page
        """
        html_lower = html_content.lower()
        text_lower = text_content.lower()

        # Check for list indicators
        list_indicators = [
            'scholarship list', 'available scholarships', 'browse scholarships',
            'search scholarships', '<ul', '<ol', 'scholarship-list',
            'scholarship-grid', 'pagination'
        ]

        if any(indicator in html_lower for indicator in list_indicators):
            return 'list'

        # Check for detail page indicators
        detail_indicators = [
            'application form', 'apply now', 'eligibility criteria',
            'how to apply', 'required documents', 'selection process',
            'application deadline', 'benefits'
        ]

        if any(indicator in text_lower for indicator in detail_indicators):
            return 'detail'

        # Check for category page indicators
        category_indicators = [
            'category', 'scholarship types', 'browse by', 'filter',
            'merit based', 'need based', 'minority', 'sc/st'
        ]

        if any(indicator in text_lower for indicator in category_indicators):
            return 'category'

        return 'unknown'

    def _estimate_scholarship_count(self, html_content: str, text_content: str) -> int:
        """
        Estimate number of scholarships on the page
        """
        # Look for common scholarship item patterns
        patterns = [
            r'scholarship-item',
            r'scholarship-card',
            r'scholarship-row',
            r'scheme-item',
            r'fellowship-item'
        ]

        max_count = 0
        for pattern in patterns:
            count = len(re.findall(pattern, html_content, re.IGNORECASE))
            max_count = max(max_count, count)

        # Fallback: count scholarship keyword occurrences
        if max_count == 0:
            scholarship_mentions = text_content.lower().count('scholarship')
            max_count = min(scholarship_mentions // 2, 50)  # Rough estimate

        return max_count

    async def _extract_relevant_links(self, page, base_url: str) -> List[str]:
        """
        Extract links that are likely to contain scholarship information
        """
        try:
            links = await page.evaluate('''
                () => {
                    const links = Array.from(document.querySelectorAll('a[href]'));
                    return links.map(link => ({
                        href: link.href,
                        text: link.textContent.trim(),
                        title: link.getAttribute('title') || ''
                    }));
                }
            ''')

            relevant_links = []
            base_domain = urlparse(base_url).netloc

            for link_info in links:
                href = link_info['href']
                text = link_info['text'].lower()
                title = link_info['title'].lower()

                # Skip non-HTTP links
                if not href.startswith(('http://', 'https://')):
                    continue

                # Prefer same domain links
                link_domain = urlparse(href).netloc
                if link_domain != base_domain:
                    continue

                # Check if link text/title contains scholarship keywords
                relevance_score = 0
                for keyword in self.scholarship_keywords['high_relevance']:
                    if keyword in text or keyword in title:
                        relevance_score += 1

                if relevance_score > 0 or any(pattern in href.lower() for pattern in self.scholarship_url_patterns):
                    relevant_links.append(href)

            return list(set(relevant_links))  # Remove duplicates

        except Exception as e:
            logger.error(f"Error extracting links from {base_url}: {str(e)}")
            return []

    async def _extract_page_metadata(self, page) -> Dict:
        """
        Extract useful metadata from the page
        """
        try:
            metadata = await page.evaluate('''
                () => {
                    const meta = {};
                    
                    // Get meta tags
                    const metaTags = document.querySelectorAll('meta');
                    metaTags.forEach(tag => {
                        const name = tag.getAttribute('name') || tag.getAttribute('property');
                        const content = tag.getAttribute('content');
                        if (name && content) {
                            meta[name] = content;
                        }
                    });
                    
                    // Get structured data
                    const jsonLdScripts = document.querySelectorAll('script[type="application/ld+json"]');
                    const structuredData = [];
                    jsonLdScripts.forEach(script => {
                        try {
                            structuredData.push(JSON.parse(script.textContent));
                        } catch(e) {}
                    });
                    
                    if (structuredData.length > 0) {
                        meta.structuredData = structuredData;
                    }
                    
                    return meta;
                }
            ''')

            return metadata

        except Exception as e:
            logger.error(f"Error extracting metadata: {str(e)}")
            return {}

    def save_discovered_sources(self, filename: str = 'discovered_scholarship_sources.json'):
        """
        Save discovered sources to a file for future use
        """
        data = {
            'discovery_date': datetime.now().isoformat(),
            'total_discovered': len(self.discovered_pages),
            'sources': [
                {
                    'url': page.url,
                    'title': page.title,
                    'relevance_score': page.relevance_score,
                    'page_type': page.page_type,
                    'estimated_scholarships': page.estimated_scholarships,
                    'source_domain': page.source_domain,
                    'metadata': page.metadata
                }
                for page in self.discovered_pages
            ]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(
            f"Saved {len(self.discovered_pages)} discovered sources to {filename}")

    def get_high_priority_sources(self, min_score: float = 0.7) -> List[DiscoveredPage]:
        """
        Get high-priority sources for immediate scraping
        """
        return [page for page in self.discovered_pages if page.relevance_score >= min_score]


# Example usage and integration
async def discover_new_scholarship_sources():
    """
    Main function to discover new scholarship sources
    """
    crawler = DynamicScholarshipCrawler()

    # Seed URLs - starting points for discovery
    seed_urls = [
        'https://scholarships.gov.in/',
        'https://www.buddy4study.com/',
        'https://www.aicte-india.org/schemes',
        'https://www.ugc.ac.in/schemes',
        'https://www.education.gov.in/',
        'https://www.tribal.nic.in/',
        'https://socialjustice.nic.in/',
        'https://minorityaffairs.gov.in/'
    ]

    # Discover sources
    discovered_pages = await crawler.discover_scholarship_sources(
        seed_urls=seed_urls,
        max_depth=2,
        max_pages_per_source=30
    )

    # Save results
    crawler.save_discovered_sources()

    # Get high-priority sources
    high_priority = crawler.get_high_priority_sources(min_score=0.6)

    logger.info(
        f"Found {len(high_priority)} high-priority scholarship sources")

    return high_priority


if __name__ == "__main__":
    asyncio.run(discover_new_scholarship_sources())
