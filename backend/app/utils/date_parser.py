"""
Date parsing utilities.
"""

import re
from datetime import datetime, timedelta
from typing import Optional, List
import calendar


def parse_date(date_string: str) -> Optional[datetime]:
    """Parse date string into datetime object."""
    if not date_string:
        return None

    # Clean the string
    date_string = date_string.strip().lower()

    # Common date formats
    date_formats = [
        '%Y-%m-%d',
        '%d-%m-%Y',
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%Y/%m/%d',
        '%d-%m-%y',
        '%d/%m/%y',
        '%Y-%m-%d %H:%M:%S',
        '%d-%m-%Y %H:%M:%S',
        '%B %d, %Y',
        '%b %d, %Y',
        '%d %B %Y',
        '%d %b %Y',
        '%B %d %Y',
        '%b %d %Y',
    ]

    # Try each format
    for fmt in date_formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue

    # Try parsing relative dates
    relative_date = parse_relative_date(date_string)
    if relative_date:
        return relative_date

    # Try parsing Indian date formats
    indian_date = parse_indian_date(date_string)
    if indian_date:
        return indian_date

    return None


def parse_relative_date(date_string: str) -> Optional[datetime]:
    """Parse relative date expressions."""
    now = datetime.now()
    date_string = date_string.lower().strip()

    # Today, tomorrow, yesterday
    if 'today' in date_string:
        return now
    elif 'tomorrow' in date_string:
        return now + timedelta(days=1)
    elif 'yesterday' in date_string:
        return now - timedelta(days=1)

    # Next/last week/month/year
    if 'next week' in date_string:
        return now + timedelta(weeks=1)
    elif 'last week' in date_string:
        return now - timedelta(weeks=1)
    elif 'next month' in date_string:
        # Approximate next month
        return now + timedelta(days=30)
    elif 'last month' in date_string:
        return now - timedelta(days=30)
    elif 'next year' in date_string:
        return now.replace(year=now.year + 1)
    elif 'last year' in date_string:
        return now.replace(year=now.year - 1)

    # X days/weeks/months ago/from now
    time_patterns = [
        (r'(\d+)\s*days?\s*ago', lambda x: now - timedelta(days=int(x))),
        (r'(\d+)\s*weeks?\s*ago', lambda x: now - timedelta(weeks=int(x))),
        (r'(\d+)\s*months?\s*ago', lambda x: now - timedelta(days=int(x) * 30)),
        (r'(\d+)\s*days?\s*from\s*now', lambda x: now + timedelta(days=int(x))),
        (r'(\d+)\s*weeks?\s*from\s*now', lambda x: now + timedelta(weeks=int(x))),
        (r'(\d+)\s*months?\s*from\s*now',
         lambda x: now + timedelta(days=int(x) * 30)),
        (r'in\s*(\d+)\s*days?', lambda x: now + timedelta(days=int(x))),
        (r'in\s*(\d+)\s*weeks?', lambda x: now + timedelta(weeks=int(x))),
        (r'in\s*(\d+)\s*months?', lambda x: now + timedelta(days=int(x) * 30)),
    ]

    for pattern, calculator in time_patterns:
        match = re.search(pattern, date_string)
        if match:
            try:
                return calculator(match.group(1))
            except (ValueError, OverflowError):
                continue

    return None


def parse_indian_date(date_string: str) -> Optional[datetime]:
    """Parse Indian date formats."""
    # Month names in various Indian languages (simplified)
    month_mapping = {
        'jan': 1, 'january': 1,
        'feb': 2, 'february': 2,
        'mar': 3, 'march': 3,
        'apr': 4, 'april': 4,
        'may': 5,
        'jun': 6, 'june': 6,
        'jul': 7, 'july': 7,
        'aug': 8, 'august': 8,
        'sep': 9, 'september': 9,
        'oct': 10, 'october': 10,
        'nov': 11, 'november': 11,
        'dec': 12, 'december': 12,
    }

    # Try to extract day, month, year
    date_pattern = r'(\d{1,2})[^\w]*(\w+)[^\w]*(\d{2,4})'
    match = re.search(date_pattern, date_string.lower())

    if match:
        try:
            day = int(match.group(1))
            month_str = match.group(2)
            year = int(match.group(3))

            # Convert month string to number
            month = month_mapping.get(month_str)
            if not month:
                # Try to find partial matches
                for name, num in month_mapping.items():
                    if name.startswith(month_str[:3]) or month_str.startswith(name[:3]):
                        month = num
                        break

            if month:
                # Handle 2-digit years
                if year < 100:
                    current_year = datetime.now().year
                    if year < 50:
                        year += 2000
                    else:
                        year += 1900

                return datetime(year, month, day)
        except (ValueError, TypeError):
            pass

    return None


def extract_deadline_from_text(text: str) -> Optional[datetime]:
    """Extract deadline dates from text."""
    if not text:
        return None

    text = text.lower()

    # Look for deadline keywords
    deadline_keywords = [
        'deadline', 'last date', 'closing date', 'due date', 'final date',
        'submission date', 'application closes', 'before', 'by', 'until'
    ]

    # Find sentences containing deadline keywords
    sentences = re.split(r'[.!?;]', text)
    deadline_sentences = []

    for sentence in sentences:
        for keyword in deadline_keywords:
            if keyword in sentence:
                deadline_sentences.append(sentence.strip())
                break

    # Try to extract dates from deadline sentences
    for sentence in deadline_sentences:
        date = parse_date(sentence)
        if date:
            return date

        # Look for date patterns in the sentence
        date_patterns = [
            r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b',
            r'\b(\d{1,2})\s+(\w+)\s+(\d{2,4})\b',
            r'\b(\w+)\s+(\d{1,2}),?\s+(\d{2,4})\b',
        ]

        for pattern in date_patterns:
            matches = re.findall(pattern, sentence)
            for match in matches:
                try:
                    date = parse_date(' '.join(match))
                    if date:
                        return date
                except:
                    continue

    return None


def is_valid_deadline(date: datetime) -> bool:
    """Check if a deadline date is valid (not in the past, not too far in future)."""
    if not date:
        return False

    now = datetime.now()

    # Check if date is in the past (with some tolerance)
    if date < now - timedelta(days=1):
        return False

    # Check if date is too far in the future (more than 5 years)
    if date > now + timedelta(days=365 * 5):
        return False

    return True


def format_date_indian(date: datetime) -> str:
    """Format date in Indian style."""
    if not date:
        return ""

    return date.strftime("%d %B %Y")


def get_days_until_deadline(deadline: datetime) -> int:
    """Get number of days until deadline."""
    if not deadline:
        return -1

    now = datetime.now()
    delta = deadline - now

    return delta.days


def is_deadline_approaching(deadline: datetime, days_threshold: int = 7) -> bool:
    """Check if deadline is approaching within threshold days."""
    days_left = get_days_until_deadline(deadline)
    return 0 <= days_left <= days_threshold
