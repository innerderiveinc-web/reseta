# RESETA™ Enterprise Auth & Role Switching Router
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.database import get_db
from backend.models import User
from backend.schemas import UserProfile, SwitchUserRequest

router = APIRouter(prefix="/api/auth", tags=["Authentication & Identity"])

# For interactive evaluation, allow switching among the seeded enterprise personas
ACTIVE_USER_ID = "user-emp-arjun"

@router.get("/users", response_model=List[UserProfile])
def get_available_users(db: Session = Depends(get_db)):
    """List available enterprise personas across all 7 RBAC roles"""
    users = db.query(User).filter(User.id.in_([
        "user-emp-arjun",
        "user-mgr-priya",
        "user-hr-kavita",
        "user-admin-rahul",
        "user-care-ananya",
        "user-audit-suresh"
    ])).all()
    return [
        UserProfile(
            id=u.id,
            organization_id=u.organization_id,
            department_id=u.department_id,
            team_id=u.team_id,
            email=u.email,
            full_name=u.full_name,
            role=u.role,
            preferred_language=u.preferred_language,
            avatar_url=u.avatar_url
        ) for u in users
    ]

@router.get("/me", response_model=UserProfile)
def get_current_user(db: Session = Depends(get_db)):
    global ACTIVE_USER_ID
    user = db.query(User).filter(User.id == ACTIVE_USER_ID).first()
    if not user:
        user = db.query(User).first()
    return UserProfile(
        id=user.id,
        organization_id=user.organization_id,
        department_id=user.department_id,
        team_id=user.team_id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        preferred_language=user.preferred_language,
        avatar_url=user.avatar_url
    )

@router.post("/switch-user", response_model=UserProfile)
def switch_active_user(req: SwitchUserRequest, db: Session = Depends(get_db)):
    global ACTIVE_USER_ID
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User persona not found")
    ACTIVE_USER_ID = user.id
    return UserProfile(
        id=user.id,
        organization_id=user.organization_id,
        department_id=user.department_id,
        team_id=user.team_id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        preferred_language=user.preferred_language,
        avatar_url=user.avatar_url
    )
