# RESETA™ Enterprise Security & Token Engine
# RFC 7519 Compliant JSON Web Tokens & Password Hashing
import hmac
import hashlib
import base64
import json
import os
import time
import secrets
from typing import Optional, Dict, Any
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User
from backend.config import settings

# Unified JWT secret & algorithm from application settings
JWT_SECRET_KEY = settings.SECRET_KEY
JWT_ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_SECONDS = 86400 * 7 # 7 days validity

def hash_password(password: str, salt: Optional[str] = None) -> str:
    """PBKDF2-HMAC-SHA256 password hashing with salt"""
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
    return f"{salt}${key.hex()}"

def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Verify password against stored salt$hash"""
    if "$" not in stored_hash:
        return plain_password == stored_hash
    salt, key_hex = stored_hash.split("$", 1)
    computed = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100000)
    return hmac.compare_digest(computed.hex(), key_hex)

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

def _b64url_decode(data: str) -> bytes:
    rem = len(data) % 4
    if rem > 0:
        data += "=" * (4 - rem)
    return base64.urlsafe_b64decode(data.encode("utf-8"))

def create_access_token(user_id: str, role: str, org_id: str, expires_in: int = ACCESS_TOKEN_EXPIRE_SECONDS) -> str:
    """Generate RFC 7519 compliant JWT access token"""
    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}
    payload = {
        "sub": user_id,
        "role": role,
        "org_id": org_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + expires_in
    }
    h_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    p_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{h_b64}.{p_b64}"
    sig = hmac.new(JWT_SECRET_KEY.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256).digest()
    sig_b64 = _b64url_encode(sig)
    return f"{signing_input}.{sig_b64}"

def decode_access_token(token: str) -> Dict[str, Any]:
    """Validate token signature and expiry"""
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")
    h_b64, p_b64, sig_b64 = parts
    signing_input = f"{h_b64}.{p_b64}"
    expected_sig = _b64url_encode(hmac.new(JWT_SECRET_KEY.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256).digest())
    if not hmac.compare_digest(sig_b64, expected_sig):
        raise ValueError("Token signature verification failed")
    payload = json.loads(_b64url_decode(p_b64).decode("utf-8"))
    if payload.get("exp") and payload["exp"] < time.time():
        raise ValueError("Token expired")
    return payload

def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    FastAPI dependency resolving current user strictly via RFC 7519 JWT Bearer Token.
    CRITICAL SECURITY GUARANTEE:
    - Rejects missing, invalid, expired or unresolvable tokens with HTTP 401 Unauthorized.
    - Zero silent fallbacks to default or demo users.
    - Full cryptographic tenant and user resolution.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authentication required: Please provide a valid Bearer token in the Authorization header.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = authorization[7:].strip()
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token: missing subject claim.",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid or expired authentication token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User account does not exist or has been deactivated.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user

def require_roles(allowed_roles: list):
    """
    Dependency factory enforcing strict cryptographic Role-Based Access Control (RBAC).
    - Unauthenticated callers (missing or invalid Bearer token) receive 401 Unauthorized.
    - Authenticated users with insufficient privileges receive 403 Forbidden.
    - Zero global state leakage across concurrent server requests.
    """
    def role_checker(
        authorization: Optional[str] = Header(None),
        db: Session = Depends(get_db)
    ) -> User:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Authentication required: Please provide a valid Bearer token in the Authorization header.",
                headers={"WWW-Authenticate": "Bearer"}
            )

        token = authorization[7:].strip()
        try:
            payload = decode_access_token(token)
            user_id = payload.get("sub")
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid or expired authentication token: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"}
            )

        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        if not user:
            raise HTTPException(
                status_code=401,
                detail="User specified in authentication token does not exist or has been deactivated.",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Forbidden: Access requires one of {allowed_roles} roles. Current role: '{user.role}'."
            )
        return user
    return role_checker

