"""Core service interfaces."""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from ..models.job_posting import JobPosting


class TerminologyService(ABC):
    """Service for industry-specific terminology lookup and expansion."""

    @abstractmethod
    def expand_acronym(self, acronym: str) -> Optional[str]:
        """Expand an acronym to its full form."""
        pass

    @abstractmethod
    def get_common_terms(self) -> List[str]:
        """Get common industry terms."""
        pass

    @abstractmethod
    def validate_skill(self, skill: str) -> bool:
        """Check if a skill is recognized in this industry."""
        pass


class JobSource(ABC):
    """Interface for job posting sources."""

    @abstractmethod
    def search_jobs(
        self, keywords: List[str], location: Optional[str] = None, limit: int = 10
    ) -> List[JobPosting]:
        """Search for job postings."""
        pass

    @abstractmethod
    def fetch_job_details(self, url: str) -> JobPosting:
        """Fetch full details of a specific job posting."""
        pass


class KeywordOptimizer(ABC):
    """Service for optimizing resume keywords for ATS."""

    @abstractmethod
    def get_priority_keywords(self) -> List[str]:
        """Get high-priority keywords for this industry."""
        pass

    @abstractmethod
    def suggest_keywords(
        self, job_description: str, current_resume: str
    ) -> List[str]:
        """Suggest keywords to add based on job description."""
        pass

    @abstractmethod
    def get_action_verbs(self) -> List[str]:
        """Get industry-appropriate action verbs."""
        pass

    @abstractmethod
    def get_metric_templates(self) -> List[str]:
        """Get templates for impactful metrics."""
        pass


class SkillTaxonomy(ABC):
    """Service for understanding skill hierarchies and relationships."""

    @abstractmethod
    def get_skill_categories(self) -> Dict[str, List[str]]:
        """Get skills organized by category."""
        pass

    @abstractmethod
    def get_related_skills(self, skill: str) -> List[str]:
        """Get skills related to the given skill."""
        pass

    @abstractmethod
    def get_high_priority_skills(self) -> List[str]:
        """Get high-priority skills for this industry."""
        pass

    @abstractmethod
    def categorize_skill(self, skill: str) -> Optional[str]:
        """Determine which category a skill belongs to."""
        pass
