from typing import Any
from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/secure/ssrf", tags=["secure"])

ALLOWED_HOSTS = ("example.com",)


def is_allowed_url(url: str) -> bool:
    """
    Validate that URL is allowed.

    Blocks:
        - localhost
        - internal IPs
        - non-allowed domains
    """
    parsed = urlparse(url)

    if parsed.hostname is None:
        return False

    if parsed.hostname in ("localhost", "127.0.0.1"):
        return False

    if parsed.hostname not in ALLOWED_HOSTS:
        return False

    return True


@router.get("/fetch")
async def fetch_url_secure(url: str) -> Any:
    """
    Secure implementation of URL fetching.

    Prevents SSRF via:
        - allowlist validation
        - blocking internal addresses

    OWASP:
        A10:2021 - SSRF (Fixed)
    """

    if not is_allowed_url(url):
        raise HTTPException(status_code=400, detail="URL not allowed")

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return {
        "status_code": response.status_code,
        "content": response.text,
    }
