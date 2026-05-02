from typing import Any

import httpx
from fastapi import APIRouter

router = APIRouter(prefix="/vulnerable/ssrf", tags=["vulnerable"])


@router.get("/fetch")
async def fetch_url_vulnerable(url: str) -> Any:
    """
    [VULNERABLE] Server-Side Request Forgery (SSRF)

    This endpoint fetches ANY user-supplied URL without validation.

    Attackers can:
        - Access internal services
        - Reach cloud metadata endpoints
        - Scan internal network

    Example:
        /fetch?url=http://localhost:8000/internal/metadata

    OWASP:
        A10:2021 - SSRF
    """

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return {
        "status_code": response.status_code,
        "content": response.text,
    }
