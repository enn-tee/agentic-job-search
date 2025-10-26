"""Tailoring orchestrator agent - coordinates resume modifications."""

import json
from typing import List
from .base import BaseAgent
from ..models.job_posting import JobAnalysis
from ..models.resume import Resume, ResumeDiff
from ..core.adapters import IndustryAdapter


class TailoringOrchestratorAgent(BaseAgent):
    """
    Agent that orchestrates resume tailoring.

    Coordinates multiple sub-tasks:
    - Summary optimization
    - Bullet point enhancement
    - ATS keyword integration
    - Skills alignment
    """

    def __init__(
        self,
        industry_adapter: IndustryAdapter,
        model: str = "claude-sonnet-4-20250514",
        api_key: str = None,
    ):
        """
        Initialize the tailoring orchestrator.

        Args:
            industry_adapter: Industry-specific adapter
            model: Claude model to use
            api_key: Anthropic API key
        """
        super().__init__(name="TailoringOrchestrator", model=model, api_key=api_key)
        self.industry_adapter = industry_adapter

    def run(
        self,
        job_analysis: JobAnalysis,
        base_resume: Resume,
        focus_areas: List[str] = None,
    ) -> tuple[Resume, ResumeDiff]:
        """
        Tailor a resume for a specific job posting.

        Args:
            job_analysis: Analyzed job posting
            base_resume: Original resume to tailor
            focus_areas: Specific areas to focus on (default: all)

        Returns:
            Tuple of (tailored_resume, diff_tracking)
        """
        self.log(f"Tailoring resume for {job_analysis.job_posting.title}")

        if focus_areas is None:
            focus_areas = ["summary", "bullets", "keywords", "skills"]

        # Create a copy of the base resume to modify
        tailored = Resume(**base_resume.to_dict())

        # Track changes
        diff = ResumeDiff(
            original_resume_id="",  # Will be set by caller
            tailored_resume_id="",  # Will be set by caller
        )

        # Execute tailoring tasks
        if "summary" in focus_areas:
            self.log("  → Optimizing professional summary")
            tailored.professional_summary = self._optimize_summary(
                job_analysis, base_resume
            )
            diff.summary_changed = True
            diff.original_summary = base_resume.professional_summary
            diff.new_summary = tailored.professional_summary

        if "bullets" in focus_areas:
            self.log("  → Enhancing experience bullet points")
            tailored.experience = self._enhance_bullets(
                job_analysis, base_resume, diff
            )

        if "keywords" in focus_areas:
            self.log("  → Integrating ATS keywords")
            keywords_added = self._integrate_keywords(job_analysis, tailored)
            diff.keywords_integrated = keywords_added

        if "skills" in focus_areas:
            self.log("  → Aligning skills section")
            tailored.technical_skills = self._align_skills(job_analysis, tailored)

        self.log("Tailoring complete")
        return tailored, diff

    def _optimize_summary(
        self, job_analysis: JobAnalysis, resume: Resume
    ) -> str:
        """Optimize the professional summary for the target job."""
        keyword_optimizer = self.industry_adapter.get_keyword_optimizer()
        priority_keywords = keyword_optimizer.get_priority_keywords()

        system_prompt = f"""You are an expert resume writer specializing in {self.industry_adapter.config.display_name}.

Your task is to rewrite a professional summary to be:
1. Concise (2-3 sentences, max 100 words)
2. Engaging and compelling
3. Aligned with the target role and industry
4. Incorporating relevant keywords naturally
5. Highlighting the candidate's strengths and value proposition

Industry-specific tips:
{json.dumps(self.industry_adapter.config.resume_tips.get('summary', []), indent=2)}

Return ONLY the rewritten summary, no additional text."""

        user_message = f"""Rewrite this professional summary for the target job:

CURRENT SUMMARY:
{resume.professional_summary}

TARGET JOB:
- Title: {job_analysis.job_posting.title}
- Company: {job_analysis.job_posting.company}
- Role Type: {job_analysis.role_type}
- Seniority: {job_analysis.seniority}
- Key Requirements: {', '.join(job_analysis.required_skills[:8])}

PRIORITY KEYWORDS TO INCORPORATE:
{', '.join(priority_keywords[:10])}

CANDIDATE'S STRENGTHS (from resume):
- Technical Skills: {', '.join(resume.technical_skills[:10])}
- Years Experience: {len(resume.experience)} roles
- Most Recent: {resume.experience[0].title if resume.experience else 'N/A'}

Write the optimized summary:"""

        return self._call_claude(
            system_prompt=system_prompt,
            user_message=user_message,
            max_tokens=512,
            temperature=0.7,
        ).strip()

    def _enhance_bullets(
        self, job_analysis: JobAnalysis, resume: Resume, diff: ResumeDiff
    ) -> List:
        """Enhance bullet points to be more achievement-focused."""
        from ..models.resume import WorkExperience

        enhanced_experience = []

        # Focus on most recent 2-3 positions
        positions_to_enhance = min(3, len(resume.experience))

        for i, exp in enumerate(resume.experience):
            if i < positions_to_enhance:
                # Enhance this position's bullets
                enhanced_bullets = self._enhance_position_bullets(
                    job_analysis, exp, resume
                )

                # Track changes
                for j, (original, enhanced) in enumerate(
                    zip(exp.bullets, enhanced_bullets)
                ):
                    if original != enhanced:
                        diff.bullets_modified.append(
                            {
                                "position_index": i,
                                "bullet_index": j,
                                "original": original,
                                "new": enhanced,
                            }
                        )

                # Create new WorkExperience with enhanced bullets
                enhanced_exp = WorkExperience(
                    company=exp.company,
                    title=exp.title,
                    start_date=exp.start_date,
                    end_date=exp.end_date,
                    location=exp.location,
                    bullets=enhanced_bullets,
                    technologies=exp.technologies,
                )
                enhanced_experience.append(enhanced_exp)
            else:
                # Keep older positions as-is
                enhanced_experience.append(exp)

        return enhanced_experience

    def _enhance_position_bullets(
        self, job_analysis: JobAnalysis, experience: object, resume: Resume
    ) -> List[str]:
        """Enhance bullets for a specific position."""
        action_verbs = self.industry_adapter.get_keyword_optimizer().get_action_verbs()
        metric_templates = (
            self.industry_adapter.get_keyword_optimizer().get_metric_templates()
        )

        system_prompt = f"""You are an expert resume writer. Rewrite experience bullets to be:

1. Achievement-focused (not responsibility-focused)
2. Start with strong action verbs
3. Include metrics and quantifiable results
4. Relevant to the target role
5. Use industry-appropriate terminology

Guidelines:
- Use action verbs: {', '.join(action_verbs[:10])}
- Include metrics using patterns like: {', '.join(metric_templates[:3])}
- Keep each bullet to 1-2 lines
- Make impact clear and measurable

Industry tips for experience section:
{json.dumps(self.industry_adapter.config.resume_tips.get('experience', []), indent=2)}

Return the enhanced bullets as a JSON array of strings."""

        user_message = f"""Enhance these experience bullets for the target role:

CURRENT BULLETS:
{json.dumps(experience.bullets, indent=2)}

POSITION:
{experience.title} at {experience.company}

TARGET ROLE:
{job_analysis.role_type} ({job_analysis.seniority})

KEY REQUIREMENTS FROM JOB:
{', '.join(job_analysis.key_responsibilities[:5])}

RELEVANT SKILLS TO HIGHLIGHT:
{', '.join(job_analysis.required_skills[:8])}

Return enhanced bullets as JSON array:"""

        try:
            response = self._call_claude(
                system_prompt=system_prompt,
                user_message=user_message,
                max_tokens=2048,
                temperature=0.7,
            )

            # Extract JSON array
            import re

            json_match = re.search(r"\[.*\]", response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                self.log(f"Warning: Could not parse enhanced bullets, keeping original")
                return experience.bullets

        except Exception as e:
            self.log(f"Warning: Error enhancing bullets: {e}, keeping original")
            return experience.bullets

    def _integrate_keywords(
        self, job_analysis: JobAnalysis, resume: Resume
    ) -> List[str]:
        """Integrate ATS keywords naturally into the resume."""
        # This would analyze the resume and suggest where to add keywords
        # For now, return the critical keywords that should be present
        return job_analysis.critical_keywords[:8]

    def _align_skills(
        self, job_analysis: JobAnalysis, resume: Resume
    ) -> List[str]:
        """Align skills section with job requirements."""
        skill_taxonomy = self.industry_adapter.get_skill_taxonomy()

        # Combine job required and preferred skills
        job_skills = set(job_analysis.required_skills + job_analysis.preferred_skills)

        # Current resume skills
        current_skills = set(resume.technical_skills)

        # Skills that match the job
        matching_skills = current_skills.intersection(job_skills)

        # Skills in resume not in job (keep high-priority ones)
        other_skills = current_skills - job_skills
        high_priority_other = [
            s for s in other_skills if skill_taxonomy.is_high_priority_skill(s)
        ]

        # Combine: matching skills first, then high-priority others
        aligned_skills = list(matching_skills) + high_priority_other[:5]

        return aligned_skills[:20]  # Limit to top 20 skills
