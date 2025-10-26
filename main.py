#!/usr/bin/env python3
"""Main CLI entry point for the resume tailoring system."""

import click
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

from src.core.adapters import IndustryAdapter
from src.agents import (
    JobAnalyzerAgent,
    ResumeMatcherAgent,
    TailoringOrchestratorAgent,
    QualityReviewerAgent,
)
from src.models.job_posting import JobPosting
from src.models.resume import Resume, ResumeMetadata

# Load environment variables
load_dotenv()


@click.group()
def cli():
    """Agentic Resume Tailoring System"""
    pass


@cli.command()
@click.option(
    "--job-url",
    help="URL to job posting",
)
@click.option(
    "--job-text",
    help="Path to text file containing job description",
    type=click.Path(exists=True),
)
@click.option(
    "--company",
    required=True,
    help="Company name",
)
@click.option(
    "--title",
    required=True,
    help="Job title",
)
@click.option(
    "--base-resume",
    help="Base resume ID to use (default: best match)",
)
@click.option(
    "--industry",
    default=os.getenv("DEFAULT_INDUSTRY", "healthcare"),
    help="Target industry (default: healthcare)",
)
@click.option(
    "--output",
    help="Output file path for tailored resume",
)
def tailor(job_url, job_text, company, title, base_resume, industry, output):
    """Tailor a resume for a specific job posting."""
    click.echo(f"🎯 Agentic Resume Tailoring System")
    click.echo(f"Industry: {industry}")
    click.echo(f"Job: {title} at {company}\n")

    # Load job description
    if job_text:
        with open(job_text, "r") as f:
            description = f.read()
    else:
        # For now, require job text file
        # TODO: Implement web scraping
        click.echo("Error: --job-text is required (web scraping not yet implemented)")
        return

    # Create job posting
    job_posting = JobPosting(
        url=job_url or "manual-entry",
        company=company,
        title=title,
        description=description,
    )

    # Load industry adapter
    config_dir = Path("config/industries")
    try:
        adapter = IndustryAdapter.create(industry, config_dir, mcp_enabled=False)
        click.echo(f"✓ Loaded {adapter.config.display_name} industry configuration\n")
    except Exception as e:
        click.echo(f"Error loading industry config: {e}")
        return

    # Initialize agents
    click.echo("🤖 Initializing agents...")
    job_analyzer = JobAnalyzerAgent(industry_adapter=adapter)
    resume_matcher = ResumeMatcherAgent()
    tailoring_orchestrator = TailoringOrchestratorAgent(industry_adapter=adapter)
    quality_reviewer = QualityReviewerAgent(industry_adapter=adapter)

    # Step 1: Analyze job posting
    click.echo("\n📋 Analyzing job posting...")
    job_analysis = job_analyzer.run(job_posting)
    click.echo(f"   Role: {job_analysis.role_type} ({job_analysis.seniority})")
    click.echo(f"   Required skills: {', '.join(job_analysis.required_skills[:5])}...")

    # Step 2: Load resume pool and match
    click.echo("\n📚 Loading resume pool...")
    resume_pool_dir = Path("resume_pool/base_resumes")
    resume_pool = load_resume_pool(resume_pool_dir)

    if not resume_pool:
        click.echo("   ⚠️  No base resumes found in pool")
        click.echo(
            f"   Please add resumes to {resume_pool_dir} (see example_resume.json)"
        )
        return

    click.echo(f"   Found {len(resume_pool)} base resume(s)")

    # Step 3: Match or select specific resume
    if base_resume:
        # Find specific resume
        selected = next(
            (r for r in resume_pool if r[1].resume_id == base_resume), None
        )
        if not selected:
            click.echo(f"Error: Resume '{base_resume}' not found")
            return
        best_resume, best_metadata, score = selected[0], selected[1], 1.0
    else:
        click.echo("\n🎯 Matching resumes to job...")
        matches = resume_matcher.run(job_analysis, resume_pool)
        if not matches:
            click.echo("   Error: No matching resumes found")
            return
        best_resume, best_metadata, score = matches[0]
        click.echo(f"   Best match: {best_metadata.resume_id} (score: {score:.2f})")

    # Step 4: Tailor the resume
    click.echo("\n✍️  Tailoring resume...")
    tailored_resume, diff = tailoring_orchestrator.run(job_analysis, best_resume)

    # Step 5: Quality review
    click.echo("\n🔍 Reviewing tailored resume...")
    review = quality_reviewer.run(job_analysis, tailored_resume)
    click.echo(f"   Overall score: {review.get('overall_score', 'N/A')}/10")
    click.echo(
        f"   Interview likelihood: {review.get('interview_likelihood', 'N/A')}"
    )

    if review.get("strengths"):
        click.echo("\n   ✅ Strengths:")
        for strength in review["strengths"][:3]:
            click.echo(f"      • {strength}")

    if review.get("suggestions"):
        click.echo("\n   💡 Suggestions:")
        for suggestion in review["suggestions"][:3]:
            click.echo(f"      • {suggestion}")

    # Step 6: Save tailored resume
    if not output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_company = company.replace(" ", "_").lower()
        output = f"resume_pool/tailored_resumes/{timestamp}_{safe_company}.json"

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save resume
    with open(output_path, "w") as f:
        json.dump(tailored_resume.to_dict(), f, indent=2)

    # Save metadata
    metadata = ResumeMetadata(
        resume_id=f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_company}",
        created_at=datetime.now(),
        base_resume_id=best_metadata.resume_id,
        job_posting_url=job_posting.url,
        company=company,
        job_title=title,
        target_role=job_analysis.role_type,
        target_industry=industry,
        key_skills_highlighted=job_analysis.required_skills[:10],
        ats_optimized=True,
        match_score=score,
        file_path=str(output_path),
    )

    metadata_path = output_path.parent.parent / "metadata" / f"{metadata.resume_id}.json"
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    with open(metadata_path, "w") as f:
        json.dump(metadata.to_dict(), f, indent=2)

    click.echo(f"\n✅ Tailored resume saved to: {output_path}")
    click.echo(f"✅ Metadata saved to: {metadata_path}")
    click.echo("\n🎉 Done!")


def load_resume_pool(resume_dir: Path) -> list:
    """Load all resumes from the pool."""
    pool = []

    if not resume_dir.exists():
        return pool

    for resume_file in resume_dir.glob("*.json"):
        if resume_file.name.startswith("example_"):
            continue

        try:
            with open(resume_file, "r") as f:
                data = json.load(f)

            resume = Resume.from_dict(data)

            # Create basic metadata
            metadata = ResumeMetadata(
                resume_id=resume_file.stem,
                created_at=datetime.now(),
                file_path=str(resume_file),
            )

            pool.append((resume, metadata))
        except Exception as e:
            click.echo(f"Warning: Could not load {resume_file}: {e}")

    return pool


@cli.command()
@click.option(
    "--industry",
    default="healthcare",
    help="Industry to show info for",
)
def info(industry):
    """Show industry configuration information."""
    config_dir = Path("config/industries")

    try:
        adapter = IndustryAdapter.create(industry, config_dir)
        config = adapter.config

        click.echo(f"\n📊 {config.display_name}")
        click.echo(f"{config.description}\n")

        click.echo(f"🎯 Priority Keywords ({len(config.priority_keywords)}):")
        for kw in config.priority_keywords[:10]:
            click.echo(f"   • {kw}")

        click.echo(f"\n🔧 High-Priority Skills:")
        for skill in config.get_high_priority_skills()[:15]:
            click.echo(f"   • {skill}")

        click.echo(f"\n💼 Primary Roles:")
        for role in config.primary_roles[:5]:
            click.echo(f"   • {role}")

    except Exception as e:
        click.echo(f"Error: {e}")


if __name__ == "__main__":
    cli()
