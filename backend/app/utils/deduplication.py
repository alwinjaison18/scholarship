"""
Deduplication utility for detecting duplicate scholarships.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass
from datetime import datetime
import re
import difflib
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


@dataclass
class DuplicationResult:
    """Result of duplication detection."""
    is_duplicate: bool
    similarity_score: float
    matching_fields: List[str]
    confidence: float
    reasons: List[str]


class DuplicationDetector:
    """Utility class for detecting duplicate scholarships."""

    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold
        self.field_weights = self._init_field_weights()
        self.stop_words = self._init_stop_words()

    def _init_field_weights(self) -> Dict[str, float]:
        """Initialize field weights for comparison."""
        return {
            'title': 0.3,
            'url': 0.25,
            'description': 0.2,
            'amount': 0.1,
            'deadline': 0.05,
            'category': 0.05,
            'eligibility': 0.05
        }

    def _init_stop_words(self) -> Set[str]:
        """Initialize stop words for text comparison."""
        return {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
            'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'shall', 'this', 'that',
            'these', 'those', 'scholarship', 'award', 'grant', 'fellowship'
        }

    def are_duplicates(
        self,
        scholarship1: Dict[str, Any],
        scholarship2: Dict[str, Any]
    ) -> bool:
        """
        Check if two scholarships are duplicates.

        Args:
            scholarship1: First scholarship data
            scholarship2: Second scholarship data

        Returns:
            True if scholarships are duplicates
        """
        result = self.detect_duplication(scholarship1, scholarship2)
        return result.is_duplicate

    def detect_duplication(
        self,
        scholarship1: Dict[str, Any],
        scholarship2: Dict[str, Any]
    ) -> DuplicationResult:
        """
        Detect duplication between two scholarships.

        Args:
            scholarship1: First scholarship data
            scholarship2: Second scholarship data

        Returns:
            DuplicationResult with detailed analysis
        """
        if not scholarship1 or not scholarship2:
            return DuplicationResult(
                is_duplicate=False,
                similarity_score=0.0,
                matching_fields=[],
                confidence=0.0,
                reasons=["Missing scholarship data"]
            )

        # Calculate similarity for each field
        field_similarities = {}
        matching_fields = []
        reasons = []

        # URL comparison (exact match)
        url1 = scholarship1.get('url', '')
        url2 = scholarship2.get('url', '')
        if url1 and url2:
            if self._normalize_url(url1) == self._normalize_url(url2):
                field_similarities['url'] = 1.0
                matching_fields.append('url')
                reasons.append("Exact URL match")
            else:
                field_similarities['url'] = 0.0

        # Title comparison
        title1 = scholarship1.get('title', '')
        title2 = scholarship2.get('title', '')
        if title1 and title2:
            title_sim = self._calculate_text_similarity(title1, title2)
            field_similarities['title'] = title_sim
            if title_sim > 0.8:
                matching_fields.append('title')
                reasons.append(f"High title similarity: {title_sim:.2f}")

        # Description comparison
        desc1 = scholarship1.get('description', '')
        desc2 = scholarship2.get('description', '')
        if desc1 and desc2:
            desc_sim = self._calculate_text_similarity(desc1, desc2)
            field_similarities['description'] = desc_sim
            if desc_sim > 0.7:
                matching_fields.append('description')
                reasons.append(f"High description similarity: {desc_sim:.2f}")

        # Amount comparison
        amount1 = scholarship1.get('amount')
        amount2 = scholarship2.get('amount')
        if amount1 and amount2:
            amount_sim = self._compare_amounts(amount1, amount2)
            field_similarities['amount'] = amount_sim
            if amount_sim > 0.9:
                matching_fields.append('amount')
                reasons.append("Similar amounts")

        # Deadline comparison
        deadline1 = scholarship1.get('deadline')
        deadline2 = scholarship2.get('deadline')
        if deadline1 and deadline2:
            deadline_sim = self._compare_dates(deadline1, deadline2)
            field_similarities['deadline'] = deadline_sim
            if deadline_sim > 0.8:
                matching_fields.append('deadline')
                reasons.append("Similar deadlines")

        # Category comparison
        category1 = scholarship1.get('category', '')
        category2 = scholarship2.get('category', '')
        if category1 and category2:
            category_sim = self._calculate_text_similarity(
                category1, category2)
            field_similarities['category'] = category_sim
            if category_sim > 0.7:
                matching_fields.append('category')
                reasons.append("Similar categories")

        # Eligibility comparison
        eligibility1 = scholarship1.get('eligibility', '')
        eligibility2 = scholarship2.get('eligibility', '')
        if eligibility1 and eligibility2:
            eligibility_sim = self._calculate_text_similarity(
                eligibility1, eligibility2)
            field_similarities['eligibility'] = eligibility_sim
            if eligibility_sim > 0.6:
                matching_fields.append('eligibility')
                reasons.append("Similar eligibility criteria")

        # Calculate overall similarity score
        overall_similarity = self._calculate_overall_similarity(
            field_similarities)

        # Determine if duplicate
        is_duplicate = overall_similarity >= self.similarity_threshold

        # Calculate confidence
        confidence = self._calculate_confidence(
            field_similarities, matching_fields)

        return DuplicationResult(
            is_duplicate=is_duplicate,
            similarity_score=overall_similarity,
            matching_fields=matching_fields,
            confidence=confidence,
            reasons=reasons
        )

    def _normalize_url(self, url: str) -> str:
        """Normalize URL for comparison."""
        if not url:
            return ""

        # Parse URL
        parsed = urlparse(url.lower())

        # Remove www and common prefixes
        netloc = parsed.netloc
        if netloc.startswith('www.'):
            netloc = netloc[4:]

        # Remove common tracking parameters
        path = parsed.path.rstrip('/')

        return f"{parsed.scheme}://{netloc}{path}"

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings."""
        if not text1 or not text2:
            return 0.0

        # Normalize texts
        norm_text1 = self._normalize_text(text1)
        norm_text2 = self._normalize_text(text2)

        if not norm_text1 or not norm_text2:
            return 0.0

        # Use difflib for similarity calculation
        similarity = difflib.SequenceMatcher(
            None, norm_text1, norm_text2).ratio()

        return similarity

    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        if not text:
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove punctuation and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        # Remove stop words
        words = text.split()
        words = [word for word in words if word not in self.stop_words]

        return ' '.join(words)

    def _compare_amounts(self, amount1: Any, amount2: Any) -> float:
        """Compare two amounts."""
        try:
            amt1 = float(amount1) if amount1 else 0
            amt2 = float(amount2) if amount2 else 0

            if amt1 == 0 and amt2 == 0:
                return 1.0

            if amt1 == 0 or amt2 == 0:
                return 0.0

            # Calculate relative difference
            diff = abs(amt1 - amt2)
            avg = (amt1 + amt2) / 2

            if avg == 0:
                return 1.0

            relative_diff = diff / avg

            # Convert to similarity score (0-1)
            similarity = max(0.0, 1.0 - relative_diff)

            return similarity

        except (ValueError, TypeError):
            return 0.0

    def _compare_dates(self, date1: Any, date2: Any) -> float:
        """Compare two dates."""
        try:
            # Convert to datetime if needed
            if isinstance(date1, str):
                date1 = datetime.fromisoformat(date1.replace('Z', '+00:00'))
            if isinstance(date2, str):
                date2 = datetime.fromisoformat(date2.replace('Z', '+00:00'))

            if not isinstance(date1, datetime) or not isinstance(date2, datetime):
                return 0.0

            # Calculate difference in days
            diff_days = abs((date1 - date2).days)

            # Consider same if within 3 days
            if diff_days <= 3:
                return 1.0
            elif diff_days <= 7:
                return 0.8
            elif diff_days <= 14:
                return 0.6
            elif diff_days <= 30:
                return 0.4
            else:
                return 0.0

        except (ValueError, TypeError, AttributeError):
            return 0.0

    def _calculate_overall_similarity(self, field_similarities: Dict[str, float]) -> float:
        """Calculate overall similarity score using weighted average."""
        if not field_similarities:
            return 0.0

        total_weight = 0.0
        weighted_sum = 0.0

        for field, similarity in field_similarities.items():
            weight = self.field_weights.get(field, 0.1)
            weighted_sum += similarity * weight
            total_weight += weight

        if total_weight == 0:
            return 0.0

        return weighted_sum / total_weight

    def _calculate_confidence(
        self,
        field_similarities: Dict[str, float],
        matching_fields: List[str]
    ) -> float:
        """Calculate confidence score for the duplication result."""
        if not field_similarities:
            return 0.0

        # Base confidence on number of fields compared
        field_coverage = len(field_similarities) / len(self.field_weights)

        # Boost confidence if critical fields match
        critical_fields = ['url', 'title']
        critical_matches = sum(
            1 for field in critical_fields if field in matching_fields)
        critical_bonus = critical_matches / len(critical_fields)

        # Calculate overall confidence
        confidence = (field_coverage * 0.6) + (critical_bonus * 0.4)

        return min(1.0, confidence)

    def find_duplicates_in_batch(
        self,
        scholarships: List[Dict[str, Any]]
    ) -> List[Tuple[int, int, DuplicationResult]]:
        """
        Find duplicates in a batch of scholarships.

        Args:
            scholarships: List of scholarship data

        Returns:
            List of tuples (index1, index2, duplication_result)
        """
        duplicates = []

        for i in range(len(scholarships)):
            for j in range(i + 1, len(scholarships)):
                result = self.detect_duplication(
                    scholarships[i], scholarships[j])
                if result.is_duplicate:
                    duplicates.append((i, j, result))

        return duplicates

    def get_duplicate_groups(
        self,
        scholarships: List[Dict[str, Any]]
    ) -> List[List[int]]:
        """
        Group scholarships by duplicates.

        Args:
            scholarships: List of scholarship data

        Returns:
            List of groups, where each group is a list of indices
        """
        # Find all duplicate pairs
        duplicate_pairs = self.find_duplicates_in_batch(scholarships)

        # Build groups using union-find like approach
        groups = []
        index_to_group = {}

        for i, j, _ in duplicate_pairs:
            group_i = index_to_group.get(i)
            group_j = index_to_group.get(j)

            if group_i is None and group_j is None:
                # Create new group
                new_group = [i, j]
                groups.append(new_group)
                index_to_group[i] = len(groups) - 1
                index_to_group[j] = len(groups) - 1
            elif group_i is not None and group_j is None:
                # Add j to group i
                groups[group_i].append(j)
                index_to_group[j] = group_i
            elif group_i is None and group_j is not None:
                # Add i to group j
                groups[group_j].append(i)
                index_to_group[i] = group_j
            elif group_i != group_j:
                # Merge groups
                group_to_merge = groups[group_j]
                groups[group_i].extend(group_to_merge)

                # Update index mapping
                for idx in group_to_merge:
                    index_to_group[idx] = group_i

                # Remove merged group
                groups[group_j] = []

        # Remove empty groups
        groups = [group for group in groups if group]

        return groups

    def deduplicate_scholarships(
        self,
        scholarships: List[Dict[str, Any]],
        keep_strategy: str = 'first'
    ) -> List[Dict[str, Any]]:
        """
        Remove duplicates from a list of scholarships.

        Args:
            scholarships: List of scholarship data
            keep_strategy: Strategy for keeping duplicates ('first', 'last', 'best')

        Returns:
            List of deduplicated scholarships
        """
        if not scholarships:
            return []

        # Get duplicate groups
        duplicate_groups = self.get_duplicate_groups(scholarships)

        # Determine which scholarships to keep
        indices_to_remove = set()

        for group in duplicate_groups:
            if len(group) <= 1:
                continue

            if keep_strategy == 'first':
                # Keep the first one, remove others
                indices_to_remove.update(group[1:])
            elif keep_strategy == 'last':
                # Keep the last one, remove others
                indices_to_remove.update(group[:-1])
            elif keep_strategy == 'best':
                # Keep the one with highest quality score
                best_idx = group[0]
                best_score = scholarships[best_idx].get('quality_score', 0)

                for idx in group[1:]:
                    score = scholarships[idx].get('quality_score', 0)
                    if score > best_score:
                        best_idx = idx
                        best_score = score

                # Remove all except the best
                for idx in group:
                    if idx != best_idx:
                        indices_to_remove.add(idx)

        # Return scholarships without duplicates
        return [
            scholarship for i, scholarship in enumerate(scholarships)
            if i not in indices_to_remove
        ]

    def calculate_deduplication_stats(
        self,
        original_count: int,
        deduplicated_count: int,
        duplicate_groups: List[List[int]]
    ) -> Dict[str, Any]:
        """
        Calculate deduplication statistics.

        Args:
            original_count: Original number of scholarships
            deduplicated_count: Number after deduplication
            duplicate_groups: List of duplicate groups

        Returns:
            Dict with deduplication stats
        """
        removed_count = original_count - deduplicated_count
        duplicate_pairs = sum(
            len(group) - 1 for group in duplicate_groups if len(group) > 1)

        return {
            'original_count': original_count,
            'deduplicated_count': deduplicated_count,
            'removed_count': removed_count,
            'duplicate_groups': len(duplicate_groups),
            'duplicate_pairs': duplicate_pairs,
            'deduplication_rate': (removed_count / original_count) * 100 if original_count > 0 else 0
        }
