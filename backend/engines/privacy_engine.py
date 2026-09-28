# RESETA™ Enterprise Privacy & DPDP Engine
# Section 19, 22, 23, 43, 66: Technical privacy wall, k-anonymity suppression, DPDP Act 2025 compliance
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models import User, InterventionSession, AuditLog, Consent
from backend.config import settings

class PrivacyEngine:
    """
    Enforces the Employee Privacy Wall and DPDP 2025 compliance:
    - Minimum cohort threshold suppression (k >= 5)
    - Prevents individual inference attacks
    - Translates clinical/risk terminology into respectful workplace language (Section 22)
    - Records privileged audit events
    """

    MIN_COHORT_THRESHOLD = settings.MIN_COHORT_SIZE

    @classmethod
    def audit_access(cls, db: Session, actor_id: str, actor_role: str, action: str, details: str = None):
        """Record privileged analytics queries in immutable audit logs"""
        log_entry = AuditLog(
            organization_id=settings.DEFAULT_TENANT_ID,
            actor_id=actor_id,
            actor_role=actor_role,
            action=action,
            details=details
        )
        db.add(log_entry)
        db.commit()

    @classmethod
    def sanitize_hr_language(cls, raw_insight: str) -> str:
        """
        Section 22: Never call employees 'high-risk' or 'clinically depressed'.
        Use objective, constructive organizational wellbeing vocabulary.
        """
        replacements = [
            ("high-risk employees", "participating team members experiencing elevated workplace strain"),
            ("burnout risk", "workload-related recovery opportunity"),
            ("mental health hazard", "team-level focus & recovery signal"),
            ("depressed workers", "employees navigating sustained workload demands"),
            ("toxic team", "team with elevated meeting and deadline density")
        ]
        sanitized = raw_insight
        for pattern, replacement in replacements:
            sanitized = sanitized.replace(pattern, replacement)
        return sanitized

    @classmethod
    def aggregate_workforce_themes(
        cls,
        db: Session,
        organization_id: str,
        department_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Aggregate themes with strict minimum cohort size suppression.
        """
        query = db.query(InterventionSession).filter(InterventionSession.organization_id == organization_id)
        if department_id:
            query = query.filter(InterventionSession.department_id == department_id)

        distinct_users_count = query.with_entities(func.count(func.distinct(InterventionSession.user_id))).scalar() or 0

        # Cohort suppression check
        if distinct_users_count < cls.MIN_COHORT_THRESHOLD:
            return {
                "cohort_meets_threshold": False,
                "cohort_size": distinct_users_count,
                "min_threshold_required": cls.MIN_COHORT_THRESHOLD,
                "privacy_message": (
                    f"To safeguard individual employee privacy (k ≥ {cls.MIN_COHORT_THRESHOLD}), "
                    "aggregate themes are suppressed for groups with fewer than 5 active participants."
                ),
                "themes": []
            }

        # Safe aggregation
        sessions = query.all()
        theme_counts: Dict[str, int] = {
            "Workload & Deadlines": 0,
            "Meeting Density & Focus": 0,
            "Cognitive Switching / Multitasking": 0,
            "End-of-Day Shutdown": 0,
            "General Somatic Tension": 0
        }

        for s in sessions:
            st = s.starting_state.lower()
            if "work" in st or "overload" in st:
                theme_counts["Workload & Deadlines"] += 1
            elif "racing" in st or "rumination" in st:
                theme_counts["Meeting Density & Focus"] += 1
            elif "cant_start" in st or "decision" in st:
                theme_counts["Cognitive Switching / Multitasking"] += 1
            elif "night" in st:
                theme_counts["End-of-Day Shutdown"] += 1
            else:
                theme_counts["General Somatic Tension"] += 1

        total_sessions = len(sessions) or 1
        themes_list = [
            {
                "theme_name": name,
                "session_count": count,
                "percentage": round((count / total_sessions) * 100, 1),
                "status_indicator": "Elevated" if (count / total_sessions) > 0.3 else "Steady"
            }
            for name, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        return {
            "cohort_meets_threshold": True,
            "cohort_size": distinct_users_count,
            "min_threshold_required": cls.MIN_COHORT_THRESHOLD,
            "privacy_message": "Protected by RESETA Privacy Wall™: No individual user conversations or scores are exposed.",
            "themes": themes_list
        }
