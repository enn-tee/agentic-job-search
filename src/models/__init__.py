"""Data models for the resume tailoring system."""

from .job_posting import JobPosting, JobAnalysis
from .resume import Resume, ResumeMetadata, ResumeDiff
from .industry import IndustryConfig

__all__ = [
    "JobPosting",
    "JobAnalysis",
    "Resume",
    "ResumeMetadata",
    "ResumeDiff",
    "IndustryConfig",
]
