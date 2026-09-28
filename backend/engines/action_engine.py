# RESETA™ Enterprise Organizational Action Engine & Team Recovery Lab™
# Section 24, 25: SIGNAL -> ACTION -> MEASURE & Controlled workplace recovery experiments
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.models import TeamRecoveryExperiment, InterventionSession

class ActionEngine:
    """
    Transforms aggregate wellbeing signals into concrete organizational actions
    and tracks Team Recovery Lab experiments.
    """

    @classmethod
    def generate_recommendations(cls, db: Session, organization_id: str) -> List[Dict[str, Any]]:
        """
        Produces actionable HR recommendations without claiming clinical causation.
        """
        return [
            {
                "id": "rec_01",
                "signal": "High self-reported workload strain concentrated between 2:00 PM and 4:30 PM",
                "possible_interpretation": "Consecutive afternoon meeting blocks may restrict focus time.",
                "questions_to_investigate": [
                    "Are afternoon sprint syncs overlapping with key delivery windows?",
                    "Can 30-minute status check-ins be converted into asynchronous updates?"
                ],
                "recommended_action": "Introduce a 2-hour 'Protected Focus Block' on Tuesday and Thursday afternoons.",
                "owner": "Director of Engineering & People Ops",
                "deadline": "2 Weeks",
                "remeasure_date": "30 Days after implementation",
                "status": "IN_PROGRESS"
            },
            {
                "id": "rec_02",
                "signal": "Elevated end-of-day shutdown resets among Customer Success team",
                "possible_interpretation": "Delayed client replies late in the evening create prolonged anticipation.",
                "questions_to_investigate": [
                    "Is there an implicit expectation to answer non-emergency Slack messages after 7 PM?"
                ],
                "recommended_action": "Publish team-level 'Right-to-Disconnect' communication norms.",
                "owner": "Head of Customer Success",
                "deadline": "Next Sprint",
                "remeasure_date": "Next Month",
                "status": "PLANNED"
            },
            {
                "id": "rec_03",
                "signal": "Positive 3.4-point relief delta in teams adopting the 5-Minute Reset Campaign",
                "possible_interpretation": "Active manager endorsement increases employee willingness to take micro-resets.",
                "questions_to_investigate": [
                    "Can manager micro-training be expanded to the Sales and Operations units?"
                ],
                "recommended_action": "Launch the '5-Minute Manager Recovery Coach' across all department leads.",
                "owner": "People & Culture Lead",
                "deadline": "Immediate",
                "remeasure_date": "Ongoing",
                "status": "COMPLETED"
            }
        ]

    @classmethod
    def get_recovery_lab_experiments(cls, db: Session, organization_id: str) -> List[Dict[str, Any]]:
        experiments = db.query(TeamRecoveryExperiment).filter(
            TeamRecoveryExperiment.organization_id == organization_id
        ).all()

        results = []
        for exp in experiments:
            results.append({
                "id": exp.id,
                "title": exp.title,
                "hypothesis": exp.hypothesis,
                "intervention_type": exp.intervention_type,
                "duration_weeks": exp.duration_weeks,
                "target_departments": exp.target_departments,
                "status": exp.status,
                "baseline_recovery_score": exp.baseline_recovery_score,
                "current_recovery_score": exp.current_recovery_score,
                "score_improvement": round(exp.current_recovery_score - exp.baseline_recovery_score, 1),
                "participation_count": exp.participation_count,
                "findings": exp.findings
            })
        return results
