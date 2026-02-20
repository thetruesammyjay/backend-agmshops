"""
AGM Store Builder - Security Utilities

JWT token handling and password hashing utilities.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple
from jose import JWTError, jwt
import bcrypt

from app.core.config import settings
from app.core.exceptions import TokenError


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string
    """
    # Encode password to bytes and hash using bcrypt directly
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Payload data to encode in the token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "token_type": "access",
    })
    
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        data: Payload data to encode in the token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "token_type": "refresh",
    })
    
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_tokens(user_id: str) -> Dict[str, str]:
    """
    Create both access and refresh tokens for a user.
    
    Args:
        user_id: The user's unique identifier
        
    Returns:
        Dictionary containing accessToken and refreshToken
    """
    token_data = {"sub": user_id}
    
    return {
        "accessToken": create_access_token(token_data),
        "refreshToken": create_refresh_token(token_data),
    }


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string to decode
        
    Returns:
        Decoded token payload
        
    Raises:
        TokenError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError as e:
        raise TokenError(message="Invalid or expired token", details={"error": str(e)})


def verify_access_token(token: str) -> str:
    """
    Verify an access token and extract user ID.
    
    Args:
        token: JWT access token to verify
        
    Returns:
        User ID from the token
        
    Raises:
        TokenError: If token is invalid, expired, or not an access token
    """
    payload = decode_token(token)
    
    if payload.get("token_type") != "access":
        raise TokenError(message="Invalid token type")
    
    user_id = payload.get("sub")
    if not user_id:
        raise TokenError(message="Invalid token payload")
    
    return str(user_id)


def verify_refresh_token(token: str) -> str:
    """
    Verify a refresh token and extract user ID.
    
    Args:
        token: JWT refresh token to verify
        
    Returns:
        User ID from the token
        
    Raises:
        TokenError: If token is invalid, expired, or not a refresh token
    """
    payload = decode_token(token)
    
    if payload.get("token_type") != "refresh":
        raise TokenError(message="Invalid token type")
    
    user_id = payload.get("sub")
    if not user_id:
        raise TokenError(message="Invalid token payload")
    
    return str(user_id)


def create_password_reset_token(user_id: str) -> str:
    """
    Create a short-lived token for password reset.
    
    Args:
        user_id: The user's unique identifier
        
    Returns:
        Password reset token (expires in 10 minutes)
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    
    to_encode = {
        "sub": user_id,
        "exp": expire,
        "token_type": "password_reset",
    }
    
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def verify_password_reset_token(token: str) -> str:
    """
    Verify a password reset token.
    
    Args:
        token: Password reset token to verify
        
    Returns:
        User ID from the token
        
    Raises:
        TokenError: If token is invalid or expired
    """
    payload = decode_token(token)
    
    if payload.get("token_type") != "password_reset":
        raise TokenError(message="Invalid token type")
    
    user_id = payload.get("sub")
    if not user_id:
        raise TokenError(message="Invalid token payload")
    
    return str(user_id)
