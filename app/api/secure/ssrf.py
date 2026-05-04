import ipaddress
import socket
from typing import Any
from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, HTTPException

ALLOWED_HOSTS = {"example.com", "api.github.com"}

router = APIRouter(prefix="/secure/ssrf", tags=["secure"])


def is_private_ip(host: str) -> bool:
    """
    Resolve hostname and check if it's private/internal.
    """
    try:
        ip = socket.gethostbyname(host)
        ip_obj = ipaddress.ip_address(ip)

        return (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_reserved
        )
    except Exception:
        return True  # fail closed


def validate_url(url: str) -> None:
    """
    Validate URL to prevent SSRF.
    """
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="URL not allowed")

    if not parsed.hostname:
        raise HTTPException(status_code=400, detail="URL not allowed")

    if is_private_ip(parsed.hostname):
        raise HTTPException(status_code=400, detail="URL not allowed")

    if parsed.hostname not in ALLOWED_HOSTS:
        raise HTTPException(status_code=400, detail="URL not allowed")


@router.get("/fetch")
async def fetch_url_secure(url: str) -> Any:
    """
    [SECURE] SSRF-protected endpoint.

    - Blocks internal IPs
    - Blocks localhost
    - Allows only http/https
    """

    validate_url(url)

    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(url)

    return {
        "status_code": response.status_code,
        "content": response.text,
    }
