import os
import re
from typing import Iterable

from fastapi import HTTPException, status, UploadFile


MAX_FILE_SIZE = int(
    os.getenv("MAX_FILE_SIZE", str(10 * 1024 * 1024)))  # 10MB default
ALLOWED_FILE_TYPES = set(
    (os.getenv("ALLOWED_FILE_TYPES", "pdf,docx,txt").split(","))
)


def sanitize_filename(filename: str) -> str:
    """Return a safe filename by stripping path separators and unsafe chars."""
    filename = os.path.basename(filename)
    filename = re.sub(r"[^A-Za-z0-9._-]", "_", filename)
    return filename


def ensure_uploads_dir(path: str = "uploads") -> str:
    os.makedirs(path, exist_ok=True)
    return path


def assert_allowed_extension(filename: str) -> None:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in {e.strip().lower() for e in ALLOWED_FILE_TYPES}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed: {', '.join(sorted(ALLOWED_FILE_TYPES))}",
        )


def read_limited(upload_file: UploadFile, limit: int) -> bytes:
    data = upload_file.file.read(limit + 1)
    if len(data) > limit:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max {limit} bytes",
        )
    return data


def save_upload_file(upload_file: UploadFile, target_dir: str = "uploads") -> str:
    ensure_uploads_dir(target_dir)
    safe_name = sanitize_filename(upload_file.filename or "upload.bin")
    assert_allowed_extension(safe_name)
    data = read_limited(upload_file, MAX_FILE_SIZE)
    target_path = os.path.join(target_dir, safe_name)
    with open(target_path, "wb") as f:
        f.write(data)
    return target_path
