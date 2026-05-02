from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.session import get_db

router = APIRouter(prefix="/vulnerable/auth", tags=["vulnerable"])


@router.post("/login")
def login_vulnerable(
    username: str,
    db: Session = Depends(get_db),
) -> Dict[str, str]:
    """
    [VULNERABLE] Authentication without rate limiting.

    Allows unlimited login attempts → enables brute force attacks.

    OWASP:
        A07:2021 - Identification and Authentication Failures
    """

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "login success",
        "user_id": str(user.id),
    }
