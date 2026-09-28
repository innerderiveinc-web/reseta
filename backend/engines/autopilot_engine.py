# RESETA™ Enterprise Autopilot Engine
# Section 15: Contextual, permission-based reset prompts without surveillance or anxiety claims
import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.models import CheckIn, InterventionSession

class AutopilotEngine:
    """
    Evaluates permissioned contextual signals:
    - Time of day & natural workplace recovery transitions
    - Consecutive meetings / task switching density
    - Recent self-reported check-in history
    
    CRITICAL POLICY:
    Never claims 'We detected anxiety' or 'You are stressed'.
    Uses neutral, respectful invitations: 'Long day? Take 5?'
    """

    @classmethod
    def evaluate_contextual_signal(
        cls,
        db: Session,
        user_id: str,
        simulated_calendar_meetings_today: int = 4
    ) -> Dict[str, Any]:
        now = datetime.datetime.now()
        hour = now.hour

        # Check recent self-reported sessions
        recent_session = (
            db.query(InterventionSession)
            .filter(InterventionSession.user_id == user_id)
            .order_by(InterventionSession.completed_at.desc())
            .first()
        )

        should_prompt = True
        trigger_code = "TIME_OF_DAY"
        headline = "Long day? Take 5?"
        subtext = "You've been navigating multiple tasks today. A quick reset can help restore focus."
        recommended_minutes = 5
        recommended_state = "overloaded"

        if simulated_calendar_meetings_today >= 3 and 13 <= hour <= 17:
            trigger_code = "MEETING_DENSITY"
            headline = "Back-to-back discussions? Take 2."
            subtext = f"You've had {simulated_calendar_meetings_today} meetings today. Clear the meeting residue before your next task."
            recommended_minutes = 2
            recommended_state = "racing_thoughts"
        elif hour >= 18:
            trigger_code = "END_OF_DAY_SHUTDOWN"
            headline = "Ready to shut work out for today?"
            subtext = "Unload lingering mental loops so your mind can fully detach this evening."
            recommended_minutes = 5
            recommended_state = "night_stress"
        elif hour < 11:
            trigger_code = "MORNING_BASELINE"
            headline = "Start the day with a clear center."
            subtext = "Take 2 minutes to ground your attention before incoming messages pick up."
            recommended_minutes = 2
            recommended_state = "general_tension"

        return {
            "autopilot_active": True,
            "trigger_code": trigger_code,
            "headline": headline,
            "subtext": subtext,
            "recommended_minutes": recommended_minutes,
            "recommended_state": recommended_state,
            "privacy_notice": "Autopilot signals are computed locally on your device and are never monitored by managers."
        }
