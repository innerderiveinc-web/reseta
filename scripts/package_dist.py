#!/usr/bin/env python3
"""
RESETA™ Enterprise Distribution Packager
Builds production-ready, clean distribution zip archives into the dist/ directory.
Excludes git, databases, virtualenvs, bytecode, test caches, and macOS metadata.
"""
import os
import sys
import zipfile
import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIST_DIR = os.path.join(PROJECT_ROOT, "dist")

EXCLUDE_PATTERNS = [
    ".git",
    ".venv",
    ".pytest_cache",
    "__pycache__",
    ".DS_Store",
    "reseta.db",
    "reseta.db-shm",
    "reseta.db-wal",
    "dist",
    "build",
    ".coverage",
    "htmlcov"
]

def should_exclude(rel_path: str) -> bool:
    parts = rel_path.replace("\\", "/").split("/")
    for part in parts:
        for pattern in EXCLUDE_PATTERNS:
            if part == pattern or part.endswith(pattern):
                return True
    return False

def build_package(output_filename: str = "reseta_enterprise_distribution.zip") -> str:
    os.makedirs(DIST_DIR, exist_ok=True)
    out_path = os.path.join(DIST_DIR, output_filename)

    if os.path.exists(out_path):
        os.remove(out_path)

    print(f"[+] Creating production distribution archive: {output_filename} ...")
    file_count = 0

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if not should_exclude(os.path.relpath(os.path.join(root, d), PROJECT_ROOT))]
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, PROJECT_ROOT)

                if should_exclude(rel_path) or rel_path.endswith(".zip"):
                    continue

                zipf.write(full_path, rel_path)
                file_count += 1

    size_kb = round(os.path.getsize(out_path) / 1024, 2)
    print(f"[✓] Package built successfully: {out_path} ({size_kb} KB, {file_count} files)")
    return out_path

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "reseta_enterprise_distribution.zip"
    build_package(name)
