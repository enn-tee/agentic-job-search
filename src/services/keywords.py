"""Keyword optimization service implementations."""

from typing import List
from ..core.services import KeywordOptimizer
from ..models.industry import IndustryConfig


class ConfigBasedKeywordOptimizer(KeywordOptimizer):
    """Keyword optimizer using industry configuration."""

    def __init__(self, config: IndustryConfig):
        """
        Initialize with industry configuration.

        Args:
            config: Industry configuration
        """
        self.config = config

    def get_priority_keywords(self) -> List[str]:
        """Get high-priority keywords for this industry."""
        return self.config.priority_keywords.copy()

    def suggest_keywords(
        self, job_description: str, current_resume: str
    ) -> List[str]:
        """
        Suggest keywords to add based on job description.

        This is a basic implementation. Agents will use LLMs for
        more sophisticated keyword extraction and matching.

        Args:
            job_description: Full job description text
            current_resume: Current resume text

        Returns:
            List of suggested keywords to integrate
        """
        suggested = []
        job_lower = job_description.lower()
        resume_lower = current_resume.lower()

        # Check priority keywords
        for keyword in self.config.priority_keywords:
            if keyword.lower() in job_lower and keyword.lower() not in resume_lower:
                suggested.append(keyword)

        # Check common terms
        for term in self.config.common_terms:
            if term.lower() in job_lower and term.lower() not in resume_lower:
                suggested.append(term)

        return suggested

    def get_action_verbs(self) -> List[str]:
        """Get industry-appropriate action verbs."""
        return self.config.action_verbs.copy()

    def get_metric_templates(self) -> List[str]:
        """Get templates for impactful metrics."""
        return self.config.impactful_metrics.copy()


class HealthcareKeywordOptimizer(ConfigBasedKeywordOptimizer):
    """Healthcare-specific keyword optimizer with additional logic."""

    def get_priority_keywords(self) -> List[str]:
        """
        Get high-priority healthcare keywords.

        Extends base implementation with healthcare-specific prioritization.
        """
        keywords = super().get_priority_keywords()

        # Add expanded acronyms as keywords too
        for acronym, expansion in self.config.acronyms.items():
            if acronym not in keywords:
                keywords.append(acronym)

        return keywords

    def suggest_keywords(
        self, job_description: str, current_resume: str
    ) -> List[str]:
        """
        Suggest healthcare keywords with emphasis on clinical terms.

        Args:
            job_description: Full job description text
            current_resume: Current resume text

        Returns:
            List of suggested keywords prioritizing clinical terms
        """
        suggested = super().suggest_keywords(job_description, current_resume)

        # Add acronym suggestions
        job_lower = job_description.lower()
        resume_lower = current_resume.lower()

        for acronym in self.config.acronyms.keys():
            if acronym.lower() in job_lower and acronym.lower() not in resume_lower:
                if acronym not in suggested:
                    suggested.append(acronym)

        return suggested
