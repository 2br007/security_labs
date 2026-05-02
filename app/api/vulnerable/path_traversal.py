from pathlib import Path
from typing import Dict

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/vulnerable/path", tags=["vulnerable"])

BASE_DIR = Path("app/files")


@router.get("/read")
def read_file_vulnerable(filename: str) -> Dict[str, str]:
    """
    [VULNERABLE] Path Traversal

    This endpoint allows reading arbitrary files from the filesystem
    due to lack of path validation.

    Attack example:
        filename=../../../../etc/passwd

    OWASP:
        A05:2021 - Security Misconfiguration / Path Traversal
    """

    file_path = BASE_DIR / filename  # no validation

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    content = file_path.read_text()

    return {"content": content}
