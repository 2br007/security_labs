from typing import Dict

from fastapi import APIRouter

router = APIRouter(prefix="/internal", tags=["internal"])


@router.get("/metadata")
def get_metadata() -> Dict[str, str]:
    """
    Simulated internal metadata service.

    This represents sensitive internal-only data
    that should NOT be accessible externally.
    """
    return {
        "service": "internal-metadata",
        "secret_key": "SUPER_SECRET_KEY",
        "db_password": "postgres123",
    }
