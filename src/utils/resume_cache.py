"""Resume parsing cache to avoid re-parsing unchanged PDFs."""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict


class ResumeCache:
    """Cache parsed resume data to avoid re-parsing unchanged PDFs."""

    def __init__(self, cache_dir: Path = None):
        """
        Initialize resume cache.

        Args:
            cache_dir: Directory to store cache files (default: .cache/resumes/)
        """
        self.cache_dir = cache_dir or Path(".cache/resumes")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_hash(self, file_path: Path) -> str:
        """
        Calculate hash of file contents.

        Args:
            file_path: Path to file

        Returns:
            SHA256 hash of file contents (first 16 chars)
        """
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read in chunks for large files
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()[:16]

    def _get_cache_path(self, resume_id: str) -> Path:
        """Get cache file path for a resume."""
        return self.cache_dir / f"{resume_id}.json"

    def _get_metadata_path(self, resume_id: str) -> Path:
        """Get metadata file path for tracking file changes."""
        return self.cache_dir / f"{resume_id}_meta.json"

    def save_parsed_resume(
        self, resume_id: str, file_path: Path, resume_data: Dict
    ) -> None:
        """
        Save parsed resume data to cache.

        Args:
            resume_id: Unique ID for the resume (typically filename without extension)
            file_path: Path to original resume file
            resume_data: Parsed resume data (dict)
        """
        # Calculate file hash
        file_hash = self._get_file_hash(file_path)

        # Save resume data
        cache_path = self._get_cache_path(resume_id)
        cache_data = {
            "resume_id": resume_id,
            "source_file": str(file_path),
            "parsed_at": datetime.now().isoformat(),
            "file_hash": file_hash,
            "data": resume_data,
        }

        with open(cache_path, "w") as f:
            json.dump(cache_data, f, indent=2)

        # Save metadata for quick hash checking
        meta_path = self._get_metadata_path(resume_id)
        metadata = {
            "resume_id": resume_id,
            "source_file": str(file_path),
            "file_hash": file_hash,
            "file_size": file_path.stat().st_size,
            "last_modified": datetime.fromtimestamp(
                file_path.stat().st_mtime
            ).isoformat(),
            "cached_at": datetime.now().isoformat(),
        }

        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=2)

    def load_parsed_resume(
        self, resume_id: str, file_path: Path
    ) -> Optional[Dict]:
        """
        Load parsed resume from cache if available and file hasn't changed.

        Args:
            resume_id: Unique ID for the resume
            file_path: Path to original resume file

        Returns:
            Parsed resume data dict or None if cache miss or file changed
        """
        cache_path = self._get_cache_path(resume_id)
        meta_path = self._get_metadata_path(resume_id)

        # Check if cache exists
        if not cache_path.exists() or not meta_path.exists():
            return None

        try:
            # Load metadata
            with open(meta_path, "r") as f:
                metadata = json.load(f)

            # Quick check: file size
            current_size = file_path.stat().st_size
            if metadata["file_size"] != current_size:
                return None  # File changed

            # Full check: file hash
            current_hash = self._get_file_hash(file_path)
            if metadata["file_hash"] != current_hash:
                return None  # File changed

            # Cache is valid, load resume data
            with open(cache_path, "r") as f:
                cache_data = json.load(f)

            return cache_data["data"]

        except Exception:
            # If anything goes wrong, just return None (cache miss)
            return None

    def is_cached(self, resume_id: str, file_path: Path) -> bool:
        """
        Check if resume is cached and file hasn't changed.

        Args:
            resume_id: Unique ID for the resume
            file_path: Path to original resume file

        Returns:
            True if cached and unchanged, False otherwise
        """
        return self.load_parsed_resume(resume_id, file_path) is not None

    def get_cache_info(self, resume_id: str) -> Optional[Dict]:
        """
        Get cache metadata for a resume.

        Args:
            resume_id: Unique ID for the resume

        Returns:
            Metadata dict or None if not cached
        """
        meta_path = self._get_metadata_path(resume_id)
        if meta_path.exists():
            try:
                with open(meta_path, "r") as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def list_cached_resumes(self) -> Dict[str, Dict]:
        """
        List all cached resumes.

        Returns:
            Dict mapping resume_id to metadata
        """
        cached = {}

        for meta_file in self.cache_dir.glob("*_meta.json"):
            try:
                with open(meta_file, "r") as f:
                    metadata = json.load(f)
                    resume_id = metadata["resume_id"]
                    cached[resume_id] = metadata
            except Exception:
                continue

        return cached

    def clear_cache(self, resume_id: Optional[str] = None) -> int:
        """
        Clear resume cache.

        Args:
            resume_id: Specific resume to clear, or None to clear all

        Returns:
            Number of cache entries deleted
        """
        deleted = 0

        if resume_id:
            # Clear specific resume
            cache_path = self._get_cache_path(resume_id)
            meta_path = self._get_metadata_path(resume_id)

            if cache_path.exists():
                cache_path.unlink()
                deleted += 1
            if meta_path.exists():
                meta_path.unlink()
                deleted += 1
        else:
            # Clear all
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
                deleted += 1

        return deleted

    def invalidate_resume(self, resume_id: str) -> bool:
        """
        Force invalidate a cached resume.

        Args:
            resume_id: Resume to invalidate

        Returns:
            True if cache was cleared, False if not cached
        """
        count = self.clear_cache(resume_id)
        return count > 0
