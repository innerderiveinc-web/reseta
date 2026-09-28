# RESETA™ Enterprise AI Gateway & Talk It Out™ Engine
# Section 16, 27, 28, 31, 32: Multilingual Hinglish/Hindi/English reflection, independent safety check & model gateway
from typing import Dict, Any
from backend.engines.safety_firewall import SafetyFirewall
from backend.engines.state_engine import StateEngine
from backend.engines.intervention_router import InterventionRouter

class AIGateway:
    """
    Vendor-independent AI routing gateway.
    Handles speech-to-text reflections, cultural nuance in Hinglish,
    and guarantees clinical safety boundaries.
    """

    @classmethod
    def process_talk_it_out(
        cls,
        user_text: str,
        preferred_language: str = "Hinglish"
    ) -> Dict[str, Any]:
        # Step 1: Independent Safety Screen
        safety_tier, escalation_needed, crisis_info = SafetyFirewall.evaluate_input(user_text)

        if safety_tier == "RED":
            return {
                "reflection": (
                    "Please pause. Your wellbeing and safety are paramount. "
                    "RESETA is a workplace stress recovery platform and cannot substitute for crisis care. "
                    "Please connect right away with professional emergency support."
                ),
                "safety_tier": "RED",
                "detected_state": "crisis",
                "recommended_time_minutes": 0,
                "action_prompt": "Emergency resources activated.",
                "suggested_intervention_id": "care_escalation",
                "suggested_intervention_name": "Immediate Care Support",
                "crisis_info": crisis_info
            }

        # Step 2: State Detection
        detected_state = StateEngine.identify_state(user_text)

        # Step 3: Route Intervention
        routed = InterventionRouter.route(detected_state, duration_minutes=5)

        # Step 4: Culturally tailored empathetic reflection
        text_lower = user_text.lower()
        is_hinglish_or_hindi = any(w in text_lower for w in ["hai", "yaar", "kaam", "bahut", "dimaag", "karna", "nahi", "ho raha", "hoga", "mujhe"])

        if is_hinglish_or_hindi or preferred_language == "Hinglish":
            reflection = (
                "Main sun raha hoon. Jab ek ke baad ek cheezein aati hain, to dimaag overwhelmed feel hona natural hai. "
                "Aapko sab kuch abhi isi pal solve nahi karna hai. Chaliye pehle 5 minute ka reset karte hain aur isko clear karte hain."
            )
            action_prompt = "Chaliye 2 minute mein sabse pehle aapka mental load unload karte hain."
        elif preferred_language == "Hindi":
            reflection = (
                "मैं आपकी बात समझ रहा हूँ। जब काम का दबाव बढ़ता है, तो मन पर बोझ महसूस होना स्वाभाविक है। "
                "आपको सब कुछ अभी एक साथ हल करने की आवश्यकता नहीं है। आइए 5 मिनट का विराम लें।"
            )
            action_prompt = "आइए पहले अपने दिमाग से इस तनाव को खाली करें।"
        else:
            reflection = (
                "I hear you. When multiple priorities demand your attention at once, feeling overloaded is a completely natural reaction. "
                "You do not need to resolve everything this very minute. Let's take 5 minutes together to clear the noise."
            )
            action_prompt = "Let's unload what's occupying your headspace right now."

        # Sanitize output through anti-diagnosis guardrail
        clean_reflection = SafetyFirewall.sanitize_ai_output(reflection)

        return {
            "reflection": clean_reflection,
            "safety_tier": safety_tier,
            "detected_state": detected_state,
            "recommended_time_minutes": 5,
            "action_prompt": action_prompt,
            "suggested_intervention_id": routed["intervention_id"],
            "suggested_intervention_name": routed["intervention_name"],
            "crisis_info": crisis_info if safety_tier == "AMBER" else None
        }
