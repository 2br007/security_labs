from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas import UserResponse
from app.core.security import get_current_user_id
from app.db.models import User
from app.db.session import get_db

router = APIRouter(prefix="/secure/users", tags=["secure"])


@router.get("/{user_id}", response_model=UserResponse)
def get_user_secure(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
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

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # CRITICAL FIX
    if user.id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )

    return user
