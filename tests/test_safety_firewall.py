# Unit tests for RESETA™ Safety Firewall
import pytest
from backend.engines.safety_firewall import SafetyFirewall

def test_safety_firewall_green_tier():
    text = "Client deadline is tomorrow and I have 4 back-to-back sprint calls."
    tier, escalated, resources = SafetyFirewall.evaluate_input(text)
    assert tier == "GREEN"
    assert escalated is False
    assert resources == {}

def test_safety_firewall_amber_tier():
    text = "I feel completely hopeless, crying non stop, can't cope with anything anymore."
    tier, escalated, resources = SafetyFirewall.evaluate_input(text)
    assert tier == "AMBER"
    assert escalated is False
    assert "tele_manas" in resources
    assert "14416" in resources["tele_manas"]["toll_free"]

def test_safety_firewall_red_tier():
    text = "I want to end my life, mar jana chahta hoon."
    tier, escalated, resources = SafetyFirewall.evaluate_input(text)
    assert tier == "RED"
    assert escalated is True
    assert "resources" in resources
    assert "india_tele_manas" in resources["resources"]
    assert "14416 / 1800-89-14416" in resources["resources"]["india_tele_manas"]["toll_free"]

def test_anti_diagnosis_sanitizer():
    # Section 28: AI must not diagnose
    raw_ai_text = "Based on our conversation, you have depression and you are clinically burned out."
    sanitized = SafetyFirewall.sanitize_ai_output(raw_ai_text)
    assert "you have depression" not in sanitized.lower()
    assert "clinically burned out" not in sanitized.lower()
    assert "what you are describing may be worth discussing with a qualified professional" in sanitized
