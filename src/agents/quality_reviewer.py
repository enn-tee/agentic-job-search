"""Quality reviewer agent - acts as a hiring manager."""

import json
from typing import Dict, List
from .base import BaseAgent
from ..models.job_posting import JobAnalysis
from ..models.resume import Resume
from ..core.adapters import IndustryAdapter


class QualityReviewerAgent(BaseAgent):
    """
    Agent that reviews tailored resumes from a hiring manager's perspective.

    Provides feedback and suggestions for improvement.
    """

    def __init__(
        self,
        industry_adapter: IndustryAdapter,
        model: str = "claude-sonnet-4-20250514",
        api_key: str = None,
    ):
        """
        Initialize the quality reviewer.

        Args:
            industry_adapter: Industry-specific adapter
            model: Claude model to use
            api_key: Anthropic API key
        """
        super().__init__(name="QualityReviewer", model=model, api_key=api_key)
        self.industry_adapter = industry_adapter

    def run(
        self, job_analysis: JobAnalysis, tailored_resume: Resume
    ) -> Dict:
        """
        Review a tailored resume.

        Args:
            job_analysis: The job posting analysis
            tailored_resume: The tailored resume to review

        Returns:
            Review results with score, strengths, weaknesses, and suggestions
        """
        self.log(f"Reviewing resume for {job_analysis.job_posting.title}")

        system_prompt = self._build_system_prompt(job_analysis)
        user_message = self._build_user_message(job_analysis, tailored_resume)

        response = self._call_claude(
            system_prompt=system_prompt,
            user_message=user_message,
            max_tokens=2048,
            temperature=0.5,
        )

        # Parse response
        try:
            import re

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                review = json.loads(json_match.group(0))
            else:
                # Fallback if not JSON
                review = {
                    "overall_score": 7.0,
                    "feedback": response,
                    "strengths": [],
                    "weaknesses": [],
                    "suggestions": [],
                }
        except Exception as e:
            self.log(f"Warning: Could not parse review: {e}")
            review = {
                "overall_score": 7.0,
                "feedback": response,
                "strengths": [],
                "weaknesses": [],
                "suggestions": [],
            }

        self.log(f"Review complete - Score: {review.get('overall_score', 'N/A')}/10")
        return review

    def _build_system_prompt(self, job_analysis: JobAnalysis) -> str:
        """Build system prompt as hiring manager."""
        return f"""You are a hiring manager in the {self.industry_adapter.config.display_name} industry reviewing resumes for a {job_analysis.role_type} position.

Your company is: {job_analysis.job_posting.company}
Role: {job_analysis.job_posting.title}
Seniority: {job_analysis.seniority}

Industry context:
{self.industry_adapter.config.description}

Key things you look for in candidates:
- Relevant technical skills: {', '.join(job_analysis.required_skills[:8])}
- Industry experience in: {', '.join(job_analysis.industry_experience[:5])}
- Cultural fit indicators: {', '.join(job_analysis.culture_keywords[:5])}

Review the resume and provide:
1. Overall score (0-10 scale)
2. Likelihood to invite for interview (High/Medium/Low)
3. Strengths (what stands out positively)
4. Weaknesses (what's missing or concerning)
5. Specific suggestions for improvement
6. Red flags (if any)
7. Keywords/phrases that caught your attention

Be critical but fair. Focus on whether this candidate can do the job effectively.

Return your review as a JSON object:
{{
    "overall_score": 8.5,
    "interview_likelihood": "High",
    "strengths": ["strength 1", "strength 2", ...],
    "weaknesses": ["weakness 1", "weakness 2", ...],
    "suggestions": ["suggestion 1", "suggestion 2", ...],
    "red_flags": ["flag 1", ...],
    "positive_keywords": ["keyword 1", "keyword 2", ...],
    "summary": "Brief overall assessment"
}}

Return ONLY valid JSON."""

    def _build_user_message(
        self, job_analysis: JobAnalysis, resume: Resume
    ) -> str:
        """Build user message with resume to review."""
        # Format resume as readable text
        resume_text = self._format_resume(resume)

        return f"""Please review this resume for our {job_analysis.role_type} opening:

{resume_text}

Key requirements for this role:
- Required skills: {', '.join(job_analysis.required_skills[:10])}
- Preferred skills: {', '.join(job_analysis.preferred_skills[:8])}
- Experience level: {job_analysis.years_experience or 'Not specified'}
- Key responsibilities: {', '.join(job_analysis.key_responsibilities[:5])}

Provide your review as a hiring manager."""

    def _format_resume(self, resume: Resume) -> str:
        """Format resume as readable text for review."""
        sections = []

        # Header
        sections.append(f"=== {resume.name} ===")
        sections.append(f"Email: {resume.email} | Phone: {resume.phone or 'N/A'}")
        if resume.linkedin:
            sections.append(f"LinkedIn: {resume.linkedin}")
        sections.append("")

        # Summary
        if resume.professional_summary:
            sections.append("PROFESSIONAL SUMMARY")
            sections.append(resume.professional_summary)
            sections.append("")

        # Technical Skills
        if resume.technical_skills:
            sections.append("TECHNICAL SKILLS")
            sections.append(", ".join(resume.technical_skills[:20]))
            sections.append("")

        # Experience
        sections.append("PROFESSIONAL EXPERIENCE")
        for i, exp in enumerate(resume.experience[:3]):  # Show top 3 positions
            # Handle both dict and object formats
            if isinstance(exp, dict):
                title = exp.get('title', 'N/A')
                company = exp.get('company', 'N/A')
                start_date = exp.get('start_date', 'N/A')
                end_date = exp.get('end_date') or 'Present'
                bullets = exp.get('bullets', [])
            else:
                title = exp.title
                company = exp.company
                start_date = exp.start_date
                end_date = exp.end_date or 'Present'
                bullets = exp.bullets

            sections.append(f"\n{title} at {company} ({start_date} - {end_date})")
            for bullet in bullets:
                sections.append(f"  • {bullet}")

        # Education
        if resume.education:
            sections.append("\nEDUCATION")
            for edu in resume.education:
                # Handle both dict and object formats
                if isinstance(edu, dict):
                    degree = edu.get('degree', 'N/A')
                    field = edu.get('field_of_study') or 'N/A'
                    institution = edu.get('institution', 'N/A')
                else:
                    degree = edu.degree
                    field = edu.field_of_study or 'N/A'
                    institution = edu.institution

                sections.append(f"{degree} in {field} - {institution}")

        # Certifications
        if resume.certifications:
            sections.append("\nCERTIFICATIONS")
            sections.append(", ".join(resume.certifications))

        return "\n".join(sections)
