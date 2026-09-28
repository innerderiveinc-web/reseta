# RESETA™ Enterprise Mental Load Unload™
# Section 11: Signature capability converting mental clutter into structured buckets
import re
from typing import Dict, List, Any

class MentalLoadUnloadEngine:
    """
    Parses unstructured employee thought dumps / speech into clear actionable quadrants:
    - NOW (Highest single priority)
    - SCHEDULED (Time-bound events / meetings)
    - WAITING (Dependent on third parties)
    - LATER (Inbox, non-urgent backlog)
    - NEXT (One single 5-10 minute micro-action)
    """

    @classmethod
    def decompose_mental_load(cls, raw_text: str) -> Dict[str, Any]:
        text = raw_text.strip() if raw_text else ""

        # Default fallback items if text is brief or generic
        if not text or len(text) < 10:
            return {
                "now": ["Focus on the primary immediate deliverable"],
                "scheduled": ["Calendar meetings for today"],
                "waiting": ["Pending approvals or external replies"],
                "later": ["Unread emails & non-urgent messages"],
                "next_action": "Complete the first 10-minute portion of your top task."
            }

        lines_or_phrases = re.split(r"[,;.\n]+|(?:\band\b|\bphir\b|\bhai\b|\baur\b)", text, flags=re.IGNORECASE)
        phrases = [p.strip() for p in lines_or_phrases if len(p.strip()) > 3]

        now_items: List[str] = []
        scheduled_items: List[str] = []
        waiting_items: List[str] = []
        later_items: List[str] = []

        meeting_regex = re.compile(r"meeting|call|sync|standup|1:1|calendar", re.I)
        waiting_regex = re.compile(r"waiting|pending|reply|response|approval|client revert|feedback", re.I)
        later_regex = re.compile(r"inbox|email|messages|slack|backlog|documentation|later|review baad", re.I)
        urgent_regex = re.compile(r"deadline|urgent|presentation|deck|bug|release|client|priority|main", re.I)

        for p in phrases:
            clean_phrase = p.strip().capitalize()
            if meeting_regex.search(p):
                scheduled_items.append(clean_phrase)
            elif waiting_regex.search(p):
                waiting_items.append(clean_phrase)
            elif later_regex.search(p):
                later_items.append(clean_phrase)
            elif urgent_regex.search(p):
                now_items.append(clean_phrase)
            else:
                if len(now_items) < 2:
                    now_items.append(clean_phrase)
                else:
                    later_items.append(clean_phrase)

        # Ensure sensible defaults if some buckets are empty
        if not now_items:
            now_items = [phrases[0].capitalize() if phrases else "Primary focus item"]
        if not scheduled_items:
            scheduled_items = ["Today's existing calendar commitments"]
        if not waiting_items:
            waiting_items = ["Pending client / stakeholder updates"]
        if not later_items:
            later_items = ["Inbox & background tasks"]

        # Craft singular next action
        top_now = now_items[0]
        next_action = f"Work uninterrupted on '{top_now}' for just 10 minutes without switching tabs."

        return {
            "now": now_items[:2],
            "scheduled": scheduled_items[:3],
            "waiting": waiting_items[:2],
            "later": later_items[:3],
            "next_action": next_action
        }
