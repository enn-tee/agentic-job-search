"""Industry adapter implementations."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from pathlib import Path

from .services import TerminologyService, JobSource, KeywordOptimizer, SkillTaxonomy
from ..models.industry import IndustryConfig


class IndustryAdapter(ABC):
    """Base class for industry-specific adapters."""

    def __init__(self, config: IndustryConfig, mcp_enabled: bool = False):
        """
        Initialize the industry adapter.

        Args:
            config: Industry configuration
            mcp_enabled: Whether to use MCP servers (if available)
        """
        self.config = config
        self.mcp_enabled = mcp_enabled and config.mcp_enabled

    @abstractmethod
    def get_terminology_service(self) -> TerminologyService:
        """Returns industry-specific terminology lookup."""
        pass

    @abstractmethod
    def get_job_sources(self) -> List[JobSource]:
        """Returns industry-specific job boards/sources."""
        pass

    @abstractmethod
    def get_keyword_optimizer(self) -> KeywordOptimizer:
        """Returns industry-specific keyword strategies."""
        pass

    @abstractmethod
    def get_skill_taxonomy(self) -> SkillTaxonomy:
        """Returns industry skill hierarchies."""
        pass

    @classmethod
    def create(
        cls, industry: str, config_dir: Path, mcp_enabled: bool = False
    ) -> "IndustryAdapter":
        """
        Factory method to create appropriate adapter for an industry.

        Args:
            industry: Industry name (e.g., "healthcare", "tech")
            config_dir: Directory containing industry YAML configs
            mcp_enabled: Whether to enable MCP servers

        Returns:
            Appropriate IndustryAdapter subclass instance
        """
        # Load configuration
        config_file = config_dir / f"{industry}.yaml"
        if not config_file.exists():
            raise ValueError(f"Configuration file not found: {config_file}")

        config = IndustryConfig.load_from_yaml(config_file)

        # Map industry to adapter class
        adapter_map = {
            "healthcare": HealthcareAdapter,
            "tech": TechAdapter,
        }

        adapter_class = adapter_map.get(industry, GenericAdapter)
        return adapter_class(config, mcp_enabled)


class GenericAdapter(IndustryAdapter):
    """Generic adapter that works with any industry config."""

    def get_terminology_service(self) -> TerminologyService:
        """Returns generic terminology service."""
        from ..services.terminology import StaticTerminologyService

        return StaticTerminologyService(self.config)

    def get_job_sources(self) -> List[JobSource]:
        """Returns generic job sources."""
        # Will implement basic web scraping job source
        return []

    def get_keyword_optimizer(self) -> KeywordOptimizer:
        """Returns generic keyword optimizer."""
        from ..services.keywords import ConfigBasedKeywordOptimizer

        return ConfigBasedKeywordOptimizer(self.config)

    def get_skill_taxonomy(self) -> SkillTaxonomy:
        """Returns generic skill taxonomy."""
        from ..services.skills import ConfigBasedSkillTaxonomy

        return ConfigBasedSkillTaxonomy(self.config)


class HealthcareAdapter(IndustryAdapter):
    """Adapter for healthcare industry with optional MCP support."""

    def get_terminology_service(self) -> TerminologyService:
        """Returns healthcare terminology service."""
        if self.mcp_enabled:
            # Check if OMOP MCP server is configured
            omop_server = next(
                (s for s in self.config.mcp_servers if s.name == "omop-terminology"),
                None,
            )
            if omop_server:
                # TODO: Implement MCP-based terminology service
                # from ..services.mcp.omop_terminology import MCPOMOPTerminologyService
                # return MCPOMOPTerminologyService(omop_server)
                pass

        # Fallback to static terminology
        from ..services.terminology import StaticTerminologyService

        return StaticTerminologyService(self.config)

    def get_job_sources(self) -> List[JobSource]:
        """Returns healthcare-specific job sources."""
        sources = []

        # Add healthcare-specific job boards
        # TODO: Implement job board scrapers
        # from ..services.job_sources import HealthcareJobBoardSource
        # sources.append(HealthcareJobBoardSource(self.config))

        if self.mcp_enabled:
            # Add Google Jobs MCP if configured
            google_jobs = next(
                (s for s in self.config.mcp_servers if s.name == "google-jobs"), None
            )
            if google_jobs:
                # TODO: Implement MCP-based job source
                # from ..services.mcp.google_jobs import MCPGoogleJobsSource
                # sources.append(MCPGoogleJobsSource(google_jobs, self.config))
                pass

        return sources

    def get_keyword_optimizer(self) -> KeywordOptimizer:
        """Returns healthcare-specific keyword optimizer."""
        from ..services.keywords import HealthcareKeywordOptimizer

        return HealthcareKeywordOptimizer(self.config)

    def get_skill_taxonomy(self) -> SkillTaxonomy:
        """Returns healthcare skill taxonomy."""
        from ..services.skills import ConfigBasedSkillTaxonomy

        return ConfigBasedSkillTaxonomy(self.config)


class TechAdapter(IndustryAdapter):
    """Adapter for technology industry."""

    def get_terminology_service(self) -> TerminologyService:
        """Returns tech terminology service."""
        from ..services.terminology import StaticTerminologyService

        return StaticTerminologyService(self.config)

    def get_job_sources(self) -> List[JobSource]:
        """Returns tech-specific job sources."""
        sources = []

        if self.mcp_enabled:
            google_jobs = next(
                (s for s in self.config.mcp_servers if s.name == "google-jobs"), None
            )
            if google_jobs:
                # TODO: Implement MCP-based job source
                pass

        return sources

    def get_keyword_optimizer(self) -> KeywordOptimizer:
        """Returns tech-specific keyword optimizer."""
        from ..services.keywords import ConfigBasedKeywordOptimizer

        return ConfigBasedKeywordOptimizer(self.config)

    def get_skill_taxonomy(self) -> SkillTaxonomy:
        """Returns tech skill taxonomy."""
        from ..services.skills import ConfigBasedSkillTaxonomy

        return ConfigBasedSkillTaxonomy(self.config)
