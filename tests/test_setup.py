"""Basic setup tests to verify the system is configured correctly."""

import pytest
from pathlib import Path
import yaml


def test_project_structure():
    """Test that all required directories exist."""
    required_dirs = [
        "src/agents",
        "src/core",
        "src/models",
        "src/services",
        "config/industries",
        "resume_pool/base_resumes",
        "resume_pool/tailored_resumes",
        "resume_pool/metadata",
    ]

    for dir_path in required_dirs:
        assert Path(dir_path).exists(), f"Missing directory: {dir_path}"


def test_healthcare_config_loads():
    """Test that healthcare industry config loads correctly."""
    config_file = Path("config/industries/healthcare.yaml")
    assert config_file.exists(), "Healthcare config file not found"

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    # Check required fields
    assert config["industry"] == "healthcare"
    assert "display_name" in config
    assert "terminology" in config
    assert "skill_categories" in config
    assert "keyword_optimization" in config

    # Check acronyms
    assert "EHR" in config["terminology"]["acronyms"]
    assert "HIPAA" in config["terminology"]["acronyms"]
    assert "FHIR" in config["terminology"]["acronyms"]


def test_tech_config_loads():
    """Test that tech industry config loads correctly."""
    config_file = Path("config/industries/tech.yaml")
    assert config_file.exists(), "Tech config file not found"

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    assert config["industry"] == "tech"
    assert "skill_categories" in config


def test_example_resume_exists():
    """Test that example resume file exists."""
    example_resume = Path("resume_pool/base_resumes/example_resume.json")
    assert example_resume.exists(), "Example resume not found"


def test_sample_job_posting_exists():
    """Test that sample job posting exists."""
    sample_job = Path("examples/sample_job_posting.txt")
    assert sample_job.exists(), "Sample job posting not found"


def test_imports():
    """Test that all core modules can be imported."""
    # Models
    from src.models import JobPosting, JobAnalysis, Resume, ResumeMetadata

    # Core
    from src.core import IndustryAdapter

    # Agents
    from src.agents import (
        JobAnalyzerAgent,
        ResumeMatcherAgent,
        TailoringOrchestratorAgent,
        QualityReviewerAgent,
    )

    # Services
    from src.services import StaticTerminologyService, ConfigBasedKeywordOptimizer

    # If we get here, all imports worked
    assert True


def test_industry_adapter_creation():
    """Test that industry adapters can be created."""
    from src.core.adapters import IndustryAdapter

    config_dir = Path("config/industries")

    # Test healthcare adapter
    healthcare_adapter = IndustryAdapter.create("healthcare", config_dir)
    assert healthcare_adapter is not None
    assert healthcare_adapter.config.industry == "healthcare"

    # Test tech adapter
    tech_adapter = IndustryAdapter.create("tech", config_dir)
    assert tech_adapter is not None
    assert tech_adapter.config.industry == "tech"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
