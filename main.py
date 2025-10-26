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


def load_last_job_cache():
    """Load cached job details from last run."""
    cache_file = Path(".last_job_cache.json")
    if cache_file.exists():
        try:
            with open(cache_file, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "job_file": "current_job.txt",
        "company": "",
        "title": "",
        "industry": os.getenv("DEFAULT_INDUSTRY", "healthcare"),
    }


def save_last_job_cache(job_file, company, title, industry):
    """Save job details for next run."""
    cache_file = Path(".last_job_cache.json")
    cache_data = {
        "job_file": job_file,
        "company": company,
        "title": title,
        "industry": industry,
    }
    with open(cache_file, "w") as f:
        json.dump(cache_data, f, indent=2)


def get_job_details(cache):
    """Get job details from user, using cache as defaults."""
    # Check if current_job.txt exists and has content
    current_job_file = Path("current_job.txt")
    use_current_job = False

    if current_job_file.exists():
        with open(current_job_file, "r") as f:
            content = f.read().strip()
            if content and not content.startswith("PASTE YOUR JOB DESCRIPTION"):
                # File has actual content
                click.echo("Found job description in current_job.txt")
                preview = content[:200] + "..." if len(content) > 200 else content
                click.echo(f"\nPreview:\n{preview}\n")
                use_current_job = click.confirm(
                    "Use this job description?", default=True
                )

    # Get job file path
    if use_current_job:
        job_file = "current_job.txt"
    else:
        job_file = click.prompt(
            "Path to job description file",
            type=click.Path(exists=True),
            default=cache.get("job_file", "current_job.txt"),
        )

    # Get company name (with cached default)
    company = click.prompt(
        "Company name",
        type=str,
        default=cache.get("company", ""),
    )

    # Get job title (with cached default)
    title = click.prompt(
        "Job title",
        type=str,
        default=cache.get("title", ""),
    )

    # Get industry (with cached default)
    industry = click.prompt(
        "Industry",
        type=str,
        default=cache.get("industry", os.getenv("DEFAULT_INDUSTRY", "healthcare")),
    )

    return job_file, company, title, industry


def interactive_mode():
    """Interactive mode - prompts user for what they want to do."""
    click.echo("🎯 Agentic Resume Tailoring System\n")

    # Load cached values from last run
    cache = load_last_job_cache()

    # Ask what the user wants to do
    action = click.prompt(
        "What would you like to do?",
        type=click.Choice(["tailor", "info", "exit"], case_sensitive=False),
        default="tailor",
    )

    if action == "exit":
        click.echo("Goodbye!")
        return

    if action == "info":
        # Show industry info
        industry = click.prompt(
            "Which industry?",
            type=str,
            default=os.getenv("DEFAULT_INDUSTRY", "healthcare"),
        )
        # Call the info command
        ctx = click.Context(info)
        ctx.invoke(info, industry=industry)
        return

    if action == "tailor":
        click.echo("\n📋 Let's tailor your resume!\n")

        # Check if we have cached values
        if cache.get("company") and cache.get("title"):
            click.echo(
                f"💾 Last job: {cache['title']} at {cache['company']}"
            )
            use_cached = click.confirm("Use these details again?", default=True)
            if use_cached:
                click.echo("✅ Using cached job details\n")
                job_file = cache.get("job_file", "current_job.txt")
                company = cache["company"]
                title = cache["title"]
                industry = cache.get("industry", os.getenv("DEFAULT_INDUSTRY", "healthcare"))
            else:
                # Get new details
                job_file, company, title, industry = get_job_details(cache)
        else:
            # No cache, get details
            job_file, company, title, industry = get_job_details(cache)

        # Save to cache for next time
        save_last_job_cache(job_file, company, title, industry)

        # Optional: base resume selection
        base_resume = None
        if click.confirm("\nUse a specific base resume?", default=False):
            base_resume = click.prompt("Base resume ID", type=str)

        # Optional: custom output path
        output = None
        if click.confirm("Specify custom output path?", default=False):
            output = click.prompt("Output file path", type=str)

        click.echo("\n" + "=" * 60)
        click.echo("Starting resume tailoring...")
        click.echo("=" * 60 + "\n")

        # Call the tailor command
        ctx = click.Context(tailor)
        ctx.invoke(
            tailor,
            job_file=job_file,
            company=company,
            title=title,
            base_resume=base_resume,
            industry=industry,
            output=output,
        )


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Agentic Resume Tailoring System"""
    # If no subcommand is provided, run interactive mode
    if ctx.invoked_subcommand is None:
        interactive_mode()


@cli.command()
@click.option(
    "--job",
    "--job-text",
    "job_file",
    required=True,
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
    help="Target industry (default: from .env or healthcare)",
)
@click.option(
    "--output",
    help="Output file path for tailored resume",
)
def tailor(job_file, company, title, base_resume, industry, output):
    """Tailor a resume for a specific job posting."""
    from src.utils.artifact_cache import ArtifactCache
    from src.models.job_posting import JobAnalysis

    click.echo(f"🎯 Agentic Resume Tailoring System")
    click.echo(f"Industry: {industry}")
    click.echo(f"Job: {title} at {company}\n")

    # Initialize artifact cache
    cache = ArtifactCache()

    # Load job description
    with open(job_file, "r") as f:
        description = f.read()

    # Get job hash for caching
    job_hash = cache.get_job_hash(description)

    # Create job posting
    job_posting = JobPosting(
        url="manual-entry",
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

    # Step 1: Analyze job posting (with caching)
    click.echo("📋 Analyzing job posting...")
    cached_analysis = cache.load_job_analysis(description)

    if cached_analysis:
        click.echo("   💾 Using cached job analysis")
        job_analysis = JobAnalysis.from_dict(cached_analysis)
    else:
        click.echo("   🔍 Running job analysis (will be cached)...")
        job_analyzer = JobAnalyzerAgent(industry_adapter=adapter)
        job_analysis = job_analyzer.run(job_posting)
        # Save to cache
        cache.save_job_analysis(description, job_analysis.to_dict())
        click.echo("   ✅ Job analysis cached for future runs")

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
        # Initialize matcher agent (not cached - always runs fresh)
        resume_matcher = ResumeMatcherAgent()
        matches = resume_matcher.run(job_analysis, resume_pool)
        if not matches:
            click.echo("   Error: No matching resumes found")
            return
        best_resume, best_metadata, score = matches[0]
        click.echo(f"   Best match: {best_metadata.resume_id} (score: {score:.2f})")

    # Step 4: Tailor the resume (with caching)
    click.echo("\n✍️  Tailoring resume...")
    cached_tailored = cache.load_tailored_resume(job_hash, best_metadata.resume_id)

    if cached_tailored:
        click.echo("   💾 Using cached tailored resume")
        tailored_resume = Resume.from_dict(cached_tailored["resume_data"])
        # diff info is also in cache but we'll regenerate for display
        diff = None  # Could reconstruct from cached_tailored["diff"]
    else:
        click.echo("   ✍️  Running resume tailoring (will be cached)...")
        tailoring_orchestrator = TailoringOrchestratorAgent(industry_adapter=adapter)
        tailored_resume, diff = tailoring_orchestrator.run(job_analysis, best_resume)
        # Save to cache
        cache.save_tailored_resume(
            job_hash,
            best_metadata.resume_id,
            tailored_resume.to_dict(),
            diff.to_dict() if diff else {},
        )
        click.echo("   ✅ Tailored resume cached for future runs")

    # Step 5: Quality review (with caching)
    click.echo("\n🔍 Reviewing tailored resume...")
    cached_review = cache.load_quality_review(job_hash, best_metadata.resume_id)

    if cached_review:
        click.echo("   💾 Using cached quality review")
        review = cached_review
    else:
        click.echo("   🔍 Running quality review (will be cached)...")
        quality_reviewer = QualityReviewerAgent(industry_adapter=adapter)
        review = quality_reviewer.run(job_analysis, tailored_resume)
        # Save to cache
        cache.save_quality_review(job_hash, best_metadata.resume_id, review)
        click.echo("   ✅ Quality review cached for future runs")
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
    """Load all resumes from the pool (supports JSON and PDF with caching)."""
    from src.utils.pdf_parser import PDFResumeParser
    from src.utils.resume_cache import ResumeCache

    pool = []

    if not resume_dir.exists():
        return pool

    # Initialize PDF parser and resume cache
    pdf_parser = PDFResumeParser()
    resume_cache = ResumeCache()

    # Load JSON resumes
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
            click.echo(f"   ⚠️  Warning: Could not load {resume_file}: {e}")

    # Load PDF resumes (with caching)
    for resume_file in resume_dir.glob("*.pdf"):
        resume_id = resume_file.stem

        try:
            # Check if we have a cached version
            cached_data = resume_cache.load_parsed_resume(resume_id, resume_file)

            if cached_data:
                click.echo(f"   📄 {resume_file.name}")
                click.echo(f"      💾 Using cached parse (file unchanged)")
                resume_data = cached_data
            else:
                click.echo(f"   📄 {resume_file.name}")
                click.echo(f"      🔍 Parsing PDF (will be cached)...")

                # Parse PDF to structured data using Claude
                resume_data = pdf_parser.parse_pdf_resume(resume_file)

                # Cache the parsed data
                resume_cache.save_parsed_resume(resume_id, resume_file, resume_data)
                click.echo(f"      ✅ Parsed and cached")

            # Convert to Resume object
            resume = Resume.from_dict(resume_data)

            # Create metadata
            metadata = ResumeMetadata(
                resume_id=resume_id,
                created_at=datetime.now(),
                file_path=str(resume_file),
            )

            pool.append((resume, metadata))

        except Exception as e:
            click.echo(f"   ⚠️  Warning: Could not parse PDF {resume_file}: {e}")

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


@cli.command()
@click.option(
    "--list",
    "list_cache",
    is_flag=True,
    help="List cached artifacts",
)
@click.option(
    "--clear",
    "clear_cache",
    is_flag=True,
    help="Clear all cached artifacts",
)
@click.option(
    "--stage",
    help="Specific stage to clear (job_analysis, tailored_resume, quality_review, resumes)",
)
def cache(list_cache, clear_cache, stage):
    """Manage artifact cache."""
    from src.utils.artifact_cache import ArtifactCache
    from src.utils.resume_cache import ResumeCache

    artifact_cache = ArtifactCache()
    resume_cache = ResumeCache()

    if list_cache:
        # Show artifact cache
        counts = artifact_cache.list_cached_artifacts()
        click.echo("\n📦 Cached Artifacts:\n")
        click.echo(f"   Job Analyses:      {counts['job_analysis']}")
        click.echo(f"   Resume Matches:    {counts['resume_matches']}")
        click.echo(f"   Tailored Resumes:  {counts['tailored_resume']}")
        click.echo(f"   Quality Reviews:   {counts['quality_review']}")
        total = sum(counts.values())
        click.echo(f"\n   Total: {total} artifacts")

        # Show parsed resume cache
        cached_resumes = resume_cache.list_cached_resumes()
        click.echo(f"\n📄 Parsed PDF Resumes: {len(cached_resumes)}")
        if cached_resumes:
            for resume_id, meta in cached_resumes.items():
                click.echo(f"   • {resume_id}")
                click.echo(f"     Cached: {meta.get('cached_at', 'unknown')}")
                click.echo(f"     Source: {Path(meta.get('source_file', '')).name}")

        click.echo()

    elif clear_cache:
        if stage == "resumes":
            # Clear only parsed resumes
            deleted = resume_cache.clear_cache()
            click.echo(f"✅ Cleared {deleted // 2} parsed resume(s)")  # Divide by 2 (data + meta files)
        elif stage:
            # Clear specific artifact stage
            deleted = artifact_cache.clear_cache(stage)
            click.echo(f"✅ Cleared {deleted} {stage} artifact(s)")
        else:
            # Clear all caches
            if click.confirm("Clear ALL cached artifacts and parsed resumes?"):
                artifact_deleted = artifact_cache.clear_cache()
                resume_deleted = resume_cache.clear_cache()
                click.echo(f"✅ Cleared {artifact_deleted} artifact(s)")
                click.echo(f"✅ Cleared {resume_deleted // 2} parsed resume(s)")
    else:
        # Show help
        click.echo("\nCache Management Commands:\n")
        click.echo("  --list              View all cached items")
        click.echo("  --clear             Clear all caches")
        click.echo("  --clear --stage X   Clear specific cache")
        click.echo("\nStages:")
        click.echo("  job_analysis        Job posting analyses")
        click.echo("  tailored_resume     Tailored resumes")
        click.echo("  quality_review      Quality reviews")
        click.echo("  resumes             Parsed PDF resumes")
        click.echo()


if __name__ == "__main__":
    cli()
