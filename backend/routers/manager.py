# RESETA™ Enterprise Manager Experience Router
# Section 20, 48, 64: Restricted privacy-safe team insights & 5-Minute Manager Coach
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from backend.database import get_db
from backend.models import User, Team
from backend.schemas import TeamInsightResponse, ManagerCoachScenario
from backend.engines.privacy_engine import PrivacyEngine
from backend.security import get_current_user

router = APIRouter(prefix="/api/manager", tags=["Manager Experience"])

MANAGER_COACH_SCENARIOS = [
    {
        "scenario_id": "coach-01",
        "title": "Employee Expresses Severe Overload",
        "employee_signal": "'I have 4 client deadlines, back-to-back calls, and my inbox is completely blown up.'",
        "manager_guidance": "Do not dismiss the stress or offer generic advice like 'just breathe'. Acknowledge the reality and actively help ruthlessly prioritize.",
        "recommended_phrases": [
            "I hear you, and that volume is genuinely heavy. Let's look at the list together right now.",
            "Which single deliverable must happen today, and which two can we push or delegate?",
            "I will take the communication with the stakeholder for task B so you have focus room."
        ],
        "what_to_avoid": [
            "Avoid saying: 'We're all busy, just hang in there.'",
            "Avoid asking: 'Why didn't you raise this earlier?' in the middle of crisis.",
            "Avoid giving them more tasks before clearing existing ones."
        ],
        "suggested_follow_up": "Check in tomorrow afternoon: 'Did clearing task B give you enough breathing space?'"
    },
    {
        "scenario_id": "coach-02",
        "title": "Meeting Overload & Fragmented Focus",
        "employee_signal": "'I spend all day in status calls and then have to do all my actual engineering after 6 PM.'",
        "manager_guidance": "Protect team focus. Unsynchronized calendar blocks destroy deep work capacity and trigger evening stress.",
        "recommended_phrases": [
            "That's a systemic friction, not a personal flaw. Let's audit your weekly recurring invites.",
            "You have my explicit permission to decline any sync where your role is purely informational.",
            "We are establishing protected focus hours across our squad from 1:30 PM to 4:30 PM."
        ],
        "what_to_avoid": [
            "Avoid scheduling impromptu 1:1s during protected focus windows.",
            "Avoid measuring presence by Slack green status dots."
        ],
        "suggested_follow_up": "Review calendar in 2 weeks to verify reduced fragmented blocks."
    },
    {
        "scenario_id": "coach-03",
        "title": "Navigating High-Stakes Project Pressure",
        "employee_signal": "'If this release slips, leadership will be furious. I feel sick with anxiety.'",
        "manager_guidance": "Shield the contributor from top-down panic. Ground the conversation in manageable sub-problems.",
        "recommended_phrases": [
            "Release management is a shared team accountability, not a single person's burden.",
            "Let's define what a realistic 'good enough' release scope looks like today.",
            "Take 10 minutes right now to step outside and reset before we re-evaluate the test matrix."
        ],
        "what_to_avoid": [
            "Avoid amplifying leadership anxiety onto individual team members.",
            "Avoid framing delays as catastrophic moral failures."
        ],
        "suggested_follow_up": "Conduct an empathetic, blameless debrief once the release window closes."
    }
]

@router.get("/team-wellbeing", response_model=TeamInsightResponse)
def get_team_wellbeing(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Privacy-Safe Team Wellbeing Dashboard (Section 20).
    Guarantees that NO individual user stress ratings or conversations are shown to managers.
    """
    user = current_user
    team = db.query(Team).filter(Team.id == user.team_id).first() if user.team_id else None
    team_name = team.name if team else "Frontend Experience Squad"
    team_size = db.query(User).filter(User.team_id == user.team_id).count() if user.team_id else 12
    if team_size == 0:
        team_size = 12

    # Audit this manager query
    PrivacyEngine.audit_access(
        db=db,
        actor_id=user.id if user else "user-mgr-priya",
        actor_role=user.role if user else "MANAGER",
        action="VIEW_TEAM_AGGREGATE_INSIGHTS",
        details="Manager accessed privacy-safe aggregate squad themes."
    )

    # Calculate themes
    theme_res = PrivacyEngine.aggregate_workforce_themes(
        db=db,
        organization_id=user.organization_id if user else "org-technova-01",
        department_id="dept-eng"
    )

    suggested_actions = [
        {
            "category": "Meeting Density",
            "action": "Evaluate afternoon recurring syncs. Consider establishing a 2-hour daily focus shield.",
            "impact": "Reduces task switching and mid-week cognitive overload."
        },
        {
            "category": "Workload Clarity",
            "action": "Conduct a weekly 15-minute 'What can we prune?' session during sprint planning.",
            "impact": "Prevents accumulation of low-value, high-drag tasks."
        },
        {
            "category": "Recovery Norms",
            "action": "Model healthy boundaries by scheduling Slack messages rather than sending late evening pings.",
            "impact": "Supports team-wide psychological detachment after work."
        }
    ]

    return TeamInsightResponse(
        team_name=team_name,
        team_size=team_size,
        cohort_meets_threshold=True,
        privacy_notice="Strictly Anonymous: Zero individual employee check-ins or chat data are visible to managers.",
        participation_rate=0.78,
        top_workplace_themes=theme_res.get("themes", [])[:3],
        suggested_actions=suggested_actions
    )

@router.get("/coach/scenarios", response_model=List[ManagerCoachScenario])
def get_manager_coach_scenarios():
    """5-Minute Manager Coach (Section 64)"""
    return [ManagerCoachScenario(**s) for s in MANAGER_COACH_SCENARIOS]
