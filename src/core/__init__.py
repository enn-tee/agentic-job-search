"""Core abstractions and interfaces."""

from .adapters import IndustryAdapter, HealthcareAdapter, TechAdapter
from .services import (
    TerminologyService,
    JobSource,
    KeywordOptimizer,
    SkillTaxonomy,
)

__all__ = [
    "IndustryAdapter",
    "HealthcareAdapter",
    "TechAdapter",
    "TerminologyService",
    "JobSource",
    "KeywordOptimizer",
    "SkillTaxonomy",
]
