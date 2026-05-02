from pathlib import Path
from typing import Dict

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/secure/path", tags=["secure"])

BASE_DIR = Path("app/files").resolve()


@router.get("/read")
def read_file_secure(filename: str) -> Dict[str, str]:
    """
    Secure file reader.

    Prevents path traversal by enforcing that the resolved path
    stays within the allowed base directory.

    Security:
        - Uses path resolution
        - Blocks directory escape

    OWASP:
        A05:2021 - Path Traversal (Fixed)
    """

    file_path = (BASE_DIR / filename).resolve()

    # CRITICAL FIX
    if not str(file_path).startswith(str(BASE_DIR)):
        raise HTTPException(status_code=403, detail="Access denied")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    content = file_path.read_text()

    return {"content": content}
