"""Job posting data models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class JobPosting:
    """Represents a job posting."""

    url: str
    company: str
    title: str
    description: str
    location: Optional[str] = None
    salary_range: Optional[str] = None
    posted_date: Optional[datetime] = None
    fetched_date: datetime = field(default_factory=datetime.now)
    raw_html: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "url": self.url,
            "company": self.company,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "salary_range": self.salary_range,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "fetched_date": self.fetched_date.isoformat(),
            "raw_html": self.raw_html,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "JobPosting":
        """Create from dictionary."""
        data = data.copy()
        if data.get("posted_date"):
            data["posted_date"] = datetime.fromisoformat(data["posted_date"])
        if data.get("fetched_date"):
            data["fetched_date"] = datetime.fromisoformat(data["fetched_date"])
        return cls(**data)


@dataclass
class JobAnalysis:
    """Analysis of a job posting."""

    job_posting: JobPosting

    # Extracted information
    role_type: str  # e.g., "Data Analyst", "Software Engineer"
    seniority: str  # e.g., "Entry", "Mid", "Senior", "Lead"
    industry: str  # e.g., "healthcare", "tech", "finance"

    # Skills and requirements
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    technical_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)

    # Keywords for ATS
    critical_keywords: List[str] = field(default_factory=list)
    secondary_keywords: List[str] = field(default_factory=list)

    # Education and certifications
    education_requirements: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)

    # Experience requirements
    years_experience: Optional[str] = None
    industry_experience: List[str] = field(default_factory=list)

    # Company culture indicators
    culture_keywords: List[str] = field(default_factory=list)
    values: List[str] = field(default_factory=list)

    # Responsibilities
    key_responsibilities: List[str] = field(default_factory=list)

    # Analysis metadata
    analysis_date: datetime = field(default_factory=datetime.now)
    confidence_score: float = 0.0  # 0.0 to 1.0

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "job_posting": self.job_posting.to_dict(),
            "role_type": self.role_type,
            "seniority": self.seniority,
            "industry": self.industry,
            "required_skills": self.required_skills,
            "preferred_skills": self.preferred_skills,
            "technical_skills": self.technical_skills,
            "soft_skills": self.soft_skills,
            "critical_keywords": self.critical_keywords,
            "secondary_keywords": self.secondary_keywords,
            "education_requirements": self.education_requirements,
            "certifications": self.certifications,
            "years_experience": self.years_experience,
            "industry_experience": self.industry_experience,
            "culture_keywords": self.culture_keywords,
            "values": self.values,
            "key_responsibilities": self.key_responsibilities,
            "analysis_date": self.analysis_date.isoformat(),
            "confidence_score": self.confidence_score,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "JobAnalysis":
        """Create from dictionary."""
        data = data.copy()
        data["job_posting"] = JobPosting.from_dict(data["job_posting"])
        if data.get("analysis_date"):
            data["analysis_date"] = datetime.fromisoformat(data["analysis_date"])
        return cls(**data)
