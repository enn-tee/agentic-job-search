"""Skill taxonomy service implementations."""

from typing import List, Dict, Optional
from ..core.services import SkillTaxonomy
from ..models.industry import IndustryConfig


class ConfigBasedSkillTaxonomy(SkillTaxonomy):
    """Skill taxonomy using industry configuration."""

    def __init__(self, config: IndustryConfig):
        """
        Initialize with industry configuration.

        Args:
            config: Industry configuration
        """
        self.config = config
        self._build_skill_index()

    def _build_skill_index(self):
        """Build reverse index from skill to category."""
        self._skill_to_category = {}
        for category_name, category in self.config.skill_categories.items():
            for skill in category.skills:
                # Store in lowercase for case-insensitive lookup
                self._skill_to_category[skill.lower()] = category_name

    def get_skill_categories(self) -> Dict[str, List[str]]:
        """
        Get skills organized by category.

        Returns:
            Dictionary mapping category names to lists of skills
        """
        result = {}
        for category_name, category in self.config.skill_categories.items():
            result[category_name] = category.skills.copy()
        return result

    def get_related_skills(self, skill: str) -> List[str]:
        """
        Get skills related to the given skill.

        Related skills are those in the same category.

        Args:
            skill: Skill name

        Returns:
            List of related skills (from same category)
        """
        category = self.categorize_skill(skill)
        if not category:
            return []

        category_obj = self.config.skill_categories.get(category)
        if not category_obj:
            return []

        # Return all skills in same category except the input skill
        return [s for s in category_obj.skills if s.lower() != skill.lower()]

    def get_high_priority_skills(self) -> List[str]:
        """
        Get high-priority skills for this industry.

        Returns:
            List of high-priority skills
        """
        return self.config.get_high_priority_skills()

    def categorize_skill(self, skill: str) -> Optional[str]:
        """
        Determine which category a skill belongs to.

        Args:
            skill: Skill name

        Returns:
            Category name or None if not found
        """
        return self._skill_to_category.get(skill.lower())

    def get_category_priority(self, category: str) -> str:
        """
        Get the priority level of a skill category.

        Args:
            category: Category name

        Returns:
            Priority level ("high", "medium", "low")
        """
        category_obj = self.config.skill_categories.get(category)
        if category_obj:
            return category_obj.priority
        return "low"

    def is_high_priority_skill(self, skill: str) -> bool:
        """
        Check if a skill is high priority.

        Args:
            skill: Skill name

        Returns:
            True if skill is in a high-priority category
        """
        category = self.categorize_skill(skill)
        if not category:
            return False
        return self.get_category_priority(category) == "high"
