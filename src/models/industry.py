"""Industry configuration data models."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import yaml
from pathlib import Path


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server."""

    name: str
    package: str
    description: str
    use_case: str
    priority: str  # "required", "recommended", "optional"
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JobBoard:
    """Job board configuration."""

    name: str
    url: str
    type: str = "general"  # "general" or "specialized"
    description: Optional[str] = None
    filters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SkillCategory:
    """A category of skills with priority."""

    name: str
    priority: str  # "high", "medium", "low"
    skills: List[str] = field(default_factory=list)


@dataclass
class IndustryConfig:
    """Configuration for an industry."""

    industry: str
    display_name: str
    description: str

    # MCP configuration
    mcp_enabled: bool = False
    mcp_servers: List[MCPServerConfig] = field(default_factory=list)

    # Job sources
    job_boards: List[JobBoard] = field(default_factory=list)

    # Terminology
    acronyms: Dict[str, str] = field(default_factory=dict)
    common_terms: List[str] = field(default_factory=list)

    # Skills
    skill_categories: Dict[str, SkillCategory] = field(default_factory=dict)

    # Keywords for ATS
    priority_keywords: List[str] = field(default_factory=list)
    action_verbs: List[str] = field(default_factory=list)
    impactful_metrics: List[str] = field(default_factory=list)

    # Certifications
    highly_valued_certs: Dict[str, str] = field(default_factory=dict)
    nice_to_have_certs: Dict[str, str] = field(default_factory=dict)

    # Role titles
    primary_roles: List[str] = field(default_factory=list)
    related_roles: List[str] = field(default_factory=list)

    # Resume tips
    resume_tips: Dict[str, List[str]] = field(default_factory=dict)

    @classmethod
    def load_from_yaml(cls, file_path: Path) -> "IndustryConfig":
        """Load industry configuration from YAML file."""
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)

        # Parse MCP servers
        mcp_servers = []
        mcp_config = data.get("mcp_servers", {})
        mcp_enabled = mcp_config.get("enabled", False)

        if "servers" in mcp_config:
            for server_data in mcp_config["servers"]:
                mcp_servers.append(MCPServerConfig(**server_data))

        # Parse job boards
        job_boards = []
        for board_data in data.get("job_boards", []):
            job_boards.append(JobBoard(**board_data))

        # Parse skill categories
        skill_categories = {}
        for cat_name, cat_data in data.get("skill_categories", {}).items():
            skill_categories[cat_name] = SkillCategory(
                name=cat_name,
                priority=cat_data.get("priority", "medium"),
                skills=cat_data.get("skills", []),
            )

        # Parse terminology
        terminology = data.get("terminology", {})
        acronyms = terminology.get("acronyms", {})
        common_terms = terminology.get("common_terms", [])

        # Parse keyword optimization
        keyword_opt = data.get("keyword_optimization", {})
        priority_keywords = keyword_opt.get("priority_keywords", [])
        action_verbs = keyword_opt.get("action_verbs", [])
        impactful_metrics = keyword_opt.get("impactful_metrics", [])

        # Parse certifications
        certs = data.get("certifications", {})
        highly_valued = certs.get("highly_valued", {})
        nice_to_have = certs.get("nice_to_have", {})

        # Parse role titles
        role_titles = data.get("role_titles", {})
        primary_roles = role_titles.get("primary", [])
        related_roles = role_titles.get("related", [])

        # Parse resume tips
        resume_tips = data.get("resume_tips", {})

        return cls(
            industry=data["industry"],
            display_name=data["display_name"],
            description=data.get("description", ""),
            mcp_enabled=mcp_enabled,
            mcp_servers=mcp_servers,
            job_boards=job_boards,
            acronyms=acronyms,
            common_terms=common_terms,
            skill_categories=skill_categories,
            priority_keywords=priority_keywords,
            action_verbs=action_verbs,
            impactful_metrics=impactful_metrics,
            highly_valued_certs=highly_valued,
            nice_to_have_certs=nice_to_have,
            primary_roles=primary_roles,
            related_roles=related_roles,
            resume_tips=resume_tips,
        )

    def get_all_skills(self) -> List[str]:
        """Get all skills across all categories."""
        all_skills = []
        for category in self.skill_categories.values():
            all_skills.extend(category.skills)
        return all_skills

    def get_high_priority_skills(self) -> List[str]:
        """Get only high-priority skills."""
        high_priority = []
        for category in self.skill_categories.values():
            if category.priority == "high":
                high_priority.extend(category.skills)
        return high_priority

    def expand_acronym(self, acronym: str) -> Optional[str]:
        """Expand an acronym to its full form."""
        return self.acronyms.get(acronym.upper())
