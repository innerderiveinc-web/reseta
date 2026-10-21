# RESETA™ Enterprise SCIM 2.0 Protocol Router
# RFC 7643 & RFC 7644 Standard Enterprise Identity Management (Microsoft Entra ID, Okta, Workday)
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from backend.database import get_db
from backend.models import User, Department, Organization
from backend.security import decode_access_token

router = APIRouter(prefix="/api/scim/v2", tags=["SCIM 2.0 Identity Provisioning"])

def get_scim_admin(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    SCIM 2.0 Authentication & Tenant Scope Resolver (RFC 7644 Section 3.2).
    Requires a valid cryptographic Bearer token with SUPER_ADMIN or HR_ADMIN role.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="SCIM 2.0 authentication required: Missing or invalid Bearer token.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'}
        )
    token = authorization[7:].strip()
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        role = payload.get("role")
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"SCIM authentication failed: {str(e)}",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'}
        )

    admin = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not admin:
        raise HTTPException(
            status_code=401,
            detail="SCIM administrator account does not exist or has been disabled.",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'}
        )

    if admin.role not in ["SUPER_ADMIN", "HR_ADMIN"]:
        raise HTTPException(
            status_code=403,
            detail=f"Forbidden: SCIM 2.0 directory operations require SUPER_ADMIN or HR_ADMIN role. Current role: '{admin.role}'."
        )

    return admin

@router.get("/ServiceProviderConfig")
def get_service_provider_config():
    """RFC 7644 Service Provider Configuration (Public Discovery)"""
    return {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"],
        "documentationUri": "https://reseta.enterprise/docs/scim",
        "patch": {"supported": True},
        "bulk": {"supported": False, "maxOperations": 0, "maxPayloadSize": 0},
        "filter": {"supported": True, "maxResults": 100},
        "changePassword": {"supported": False},
        "sort": {"supported": False},
        "etag": {"supported": False},
        "authenticationSchemes": [
            {
                "name": "OAuth Bearer Token",
                "description": "Authentication scheme using the OAuth Bearer Standard",
                "specUri": "http://www.rfc-editor.org/info/rfc6750",
                "type": "oauthbearertoken",
                "primary": True
            }
        ]
    }

@router.get("/Users")
def list_scim_users(
    startIndex: int = 1,
    count: int = 50,
    db: Session = Depends(get_db),
    admin: User = Depends(get_scim_admin)
):
    """RFC 7644 SCIM 2.0 Users Collection Endpoint - Strictly Scoped to Authenticated Tenant"""
    query = db.query(User).filter(User.organization_id == admin.organization_id)
    total_results = query.count()
    users = query.offset(startIndex - 1).limit(count).all()

    resources = [
        {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": u.id,
            "userName": u.email,
            "name": {
                "formatted": u.full_name,
                "givenName": u.full_name.split()[0] if u.full_name else "",
                "familyName": u.full_name.split()[-1] if len(u.full_name.split()) > 1 else ""
            },
            "emails": [{"value": u.email, "primary": True}],
            "active": u.is_active,
            "roles": [{"value": u.role, "primary": True}],
            "meta": {
                "resourceType": "User",
                "created": u.created_at.isoformat() if u.created_at else "2026-01-01T00:00:00Z"
            }
        }
        for u in users
    ]

    return {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": total_results,
        "startIndex": startIndex,
        "itemsPerPage": len(resources),
        "Resources": resources
    }

@router.get("/Users/{user_id}")
def get_scim_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(get_scim_admin)
):
    """RFC 7644 SCIM 2.0 Single User Resource - Strictly Scoped to Authenticated Tenant"""
    u = db.query(User).filter(
        User.id == user_id,
        User.organization_id == admin.organization_id
    ).first()
    if not u:
        raise HTTPException(
            status_code=404,
            detail="SCIM Resource not found in authenticated organization tenant."
        )

    return {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": u.id,
        "userName": u.email,
        "name": {
            "formatted": u.full_name,
            "givenName": u.full_name.split()[0] if u.full_name else "",
            "familyName": u.full_name.split()[-1] if len(u.full_name.split()) > 1 else ""
        },
        "emails": [{"value": u.email, "primary": True}],
        "active": u.is_active,
        "roles": [{"value": u.role, "primary": True}],
        "meta": {
            "resourceType": "User",
            "created": u.created_at.isoformat() if u.created_at else "2026-01-01T00:00:00Z"
        }
    }

@router.get("/Groups")
def list_scim_groups(
    db: Session = Depends(get_db),
    admin: User = Depends(get_scim_admin)
):
    """RFC 7644 SCIM 2.0 Groups - Strictly Scoped to Authenticated Tenant"""
    depts = db.query(Department).filter(Department.organization_id == admin.organization_id).all()
    resources = [
        {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
            "id": d.id,
            "displayName": d.name,
            "meta": {
                "resourceType": "Group"
            }
        }
        for d in depts
    ]

    return {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": len(resources),
        "startIndex": 1,
        "itemsPerPage": len(resources),
        "Resources": resources
    }
