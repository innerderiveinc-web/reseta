# Unit tests for RESETA™ API Endpoints
import pytest
from starlette.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["safety_firewall"] == "ACTIVE"

def test_auth_users_and_switching():
    resp = client.get("/api/auth/users")
    assert resp.status_code == 200
    users = resp.json()
    assert len(users) >= 4

    switch_resp = client.post("/api/auth/switch-user", json={"user_id": "user-hr-kavita"})
    assert switch_resp.status_code == 200
    assert switch_resp.json()["role"] == "HR_ADMIN"

def test_checkin_and_reset_flow():
    # 1. Switch back to employee
    client.post("/api/auth/switch-user", json={"user_id": "user-emp-arjun"})

    # 2. Check-in
    checkin_res = client.post("/api/employee/checkin", json={"state_reported": "Overloaded"})
    assert checkin_res.status_code == 200
    assert checkin_res.json()["state_reported"] == "Overloaded"

    # 3. Create Reset plan
    plan_res = client.post("/api/employee/reset/plan", json={
        "time_choice_minutes": 5,
        "state": "overloaded",
        "input_mode": "TEXT",
        "raw_input": "Client deadline presentation is pending and 4 meetings back to back"
    })
    assert plan_res.status_code == 200
    plan_data = plan_res.json()
    assert plan_data["safety_tier"] == "GREEN"
    assert plan_data["intervention_id"] == "int_mental_load_unload"
    assert len(plan_data["steps"]) > 0
    assert plan_data["unload_result"] is not None

    # 4. Complete reset (Relief Check™)
    complete_res = client.post("/api/employee/reset/complete", json={
        "session_id": plan_data["session_id"],
        "stress_before": 8,
        "stress_after": 4,
        "did_this_help": "YES"
    })
    assert complete_res.status_code == 200
    comp_data = complete_res.json()
    assert comp_data["delta_relief"] == 4
    assert comp_data["is_successful_recovery"] is True

def test_talk_it_out_endpoint():
    res = client.post("/api/employee/talk-it-out", json={
        "transcript_or_text": "Yaar aaj sach me bohot zyada pressure feel ho raha hai",
        "language": "Hinglish"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["safety_tier"] == "GREEN"
    assert len(data["reflection"]) > 10

def test_hr_workforce_metrics():
    res = client.get("/api/hr/workforce-metrics")
    assert res.status_code == 200
    data = res.json()
    assert data["total_employees"] == 850
    assert data["successful_recovery_moments"] > 0
    assert len(data["aggregate_themes"]) > 0

def test_manager_copilot_endpoint():
    res = client.post("/api/copilot/manager", json={
        "query": "My team is overloaded with sprint deadlines. What should I do?"
    })
    assert res.status_code == 200
    data = res.json()
    assert "RESETA Manager Copilot" in data["copilot_type"]
    assert len(data["answer"]) > 50
    assert "No employee-level check-ins" in data["privacy_guarantee"]

def test_hr_copilot_endpoint():
    res = client.post("/api/copilot/hr", json={
        "query": "What themes are increasing this quarter?"
    })
    assert res.status_code == 200
    data = res.json()
    assert "Workforce Intelligence Copilot" in data["copilot_type"]
    assert len(data["answer"]) > 50

def test_pilot_report_endpoint():
    res = client.get("/api/hr/pilot-report")
    assert res.status_code == 200
    report = res.json()
    assert "RESETA Workplace Recovery Report" in report["report_title"]
    assert "3_completed_recovery_moments" in report["sections"]
    assert report["sections"]["3_completed_recovery_moments"]["total_recovery_moments"] > 1000

