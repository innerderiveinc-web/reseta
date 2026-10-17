# RESETA™ Enterprise Care Console Router
# Section 26, 27: RESETA Care™, professional escalation pathways, Tele-MANAS triage
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from backend.database import get_db
from backend.models import SafetyEvent, User
from backend.schemas import CareEscalationItem
from backend.engines.safety_firewall import EMERGENCY_RESOURCES
from backend.security import require_roles

router = APIRouter(prefix="/api/care", tags=["RESETA Care™ Console"])

care_guard = require_roles(["CLINICIAN", "SUPER_ADMIN"])

@router.get("/resources")
def get_care_resources():
    """National and enterprise crisis & clinical care pathways"""
    return {
        "emergency_resources": EMERGENCY_RESOURCES,
        "eap_partner": {
            "name": "TechNova Corporate EAP Services",
            "provider": "Optum / Workplace Options",
            "sessions_included": 6,
            "confidentiality_guarantee": "100% strictly confidential external provider."
        },
        "care_statement": (
            "RESETA is an in-the-moment cognitive recovery system for workplace strain relief. "
            "It is not a clinical therapy or psychiatric diagnosis service. When support needs exceed self-guided resets, "
            "direct human clinical pathways and certified helplines are immediately provided."
        )
    }

@router.get("/triage-queue", response_model=List[CareEscalationItem])
def get_care_triage_queue(db: Session = Depends(get_db), current_user: User = Depends(care_guard)):
    """Safety and escalation queue for certified clinical staff (Section 26, 27)"""
    events = db.query(SafetyEvent).order_by(SafetyEvent.created_at.desc()).limit(10).all()
    return [
        CareEscalationItem(
            id=e.id,
            created_at=e.created_at.strftime("%Y-%m-%d %H:%M"),
            tier=e.tier,
            anonymized_reference=e.user_id_hash,
            trigger_type=e.trigger_type,
            tele_manas_notified=e.tele_manas_notified,
            status=e.escalation_status,
            recommended_action=e.clinical_notes or "Review care options with member."
        )
        for e in events
    ]
