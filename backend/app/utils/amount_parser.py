"""
Amount parser utility for extracting and normalizing monetary amounts.
"""

import re
import logging
from typing import Optional, Dict, Any, Tuple, List
from decimal import Decimal

logger = logging.getLogger(__name__)


class AmountParser:
    """Utility class for parsing monetary amounts from text."""

    def __init__(self):
        self.currency_patterns = self._init_currency_patterns()
        self.word_to_number = self._init_word_to_number()

    def _init_currency_patterns(self) -> Dict[str, str]:
        """Initialize currency patterns."""
        return {
            'rupees': r'(?:₹|rs\.?|rupees?|inr)\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            'lakhs': r'(\d+(?:\.\d+)?)\s*(?:lakh|lac)s?',
            'crores': r'(\d+(?:\.\d+)?)\s*crores?',
            'thousands': r'(\d+(?:\.\d+)?)\s*(?:thousand|k)',
            'numeric': r'(\d+(?:,\d+)*(?:\.\d+)?)',
            'words': r'(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|lakh|lac|crore)'
        }

    def _init_word_to_number(self) -> Dict[str, int]:
        """Initialize word to number mapping."""
        return {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
            'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
            'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40,
            'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80,
            'ninety': 90, 'hundred': 100, 'thousand': 1000,
            'lakh': 100000, 'lac': 100000, 'crore': 10000000
        }

    def parse_amount(self, text: str) -> Optional[float]:
        """
        Parse monetary amount from text.

        Args:
            text: Text containing monetary amount

        Returns:
            Parsed amount as float or None if not found
        """
        if not text:
            return None

        text = text.lower().strip()

        # Try different parsing strategies
        strategies = [
            self._parse_structured_amount,
            self._parse_word_amount,
            self._parse_numeric_amount,
            self._parse_range_amount
        ]

        for strategy in strategies:
            try:
                amount = strategy(text)
                if amount is not None:
                    return float(amount)
            except Exception as e:
                logger.debug(f"Amount parsing strategy failed: {str(e)}")
                continue

        return None

    def _parse_structured_amount(self, text: str) -> Optional[Decimal]:
        """Parse structured amount with currency symbols."""
        # Look for rupee amounts
        rupee_pattern = self.currency_patterns['rupees']
        match = re.search(rupee_pattern, text, re.IGNORECASE)

        if match:
            amount_str = match.group(1).replace(',', '')
            return Decimal(amount_str)

        return None

    def _parse_word_amount(self, text: str) -> Optional[Decimal]:
        """Parse amount expressed in words."""
        # Look for patterns like "five lakh", "ten thousand", etc.
        patterns = [
            r'(\w+)\s+lakh',
            r'(\w+)\s+crore',
            r'(\w+)\s+thousand',
            r'(\w+)\s+hundred'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                word = match.lower()
                if word in self.word_to_number:
                    base_value = self.word_to_number[word]

                    # Determine multiplier
                    if 'lakh' in text:
                        return Decimal(base_value * 100000)
                    elif 'crore' in text:
                        return Decimal(base_value * 10000000)
                    elif 'thousand' in text:
                        return Decimal(base_value * 1000)
                    elif 'hundred' in text:
                        return Decimal(base_value * 100)

        return None

    def _parse_numeric_amount(self, text: str) -> Optional[Decimal]:
        """Parse numeric amount with multipliers."""
        # Look for patterns like "5 lakh", "10 crore", etc.
        lakh_pattern = self.currency_patterns['lakhs']
        crore_pattern = self.currency_patterns['crores']
        thousand_pattern = self.currency_patterns['thousands']

        # Check for crores
        match = re.search(crore_pattern, text, re.IGNORECASE)
        if match:
            amount = Decimal(match.group(1))
            return amount * 10000000

        # Check for lakhs
        match = re.search(lakh_pattern, text, re.IGNORECASE)
        if match:
            amount = Decimal(match.group(1))
            return amount * 100000

        # Check for thousands
        match = re.search(thousand_pattern, text, re.IGNORECASE)
        if match:
            amount = Decimal(match.group(1))
            return amount * 1000

        # Check for plain numbers
        numeric_pattern = self.currency_patterns['numeric']
        match = re.search(numeric_pattern, text)
        if match:
            amount_str = match.group(1).replace(',', '')
            return Decimal(amount_str)

        return None

    def _parse_range_amount(self, text: str) -> Optional[Decimal]:
        """Parse amount ranges and return the maximum."""
        # Look for patterns like "5000 to 10000", "Rs. 1000 - 5000", etc.
        range_patterns = [
            r'(\d+(?:,\d+)*)\s*(?:to|-)\s*(\d+(?:,\d+)*)',
            r'between\s+(\d+(?:,\d+)*)\s+and\s+(\d+(?:,\d+)*)',
            r'from\s+(\d+(?:,\d+)*)\s+to\s+(\d+(?:,\d+)*)'
        ]

        for pattern in range_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                min_amount = Decimal(match.group(1).replace(',', ''))
                max_amount = Decimal(match.group(2).replace(',', ''))
                return max_amount  # Return the maximum amount

        return None

    def parse_amount_details(self, text: str) -> Dict[str, Any]:
        """
        Parse amount with additional details.

        Args:
            text: Text containing monetary amount

        Returns:
            Dict with amount details
        """
        result = {
            'amount': None,
            'currency': 'INR',
            'type': 'unknown',
            'confidence': 0.0,
            'raw_text': text
        }

        if not text:
            return result

        # Parse amount
        amount = self.parse_amount(text)
        if amount is not None:
            result['amount'] = amount
            result['confidence'] = 0.8

        # Determine amount type
        text_lower = text.lower()
        if any(word in text_lower for word in ['scholarship', 'award', 'grant']):
            result['type'] = 'scholarship'
        elif any(word in text_lower for word in ['stipend', 'monthly', 'per month']):
            result['type'] = 'stipend'
        elif any(word in text_lower for word in ['fee', 'tuition', 'cost']):
            result['type'] = 'fee'
        elif any(word in text_lower for word in ['prize', 'reward', 'cash']):
            result['type'] = 'prize'

        # Check for frequency
        if any(word in text_lower for word in ['monthly', 'per month', '/month']):
            result['frequency'] = 'monthly'
        elif any(word in text_lower for word in ['yearly', 'per year', '/year', 'annual']):
            result['frequency'] = 'yearly'
        elif any(word in text_lower for word in ['one time', 'lump sum', 'single']):
            result['frequency'] = 'one_time'

        return result

    def normalize_amount(self, amount: float) -> str:
        """
        Normalize amount to Indian currency format.

        Args:
            amount: Amount to normalize

        Returns:
            Formatted amount string
        """
        if amount is None:
            return "N/A"

        if amount >= 10000000:  # 1 crore
            crores = amount / 10000000
            return f"₹{crores:.2f} crore"
        elif amount >= 100000:  # 1 lakh
            lakhs = amount / 100000
            return f"₹{lakhs:.2f} lakh"
        elif amount >= 1000:  # 1 thousand
            thousands = amount / 1000
            return f"₹{thousands:.2f} thousand"
        else:
            return f"₹{amount:,.2f}"

    def extract_all_amounts(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract all monetary amounts from text.

        Args:
            text: Text to extract amounts from

        Returns:
            List of amount details
        """
        amounts = []

        # Split text into sentences
        sentences = re.split(r'[.!?;]', text)

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            amount_details = self.parse_amount_details(sentence)
            if amount_details['amount'] is not None:
                amounts.append(amount_details)

        return amounts

    def compare_amounts(self, amount1: str, amount2: str) -> Dict[str, Any]:
        """
        Compare two amount strings.

        Args:
            amount1: First amount string
            amount2: Second amount string

        Returns:
            Dict with comparison results
        """
        parsed1 = self.parse_amount(amount1)
        parsed2 = self.parse_amount(amount2)

        result = {
            'amount1': parsed1,
            'amount2': parsed2,
            'comparison': None,
            'difference': None,
            'percentage_difference': None
        }

        if parsed1 is not None and parsed2 is not None:
            if parsed1 > parsed2:
                result['comparison'] = 'amount1_greater'
            elif parsed1 < parsed2:
                result['comparison'] = 'amount2_greater'
            else:
                result['comparison'] = 'equal'

            result['difference'] = abs(parsed1 - parsed2)

            if parsed2 != 0:
                result['percentage_difference'] = (
                    abs(parsed1 - parsed2) / parsed2) * 100

        return result

    def validate_amount(self, amount: float) -> Tuple[bool, List[str]]:
        """
        Validate if an amount is reasonable for a scholarship.

        Args:
            amount: Amount to validate

        Returns:
            Tuple of (is_valid, issues)
        """
        is_valid = True
        issues = []

        if amount is None:
            return False, ["Amount is None"]

        if amount <= 0:
            is_valid = False
            issues.append("Amount must be positive")

        if amount > 50000000:  # 5 crores
            is_valid = False
            issues.append("Amount seems unrealistically high")

        if amount < 100:
            is_valid = False
            issues.append("Amount seems unrealistically low")

        return is_valid, issues
