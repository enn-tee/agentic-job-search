"""Resume data models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any
from enum import Enum


class ResumeFormat(Enum):
    """Supported resume formats."""

    JSON = "json"
    MARKDOWN = "markdown"
    PDF = "pdf"
    DOCX = "docx"


@dataclass
class WorkExperience:
    """A single work experience entry."""

    company: str
    title: str
    start_date: str
    end_date: Optional[str] = None  # None if current
    location: Optional[str] = None
    bullets: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)


@dataclass
class Education:
    """An education entry."""

    institution: str
    degree: str
    field_of_study: Optional[str] = None
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None
    honors: List[str] = field(default_factory=list)


@dataclass
class Resume:
    """Represents a resume."""

    # Header
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None

    # Summary
    professional_summary: str = ""

    # Work experience
    experience: List[WorkExperience] = field(default_factory=list)

    # Education
    education: List[Education] = field(default_factory=list)

    # Skills
    technical_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)

    # Certifications
    certifications: List[str] = field(default_factory=list)

    # Projects (optional)
    projects: List[Dict[str, Any]] = field(default_factory=list)

    # Publications (optional)
    publications: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        # Helper to convert experience entries
        def exp_to_dict(exp):
            if isinstance(exp, dict):
                return exp
            return {
                "company": exp.company,
                "title": exp.title,
                "start_date": exp.start_date,
                "end_date": exp.end_date,
                "location": exp.location,
                "bullets": exp.bullets,
                "technologies": exp.technologies,
            }

        # Helper to convert education entries
        def edu_to_dict(edu):
            if isinstance(edu, dict):
                return edu
            return {
                "institution": edu.institution,
                "degree": edu.degree,
                "field_of_study": edu.field_of_study,
                "graduation_date": edu.graduation_date,
                "gpa": edu.gpa,
                "honors": edu.honors,
            }

        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "linkedin": self.linkedin,
            "github": self.github,
            "portfolio": self.portfolio,
            "professional_summary": self.professional_summary,
            "experience": [exp_to_dict(exp) for exp in self.experience],
            "education": [edu_to_dict(edu) for edu in self.education],
            "technical_skills": self.technical_skills,
            "soft_skills": self.soft_skills,
            "tools": self.tools,
            "languages": self.languages,
            "certifications": self.certifications,
            "projects": self.projects,
            "publications": self.publications,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Resume":
        """Create from dictionary."""
        data = data.copy()

        # Convert experience
        if "experience" in data:
            data["experience"] = [
                WorkExperience(**exp) for exp in data["experience"]
            ]

        # Convert education
        if "education" in data:
            data["education"] = [Education(**edu) for edu in data["education"]]

        return cls(**data)


@dataclass
class ResumeMetadata:
    """Metadata for a resume in the pool."""

    resume_id: str
    created_at: datetime
    base_resume_id: Optional[str] = None  # Parent resume if this is tailored

    # Job posting info (if tailored for a job)
    job_posting_url: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    archived_job_content: Optional[str] = None

    # Classification and search
    tags: List[str] = field(default_factory=list)
    summary: str = ""  # One-line description
    target_role: Optional[str] = None
    target_industry: Optional[str] = None
    key_skills_highlighted: List[str] = field(default_factory=list)

    # Quality metrics
    ats_optimized: bool = False
    match_score: Optional[float] = None  # 0.0 to 1.0

    # Modifications tracking
    modifications: Dict[str, Any] = field(default_factory=dict)

    # File info
    file_path: str = ""
    format: ResumeFormat = ResumeFormat.JSON

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "resume_id": self.resume_id,
            "created_at": self.created_at.isoformat(),
            "base_resume_id": self.base_resume_id,
            "job_posting_url": self.job_posting_url,
            "company": self.company,
            "job_title": self.job_title,
            "archived_job_content": self.archived_job_content,
            "tags": self.tags,
            "summary": self.summary,
            "target_role": self.target_role,
            "target_industry": self.target_industry,
            "key_skills_highlighted": self.key_skills_highlighted,
            "ats_optimized": self.ats_optimized,
            "match_score": self.match_score,
            "modifications": self.modifications,
            "file_path": self.file_path,
            "format": self.format.value,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "ResumeMetadata":
        """Create from dictionary."""
        data = data.copy()
        if data.get("created_at"):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if data.get("format"):
            data["format"] = ResumeFormat(data["format"])
        return cls(**data)


@dataclass
class ResumeDiff:
    """Tracks changes made to a resume during tailoring."""

    original_resume_id: str
    tailored_resume_id: str

    # Section-level changes
    summary_changed: bool = False
    original_summary: str = ""
    new_summary: str = ""

    # Bullet point changes
    bullets_modified: List[Dict[str, str]] = field(default_factory=list)
    # Each dict: {"section": "experience", "index": 0, "original": "...", "new": "..."}

    # Skills changes
    skills_added: List[str] = field(default_factory=list)
    skills_removed: List[str] = field(default_factory=list)
    skills_reordered: bool = False

    # Keywords added
    keywords_integrated: List[str] = field(default_factory=list)

    # Structural changes
    sections_reordered: bool = False
    sections_added: List[str] = field(default_factory=list)
    sections_removed: List[str] = field(default_factory=list)

    # Metadata
    change_date: datetime = field(default_factory=datetime.now)
    change_summary: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "original_resume_id": self.original_resume_id,
            "tailored_resume_id": self.tailored_resume_id,
            "summary_changed": self.summary_changed,
            "original_summary": self.original_summary,
            "new_summary": self.new_summary,
            "bullets_modified": self.bullets_modified,
            "skills_added": self.skills_added,
            "skills_removed": self.skills_removed,
            "skills_reordered": self.skills_reordered,
            "keywords_integrated": self.keywords_integrated,
            "sections_reordered": self.sections_reordered,
            "sections_added": self.sections_added,
            "sections_removed": self.sections_removed,
            "change_date": self.change_date.isoformat(),
            "change_summary": self.change_summary,
        }
