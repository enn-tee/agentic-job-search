"""Resume matcher agent."""

import json
from typing import List, Tuple
from .base import BaseAgent
from ..models.job_posting import JobAnalysis
from ..models.resume import Resume, ResumeMetadata


class ResumeMatcherAgent(BaseAgent):
    """
    Agent responsible for matching resumes to job postings.

    Analyzes the resume pool and scores each resume's relevance
    to the target job posting.
    """

    def __init__(self, model: str = "claude-sonnet-4-20250514", api_key: str = None):
        """
        Initialize the resume matcher agent.

        Args:
            model: Claude model to use
            api_key: Anthropic API key
        """
        super().__init__(name="ResumeMatcher", model=model, api_key=api_key)

    def run(
        self,
        job_analysis: JobAnalysis,
        resume_pool: List[Tuple[Resume, ResumeMetadata]],
    ) -> List[Tuple[Resume, ResumeMetadata, float]]:
        """
        Match resumes to a job posting.

        Args:
            job_analysis: Analyzed job posting
            resume_pool: List of (resume, metadata) tuples

        Returns:
            List of (resume, metadata, match_score) tuples, sorted by score descending
        """
        self.log(f"Matching {len(resume_pool)} resumes to job posting")

        if not resume_pool:
            self.log("Warning: Resume pool is empty")
            return []

        # For each resume, calculate a match score
        scored_resumes = []
        for resume, metadata in resume_pool:
            score = self._score_resume(job_analysis, resume, metadata)
            scored_resumes.append((resume, metadata, score))
            self.log(
                f"  - {metadata.resume_id}: {score:.2f} match score"
            )

        # Sort by score descending
        scored_resumes.sort(key=lambda x: x[2], reverse=True)

        best_match = scored_resumes[0] if scored_resumes else None
        if best_match:
            self.log(
                f"Best match: {best_match[1].resume_id} (score: {best_match[2]:.2f})"
            )

        return scored_resumes

    def _score_resume(
        self, job_analysis: JobAnalysis, resume: Resume, metadata: ResumeMetadata
    ) -> float:
        """
        Score how well a resume matches a job posting.

        Uses Claude to perform intelligent matching beyond simple keyword overlap.

        Args:
            job_analysis: Analyzed job posting
            resume: Resume to score
            metadata: Resume metadata

        Returns:
            Match score between 0.0 and 1.0
        """
        system_prompt = """You are a resume matching expert. Your task is to score how well a resume matches a job posting.

Consider:
1. Skills overlap (required vs preferred)
2. Years of experience alignment
3. Industry experience relevance
4. Education requirements
5. Role type compatibility
6. Seniority level match
7. Transferable skills for career transitions

Return a JSON object with:
{
    "match_score": 0.85,  // Float between 0.0 and 1.0
    "reasoning": "Brief explanation of the score",
    "strengths": ["strength 1", "strength 2"],
    "gaps": ["gap 1", "gap 2"]
}

Return ONLY valid JSON."""

        user_message = f"""Score this resume match:

JOB POSTING:
- Company: {job_analysis.job_posting.company}
- Title: {job_analysis.job_posting.title}
- Role Type: {job_analysis.role_type}
- Seniority: {job_analysis.seniority}
- Industry: {job_analysis.industry}
- Required Skills: {', '.join(job_analysis.required_skills[:10])}
- Preferred Skills: {', '.join(job_analysis.preferred_skills[:10])}
- Years Experience: {job_analysis.years_experience or 'Not specified'}

RESUME:
- Name: {resume.name}
- Summary: {resume.professional_summary[:200]}...
- Technical Skills: {', '.join(resume.technical_skills[:15])}
- Experience: {len(resume.experience)} positions
- Most Recent Role: {resume.experience[0].title if resume.experience else 'N/A'}
- Education: {resume.education[0].degree if resume.education else 'N/A'}

RESUME METADATA:
- Target Role: {metadata.target_role or 'N/A'}
- Target Industry: {metadata.target_industry or 'N/A'}
- Tags: {', '.join(metadata.tags)}

Provide your match score and analysis as JSON."""

        try:
            response = self._call_claude(
                system_prompt=system_prompt,
                user_message=user_message,
                max_tokens=1024,
                temperature=0.3,
            )

            # Parse response
            import re
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
                return float(result.get("match_score", 0.5))
            else:
                self.log(f"Warning: Could not parse match score, using default 0.5")
                return 0.5

        except Exception as e:
            self.log(f"Warning: Error scoring resume: {e}, using default 0.5")
            return 0.5
