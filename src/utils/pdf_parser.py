"""PDF resume parser using Claude to extract structured data."""

import pdfplumber
from pathlib import Path
from typing import Optional
import anthropic
import os
import json
import re


class PDFResumeParser:
    """Parse PDF resumes and convert to structured Resume format using Claude."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize PDF parser.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract raw text from PDF file.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text content
        """
        text_parts = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)

            return "\n\n".join(text_parts)

        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {e}")

    def parse_resume_with_claude(self, resume_text: str) -> dict:
        """
        Use Claude to parse resume text into structured JSON format.

        Args:
            resume_text: Raw resume text

        Returns:
            Dictionary matching Resume model structure
        """
        system_prompt = """You are an expert resume parser. Convert the provided resume text into a structured JSON format.

The JSON should match this exact structure:

{
  "name": "Full Name",
  "email": "email@example.com",
  "phone": "(555) 123-4567",
  "location": "City, State",
  "linkedin": "linkedin.com/in/username",
  "github": "github.com/username",
  "portfolio": "website.com",
  "professional_summary": "Professional summary text...",
  "experience": [
    {
      "company": "Company Name",
      "title": "Job Title",
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM" or null if current,
      "location": "City, State",
      "bullets": ["Achievement 1", "Achievement 2"],
      "technologies": ["Tech1", "Tech2"]
    }
  ],
  "education": [
    {
      "institution": "University Name",
      "degree": "Degree Name",
      "field_of_study": "Major/Field",
      "graduation_date": "YYYY-MM",
      "gpa": "3.8" or null,
      "honors": ["Honor 1", "Honor 2"]
    }
  ],
  "technical_skills": ["Skill 1", "Skill 2"],
  "soft_skills": ["Skill 1", "Skill 2"],
  "tools": ["Tool 1", "Tool 2"],
  "languages": ["Language 1", "Language 2"],
  "certifications": ["Cert 1", "Cert 2"],
  "projects": [],
  "publications": []
}

Important:
- Extract ALL information present in the resume
- Preserve exact wording of achievements/bullets
- Use null for missing optional fields
- For dates, use "YYYY-MM" format or null for current positions
- Empty arrays [] for missing sections
- Be thorough and accurate

Return ONLY valid JSON, no additional text."""

        user_message = f"""Parse this resume into structured JSON format:

{resume_text}

Return the structured JSON:"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8192,
                temperature=0.1,  # Low temperature for consistency
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )

            response_text = message.content[0].text

            # Extract JSON from response
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                resume_data = json.loads(json_match.group(0))
                return resume_data
            else:
                raise ValueError("Could not extract JSON from Claude response")

        except Exception as e:
            raise ValueError(f"Error parsing resume with Claude: {e}")

    def parse_pdf_resume(self, pdf_path: Path) -> dict:
        """
        Parse a PDF resume file into structured format.

        Args:
            pdf_path: Path to PDF resume file

        Returns:
            Dictionary matching Resume model structure
        """
        # Step 1: Extract text from PDF
        resume_text = self.extract_text_from_pdf(pdf_path)

        if not resume_text or len(resume_text.strip()) < 100:
            raise ValueError("PDF appears to be empty or has insufficient text")

        # Step 2: Parse with Claude
        resume_data = self.parse_resume_with_claude(resume_text)

        return resume_data


def parse_pdf_resume(pdf_path: Path, api_key: Optional[str] = None) -> dict:
    """
    Convenience function to parse a PDF resume.

    Args:
        pdf_path: Path to PDF resume file
        api_key: Optional Anthropic API key

    Returns:
        Dictionary matching Resume model structure
    """
    parser = PDFResumeParser(api_key=api_key)
    return parser.parse_pdf_resume(pdf_path)
