"""
AI service for intelligent scholarship processing and recommendations.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import asyncio

logger = logging.getLogger(__name__)


@dataclass
class RecommendationScore:
    """Recommendation score with reasoning."""
    score: float
    reasons: List[str]
    confidence: float


@dataclass
class TextAnalysisResult:
    """Result of text analysis."""
    categories: List[str]
    keywords: List[str]
    sentiment: str
    confidence: float


class AIService:
    """AI service for intelligent scholarship processing."""

    def __init__(self):
        self.initialized = False
        self.model_version = "1.0.0"

    async def initialize(self):
        """Initialize AI models and services."""
        try:
            # Initialize any AI models here
            # For now, we'll use rule-based approaches
            self.initialized = True
            logger.info("AI service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI service: {str(e)}")
            raise

    def analyze_scholarship_text(self, text: str) -> TextAnalysisResult:
        """
        Analyze scholarship text for categories, keywords, and sentiment.

        Args:
            text: Text to analyze

        Returns:
            TextAnalysisResult with analysis results
        """
        if not self.initialized:
            raise RuntimeError("AI service not initialized")

        # Simple rule-based analysis (can be replaced with ML models)
        categories = self._extract_categories(text)
        keywords = self._extract_keywords(text)
        sentiment = self._analyze_sentiment(text)

        return TextAnalysisResult(
            categories=categories,
            keywords=keywords,
            sentiment=sentiment,
            confidence=0.8  # Placeholder confidence
        )

    def calculate_recommendation_score(
        self,
        user_profile: Dict[str, Any],
        scholarship_data: Dict[str, Any]
    ) -> RecommendationScore:
        """
        Calculate recommendation score for a user-scholarship pair.

        Args:
            user_profile: User profile data
            scholarship_data: Scholarship data

        Returns:
            RecommendationScore with score and reasoning
        """
        if not self.initialized:
            raise RuntimeError("AI service not initialized")

        score = 0.0
        reasons = []

        # Field of study matching
        user_field = user_profile.get('field_of_study', '').lower()
        scholarship_category = scholarship_data.get('category', '').lower()

        if user_field and scholarship_category:
            if user_field in scholarship_category or scholarship_category in user_field:
                score += 0.3
                reasons.append(f"Field of study matches: {user_field}")

        # Education level matching
        user_education = user_profile.get('education_level', '').lower()
        scholarship_eligibility = scholarship_data.get(
            'eligibility', '').lower()

        if user_education and scholarship_eligibility:
            if user_education in scholarship_eligibility:
                score += 0.2
                reasons.append(f"Education level matches: {user_education}")

        # Location matching
        user_location = user_profile.get('location', '').lower()
        scholarship_location = scholarship_data.get('location', '').lower()

        if user_location and scholarship_location:
            if user_location in scholarship_location or scholarship_location in user_location:
                score += 0.15
                reasons.append(f"Location matches: {user_location}")

        # Age matching
        user_age = user_profile.get('age')
        scholarship_age_limit = scholarship_data.get('age_limit')

        if user_age and scholarship_age_limit:
            if user_age <= scholarship_age_limit:
                score += 0.1
                reasons.append(
                    f"Age requirement met: {user_age} <= {scholarship_age_limit}")

        # Income matching
        user_income = user_profile.get('family_income')
        scholarship_income_limit = scholarship_data.get('income_limit')

        if user_income and scholarship_income_limit:
            if user_income <= scholarship_income_limit:
                score += 0.15
                reasons.append(
                    f"Income requirement met: {user_income} <= {scholarship_income_limit}")

        # Academic performance
        user_gpa = user_profile.get('gpa')
        scholarship_min_gpa = scholarship_data.get('min_gpa')

        if user_gpa and scholarship_min_gpa:
            if user_gpa >= scholarship_min_gpa:
                score += 0.1
                reasons.append(
                    f"GPA requirement met: {user_gpa} >= {scholarship_min_gpa}")

        # Ensure score is between 0 and 1
        score = min(1.0, max(0.0, score))

        # Calculate confidence based on available data
        confidence = self._calculate_confidence(user_profile, scholarship_data)

        return RecommendationScore(
            score=score,
            reasons=reasons,
            confidence=confidence
        )

    def extract_scholarship_metadata(self, raw_text: str) -> Dict[str, Any]:
        """
        Extract structured metadata from raw scholarship text.

        Args:
            raw_text: Raw scholarship text

        Returns:
            Dict with extracted metadata
        """
        if not self.initialized:
            raise RuntimeError("AI service not initialized")

        metadata = {}

        # Extract amount
        amount = self._extract_amount(raw_text)
        if amount:
            metadata['amount'] = amount

        # Extract deadline
        deadline = self._extract_deadline(raw_text)
        if deadline:
            metadata['deadline'] = deadline

        # Extract eligibility criteria
        eligibility = self._extract_eligibility(raw_text)
        if eligibility:
            metadata['eligibility'] = eligibility

        # Extract location
        location = self._extract_location(raw_text)
        if location:
            metadata['location'] = location

        # Extract application process
        application_process = self._extract_application_process(raw_text)
        if application_process:
            metadata['application_process'] = application_process

        return metadata

    def detect_spam_or_fraud(self, scholarship_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Detect potential spam or fraudulent scholarships.

        Args:
            scholarship_data: Scholarship data to analyze

        Returns:
            Tuple of (is_suspicious, reasons)
        """
        if not self.initialized:
            raise RuntimeError("AI service not initialized")

        is_suspicious = False
        reasons = []

        # Check for suspicious patterns
        title = scholarship_data.get('title', '').lower()
        description = scholarship_data.get('description', '').lower()
        url = scholarship_data.get('url', '').lower()

        # Suspicious keywords
        suspicious_keywords = [
            'guaranteed', 'no application fee', 'easy money', 'instant approval',
            'act now', 'limited time', 'secret', 'exclusive', 'lottery'
        ]

        for keyword in suspicious_keywords:
            if keyword in title or keyword in description:
                is_suspicious = True
                reasons.append(f"Suspicious keyword found: {keyword}")

        # Check for unrealistic amounts
        amount = scholarship_data.get('amount', 0)
        if amount > 1000000:  # More than 10 lakh
            is_suspicious = True
            reasons.append(f"Unrealistic amount: ₹{amount}")

        # Check for suspicious URLs
        suspicious_domains = ['.tk', '.ml', '.ga', '.cf', 'bit.ly', 'tinyurl']
        for domain in suspicious_domains:
            if domain in url:
                is_suspicious = True
                reasons.append(f"Suspicious domain: {domain}")

        # Check for missing essential information
        if not scholarship_data.get('deadline'):
            is_suspicious = True
            reasons.append("Missing deadline information")

        if not scholarship_data.get('eligibility'):
            is_suspicious = True
            reasons.append("Missing eligibility criteria")

        return is_suspicious, reasons

    def _extract_categories(self, text: str) -> List[str]:
        """Extract categories from text."""
        categories = []
        text_lower = text.lower()

        category_keywords = {
            'Engineering': ['engineering', 'technology', 'computer', 'software', 'mechanical'],
            'Medicine': ['medical', 'medicine', 'doctor', 'mbbs', 'nursing'],
            'Arts': ['arts', 'literature', 'humanities', 'fine arts', 'music'],
            'Science': ['science', 'physics', 'chemistry', 'biology', 'mathematics'],
            'Commerce': ['commerce', 'business', 'economics', 'finance', 'accounting'],
            'Law': ['law', 'legal', 'advocate', 'llb', 'judiciary'],
            'Education': ['education', 'teaching', 'b.ed', 'm.ed', 'teacher'],
            'Research': ['research', 'phd', 'doctoral', 'thesis', 'innovation']
        }

        for category, keywords in category_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                categories.append(category)

        return categories

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        # Simple keyword extraction (can be improved with NLP)
        words = text.lower().split()

        # Common important words in scholarships
        important_words = [
            'scholarship', 'grant', 'fellowship', 'award', 'merit', 'need',
            'undergraduate', 'postgraduate', 'graduate', 'doctoral', 'phd',
            'engineering', 'medical', 'arts', 'science', 'commerce', 'law',
            'research', 'innovation', 'academic', 'excellence', 'achievement'
        ]

        keywords = [word for word in words if word in important_words]
        return list(set(keywords))  # Remove duplicates

    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of text."""
        # Simple sentiment analysis
        positive_words = ['excellent', 'outstanding',
                          'prestigious', 'opportunity', 'benefit']
        negative_words = ['difficult', 'strict',
                          'limited', 'competitive', 'challenging']

        text_lower = text.lower()
        positive_count = sum(
            1 for word in positive_words if word in text_lower)
        negative_count = sum(
            1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

    def _calculate_confidence(self, user_profile: Dict[str, Any], scholarship_data: Dict[str, Any]) -> float:
        """Calculate confidence score based on available data."""
        user_fields = len([v for v in user_profile.values() if v])
        scholarship_fields = len([v for v in scholarship_data.values() if v])

        total_fields = len(user_profile) + len(scholarship_data)
        available_fields = user_fields + scholarship_fields

        if total_fields == 0:
            return 0.0

        return available_fields / total_fields

    def _extract_amount(self, text: str) -> Optional[float]:
        """Extract monetary amount from text."""
        import re

        # Look for amount patterns
        amount_patterns = [
            r'₹\s*(\d+(?:,\d+)*)',
            r'rs\.?\s*(\d+(?:,\d+)*)',
            r'rupees?\s*(\d+(?:,\d+)*)',
            r'(\d+(?:,\d+)*)\s*rupees?'
        ]

        for pattern in amount_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                amount_str = matches[0].replace(',', '')
                try:
                    return float(amount_str)
                except ValueError:
                    continue

        return None

    def _extract_deadline(self, text: str) -> Optional[str]:
        """Extract deadline from text."""
        import re

        # Look for date patterns
        date_patterns = [
            r'deadline[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'last date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'apply by[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
        ]

        for pattern in date_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return matches[0]

        return None

    def _extract_eligibility(self, text: str) -> Optional[str]:
        """Extract eligibility criteria from text."""
        # Look for eligibility sections
        text_lower = text.lower()

        eligibility_keywords = [
            'eligibility', 'eligible', 'criteria', 'requirements',
            'qualification', 'must have', 'should have'
        ]

        for keyword in eligibility_keywords:
            if keyword in text_lower:
                # Extract surrounding text
                start = text_lower.find(keyword)
                end = min(start + 500, len(text))
                return text[start:end].strip()

        return None

    def _extract_location(self, text: str) -> Optional[str]:
        """Extract location from text."""
        # Indian states and cities
        locations = [
            'delhi', 'mumbai', 'bangalore', 'chennai', 'kolkata', 'hyderabad',
            'pune', 'ahmedabad', 'surat', 'jaipur', 'lucknow', 'kanpur',
            'nagpur', 'patna', 'indore', 'thane', 'bhopal', 'visakhapatnam',
            'kerala', 'tamil nadu', 'karnataka', 'maharashtra', 'gujarat',
            'rajasthan', 'west bengal', 'andhra pradesh', 'telangana',
            'madhya pradesh', 'uttar pradesh', 'bihar', 'odisha'
        ]

        text_lower = text.lower()
        for location in locations:
            if location in text_lower:
                return location.title()

        return None

    def _extract_application_process(self, text: str) -> Optional[str]:
        """Extract application process from text."""
        text_lower = text.lower()

        process_keywords = [
            'how to apply', 'application process', 'apply online',
            'submit application', 'application procedure'
        ]

        for keyword in process_keywords:
            if keyword in text_lower:
                start = text_lower.find(keyword)
                end = min(start + 300, len(text))
                return text[start:end].strip()

        return None
