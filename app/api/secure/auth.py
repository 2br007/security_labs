from typing import Dict

from app.core.rate_limit import RateLimiter
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.session import get_db

router = APIRouter(prefix="/secure/auth", tags=["secure"])

limiter = RateLimiter(limit=3, window_seconds=60)


@router.post("/login")
def login_secure(
    request: Request,
    username: str,
    db: Session = Depends(get_db),
) -> Dict[str, str]:
    """
    Secure login with rate limiting.

    Prevents brute force attacks by limiting requests per client IP.

    Security:
        - Rate limiting per IP
        - Blocks repeated attempts
    """

    client_ip = request.client.host

    if not limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many requests",
        )

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "login success",
        "user_id": str(user.id),
    }
