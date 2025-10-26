"""Terminology service implementations."""

from typing import List, Optional
from ..core.services import TerminologyService
from ..models.industry import IndustryConfig


class StaticTerminologyService(TerminologyService):
    """Terminology service using static configuration."""

    def __init__(self, config: IndustryConfig):
        """
        Initialize with industry configuration.

        Args:
            config: Industry configuration containing terminology
        """
        self.config = config
        self._all_skills = set(config.get_all_skills())

    def expand_acronym(self, acronym: str) -> Optional[str]:
        """
        Expand an acronym to its full form.

        Args:
            acronym: Acronym to expand (e.g., "EHR")

        Returns:
            Full form of acronym or None if not found
        """
        return self.config.acronyms.get(acronym.upper())

    def get_common_terms(self) -> List[str]:
        """
        Get common industry terms.

        Returns:
            List of common terms for this industry
        """
        return self.config.common_terms

    def validate_skill(self, skill: str) -> bool:
        """
        Check if a skill is recognized in this industry.

        Args:
            skill: Skill name to validate

        Returns:
            True if skill is recognized in this industry
        """
        # Case-insensitive check
        skill_lower = skill.lower()
        return any(s.lower() == skill_lower for s in self._all_skills)

    def get_all_acronyms(self) -> dict[str, str]:
        """Get all acronyms and their expansions."""
        return self.config.acronyms.copy()
