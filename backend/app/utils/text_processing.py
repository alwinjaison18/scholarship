"""
Text processing utilities.
"""

import re
from typing import List, Optional
from html import unescape
import unicodedata


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""

    # Unescape HTML entities
    text = unescape(text)

    # Normalize unicode
    text = unicodedata.normalize('NFKD', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text."""
    if not text:
        return []

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and split
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text)

    # Remove common stop words
    stop_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'between', 'among', 'this', 'that', 'these',
        'those', 'is', 'are', 'was', 'were', 'been', 'being', 'have', 'has',
        'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
        'might', 'must', 'can', 'shall'
    }

    keywords = [
        word for word in words if word not in stop_words and len(word) > 2]

    # Remove duplicates while preserving order
    seen = set()
    result = []
    for word in keywords:
        if word not in seen:
            seen.add(word)
            result.append(word)

    return result[:20]  # Return top 20 keywords


def extract_email_addresses(text: str) -> List[str]:
    """Extract email addresses from text."""
    if not text:
        return []

    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)

    return list(set(emails))  # Remove duplicates


def extract_phone_numbers(text: str) -> List[str]:
    """Extract Indian phone numbers from text."""
    if not text:
        return []

    # Pattern for Indian phone numbers
    phone_patterns = [
        r'\+91[-\s]?\d{10}',  # +91 followed by 10 digits
        r'91[-\s]?\d{10}',    # 91 followed by 10 digits
        r'\d{10}',            # 10 digits
        r'\d{3}[-\s]?\d{3}[-\s]?\d{4}'  # Formatted numbers
    ]

    phones = []
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        phones.extend(matches)

    # Clean and normalize phone numbers
    cleaned_phones = []
    for phone in phones:
        # Remove non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', phone)
        if len(cleaned) >= 10:
            cleaned_phones.append(cleaned)

    return list(set(cleaned_phones))  # Remove duplicates


def extract_urls(text: str) -> List[str]:
    """Extract URLs from text."""
    if not text:
        return []

    url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
    urls = re.findall(url_pattern, text)

    return list(set(urls))  # Remove duplicates


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length."""
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    # Try to break at word boundary
    truncated = text[:max_length - len(suffix)]
    last_space = truncated.rfind(' ')

    if last_space > max_length * 0.7:  # If word boundary is reasonably close
        truncated = truncated[:last_space]

    return truncated + suffix


def normalize_category(category: str) -> str:
    """Normalize scholarship category."""
    if not category:
        return "Other"

    category = category.lower().strip()

    # Mapping of common variations to standard categories
    category_mapping = {
        'merit': 'Merit',
        'merit-cum-means': 'Merit-cum-Means',
        'merit cum means': 'Merit-cum-Means',
        'means': 'Means',
        'need based': 'Need-based',
        'need-based': 'Need-based',
        'sc': 'SC/ST',
        'st': 'SC/ST',
        'sc/st': 'SC/ST',
        'obc': 'OBC',
        'minority': 'Minority',
        'central government': 'Central Government',
        'state government': 'State Government',
        'private': 'Private',
        'research': 'Research',
        'fellowship': 'Fellowship',
        'international': 'International'
    }

    return category_mapping.get(category, category.title())


def normalize_level(level: str) -> str:
    """Normalize education level."""
    if not level:
        return "Other"

    level = level.lower().strip()

    level_mapping = {
        'undergraduate': 'Undergraduate',
        'ug': 'Undergraduate',
        'bachelor': 'Undergraduate',
        'bachelors': 'Undergraduate',
        'btech': 'Undergraduate',
        'be': 'Undergraduate',
        'bsc': 'Undergraduate',
        'ba': 'Undergraduate',
        'bcom': 'Undergraduate',
        'postgraduate': 'Postgraduate',
        'pg': 'Postgraduate',
        'master': 'Postgraduate',
        'masters': 'Postgraduate',
        'mtech': 'Postgraduate',
        'me': 'Postgraduate',
        'msc': 'Postgraduate',
        'ma': 'Postgraduate',
        'mcom': 'Postgraduate',
        'mba': 'Postgraduate',
        'phd': 'PhD',
        'doctoral': 'PhD',
        'doctorate': 'PhD',
        'diploma': 'Diploma',
        'certificate': 'Certificate'
    }

    return level_mapping.get(level, level.title())


def extract_amount_from_text(text: str) -> Optional[float]:
    """Extract scholarship amount from text."""
    if not text:
        return None

    # Patterns for amount extraction
    amount_patterns = [
        r'₹\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:lakh|lac)?',
        r'rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:lakh|lac)?',
        r'rupees?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:lakh|lac)?',
        r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:rs|rupees?)\s*(?:lakh|lac)?',
        r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:lakh|lac)',
        r'(\d+(?:,\d+)*(?:\.\d+)?)',
    ]

    for pattern in amount_patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            try:
                # Remove commas and convert to float
                amount_str = matches[0].replace(',', '')
                amount = float(amount_str)

                # Check if lakh is mentioned
                if 'lakh' in text.lower() or 'lac' in text.lower():
                    amount *= 100000

                return amount
            except (ValueError, IndexError):
                continue

    return None
