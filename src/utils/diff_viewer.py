"""Resume diff viewer and change summary generator."""

import difflib
from typing import Dict, List, Tuple
from pathlib import Path
from datetime import datetime
from src.models.resume import Resume, ResumeDiff
from src.models.job_posting import JobAnalysis


class ResumeDiffViewer:
    """Generate visual diffs and change summaries for resume modifications."""

    def __init__(self):
        self.changes = []

    def generate_diff_summary(
        self,
        original_resume: Resume,
        tailored_resume: Resume,
        diff: ResumeDiff,
        job_analysis: JobAnalysis,
    ) -> Dict:
        """
        Generate comprehensive summary of changes and their importance.

        Returns:
            Dict with:
                - summary: Overall change summary
                - section_changes: Changes by section
                - importance_score: How critical changes are (0-10)
                - reasoning: Why changes matter
        """
        changes_by_section = {
            "summary": [],
            "experience": [],
            "skills": [],
            "education": [],
            "other": [],
        }

        total_changes = 0

        # Analyze summary changes
        if diff.summary_changed:
            changes_by_section["summary"].append({
                "type": "modified",
                "description": "Professional summary rewritten to target role",
                "importance": "high",
                "reason": f"Aligns your background with {job_analysis.role_type} requirements",
            })
            total_changes += 1

        # Analyze experience changes
        if diff.bullets_modified:
            exp_changes = len(diff.bullets_modified)
            changes_by_section["experience"].append({
                "type": "enhanced",
                "description": f"{exp_changes} bullet points enhanced with metrics and impact",
                "importance": "high",
                "reason": "Demonstrates measurable achievements that match job responsibilities",
            })
            total_changes += exp_changes

        # Analyze skills changes
        if diff.skills_added:
            changes_by_section["skills"].append({
                "type": "added",
                "description": f"{len(diff.skills_added)} skills added: {', '.join(diff.skills_added[:5])}",
                "importance": "critical",
                "reason": "Addresses ATS keywords and required qualifications",
            })
            total_changes += len(diff.skills_added)

        if diff.skills_removed:
            changes_by_section["skills"].append({
                "type": "removed",
                "description": f"{len(diff.skills_removed)} less relevant skills deprioritized",
                "importance": "medium",
                "reason": "Focuses resume on job-specific requirements",
            })

        if diff.skills_reordered:
            changes_by_section["skills"].append({
                "type": "reordered",
                "description": "Skills reordered by relevance to job posting",
                "importance": "medium",
                "reason": "Prioritizes most important skills for ATS and hiring manager",
            })

        # Calculate importance score
        importance_score = min(10, total_changes + (3 if diff.summary_changed else 0))

        return {
            "summary": f"Made {total_changes} strategic changes to target {job_analysis.role_type} role",
            "section_changes": changes_by_section,
            "total_changes": total_changes,
            "importance_score": importance_score,
            "reasoning": self._generate_overall_reasoning(job_analysis, diff),
        }

    def _generate_overall_reasoning(
        self, job_analysis: JobAnalysis, diff: ResumeDiff
    ) -> str:
        """Generate overall reasoning for why changes matter."""
        reasons = []

        if diff.summary_changed:
            reasons.append(
                f"Repositioned your profile to align with {job_analysis.seniority} {job_analysis.role_type} requirements"
            )

        if diff.bullets_modified:
            reasons.append(
                "Enhanced achievement statements to demonstrate impact and match key responsibilities"
            )

        if diff.skills_added:
            reasons.append(
                "Added critical keywords to pass ATS screening and match job requirements"
            )

        if diff.keywords_integrated:
            reasons.append(
                f"Integrated {len(diff.keywords_integrated)} industry-specific terms to optimize for ATS"
            )

        return " • ".join(reasons) if reasons else "Minor refinements to improve presentation"

    def generate_cli_diff(
        self,
        original_resume: Resume,
        tailored_resume: Resume,
        diff: ResumeDiff,
    ) -> str:
        """
        Generate colored CLI diff output.

        Returns:
            Formatted string with color codes for terminal display
        """
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
        from rich.text import Text
        from rich.columns import Columns
        from io import StringIO

        console = Console(file=StringIO(), force_terminal=True, width=120)
        output = []

        # Header
        output.append("\n" + "=" * 120)
        output.append("📊 RESUME CHANGES SUMMARY")
        output.append("=" * 120 + "\n")

        # Summary section
        if diff.summary_changed:
            output.append("📝 PROFESSIONAL SUMMARY")
            output.append("-" * 120)
            output.append("\n❌ BEFORE:")
            output.append(f"   {diff.original_summary[:200]}...")
            output.append("\n✅ AFTER:")
            output.append(f"   {diff.new_summary[:200]}...")
            output.append("\n")

        # Experience section
        if diff.bullets_modified:
            output.append("💼 EXPERIENCE ENHANCEMENTS")
            output.append("-" * 120)
            for change in diff.bullets_modified[:5]:  # Show top 5
                pos_idx = change.get("position_index", 0)
                output.append(f"\nPosition {pos_idx + 1}:")
                output.append(f"❌ BEFORE: {change['original']}")
                output.append(f"✅ AFTER:  {change['new']}")
            if len(diff.bullets_modified) > 5:
                output.append(f"\n... and {len(diff.bullets_modified) - 5} more bullet points enhanced")
            output.append("\n")

        # Skills section
        if diff.skills_added or diff.skills_removed:
            output.append("🔧 SKILLS UPDATES")
            output.append("-" * 120)
            if diff.skills_added:
                output.append(f"✅ ADDED: {', '.join(diff.skills_added)}")
            if diff.skills_removed:
                output.append(f"❌ REMOVED: {', '.join(diff.skills_removed)}")
            output.append("\n")

        # Keywords integrated
        if diff.keywords_integrated:
            output.append("🔑 ATS KEYWORDS INTEGRATED")
            output.append("-" * 120)
            output.append(f"   {', '.join(diff.keywords_integrated[:15])}")
            if len(diff.keywords_integrated) > 15:
                output.append(f"   ... and {len(diff.keywords_integrated) - 15} more")
            output.append("\n")

        return "\n".join(output)

    def generate_html_diff(
        self,
        original_resume: Resume,
        tailored_resume: Resume,
        diff: ResumeDiff,
        job_analysis: JobAnalysis,
        output_path: Path,
    ) -> str:
        """
        Generate interactive HTML diff report.

        Args:
            original_resume: Original resume
            tailored_resume: Tailored resume
            diff: Diff object with tracked changes
            job_analysis: Job analysis for context
            output_path: Where to save HTML file

        Returns:
            Path to generated HTML file
        """
        # Generate change summary
        summary = self.generate_diff_summary(
            original_resume, tailored_resume, diff, job_analysis
        )

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Changes - {tailored_resume.name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 8px 8px 0 0;
        }}

        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}

        .header .meta {{
            opacity: 0.9;
            font-size: 14px;
        }}

        .summary-section {{
            padding: 40px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
        }}

        .summary-card {{
            background: white;
            padding: 24px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }}

        .summary-card h2 {{
            font-size: 20px;
            margin-bottom: 12px;
            color: #667eea;
        }}

        .summary-card .score {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 18px;
        }}

        .changes-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            padding: 40px;
        }}

        .change-section {{
            background: #f8f9fa;
            padding: 24px;
            border-radius: 8px;
        }}

        .change-section h3 {{
            font-size: 18px;
            margin-bottom: 20px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .change-item {{
            background: white;
            padding: 16px;
            border-radius: 6px;
            margin-bottom: 16px;
            border-left: 3px solid #ddd;
        }}

        .change-item.critical {{
            border-left-color: #e74c3c;
        }}

        .change-item.high {{
            border-left-color: #f39c12;
        }}

        .change-item.medium {{
            border-left-color: #3498db;
        }}

        .change-item.low {{
            border-left-color: #95a5a6;
        }}

        .change-type {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}

        .change-type.added {{
            background: #d4edda;
            color: #155724;
        }}

        .change-type.modified {{
            background: #fff3cd;
            color: #856404;
        }}

        .change-type.removed {{
            background: #f8d7da;
            color: #721c24;
        }}

        .diff-view {{
            padding: 40px;
        }}

        .diff-section {{
            margin-bottom: 40px;
        }}

        .diff-section h3 {{
            font-size: 20px;
            margin-bottom: 20px;
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 8px;
        }}

        .diff-block {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}

        .diff-before, .diff-after {{
            padding: 20px;
            border-radius: 6px;
            font-size: 14px;
            line-height: 1.8;
        }}

        .diff-before {{
            background: #ffebee;
            border: 1px solid #ffcdd2;
        }}

        .diff-after {{
            background: #e8f5e9;
            border: 1px solid #c8e6c9;
        }}

        .diff-label {{
            font-weight: bold;
            margin-bottom: 10px;
            text-transform: uppercase;
            font-size: 12px;
            opacity: 0.7;
        }}

        .skill-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 12px;
        }}

        .skill-tag {{
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 13px;
            font-weight: 500;
        }}

        .skill-tag.added {{
            background: #d4edda;
            color: #155724;
        }}

        .skill-tag.removed {{
            background: #f8d7da;
            color: #721c24;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .stat-card {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 6px;
        }}

        .stat-number {{
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
        }}

        .stat-label {{
            font-size: 14px;
            color: #666;
            margin-top: 8px;
        }}

        .bullet-change {{
            margin-bottom: 24px;
            padding: 16px;
            background: #fafafa;
            border-radius: 6px;
        }}

        .bullet-label {{
            font-weight: bold;
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}

        .bullet-text {{
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 8px;
        }}

        .bullet-text.before {{
            background: #fff3cd;
            border-left: 3px solid #ffc107;
        }}

        .bullet-text.after {{
            background: #d4edda;
            border-left: 3px solid #28a745;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>📊 Resume Transformation Report</h1>
            <div class="meta">
                <p>{tailored_resume.name} • {job_analysis.role_type} at {job_analysis.company or 'Target Company'}</p>
                <p>Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
        </div>

        <!-- Summary Section -->
        <div class="summary-section">
            <div class="summary-card">
                <h2>Overall Impact</h2>
                <p style="font-size: 16px; margin: 16px 0;">{summary['summary']}</p>
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{summary['total_changes']}</div>
                        <div class="stat-label">Total Changes</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{summary['importance_score']}/10</div>
                        <div class="stat-label">Importance Score</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{len(diff.skills_added)}</div>
                        <div class="stat-label">Skills Added</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{len(diff.bullets_modified)}</div>
                        <div class="stat-label">Bullets Enhanced</div>
                    </div>
                </div>
            </div>

            <div class="summary-card">
                <h2>Why These Changes Matter</h2>
                <p style="font-size: 15px; line-height: 1.8;">{summary['reasoning']}</p>
            </div>
        </div>

        <!-- Changes Grid -->
        <div class="changes-grid">
"""

        # Add change items by section
        for section_name, changes in summary['section_changes'].items():
            if changes:
                section_emoji = {
                    "summary": "📝",
                    "experience": "💼",
                    "skills": "🔧",
                    "education": "🎓",
                    "other": "📌"
                }
                html_content += f"""
            <div class="change-section">
                <h3>{section_emoji.get(section_name, '📌')} {section_name.title()}</h3>
"""
                for change in changes:
                    html_content += f"""
                <div class="change-item {change['importance']}">
                    <span class="change-type {change['type']}">{change['type']}</span>
                    <p style="margin: 8px 0; font-weight: 500;">{change['description']}</p>
                    <p style="font-size: 13px; color: #666;">{change['reason']}</p>
                </div>
"""
                html_content += """
            </div>
"""

        html_content += """
        </div>

        <!-- Detailed Diff View -->
        <div class="diff-view">
"""

        # Professional Summary Diff
        if diff.summary_changed:
            html_content += f"""
            <div class="diff-section">
                <h3>📝 Professional Summary</h3>
                <div class="diff-block">
                    <div class="diff-before">
                        <div class="diff-label">❌ Before</div>
                        {self._escape_html(diff.original_summary)}
                    </div>
                    <div class="diff-after">
                        <div class="diff-label">✅ After</div>
                        {self._escape_html(diff.new_summary)}
                    </div>
                </div>
            </div>
"""

        # Experience Bullets Diff
        if diff.bullets_modified:
            html_content += """
            <div class="diff-section">
                <h3>💼 Experience Enhancements</h3>
"""
            for i, change in enumerate(diff.bullets_modified[:10]):  # Show first 10
                html_content += f"""
                <div class="bullet-change">
                    <div class="bullet-label">Bullet Point {i + 1}</div>
                    <div class="bullet-text before">
                        ❌ {self._escape_html(change['original'])}
                    </div>
                    <div class="bullet-text after">
                        ✅ {self._escape_html(change['new'])}
                    </div>
                </div>
"""
            if len(diff.bullets_modified) > 10:
                html_content += f"""
                <p style="text-align: center; color: #666; margin-top: 20px;">
                    ... and {len(diff.bullets_modified) - 10} more bullet points enhanced
                </p>
"""
            html_content += """
            </div>
"""

        # Skills Changes
        if diff.skills_added or diff.skills_removed:
            html_content += """
            <div class="diff-section">
                <h3>🔧 Skills Updates</h3>
"""
            if diff.skills_added:
                html_content += """
                <div style="margin-bottom: 20px;">
                    <div class="bullet-label">✅ Skills Added (ATS Keywords)</div>
                    <div class="skill-list">
"""
                for skill in diff.skills_added:
                    html_content += f"""
                        <span class="skill-tag added">{self._escape_html(skill)}</span>
"""
                html_content += """
                    </div>
                </div>
"""

            if diff.skills_removed:
                html_content += """
                <div>
                    <div class="bullet-label">❌ Skills Deprioritized</div>
                    <div class="skill-list">
"""
                for skill in diff.skills_removed:
                    html_content += f"""
                        <span class="skill-tag removed">{self._escape_html(skill)}</span>
"""
                html_content += """
                    </div>
                </div>
"""
            html_content += """
            </div>
"""

        html_content += """
        </div>
    </div>
</body>
</html>
"""

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(output_path)

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        if not text:
            return ""
        return (
            text.replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#x27;')
        )
