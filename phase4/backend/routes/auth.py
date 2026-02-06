"""
Authentication routes for user signup and login.

Provides endpoints for user registration and authentication,
returning JWT tokens for authenticated sessions.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import uuid

from models import User, UserSignup, UserLogin, AuthResponse
from database import get_session, settings

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str) -> str:
    """
    Create a JWT access token for a user.

    Args:
        user_id: User's unique identifier

    Returns:
        JWT token string
    """
    # Token expires in 7 days (matching Better Auth default)
    expire = datetime.utcnow() + timedelta(days=7)

    # Create JWT payload with userId (camelCase to match Better Auth convention)
    payload = {
        "userId": user_id,
        "exp": expire
    }

    # Encode JWT token
    token = jwt.encode(
        payload,
        settings.better_auth_secret,
        algorithm="HS256"
    )

    return token


@router.post("/signup", response_model=AuthResponse, status_code=201)
def signup(
    user_data: UserSignup,
    session: Session = Depends(get_session)
):
    """
    Register a new user account.

    Creates a new user with hashed password and returns a JWT token
    for immediate authentication.

    Args:
        user_data: User registration data (email, password)
        session: Database session (dependency)

    Returns:
        AuthResponse: JWT token and user info

    Raises:
        HTTPException: 409 if email already exists
        HTTPException: 400 if validation fails

    Example:
        POST /api/auth/signup
        Body: {"email": "user@example.com", "password": "securepass123"}
        Response: {
            "token": "eyJhbGc...",
            "user": {"id": "user-abc", "email": "user@example.com"}
        }
    """
    try:
        # Check if user already exists
        statement = select(User).where(User.email == user_data.email)
        existing_user = session.exec(statement).first()

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="A user with this email already exists"
            )

        # Create new user with hashed password
        user_id = f"user-{uuid.uuid4()}"
        hashed_password = hash_password(user_data.password)

        new_user = User(
            id=user_id,
            email=user_data.email,
            hashed_password=hashed_password
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # Generate JWT token
        token = create_access_token(new_user.id)

        return AuthResponse(
            token=token,
            user={
                "id": new_user.id,
                "email": new_user.email
            }
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like 409)
        raise
    except Exception as e:
        # Catch any other exceptions and return proper JSON error
        print(f"Signup error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Signup failed: {str(e)}"
        )


@router.post("/login", response_model=AuthResponse)
def login(
    user_data: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Authenticate a user and return a JWT token.

    Verifies email and password, then returns a JWT token for
    authenticated API access.

    Args:
        user_data: User login credentials (email, password)
        session: Database session (dependency)

    Returns:
        AuthResponse: JWT token and user info

    Raises:
        HTTPException: 401 if credentials are invalid

    Example:
        POST /api/auth/login
        Body: {"email": "user@example.com", "password": "securepass123"}
        Response: {
            "token": "eyJhbGc...",
            "user": {"id": "user-abc", "email": "user@example.com"}
        }
    """
    try:
        # Find user by email
        statement = select(User).where(User.email == user_data.email)
        user = session.exec(statement).first()

        # Verify user exists and password is correct
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        # Generate JWT token
        token = create_access_token(user.id)

        return AuthResponse(
            token=token,
            user={
                "id": user.id,
                "email": user.email
            }
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like 401)
        raise
    except Exception as e:
        # Catch any other exceptions and return proper JSON error
        print(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Login failed: {str(e)}"
        )
