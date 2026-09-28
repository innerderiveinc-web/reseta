# RESETA™ Enterprise SCIM 2.0 Protocol Router
# RFC 7643 & RFC 7644 Standard Enterprise Identity Management (Microsoft Entra ID, Okta, Workday)
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from backend.database import get_db
from backend.models import User, Department, Organization

router = APIRouter(prefix="/api/scim/v2", tags=["SCIM 2.0 Identity Provisioning"])

@router.get("/ServiceProviderConfig")
def get_service_provider_config():
    """RFC 7644 Service Provider Configuration"""
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
    db: Session = Depends(get_db)
):
    """RFC 7644 SCIM 2.0 Users Collection Endpoint"""
    query = db.query(User)
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
            "active": True,
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
def get_scim_user(user_id: str, db: Session = Depends(get_db)):
    """RFC 7644 SCIM 2.0 Single User Resource"""
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="SCIM Resource not found")

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
        "active": True,
        "roles": [{"value": u.role, "primary": True}],
        "meta": {
            "resourceType": "User",
            "created": u.created_at.isoformat() if u.created_at else "2026-01-01T00:00:00Z"
        }
    }

@router.get("/Groups")
def list_scim_groups(db: Session = Depends(get_db)):
    """RFC 7644 SCIM 2.0 Groups (Departments & Teams Mapping)"""
    depts = db.query(Department).all()
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
