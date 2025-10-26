"""Artifact caching system for agent outputs."""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Any


class ArtifactCache:
    """Cache artifacts from each stage of the pipeline."""

    def __init__(self, cache_dir: Path = None):
        """
        Initialize artifact cache.

        Args:
            cache_dir: Directory to store cache files (default: .cache/)
        """
        self.cache_dir = cache_dir or Path(".cache")
        self.cache_dir.mkdir(exist_ok=True)

    def _get_content_hash(self, content: str) -> str:
        """Generate hash of content for cache key."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _get_cache_path(self, stage: str, job_hash: str) -> Path:
        """Get cache file path for a stage."""
        return self.cache_dir / f"{stage}_{job_hash}.json"

    def save_job_analysis(self, job_description: str, analysis_data: dict) -> None:
        """
        Save job analysis artifact.

        Args:
            job_description: Raw job description text
            analysis_data: JobAnalysis.to_dict() output
        """
        job_hash = self._get_content_hash(job_description)
        cache_path = self._get_cache_path("job_analysis", job_hash)

        artifact = {
            "stage": "job_analysis",
            "job_hash": job_hash,
            "cached_at": datetime.now().isoformat(),
            "job_description_preview": job_description[:200] + "...",
            "data": analysis_data,
        }

        with open(cache_path, "w") as f:
            json.dump(artifact, f, indent=2)

    def load_job_analysis(self, job_description: str) -> Optional[dict]:
        """
        Load cached job analysis if available.

        Args:
            job_description: Raw job description text

        Returns:
            JobAnalysis data dict or None if not cached
        """
        job_hash = self._get_content_hash(job_description)
        cache_path = self._get_cache_path("job_analysis", job_hash)

        if cache_path.exists():
            try:
                with open(cache_path, "r") as f:
                    artifact = json.load(f)
                return artifact["data"]
            except Exception:
                return None
        return None

    def save_resume_matches(
        self, job_hash: str, matches_data: list[dict]
    ) -> None:
        """
        Save resume matching results.

        Args:
            job_hash: Hash of job description
            matches_data: List of match results with scores
        """
        cache_path = self._get_cache_path("resume_matches", job_hash)

        artifact = {
            "stage": "resume_matches",
            "job_hash": job_hash,
            "cached_at": datetime.now().isoformat(),
            "data": matches_data,
        }

        with open(cache_path, "w") as f:
            json.dump(artifact, f, indent=2)

    def load_resume_matches(self, job_hash: str) -> Optional[list]:
        """
        Load cached resume matches.

        Args:
            job_hash: Hash of job description

        Returns:
            List of match results or None if not cached
        """
        cache_path = self._get_cache_path("resume_matches", job_hash)

        if cache_path.exists():
            try:
                with open(cache_path, "r") as f:
                    artifact = json.load(f)
                return artifact["data"]
            except Exception:
                return None
        return None

    def save_selected_resume(self, job_hash: str, resume_id: str, match_score: float) -> None:
        """
        Save which resume was selected for this job.

        Args:
            job_hash: Hash of job description
            resume_id: ID of selected resume
            match_score: Match score (0-1)
        """
        cache_path = self._get_cache_path("selected_resume", job_hash)

        artifact = {
            "stage": "selected_resume",
            "job_hash": job_hash,
            "cached_at": datetime.now().isoformat(),
            "resume_id": resume_id,
            "match_score": match_score,
        }

        with open(cache_path, "w") as f:
            json.dump(artifact, f, indent=2)

    def load_selected_resume(self, job_hash: str) -> Optional[dict]:
        """
        Load cached resume selection for this job.

        Args:
            job_hash: Hash of job description

        Returns:
            Dict with resume_id and match_score, or None if not cached
        """
        cache_path = self._get_cache_path("selected_resume", job_hash)

        if cache_path.exists():
            try:
                with open(cache_path, "r") as f:
                    artifact = json.load(f)
                return {
                    "resume_id": artifact["resume_id"],
                    "match_score": artifact["match_score"],
                }
            except Exception:
                return None
        return None

    def save_tailored_resume(
        self, job_hash: str, resume_id: str, tailored_data: dict, diff_data: dict
    ) -> None:
        """
        Save tailored resume artifact.

        Args:
            job_hash: Hash of job description
            resume_id: ID of base resume used
            tailored_data: Tailored Resume.to_dict() output
            diff_data: ResumeDiff.to_dict() output
        """
        cache_key = f"{job_hash}_{resume_id}"
        cache_path = self._get_cache_path("tailored_resume", cache_key)

        artifact = {
            "stage": "tailored_resume",
            "job_hash": job_hash,
            "base_resume_id": resume_id,
            "cached_at": datetime.now().isoformat(),
            "resume_data": tailored_data,
            "diff": diff_data,
        }

        with open(cache_path, "w") as f:
            json.dump(artifact, f, indent=2)

    def load_tailored_resume(
        self, job_hash: str, resume_id: str
    ) -> Optional[dict]:
        """
        Load cached tailored resume.

        Args:
            job_hash: Hash of job description
            resume_id: ID of base resume

        Returns:
            Artifact dict with resume_data and diff or None
        """
        cache_key = f"{job_hash}_{resume_id}"
        cache_path = self._get_cache_path("tailored_resume", cache_key)

        if cache_path.exists():
            try:
                with open(cache_path, "r") as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def save_quality_review(
        self, job_hash: str, resume_id: str, review_data: dict
    ) -> None:
        """
        Save quality review artifact.

        Args:
            job_hash: Hash of job description
            resume_id: ID of resume reviewed
            review_data: Review results dict
        """
        cache_key = f"{job_hash}_{resume_id}"
        cache_path = self._get_cache_path("quality_review", cache_key)

        artifact = {
            "stage": "quality_review",
            "job_hash": job_hash,
            "resume_id": resume_id,
            "cached_at": datetime.now().isoformat(),
            "data": review_data,
        }

        with open(cache_path, "w") as f:
            json.dump(artifact, f, indent=2)

    def load_quality_review(
        self, job_hash: str, resume_id: str
    ) -> Optional[dict]:
        """
        Load cached quality review.

        Args:
            job_hash: Hash of job description
            resume_id: ID of resume

        Returns:
            Review data dict or None
        """
        cache_key = f"{job_hash}_{resume_id}"
        cache_path = self._get_cache_path("quality_review", cache_key)

        if cache_path.exists():
            try:
                with open(cache_path, "r") as f:
                    artifact = json.load(f)
                return artifact["data"]
            except Exception:
                return None
        return None

    def list_cached_artifacts(self) -> dict:
        """
        List all cached artifacts.

        Returns:
            Dict with counts by stage
        """
        counts = {
            "job_analysis": 0,
            "resume_matches": 0,
            "selected_resume": 0,
            "tailored_resume": 0,
            "quality_review": 0,
        }

        for cache_file in self.cache_dir.glob("*.json"):
            stage = cache_file.stem.split("_")[0]
            if stage in counts:
                counts[stage] += 1

        return counts

    def clear_cache(self, stage: Optional[str] = None) -> int:
        """
        Clear cache files.

        Args:
            stage: Specific stage to clear, or None to clear all

        Returns:
            Number of files deleted
        """
        deleted = 0

        if stage:
            pattern = f"{stage}_*.json"
        else:
            pattern = "*.json"

        for cache_file in self.cache_dir.glob(pattern):
            cache_file.unlink()
            deleted += 1

        return deleted

    def get_job_hash(self, job_description: str) -> str:
        """
        Get hash for a job description (useful for external reference).

        Args:
            job_description: Raw job description text

        Returns:
            16-character hash
        """
        return self._get_content_hash(job_description)
