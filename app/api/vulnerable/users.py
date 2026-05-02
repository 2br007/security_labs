from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import UserResponse
from app.core.security import get_current_user_id
from app.db.models import User
from app.db.session import get_db

router = APIRouter(prefix="/vulnerable/users", tags=["vulnerable"])


@router.get("/{user_id}", response_model=UserResponse)
def get_user_vulnerable(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> User:
    """
    [VULNERABLE] Broken Object Level Authorization (BOLA)

    This endpoint allows any authenticated user to access
    any user's data by changing the user_id.

    OWASP:
        API1:2023 - Broken Object Level Authorization
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"error": "User not found"}

    return user
