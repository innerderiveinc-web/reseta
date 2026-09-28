# RESETA™ Enterprise Safety Firewall™
# Section 27, 28: Independent safety architecture, Green/Amber/Red tiers, Anti-diagnosis guardrails
import re
from typing import Dict, Any, Tuple

CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die", "self harm", "cut myself",
    "hurting myself", "mar jana chahta", "jaan de dunga", "zindagi khatam", "no point living",
    "overdose", "slit", "hanging myself", "can't go on anymore", "better off dead"
]

AMBER_KEYWORDS = [
    "hopeless", "can't cope", "panic attack", "crying non stop", "severe chest pain",
    "depressed for months", "can't get out of bed", "hallucinations", "hearing voices",
    "abuse", "harassment", "trauma", "breakdown", "bahut zyada bura lag raha",
    "kuch theek nahi hoga", "completely numb"
]

DIAGNOSTIC_TERMS = [
    r"\b(?:you have|you are experiencing|diagnosed with)\s+(?:severe\s+|clinical\s+|acute\s+)?(?:depression|adhd|bipolar|anxiety|ptsd|schizophrenia|major depressive disorder)\b",
    r"\b(?:you\s+)?suffer from\s+(?:ptsd|depression|anxiety|adhd|bipolar)\b",
    r"\b(?:you are\s+)?clinically burned out\b",
    r"\byou have adhd\b",
    r"\byou have depression\b",
    r"\byou have bipolar\b"
]

EMERGENCY_RESOURCES = {
    "india_tele_manas": {
        "name": "Tele-MANAS (Govt. of India National Mental Health Helpline)",
        "toll_free": "14416 / 1800-89-14416",
        "availability": "24/7, Free, Confidential in 20+ Languages",
        "description": "Comprehensive round-the-clock psychological support."
    },
    "india_vandrevala": {
        "name": "Vandrevala Foundation Helpline",
        "phone": "+91 9999 666 555",
        "availability": "24/7 Free Support"
    },
    "india_aasra": {
        "name": "AASRA Suicide Prevention",
        "phone": "+91 98204 66726",
        "availability": "24/7 Crisis Support"
    },
    "international_emergency": {
        "name": "International Crisis Lifeline",
        "phone": "988 (USA/Canada) or local emergency services (112)",
        "availability": "24/7"
    }
}

class SafetyFirewall:
    """
    Independent AI Safety Screen.
    Evaluates inputs and outputs BEFORE and AFTER LLM and intervention processing.
    Ensures zero diagnostic claims and immediate crisis escalation.
    """

    @classmethod
    def evaluate_input(cls, user_text: str) -> Tuple[str, bool, Dict[str, Any]]:
        """
        Returns:
            (tier, escalation_needed, crisis_resources_dict)
            tier: 'GREEN' | 'AMBER' | 'RED'
        """
        if not user_text:
            return "GREEN", False, {}

        text_lower = user_text.lower().strip()

        # Check RED tier (imminent safety crisis)
        for kw in CRISIS_KEYWORDS:
            if kw in text_lower:
                return "RED", True, {
                    "alert_title": "Immediate Safety Support Available",
                    "message": (
                        "We care about your safety. RESETA is a workplace stress recovery platform "
                        "and cannot provide emergency intervention. Please connect immediately with "
                        "trusted professional support below:"
                    ),
                    "resources": EMERGENCY_RESOURCES
                }

        # Check AMBER tier (persistent/deep emotional distress needing professional care)
        for kw in AMBER_KEYWORDS:
            if kw in text_lower:
                return "AMBER", False, {
                    "alert_title": "Professional Care Pathway Available",
                    "message": (
                        "Self-guided resets may not be enough for what you are experiencing right now. "
                        "Consider speaking with a qualified counsellor or our Care team."
                    ),
                    "tele_manas": EMERGENCY_RESOURCES["india_tele_manas"]
                }

        # Default GREEN tier (Everyday workplace wellness)
        return "GREEN", False, {}

    @classmethod
    def sanitize_ai_output(cls, output_text: str) -> str:
        """
        Enforce strict anti-diagnosis guardrails (Section 28).
        No AI output may provide clinical diagnosis to the employee or HR.
        """
        sanitized = output_text
        for pattern in DIAGNOSTIC_TERMS:
            sanitized = re.sub(
                pattern,
                "what you are describing may be worth discussing with a qualified professional",
                sanitized,
                flags=re.IGNORECASE
            )
        return sanitized
