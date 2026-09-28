# RESETA™ Enterprise Employee Surface Router
# Section 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 60
import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from backend.database import get_db
from backend.models import User, CheckIn, InterventionSession, WorkplaceProgram, SafetyEvent
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
from backend.engines.ai_gateway import AIGateway
from backend.routers.auth import ACTIVE_USER_ID

router = APIRouter(prefix="/api/employee", tags=["Employee Experience"])

@router.post("/checkin", response_model=CheckInResponse)
def submit_checkin(req: CheckInRequest, db: Session = Depends(get_db)):
    """Hero check-in: 'How's your mind right now?'"""
    user = db.query(User).filter(User.id == ACTIVE_USER_ID).first()
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
def create_reset_session(req: ResetIntentRequest, db: Session = Depends(get_db)):
    """
    🔴 RESET ME Engine:
    Step 1: Time (2/5/10 min)
    Step 2: What's going on (tap/type/speak)
    Step 3: Support goal -> Intervention Router -> Do It With Me™ steps + Mental Load Unload
    """
    user = db.query(User).filter(User.id == ACTIVE_USER_ID).first()
    user_id = user.id if user else "user-emp-arjun"
    org_id = user.organization_id if user else "org-technova-01"

    # 1. Independent Safety Firewall Screen
    safety_tier, escalation_needed, crisis_info = SafetyFirewall.evaluate_input(req.raw_input or "")

    # If RED tier, log safety event and return emergency crisis resources
    if safety_tier == "RED":
        safe_evt = SafetyEvent(
            id=f"safe-{uuid.uuid4().hex[:8]}",
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
        escalation_needed=(safety_tier == "AMBER"),
        crisis_resources=crisis_info if safety_tier == "AMBER" else None,
        steps=routed["steps"],
        unload_result=unload_res,
        closing_prompt="Reset complete. You don't need to solve everything today."
    )

@router.post("/reset/complete", response_model=CompleteResetResponse)
def complete_reset_session(req: CompleteResetRequest, db: Session = Depends(get_db)):
    """
    Relief Check™ (Section 12):
    Before: Stress 8/10 -> After: Stress 4/10 -> Did this help? Yes/A little/No.
    Calculates Successful Recovery Moment for North Star metric.
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
    Supports natural Hinglish / Hindi / English phrases.
    """
    result = AIGateway.process_talk_it_out(req.transcript_or_text, preferred_language=req.language)
    return TalkItOutResponse(**result)

@router.get("/personal-relief-map")
def get_personal_relief_map(db: Session = Depends(get_db)):
    """
    Personal Relief Map™ (Section 13) and Mind Mirror™ (Section 14).
    Private to the employee.
    """
    user = db.query(User).filter(User.id == ACTIVE_USER_ID).first()
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
        "user_name": user.full_name if user else "Arjun Sharma",
        "mind_mirror": mind_mirror,
        "recent_history": history
    }

@router.get("/programs")
def list_workplace_programs(db: Session = Depends(get_db)):
    """Workplace-specific programs (Section 18)"""
    programs = db.query(WorkplaceProgram).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "duration_days": p.duration_days,
            "target_audience": p.target_audience,
            "active_participants": p.active_participants,
            "completion_rate_pct": int(p.completion_rate * 100),
            "steps": p.steps
        }
        for p in programs
    ]

@router.get("/daily-recovery")
def get_daily_recovery_prompt():
    """Daily recovery routine prompts (Section 17)"""
    now = datetime.datetime.now()
    hour = now.hour

    if hour < 12:
        return {
            "period": "Morning",
            "headline": "How's your mind today?",
            "subtext": "Set a calm, centered baseline before the day's meetings begin.",
            "recommended_time": 2,
            "suggested_action": "Take a 2-minute morning grounding breath."
        }
    elif hour < 17:
        return {
            "period": "Midday",
            "headline": "Need a 2-minute reset?",
            "subtext": "Decompress from morning discussions and sharpen focus for the afternoon.",
            "recommended_time": 2,
            "suggested_action": "Quick priority compression or shoulder release."
        }
    elif hour < 21:
        return {
            "period": "Evening",
            "headline": "Unload today's mental baggage.",
            "subtext": "Park tomorrow's tasks so your mind can fully step away from work.",
            "recommended_time": 5,
            "suggested_action": "End-of-day Mental Load Unload™."
        }
    else:
        return {
            "period": "Night",
            "headline": "Ready to shut work out for today?",
            "subtext": "Your evening recovery belongs to you. Close work loops for restorative sleep.",
            "recommended_time": 5,
            "suggested_action": "End-of-day Mental Shutdown™."
        }

@router.post("/send-a-reset")
def send_a_reset(colleague_name: str = "Teammate"):
    """
    Section 60: Send a Reset
    An employee sends a colleague a neutral, caring invite:
    'Take 5 minutes. You don't have to fix everything right now.'
    No sensitive or health information is shared.
    """
    return {
        "success": True,
        "message": f"Reset invite generated for {colleague_name}.",
        "invite_text": "Take 5 minutes. You don't have to fix everything right now.",
        "invite_link": "/?action=reset_invite&from=colleague"
    }
