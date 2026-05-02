from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(prefix="/secure/sqli", tags=["secure"])


@router.get("/search")
def search_users_secure(
    username: str,
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    """
    Secure implementation of user search.

    Prevents SQL injection by using parameterized queries.

    Security:
        - Uses bound parameters
        - Prevents arbitrary SQL execution

    OWASP:
        A03:2021 - Injection (Fixed)
    """

    # SAFE: parameterized query
    query = text("SELECT id, username, email FROM users WHERE username = :username")

    result = db.execute(query, {"username": username})

    return [dict(row._mapping) for row in result]
