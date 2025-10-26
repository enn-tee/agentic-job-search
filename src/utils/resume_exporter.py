"""Resume export utilities for various formats."""

from pathlib import Path
from datetime import datetime
from src.models.resume import Resume


class ResumeExporter:
    """Export resumes to various formats."""

    def export_to_text(self, resume: Resume, output_path: Path) -> str:
        """
        Export resume to formatted plain text.

        Args:
            resume: Resume object
            output_path: Where to save the text file

        Returns:
            Path to exported file
        """
        lines = []

        # Header
        lines.append("=" * 80)
        lines.append(resume.name.upper())
        lines.append("=" * 80)
        lines.append("")

        # Contact
        contact_parts = [resume.email]
        if resume.phone:
            contact_parts.append(resume.phone)
        if resume.location:
            contact_parts.append(resume.location)
        lines.append(" | ".join(contact_parts))

        if resume.linkedin:
            lines.append(f"LinkedIn: {resume.linkedin}")
        if resume.github:
            lines.append(f"GitHub: {resume.github}")
        lines.append("")

        # Professional Summary
        if resume.professional_summary:
            lines.append("-" * 80)
            lines.append("PROFESSIONAL SUMMARY")
            lines.append("-" * 80)
            lines.append(resume.professional_summary)
            lines.append("")

        # Technical Skills
        if resume.technical_skills:
            lines.append("-" * 80)
            lines.append("TECHNICAL SKILLS")
            lines.append("-" * 80)
            # Format skills in rows
            skills_per_row = 3
            for i in range(0, len(resume.technical_skills), skills_per_row):
                row_skills = resume.technical_skills[i:i+skills_per_row]
                lines.append(" • ".join(row_skills))
            lines.append("")

        # Professional Experience
        lines.append("-" * 80)
        lines.append("PROFESSIONAL EXPERIENCE")
        lines.append("-" * 80)

        for exp in resume.experience:
            # Handle both dict and object
            if isinstance(exp, dict):
                company = exp.get('company', '')
                title = exp.get('title', '')
                start_date = exp.get('start_date', '')
                end_date = exp.get('end_date') or 'Present'
                location = exp.get('location', '')
                bullets = exp.get('bullets', [])
                technologies = exp.get('technologies', [])
            else:
                company = exp.company
                title = exp.title
                start_date = exp.start_date
                end_date = exp.end_date or 'Present'
                location = exp.location or ''
                bullets = exp.bullets
                technologies = exp.technologies

            lines.append(f"{title} | {company}")
            date_loc = f"{start_date} - {end_date}"
            if location:
                date_loc += f" | {location}"
            lines.append(date_loc)
            lines.append("")

            for bullet in bullets:
                lines.append(f"  • {bullet}")

            if technologies:
                lines.append(f"  Technologies: {', '.join(technologies)}")
            lines.append("")

        # Education
        if resume.education:
            lines.append("-" * 80)
            lines.append("EDUCATION")
            lines.append("-" * 80)

            for edu in resume.education:
                if isinstance(edu, dict):
                    degree = edu.get('degree', '')
                    field = edu.get('field_of_study', '')
                    institution = edu.get('institution', '')
                    grad_date = edu.get('graduation_date', '')
                    gpa = edu.get('gpa', '')
                else:
                    degree = edu.degree
                    field = edu.field_of_study or ''
                    institution = edu.institution
                    grad_date = edu.graduation_date or ''
                    gpa = edu.gpa or ''

                lines.append(f"{degree}" + (f" in {field}" if field else ""))
                lines.append(f"{institution}" + (f" | {grad_date}" if grad_date else ""))
                if gpa:
                    lines.append(f"GPA: {gpa}")
                lines.append("")

        # Certifications
        if resume.certifications:
            lines.append("-" * 80)
            lines.append("CERTIFICATIONS")
            lines.append("-" * 80)
            for cert in resume.certifications:
                lines.append(f"  • {cert}")
            lines.append("")

        # Write to file
        content = "\n".join(lines)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)

    def export_to_html(self, resume: Resume, output_path: Path) -> str:
        """
        Export resume to clean, printable HTML.

        Args:
            resume: Resume object
            output_path: Where to save the HTML file

        Returns:
            Path to exported file
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{resume.name} - Resume</title>
    <style>
        @media print {{
            body {{ margin: 0; padding: 20px; }}
            .no-print {{ display: none; }}
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Calibri', 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 0.5in;
            background: white;
        }}

        .header {{
            text-align: center;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }}

        .header h1 {{
            font-size: 28px;
            color: #2c3e50;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}

        .contact {{
            font-size: 11px;
            color: #555;
        }}

        .contact a {{
            color: #2c3e50;
            text-decoration: none;
        }}

        .section {{
            margin-bottom: 25px;
        }}

        .section-title {{
            font-size: 16px;
            color: #2c3e50;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid #2c3e50;
            padding-bottom: 5px;
            margin-bottom: 15px;
            font-weight: bold;
        }}

        .summary {{
            text-align: justify;
            font-size: 11px;
            line-height: 1.5;
        }}

        .skills {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            font-size: 11px;
        }}

        .skill-tag {{
            background: #ecf0f1;
            padding: 4px 10px;
            border-radius: 3px;
            color: #2c3e50;
        }}

        .job {{
            margin-bottom: 20px;
            page-break-inside: avoid;
        }}

        .job-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }}

        .job-title {{
            font-size: 13px;
            font-weight: bold;
            color: #2c3e50;
        }}

        .job-company {{
            font-size: 12px;
            color: #555;
        }}

        .job-dates {{
            font-size: 11px;
            color: #777;
            font-style: italic;
        }}

        .job-bullets {{
            list-style: none;
            margin-top: 8px;
            margin-left: 15px;
        }}

        .job-bullets li {{
            font-size: 11px;
            margin-bottom: 6px;
            padding-left: 15px;
            position: relative;
        }}

        .job-bullets li:before {{
            content: "▪";
            position: absolute;
            left: 0;
            color: #2c3e50;
        }}

        .technologies {{
            font-size: 10px;
            color: #666;
            margin-top: 5px;
            font-style: italic;
        }}

        .education-item {{
            margin-bottom: 12px;
        }}

        .degree {{
            font-size: 12px;
            font-weight: bold;
            color: #2c3e50;
        }}

        .institution {{
            font-size: 11px;
            color: #555;
        }}

        .certifications {{
            list-style: none;
        }}

        .certifications li {{
            font-size: 11px;
            margin-bottom: 5px;
            padding-left: 15px;
            position: relative;
        }}

        .certifications li:before {{
            content: "•";
            position: absolute;
            left: 0;
            color: #2c3e50;
        }}

        .print-button {{
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 24px;
            background: #2c3e50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }}

        .print-button:hover {{
            background: #34495e;
        }}

        @page {{
            margin: 0.5in;
        }}
    </style>
</head>
<body>
    <button class="print-button no-print" onclick="window.print()">🖨️ Print / Save as PDF</button>

    <!-- Header -->
    <div class="header">
        <h1>{resume.name}</h1>
        <div class="contact">
"""

        # Contact info
        contact_parts = [resume.email]
        if resume.phone:
            contact_parts.append(resume.phone)
        if resume.location:
            contact_parts.append(resume.location)
        html += " | ".join(contact_parts)

        if resume.linkedin or resume.github:
            html += "<br>"
            links = []
            if resume.linkedin:
                links.append(f'<a href="{resume.linkedin}">{resume.linkedin}</a>')
            if resume.github:
                links.append(f'<a href="{resume.github}">{resume.github}</a>')
            html += " | ".join(links)

        html += """
        </div>
    </div>
"""

        # Professional Summary
        if resume.professional_summary:
            html += f"""
    <div class="section">
        <div class="section-title">Professional Summary</div>
        <div class="summary">{self._escape_html(resume.professional_summary)}</div>
    </div>
"""

        # Technical Skills
        if resume.technical_skills:
            html += """
    <div class="section">
        <div class="section-title">Technical Skills</div>
        <div class="skills">
"""
            for skill in resume.technical_skills:
                html += f'            <span class="skill-tag">{self._escape_html(skill)}</span>\n'

            html += """        </div>
    </div>
"""

        # Professional Experience
        html += """
    <div class="section">
        <div class="section-title">Professional Experience</div>
"""

        for exp in resume.experience:
            # Handle both dict and object
            if isinstance(exp, dict):
                company = exp.get('company', '')
                title = exp.get('title', '')
                start_date = exp.get('start_date', '')
                end_date = exp.get('end_date') or 'Present'
                location = exp.get('location', '')
                bullets = exp.get('bullets', [])
                technologies = exp.get('technologies', [])
            else:
                company = exp.company
                title = exp.title
                start_date = exp.start_date
                end_date = exp.end_date or 'Present'
                location = exp.location or ''
                bullets = exp.bullets
                technologies = exp.technologies

            html += f"""
        <div class="job">
            <div class="job-header">
                <div>
                    <div class="job-title">{self._escape_html(title)}</div>
                    <div class="job-company">{self._escape_html(company)}</div>
                </div>
                <div class="job-dates">
                    {start_date} - {end_date}
                    {f" | {location}" if location else ""}
                </div>
            </div>
            <ul class="job-bullets">
"""
            for bullet in bullets:
                html += f'                <li>{self._escape_html(bullet)}</li>\n'

            html += '            </ul>\n'

            if technologies:
                html += f'            <div class="technologies">Technologies: {", ".join([self._escape_html(t) for t in technologies])}</div>\n'

            html += '        </div>\n'

        html += '    </div>\n'

        # Education
        if resume.education:
            html += """
    <div class="section">
        <div class="section-title">Education</div>
"""
            for edu in resume.education:
                if isinstance(edu, dict):
                    degree = edu.get('degree', '')
                    field = edu.get('field_of_study', '')
                    institution = edu.get('institution', '')
                    grad_date = edu.get('graduation_date', '')
                    gpa = edu.get('gpa', '')
                else:
                    degree = edu.degree
                    field = edu.field_of_study or ''
                    institution = edu.institution
                    grad_date = edu.graduation_date or ''
                    gpa = edu.gpa or ''

                html += f"""
        <div class="education-item">
            <div class="degree">{self._escape_html(degree)}{f" in {self._escape_html(field)}" if field else ""}</div>
            <div class="institution">{self._escape_html(institution)}{f" | {grad_date}" if grad_date else ""}</div>
            {f'<div class="institution">GPA: {gpa}</div>' if gpa else ''}
        </div>
"""
            html += '    </div>\n'

        # Certifications
        if resume.certifications:
            html += """
    <div class="section">
        <div class="section-title">Certifications</div>
        <ul class="certifications">
"""
            for cert in resume.certifications:
                html += f'            <li>{self._escape_html(cert)}</li>\n'

            html += """        </ul>
    </div>
"""

        html += """
</body>
</html>
"""

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return str(output_path)

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        if not text:
            return ""
        return (
            str(text)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#x27;')
        )
