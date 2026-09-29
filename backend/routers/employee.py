# RESETA™ Enterprise Employee Surface Router
# Section 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 60
import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from backend.database import get_db
from backend.models import User, CheckIn, InterventionSession, WorkplaceProgram, SafetyEvent, Consent, PersonalPattern
from backend.schemas import (
    CheckInRequest, CheckInResponse, ResetIntentRequest,
    ResetSessionPlanResponse, CompleteResetRequest, CompleteResetResponse,
    TalkItOutRequest, TalkItOutResponse, UnloadCategory
)
from backend.engines.safety_firewall import SafetyFirewall
from backend.engines.state_engine import StateEngine
from backend.engines.intervention_router import InterventionRouter
from backend.engines.mental_load_unload import MentalLoadUnloadEngine
from backend.engines.personalization_engine import PersonalizationEngine
from backend.engines.autopilot_engine import AutopilotEngine
from backend.engines.ai_gateway import AIGateway
from backend.security import get_current_user

router = APIRouter(prefix="/api/employee", tags=["Employee Experience"])

@router.post("/checkin", response_model=CheckInResponse)
def submit_checkin(
    req: CheckInRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Hero check-in: 'How's your mind right now?'"""
    time_of_day = req.time_of_day or "Midday"

    checkin = CheckIn(
        user_id=user.id if user else "user-emp-arjun",
        organization_id=user.organization_id if user else "org-technova-01",
        department_id=user.department_id if user else "dept-eng",
        state_reported=req.state_reported,
        time_of_day=time_of_day
    )
    db.add(checkin)
    db.commit()

    prompt_map = {
        "Stressed": "Let's take 5 minutes to release somatic tension and steady your nervous system.",
        "Overloaded": "Too much coming at you at once? Let's unload your mental backlog into clear buckets.",
        "Overthinking": "Mind spinning with racing thoughts? Let's ground your attention in this room.",
        "Irritated": "Take a 2-minute pause before responding. Give your mind room to cool down.",
        "Exhausted": "Energy drained? A gentle micro-reset will help recharge your mental battery.",
        "Work Pressure": "Tight deadlines pressing in? Let's compress 10 tasks down to your single next step.",
        "Heavy": "Feeling weighed down? Let's do a gentle somatic breath reset together.",
        "Don't Know": "You don't need to put a label on it. Let's just pause together for 2 minutes."
    }

    return CheckInResponse(
        success=True,
        state_reported=req.state_reported,
        suggested_time_minutes=5 if req.state_reported in ["Overloaded", "Work Pressure"] else 2,
        prompt_message=prompt_map.get(req.state_reported, "Take a moment to pause. You are supported.")
    )

@router.post("/reset/plan", response_model=ResetSessionPlanResponse)
def create_reset_session(
    req: ResetIntentRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    🔴 RESET ME Engine:
    Step 1: Time (2/5/10 min)
    Step 2: What's going on (tap/type/speak)
    Step 3: Support goal -> Intervention Router -> Do It With Me™ steps + Mental Load Unload
    """
    user_id = user.id if user else "user-emp-arjun"
    org_id = user.organization_id if user else "org-technova-01"

    # 1. Independent Safety Firewall Screen
    safety_tier, escalation_needed, crisis_info = SafetyFirewall.evaluate_input(req.raw_input or "")

    if safety_tier == "RED":
        safe_evt = SafetyEvent(
            organization_id=org_id,
            user_id_hash=f"anon-{uuid.uuid4().hex[:6]}",
            tier="RED",
            trigger_type="Immediate safety trigger detected in reset text",
            tele_manas_notified=True,
            escalation_status="URGENT_TRIAGE",
            clinical_notes="Immediate crisis helpline displayed. Normal wellness reset suspended."
        )
        db.add(safe_evt)
        db.commit()

        return ResetSessionPlanResponse(
            session_id=f"sess-crisis-{uuid.uuid4().hex[:6]}",
            intervention_id="crisis_escalation",
            intervention_name="Immediate Safety Support",
            target_state="crisis",
            duration_minutes=0,
            safety_tier="RED",
            escalation_needed=True,
            crisis_resources=crisis_info,
            steps=[],
            unload_result=None,
            closing_prompt="Please connect with professional crisis care immediately."
        )

    # 2. State classification
    target_state = StateEngine.identify_state(req.raw_input or "", user_selected_state=req.state)

    # 3. Route Intervention
    routed = InterventionRouter.route(target_state, duration_minutes=req.time_choice_minutes)

    # 4. If overloaded or text provided, decompose mental load
    unload_res = None
    if "overload" in target_state or "work" in target_state or (req.raw_input and len(req.raw_input) > 10):
        decomp = MentalLoadUnloadEngine.decompose_mental_load(req.raw_input or "")
        unload_res = UnloadCategory(**decomp)

    session_id = f"sess-{uuid.uuid4().hex[:10]}"

    # Save session entity (private user raw text stays strictly private to this record)
    new_session = InterventionSession(
        id=session_id,
        user_id=user_id,
        organization_id=org_id,
        department_id=user.department_id if user else "dept-eng",
        team_id=user.team_id if user else "team-frontend",
        channel=req.channel,
        duration_choice_minutes=req.time_choice_minutes,
        starting_state=target_state,
        user_input_mode=req.input_mode,
        private_raw_input=req.raw_input,
        intervention_id=routed["intervention_id"],
        intervention_name=routed["intervention_name"],
        unload_data=unload_res.model_dump() if unload_res else None,
        safety_tier=safety_tier,
        escalated_to_care=(safety_tier == "AMBER")
    )
    db.add(new_session)
    db.commit()

    return ResetSessionPlanResponse(
        session_id=session_id,
        intervention_id=routed["intervention_id"],
        intervention_name=routed["intervention_name"],
        target_state=target_state,
        duration_minutes=req.time_choice_minutes,
        safety_tier=safety_tier,
        escalation_needed=(safety_tier == "RED"),
        crisis_resources=crisis_info if safety_tier != "GREEN" else {},
        steps=routed["steps"],
        unload_result=unload_res,
        closing_prompt=routed.get("closing_prompt") or "You've created breathing room. Take a sip of water before returning to your work."
    )

@router.post("/reset/complete", response_model=CompleteResetResponse)
def complete_reset_session(
    req: CompleteResetRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Relief Check™ (Section 12):
    Captures before/after stress rating (1-10) and helpfulness feedback.
    Calculates Relief Delta and feeds Personal Relief Map™.
    """
    outcome = PersonalizationEngine.evaluate_relief(
        db=db,
        session_id=req.session_id,
        stress_before=req.stress_before,
        stress_after=req.stress_after,
        did_this_help=req.did_this_help
    )

    return CompleteResetResponse(
        success=True,
        session_id=req.session_id,
        delta_relief=outcome["delta_relief"],
        is_successful_recovery=outcome["is_successful_recovery"],
        personal_insight=outcome["personal_insight"],
        next_recommendation=outcome["next_recommendation"]
    )

@router.post("/talk-it-out", response_model=TalkItOutResponse)
def talk_it_out(req: TalkItOutRequest):
    """
    🎙 TALK IT OUT™ (Section 16):
    Voice or text stream -> Safety check -> Reflection -> Immediate actionable reset.
    Supports natural Hinglish / Hindi / English phrases with pluggable LLM generation.
    """
    result = AIGateway.process_talk_it_out(req.transcript_or_text, preferred_language=req.language)
    return TalkItOutResponse(**result)

@router.get("/personal-relief-map")
def get_personal_relief_map(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Personal Relief Map™ (Section 13) and Mind Mirror™ (Section 14).
    Private to the employee.
    """
    user_id = user.id if user else "user-emp-arjun"
    mind_mirror = PersonalizationEngine.get_mind_mirror_insights(db, user_id=user_id)

    # Fetch recent personal sessions
    recent_sessions = (
        db.query(InterventionSession)
        .filter(InterventionSession.user_id == user_id)
        .order_by(InterventionSession.completed_at.desc())
        .limit(10)
        .all()
    )

    history = [
        {
            "id": s.id,
            "starting_state": s.starting_state,
            "intervention_name": s.intervention_name,
            "duration": s.duration_choice_minutes,
            "stress_before": s.stress_before,
            "stress_after": s.stress_after,
            "delta": (s.stress_before - s.stress_after) if (s.stress_before and s.stress_after) else 3,
            "did_this_help": s.did_this_help or "YES",
            "date": s.completed_at.strftime("%b %d, %H:%M") if s.completed_at else "Recently"
        }
        for s in recent_sessions
    ]

    return {
        "user_id": user_id,
        "mind_mirror": mind_mirror,
        "recent_history": history
    }

@router.get("/programs")
def list_workplace_programs(db: Session = Depends(get_db)):
    """Workplace-specific Programs (Section 18)"""
    return db.query(WorkplaceProgram).all()

@router.get("/daily-recovery")
def get_daily_recovery_prompt():
    """Daily Recovery Prompt (Section 17)"""
    now_hour = datetime.datetime.now().hour
    if now_hour < 12:
        period = "Morning"
        headline = "How's your headspace today?"
        subtext = "Start clear. A 2-minute focus grounding sets your day's pace."
        suggested_action = "2-Min Morning Grounding"
    elif now_hour < 17:
        period = "Midday"
        headline = "Afternoon reset needed?"
        subtext = "Clear meeting debris and reset your focus before the next block."
        suggested_action = "5-Min Cognitive Defrag"
    else:
        period = "Evening"
        headline = "Ready to shut work out for today?"
        subtext = "Unload uncompleted items so you don't carry them home tonight."
        suggested_action = "3-Min End-of-Day Shutdown"

    return {
        "period": period,
        "headline": headline,
        "subtext": subtext,
        "suggested_action": suggested_action
    }

@router.post("/send-a-reset")
def send_a_reset_invite(colleague_name: str):
    """Peer Reset Invite Loop (Section 60)"""
    return {
        "success": True,
        "colleague_name": colleague_name,
        "invite_text": f"Hey {colleague_name}, take 5 minutes to reset. You don't have to fix everything right now."
    }

@router.get("/autopilot/prompt")
def get_autopilot_prompt(
    meetings_today: int = 4,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Contextual JITAI reset prompt based on permissioned signals"""
    return AutopilotEngine.evaluate_contextual_signal(
        db=db,
        user_id=user.id if user else "user-emp-arjun",
        simulated_calendar_meetings_today=meetings_today
    )

@router.get("/dpdp/export")
def export_employee_data_archive(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Right to Data Portability (DPDP Act 2025)"""
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    sessions = db.query(InterventionSession).filter(InterventionSession.user_id == user.id).all()
    consents = db.query(Consent).filter(Consent.user_id == user.id).all()
    patterns = db.query(PersonalPattern).filter(PersonalPattern.user_id == user.id).all()

    return {
        "data_subject": {
            "name": user.full_name,
            "email": user.email,
            "organization_id": user.organization_id
        },
        "export_timestamp": datetime.datetime.utcnow().isoformat(),
        "dpdp_notice": "Full personal export in machine-readable JSON format.",
        "consents": [
            {"purpose": c.purpose, "granted": c.granted, "granted_at": str(c.granted_at)}
            for c in consents
        ],
        "completed_sessions_count": len(sessions),
        "sessions": [
            {
                "id": s.id,
                "date": str(s.completed_at),
                "state": s.starting_state,
                "protocol": s.intervention_name,
                "stress_before": s.stress_before,
                "stress_after": s.stress_after,
                "helped": s.did_this_help
            }
            for s in sessions
        ],
        "learned_patterns": [
            {"situation": p.situation, "recommended": p.recommended_intervention, "avg_relief": p.avg_delta_relief}
            for p in patterns
        ]
    }

class ConsentToggleRequest(BaseModel):
    purpose: str
    granted: bool

@router.post("/dpdp/consent-toggle")
def toggle_consent(
    req: ConsentToggleRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Right to Withdraw Consent (DPDP Act 2025)"""
    user_id = user.id if user else "user-emp-arjun"

    consent = db.query(Consent).filter(Consent.user_id == user_id, Consent.purpose == req.purpose).first()
    if not consent:
        consent = Consent(user_id=user_id, purpose=req.purpose, granted=req.granted)
        db.add(consent)
    else:
        consent.granted = req.granted
        if not req.granted:
            consent.withdrawn_at = datetime.datetime.utcnow()
    db.commit()

    return {"success": True, "purpose": req.purpose, "granted": req.granted}

@router.post("/dpdp/erasure")
def request_personal_data_erasure(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Right to Erasure (DPDP Act 2025)"""
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Erase employee personal raw sessions and patterns
    db.query(PersonalPattern).filter(PersonalPattern.user_id == user.id).delete()
    
    # Anonymize past sessions so organization aggregates remain mathematically sound without user trace
    user_sessions = db.query(InterventionSession).filter(InterventionSession.user_id == user.id).all()
    for s in user_sessions:
        s.private_raw_input = None
        s.unload_data = None
        s.user_id = "erased-dpdp-subject"
    
    db.commit()
    return {
        "success": True,
        "message": "All private reflections, unloads, and personal relief patterns have been permanently erased per DPDP Act 2023."
    }
