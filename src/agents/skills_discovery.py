"""Skills discovery agent for identifying transferable skills and filling gaps."""

import json
from typing import List, Dict, Optional, Set, Tuple
from src.agents.base import BaseAgent
from src.models.job_posting import JobAnalysis
from src.models.resume import Resume


class SkillsDiscoveryAgent(BaseAgent):
    """
    Interactive agent that helps users discover transferable skills
    and identify experiences that demonstrate job requirements.
    """

    def __init__(self, **kwargs):
        super().__init__(name="SkillsDiscovery", **kwargs)
        self.max_rounds = 3  # Maximum rounds before offering skip
        self.current_round = 0

    def run(self, job_analysis: JobAnalysis, resume: Resume) -> Dict:
        """
        Main entry point - analyze skill gaps.

        Returns gap analysis dict.
        """
        return self.analyze_skill_gaps(job_analysis, resume)

    def analyze_skill_gaps(
        self, job_analysis: JobAnalysis, resume: Resume
    ) -> Dict[str, List[str]]:
        """
        Analyze gaps between job requirements and current resume.

        Returns:
            Dict with:
                - missing_skills: Skills not found in resume
                - weak_skills: Skills mentioned but not demonstrated
                - transferable_opportunities: Areas to explore
        """
        self.log("Analyzing skill gaps...")

        # Extract all skills from resume
        resume_skills = set()
        resume_skills.update([s.lower() for s in resume.technical_skills])
        resume_skills.update([s.lower() for s in resume.soft_skills])
        resume_skills.update([s.lower() for s in resume.tools])

        # Add skills mentioned in experience
        for exp in resume.experience:
            if isinstance(exp, dict):
                resume_skills.update([t.lower() for t in exp.get('technologies', [])])
            else:
                resume_skills.update([t.lower() for t in exp.technologies])

        # Find missing required skills
        required_skills_lower = {s.lower() for s in job_analysis.required_skills}
        missing_skills = [
            skill
            for skill in job_analysis.required_skills
            if skill.lower() not in resume_skills
        ]

        # Find preferred skills not in resume
        preferred_skills_lower = {s.lower() for s in job_analysis.preferred_skills}
        missing_preferred = [
            skill
            for skill in job_analysis.preferred_skills
            if skill.lower() not in resume_skills
        ]

        self.log(f"Found {len(missing_skills)} missing required skills")
        self.log(f"Found {len(missing_preferred)} missing preferred skills")

        return {
            "missing_required": missing_skills[:10],  # Focus on top 10
            "missing_preferred": missing_preferred[:5],
            "transferable_opportunities": missing_skills + missing_preferred,
        }

    def discover_transferable_skills(
        self,
        missing_skill: str,
        job_analysis: JobAnalysis,
        resume: Resume,
        previous_responses: List[str] = None,
    ) -> Dict:
        """
        Generate questions to help user discover transferable skills.

        Returns:
            Dict with:
                - questions: List of questions to ask
                - context: Why this skill matters
                - examples: Examples of transferable experiences
        """
        self.log(f"Generating discovery questions for: {missing_skill}")

        system_prompt = f"""You are a career coach specializing in identifying transferable skills.

Your role is to help job seekers discover experiences that demonstrate skills they didn't realize they had.

Guidelines:
1. Ask open-ended questions about past experiences
2. Look for indirect evidence of the skill
3. Consider volunteer work, academic projects, hobbies, and life experiences
4. Frame questions to prompt specific examples
5. Be encouraging and creative in finding connections

Target Role: {job_analysis.role_type} ({job_analysis.seniority})
Industry: {job_analysis.industry or 'General'}"""

        # Get user's experience context
        experience_summary = self._summarize_experience(resume)
        previous_context = ""
        if previous_responses:
            previous_context = f"\n\nPrevious questions/answers:\n" + "\n".join(
                previous_responses
            )

        user_message = f"""Help me discover if the candidate has experience with: {missing_skill}

CANDIDATE'S BACKGROUND:
{experience_summary}

WHY THIS SKILL MATTERS FOR THE JOB:
Key responsibilities: {', '.join(job_analysis.key_responsibilities[:3])}
Required skills: {', '.join(job_analysis.required_skills[:5])}
{previous_context}

Generate a JSON response with:
{{
  "questions": [
    "Question 1 that explores related experiences",
    "Question 2 that explores adjacent skills",
    "Question 3 that explores indirect evidence"
  ],
  "context": "Brief explanation of why this skill is important for the role",
  "transferable_examples": [
    "Example 1 of how other experiences might demonstrate this skill",
    "Example 2 of indirect ways to demonstrate this skill"
  ],
  "related_skills": ["related_skill_1", "related_skill_2"]
}}"""

        try:
            response = self._call_claude(
                system_prompt=system_prompt,
                user_message=user_message,
                max_tokens=2048,
                temperature=0.8,
            )

            # Parse JSON response
            import re

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                discovery = json.loads(json_match.group(0))
                return discovery
            else:
                # Fallback to generic questions
                return self._generate_generic_questions(missing_skill, job_analysis)

        except Exception as e:
            self.log(f"Error generating questions: {e}")
            return self._generate_generic_questions(missing_skill, job_analysis)

    def _generate_generic_questions(
        self, skill: str, job_analysis: JobAnalysis
    ) -> Dict:
        """Generate generic fallback questions."""
        return {
            "questions": [
                f"Have you ever worked on a project that required {skill}, even informally?",
                f"Can you describe a situation where you had to learn something similar to {skill}?",
                f"What experiences have you had that might relate to {skill}?",
            ],
            "context": f"This skill is important for the {job_analysis.role_type} role.",
            "transferable_examples": [
                "Academic projects or coursework",
                "Volunteer work or community involvement",
                "Personal projects or hobbies",
                "On-the-job training or self-study",
            ],
            "related_skills": [],
        }

    def evaluate_response(
        self, missing_skill: str, user_response: str, job_analysis: JobAnalysis
    ) -> Dict:
        """
        Evaluate if user's response demonstrates the skill or reveals transferable experience.

        Returns:
            Dict with:
                - has_skill: bool
                - confidence: float (0-1)
                - bullet_suggestions: List[str]
                - needs_more_exploration: bool
        """
        self.log(f"Evaluating response for: {missing_skill}")

        system_prompt = f"""You are an expert resume writer and skills analyst.

Evaluate whether the candidate's response demonstrates they have (or can demonstrate) the target skill.

Be generous in finding connections - look for:
1. Direct evidence of the skill
2. Transferable experiences
3. Learning ability and adaptability
4. Adjacent skills that translate

Target Role: {job_analysis.role_type}
Industry Context: {job_analysis.industry or 'General'}"""

        user_message = f"""Evaluate this response for skill: {missing_skill}

USER'S RESPONSE:
{user_response}

JOB CONTEXT:
Role: {job_analysis.role_type}
Key responsibilities: {', '.join(job_analysis.key_responsibilities[:3])}

Provide evaluation as JSON:
{{
  "has_skill": true/false,
  "confidence": 0.0-1.0,
  "reasoning": "Explanation of your evaluation",
  "bullet_suggestions": [
    "Suggested resume bullet point 1",
    "Suggested resume bullet point 2"
  ],
  "needs_more_exploration": true/false,
  "follow_up_question": "Optional follow-up question if needs more exploration"
}}"""

        try:
            response = self._call_claude(
                system_prompt=system_prompt,
                user_message=user_message,
                max_tokens=1536,
                temperature=0.5,
            )

            # Parse JSON
            import re

            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            else:
                return {
                    "has_skill": False,
                    "confidence": 0.0,
                    "reasoning": "Could not evaluate response",
                    "bullet_suggestions": [],
                    "needs_more_exploration": True,
                }

        except Exception as e:
            self.log(f"Error evaluating response: {e}")
            return {
                "has_skill": False,
                "confidence": 0.0,
                "reasoning": f"Error: {e}",
                "bullet_suggestions": [],
                "needs_more_exploration": True,
            }

    def _summarize_experience(self, resume: Resume) -> str:
        """Create a concise summary of candidate's experience."""
        summary_parts = []

        # Recent positions
        if resume.experience:
            summary_parts.append("RECENT POSITIONS:")
            for i, exp in enumerate(resume.experience[:3]):
                if isinstance(exp, dict):
                    title = exp.get('title', 'N/A')
                    company = exp.get('company', 'N/A')
                    summary_parts.append(f"  • {title} at {company}")
                else:
                    summary_parts.append(f"  • {exp.title} at {exp.company}")

        # Skills
        if resume.technical_skills:
            summary_parts.append(f"\nTECHNICAL SKILLS: {', '.join(resume.technical_skills[:10])}")

        # Education
        if resume.education:
            summary_parts.append("\nEDUCATION:")
            for edu in resume.education:
                if isinstance(edu, dict):
                    degree = edu.get('degree', 'N/A')
                    field = edu.get('field_of_study', 'N/A')
                    summary_parts.append(f"  • {degree} in {field}")
                else:
                    summary_parts.append(f"  • {edu.degree} in {edu.field_of_study or 'N/A'}")

        return "\n".join(summary_parts)

    def generate_skill_addition_bullet(
        self, skill: str, user_context: str, job_analysis: JobAnalysis
    ) -> str:
        """
        Generate a resume bullet point that incorporates the discovered skill.

        Args:
            skill: The skill to highlight
            user_context: User's description of relevant experience
            job_analysis: Job requirements for context

        Returns:
            Polished resume bullet point
        """
        system_prompt = """You are an expert resume writer.

Create a strong, achievement-focused resume bullet point that:
1. Starts with an action verb
2. Includes the skill naturally
3. Shows impact or results
4. Fits the target role
5. Sounds professional and authentic

Keep it to 1-2 lines maximum."""

        user_message = f"""Create a resume bullet point:

SKILL TO HIGHLIGHT: {skill}

CANDIDATE'S EXPERIENCE:
{user_context}

TARGET ROLE: {job_analysis.role_type}

Return just the bullet point text, no extra formatting."""

        try:
            response = self._call_claude(
                system_prompt=system_prompt,
                user_message=user_message,
                max_tokens=256,
                temperature=0.7,
            )
            return response.strip().strip("•").strip("-").strip()
        except Exception as e:
            self.log(f"Error generating bullet: {e}")
            return f"Applied {skill} in {user_context[:50]}..."
