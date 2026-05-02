from typing import Optional

from fastapi import Header, HTTPException


def get_current_user_id(x_user_id: Optional[int] = Header(default=None)) -> int:
    """
    Simulate authentication via X-User-ID header.

    Args:
        x_user_id (Optional[int]): User ID from request header.

    Returns:
        int: Authenticated user ID.

    Raises:
        HTTPException: If header is missing.
    """
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="Missing X-User-ID header")

    return x_user_id
