# RESETA™ Enterprise State Engine
# Section 8, 9, 32: Support goal classification with multilingual Hindi/Hinglish/English understanding
import re
from typing import Dict, Any

STATE_PATTERNS = {
    "overloaded": [
        "overload", "too much", "piled up", "sab kuch ek sath", "bohot sara kaam", "dimaag full",
        "drowning in work", "buried", "can't handle all this", "overwhelmed", "so many tasks"
    ],
    "racing_thoughts": [
        "racing", "mind won't stop", "overthinking", "dimag chal raha hai", "non stop thinking",
        "can't slow down", "thoughts spinning", "brain buzzing", "chalta hi ja raha hai"
    ],
    "work_pressure": [
        "deadline", "client meeting", "manager ne task diya", "pressure", "target", "deliverable",
        "escalation", "urgent", "kam ka pressure", "boss", "khatam karna hai"
    ],
    "cant_start": [
        "can't start", "stuck", "procrastinating", "shuru nahi ho raha", "frozen", "paralysis",
        "resistance", "heavy to begin", "no momentum"
    ],
    "rumination": [
        "replaying", "should have", "said the wrong thing", "kyun bola", "pachtawa", "regret",
        "can't let go", "embarrassed", "obsessing"
    ],
    "frustration": [
        "irritated", "frustrated", "gussa", "annoyed", "pissed off", "colleague", "waste of time",
        "unreasonable", "dimag kharab"
    ],
    "night_stress": [
        "bedtime", "evening", "can't sleep", "raat ko neend", "switch off", "log off",
        "work on my mind at night", "shutdown"
    ],
    "decision_overload": [
        "decision", "choose", "what to do first", "confused", "option a or b", "kaunsa pehle karun",
        "analysis paralysis"
    ],
    "low_energy": [
        "exhausted", "tired", "thak gaya", "drain", "burnout", "no energy", "sluggish", "lethargic"
    ],
    "general_tension": [
        "heavy", "stressed", "tightness", "shoulders tight", "tension", "nervous", "anxious", "breathing shallow"
    ]
}

class StateEngine:
    """
    Determines immediate workplace mental support state.
    Note: Focuses on immediate workplace support goals, never psychiatric diagnosis.
    """

    @classmethod
    def identify_state(cls, raw_input: str, user_selected_state: str = None) -> str:
        if user_selected_state:
            normalized = user_selected_state.lower().replace(" ", "_").replace("'", "")
            for state_key in STATE_PATTERNS.keys():
                if state_key in normalized or normalized in state_key:
                    return state_key

        if not raw_input:
            return "overloaded"

        text_lower = raw_input.lower().strip()

        # Score matching patterns
        scores: Dict[str, int] = {k: 0 for k in STATE_PATTERNS}
        for state_key, keywords in STATE_PATTERNS.items():
            for kw in keywords:
                if kw in text_lower:
                    scores[state_key] += 2

        best_state = max(scores, key=scores.get)
        if scores[best_state] > 0:
            return best_state

        return "overloaded"
