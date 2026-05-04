from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas import UserResponse
from app.core.deps import get_current_user
from app.db.models import User
from app.db.session import get_db

router = APIRouter(prefix="/secure/users", tags=["secure"])


@router.get("/{user_id}", response_model=UserResponse)
def get_user_secure(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """
    Secure implementation of user retrieval.

    Prevents BOLA by enforcing that users can only access
    their own resources.

    Security:
        - Validates ownership
        - Returns 403 for unauthorized access

    OWASP:
        API1:2023 - Broken Object Level Authorization (Fixed)
    """
    user: User | None = db.query(User).filter(User.id == user_id).first()

    if not current_user:
        raise HTTPException(status_code=401)

    if current_user.id != user_id:
        raise HTTPException(status_code=403)

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
