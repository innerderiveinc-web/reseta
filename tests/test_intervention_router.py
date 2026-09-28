# Unit tests for Intervention Router & Mental Load Unload
import pytest
from backend.engines.intervention_router import InterventionRouter
from backend.engines.state_engine import StateEngine
from backend.engines.mental_load_unload import MentalLoadUnloadEngine

def test_state_engine_classification():
    text_hinglish = "Yaar client deadline hai aur dimaag full ho gaya hai bohot sara kaam hai."
    state = StateEngine.identify_state(text_hinglish)
    assert state in ["overloaded", "work_pressure"]

    text_racing = "My mind won't stop spinning, overthinking everything."
    state2 = StateEngine.identify_state(text_racing)
    assert state2 == "racing_thoughts"

def test_intervention_routing():
    routed = InterventionRouter.route("overloaded", duration_minutes=5)
    assert routed["intervention_id"] == "int_mental_load_unload"
    assert routed["duration_minutes"] == 5
    assert len(routed["steps"]) > 0

    routed_2min = InterventionRouter.route("cant_start", duration_minutes=2)
    assert routed_2min["intervention_id"] == "int_2min_activation"
    assert routed_2min["duration_minutes"] == 2

def test_mental_load_unload():
    raw_input = "Client presentation deadline tomorrow, 3 meetings scheduled, waiting for manager review, inbox is overflowing."
    decomp = MentalLoadUnloadEngine.decompose_mental_load(raw_input)
    assert "now" in decomp
    assert "scheduled" in decomp
    assert "waiting" in decomp
    assert "later" in decomp
    assert "next_action" in decomp
    assert len(decomp["now"]) > 0
    assert len(decomp["next_action"]) > 5
