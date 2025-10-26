"""Job posting analyzer agent."""

import json
from typing import Optional
from .base import BaseAgent
from ..models.job_posting import JobPosting, JobAnalysis
from ..core.adapters import IndustryAdapter


class JobAnalyzerAgent(BaseAgent):
    """
    Agent responsible for analyzing job postings.

    Extracts key requirements, skills, keywords, and other relevant
    information from job descriptions.
    """

    def __init__(
        self,
        industry_adapter: Optional[IndustryAdapter] = None,
        model: str = "claude-sonnet-4-20250514",
        api_key: Optional[str] = None,
    ):
        """
        Initialize the job analyzer agent.

        Args:
            industry_adapter: Industry-specific adapter for context
            model: Claude model to use
            api_key: Anthropic API key
        """
        super().__init__(name="JobAnalyzer", model=model, api_key=api_key)
        self.industry_adapter = industry_adapter

    def run(self, job_posting: JobPosting) -> JobAnalysis:
        """
        Analyze a job posting.

        Args:
            job_posting: Job posting to analyze

        Returns:
            Detailed analysis of the job posting
        """
        self.log(f"Analyzing job: {job_posting.title} at {job_posting.company}")

        system_prompt = self._build_system_prompt()
        user_message = self._build_user_message(job_posting)

        response = self._call_claude(
            system_prompt=system_prompt,
            user_message=user_message,
            max_tokens=4096,
            temperature=0.3,  # Lower temperature for more consistent extraction
        )

        # Parse JSON response
        try:
            analysis_data = json.loads(response)
        except json.JSONDecodeError:
            # If Claude didn't return valid JSON, try to extract it
            import re

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                analysis_data = json.loads(json_match.group(0))
            else:
                raise ValueError(f"Failed to parse job analysis response: {response}")

        # Create JobAnalysis object
        job_analysis = JobAnalysis(
            job_posting=job_posting,
            role_type=analysis_data.get("role_type", "Unknown"),
            seniority=analysis_data.get("seniority", "Unknown"),
            industry=analysis_data.get("industry", "Unknown"),
            required_skills=analysis_data.get("required_skills", []),
            preferred_skills=analysis_data.get("preferred_skills", []),
            technical_skills=analysis_data.get("technical_skills", []),
            soft_skills=analysis_data.get("soft_skills", []),
            critical_keywords=analysis_data.get("critical_keywords", []),
            secondary_keywords=analysis_data.get("secondary_keywords", []),
            education_requirements=analysis_data.get("education_requirements", []),
            certifications=analysis_data.get("certifications", []),
            years_experience=analysis_data.get("years_experience"),
            industry_experience=analysis_data.get("industry_experience", []),
            culture_keywords=analysis_data.get("culture_keywords", []),
            values=analysis_data.get("values", []),
            key_responsibilities=analysis_data.get("key_responsibilities", []),
            confidence_score=analysis_data.get("confidence_score", 0.8),
        )

        self.log(
            f"Analysis complete: {job_analysis.role_type} ({job_analysis.seniority})"
        )
        return job_analysis

    def _build_system_prompt(self) -> str:
        """Build system prompt for job analysis."""
        industry_context = ""
        if self.industry_adapter:
            config = self.industry_adapter.config
            industry_context = f"""
You are analyzing jobs in the {config.display_name} industry.

Key industry terminology to recognize:
{json.dumps(dict(list(config.acronyms.items())[:20]), indent=2)}

High-priority skills in this industry:
{json.dumps(config.get_high_priority_skills()[:30], indent=2)}

Common role titles:
{json.dumps(config.primary_roles, indent=2)}
"""

        return f"""You are a job posting analyzer. Your task is to extract structured information from job postings.

{industry_context}

Analyze the job posting and extract the following information:

1. Role type (e.g., "Data Analyst", "Software Engineer", "Clinical Data Analyst")
2. Seniority level (Entry, Mid, Senior, Lead, Principal)
3. Industry (healthcare, tech, finance, etc.)
4. Required skills (must-have skills explicitly stated)
5. Preferred skills (nice-to-have skills)
6. Technical skills (programming languages, tools, systems)
7. Soft skills (communication, leadership, etc.)
8. Critical keywords (most important terms for ATS)
9. Secondary keywords (supporting terms for ATS)
10. Education requirements
11. Certifications mentioned
12. Years of experience required
13. Industry experience needed
14. Company culture keywords
15. Company values
16. Key responsibilities

Return your analysis as a JSON object with these fields. Be thorough but concise.
Extract exact phrases from the job posting when possible.

Return ONLY valid JSON, no additional text or markdown formatting."""

    def _build_user_message(self, job_posting: JobPosting) -> str:
        """Build user message with job posting details."""
        return f"""Analyze this job posting:

Company: {job_posting.company}
Title: {job_posting.title}
Location: {job_posting.location or "Not specified"}

Job Description:
{job_posting.description}

Provide your analysis as a JSON object."""
