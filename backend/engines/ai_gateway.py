# RESETA™ Enterprise AI Gateway & Talk It Out™ Engine
# Section 16, 27, 28, 31, 32: Multilingual Hinglish/Hindi/English reflection, independent safety check & model gateway
from typing import Dict, Any
from backend.engines.safety_firewall import SafetyFirewall
from backend.engines.state_engine import StateEngine
from backend.engines.intervention_router import InterventionRouter
from backend.engines.llm_provider import LLMProvider

class AIGateway:
    """
    Vendor-independent AI routing gateway.
    Handles speech-to-text reflections, cultural nuance in Hinglish/Hindi/English,
    and guarantees clinical safety boundaries with pluggable LLM provider support.
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
            fallback_reflection = (
                "Main bilkul samajh raha hoon. Jab ek ke baad ek deliverables aate hain, to dimaag exhaust ho jana bilkul natural hai. "
                "Aapko abhi sab kuch akele fix nahi karna hai. Chaliye 5 minute ka pause lete hain aur saath milkar thoda headspace banate hain."
            )
            action_prompt = "Chaliye 2 minute mein sabse pehle aapka mental load unload karte hain, ek-ek karke."
            lang_instruction = "Respond in warm, natural Hinglish (conversational Hindi-English blend)."
        elif preferred_language == "Hindi":
            fallback_reflection = (
                "मैं आपकी बात पूरी तरह समझ रहा हूँ। जब काम का दबाव एक साथ बढ़ता है, तो थकान महसूस होना स्वाभाविक है। "
                "आपको सब कुछ अभी एक साथ हल करने की ज़रूरत नहीं है। आइए 5 मिनट का शांत विराम लेते हैं।"
            )
            action_prompt = "आइए पहले अपने दिमाग से इस भारीपन को हल्का करें।"
            lang_instruction = "Respond in supportive, calm Hindi."
        else:
            fallback_reflection = (
                "I hear you completely. When multiple urgent demands stack up, feeling overloaded is an entirely natural human response. "
                "You don't have to carry or solve everything this very minute. Let's take 5 quiet minutes together to step back and clear the fog."
            )
            action_prompt = "Let's unload what's occupying your headspace right now, one piece at a time."
            lang_instruction = "Respond in warm, actionable calm English."

        system_prompt = (
            f"You are RESETA TALK™, an empathetic workplace companion having a genuine, supportive 1-on-1 conversation with a colleague. {lang_instruction} "
            "Speak with warmth, authenticity, and actionable calm—like a thoughtful, grounded human mentor. "
            "Never use robotic AI clichés ('As an AI', 'I understand your query', 'How may I assist you today?'). "
            "Acknowledge what they shared in 2 grounded sentences, gently validating their pressure without judgment. "
            "CRITICAL BOUNDARIES: Absolutely NEVER diagnose or use medicalized/clinical terms (such as depression, ADHD, anxiety disorder). "
            "Warmly invite them to take a 5-minute breather together."
        )

        llm_res = LLMProvider.generate_chat_response(
            system_prompt=system_prompt,
            user_prompt=user_text,
            fallback_response=fallback_reflection,
            max_tokens=200,
            temperature=0.3
        )

        # Sanitize output through anti-diagnosis guardrail
        clean_reflection = SafetyFirewall.sanitize_ai_output(llm_res["text"])

        return {
            "reflection": clean_reflection,
            "safety_tier": safety_tier,
            "detected_state": detected_state,
            "recommended_time_minutes": 5,
            "action_prompt": action_prompt,
            "suggested_intervention_id": routed["intervention_id"],
            "suggested_intervention_name": routed["intervention_name"],
            "engine_details": {
                "provider": llm_res["provider"],
                "model": llm_res["model"],
                "status": llm_res["status"]
            },
            "crisis_info": crisis_info if safety_tier == "AMBER" else None
        }
