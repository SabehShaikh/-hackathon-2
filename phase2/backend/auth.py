"""
JWT authentication middleware for the Todo Backend API.

This module provides JWT token verification and user ID extraction
for protected endpoints.
"""

from fastapi import Header, HTTPException
from jose import JWTError, jwt
from database import settings


def get_current_user(authorization: str = Header(...)) -> str:
    """
    Extract and verify user ID from JWT token.

    This dependency verifies the JWT token from the Authorization header,
    validates its signature using the shared BETTER_AUTH_SECRET, and
    extracts the userId claim.

    Args:
        authorization: Authorization header value (format: "Bearer <token>")

    Returns:
        str: User ID extracted from JWT token payload

    Raises:
        HTTPException: 401 Unauthorized if token is missing, invalid, expired,
                       or doesn't contain userId claim

    Example:
        @app.get("/api/tasks")
        def get_tasks(user_id: str = Depends(get_current_user)):
            # user_id automatically extracted and verified
            return get_user_tasks(user_id)
    """
    try:
        # Extract token by removing "Bearer " prefix
        token = authorization.replace("Bearer ", "")

        # Decode and verify JWT token
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"]
        )

        # Extract user_id from payload (note: Better Auth uses "userId" camelCase)
        user_id = payload.get("userId")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )

        return user_id

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
