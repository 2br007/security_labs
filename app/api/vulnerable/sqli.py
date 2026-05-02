from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(prefix="/vulnerable/sqli", tags=["vulnerable"])


@router.get("/search")
def search_users_vulnerable(
    username: str,
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:
    """
    [VULNERABLE] SQL Injection

    This endpoint is vulnerable because it directly injects user input
    into a raw SQL query.

    Example attack:
        username=' OR 1=1--

    OWASP:
        A03:2021 - Injection
    """

    # VULNERABLE: string interpolation
    query = f"SELECT id, username, email FROM users WHERE username = '{username}'"

    result = db.execute(text(query))

    return [dict(row._mapping) for row in result]
