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
    client.post("/api/auth/switch-user", json={"user_id": "user-hr-kavita"})
    res = client.get("/api/hr/workforce-metrics")
    assert res.status_code == 200
    data = res.json()
    assert data["total_employees"] == 850
    assert data["successful_recovery_moments"] > 0
    assert len(data["aggregate_themes"]) > 0

def test_manager_copilot_endpoint():
    client.post("/api/auth/switch-user", json={"user_id": "user-mgr-priya"})
    res = client.post("/api/copilot/manager", json={
        "query": "My team is overloaded with sprint deadlines. What should I do?"
    })
    assert res.status_code == 200
    data = res.json()
    assert "RESETA Manager Copilot" in data["copilot_type"]
    assert len(data["answer"]) > 50
    assert "No employee-level check-ins" in data["privacy_guarantee"]

def test_hr_copilot_endpoint():
    client.post("/api/auth/switch-user", json={"user_id": "user-hr-kavita"})
    res = client.post("/api/copilot/hr", json={
        "query": "What themes are increasing this quarter?"
    })
    assert res.status_code == 200
    data = res.json()
    assert "Workforce Intelligence Copilot" in data["copilot_type"]
    assert len(data["answer"]) > 50

def test_pilot_report_endpoint():
    client.post("/api/auth/switch-user", json={"user_id": "user-hr-kavita"})
    res = client.get("/api/hr/pilot-report")
    assert res.status_code == 200
    report = res.json()
    assert "RESETA Workplace Recovery Report" in report["report_title"]
    assert "3_completed_recovery_moments" in report["sections"]
    assert report["sections"]["3_completed_recovery_moments"]["total_recovery_moments"] > 1000

def test_autopilot_prompt_endpoint():
    client.post("/api/auth/switch-user", json={"user_id": "user-emp-arjun"})
    res = client.get("/api/employee/autopilot/prompt?meetings_today=4")
    assert res.status_code == 200
    data = res.json()
    assert data["autopilot_active"] is True
    assert "Take" in data["headline"] or "day" in data["headline"].lower()
    assert "anxiety" not in data["headline"].lower()

def test_dpdp_export_and_consent_toggle():
    client.post("/api/auth/switch-user", json={"user_id": "user-emp-arjun"})
    res = client.get("/api/employee/dpdp/export")
    assert res.status_code == 200
    data = res.json()
    assert "data_subject" in data
    assert "consents" in data
    assert "completed_sessions_count" in data

    toggle_res = client.post("/api/employee/dpdp/consent-toggle", json={
        "purpose": "ANONYMIZED_WORKFORCE_AGGREGATION",
        "granted": False
    })
    assert toggle_res.status_code == 200
    assert toggle_res.json()["granted"] is False

def test_experiment_creation():
    client.post("/api/auth/switch-user", json={"user_id": "user-hr-kavita"})
    res = client.post("/api/hr/experiments", json={
        "title": "25-Minute Meeting Rule Pilot",
        "hypothesis": "Ending meetings 5 minutes early will reduce cognitive fatigue.",
        "intervention_type": "25/50 Min Meeting Rule",
        "duration_weeks": 4,
        "target_departments": ["Engineering"]
    })
    assert res.status_code == 200
    assert res.json()["success"] is True

def test_campaign_creation():
    client.post("/api/auth/switch-user", json={"user_id": "user-hr-kavita"})
    res = client.post("/api/hr/campaigns", json={
        "title": "Focus Without Burnout Week",
        "theme": "Restorative Work Practices",
        "channels": ["SLACK", "TEAMS"],
        "frequency_cap": "Max 1 gentle nudge per 48 hours"
    })
    assert res.status_code == 200
    assert res.json()["success"] is True

def test_governance_hris_connectors_and_sync():
    res = client.get("/api/governance/hris/connectors")
    assert res.status_code == 200
    connectors = res.json()
    assert len(connectors) >= 3
    provider_ids = [c["provider_id"] for c in connectors]
    assert "darwinbox" in provider_ids
    assert "zoho_people" in provider_ids
    assert "workday" in provider_ids

    sync_res = client.post("/api/governance/hris/sync", json={"provider_id": "darwinbox"})
    assert sync_res.status_code == 200
    data = sync_res.json()
    assert data["success"] is True
    assert "Darwinbox" in data["provider"]

def test_governance_red_team_and_checklist():
    res = client.post("/api/governance/red-team/run")
    assert res.status_code == 200
    data = res.json()
    assert data["pass_rate_pct"] == 100
    assert data["total_vectors_tested"] == 10

    chk_res = client.get("/api/governance/ai-release-checklist")
    assert chk_res.status_code == 200
    chk = chk_res.json()
    assert len(chk["items"]) == 7
    assert all(item["status"] == "CERTIFIED" for item in chk["items"])

def test_modular_enterprise_pages():
    routes = {
        "/about": "Qsura India Pvt. Ltd.",
        "/security": "Zero-Surveillance",
        "/pricing": "Predictable Seat-Based Pricing",
        "/faq": "Frequently Asked Questions",
        "/contact": "Book an Enterprise Demo",
        "/privacy": "Digital Personal Data Protection Act",
        "/terms": "Master Services Agreement"
    }
    for route, expected_text in routes.items():
        resp = client.get(route)
        assert resp.status_code == 200, f"Route {route} failed with status {resp.status_code}"
        assert expected_text in resp.text, f"Expected '{expected_text}' not found in {route}"

def test_rbac_forbidden_and_allowed_access():
    # 1. Switch to normal employee
    client.post("/api/auth/switch-user", json={"user_id": "user-emp-arjun"})

    # Employee attempting privileged operations -> 403 Forbidden
    admin_res = client.get("/api/admin/organization-settings")
    assert admin_res.status_code == 403, f"Expected 403 for employee on admin, got {admin_res.status_code}"

    hr_res = client.get("/api/hr/workforce-metrics")
    assert hr_res.status_code == 403, f"Expected 403 for employee on hr, got {hr_res.status_code}"

    care_res = client.get("/api/care/triage-queue")
    assert care_res.status_code == 403, f"Expected 403 for employee on care, got {care_res.status_code}"

    # 2. Switch to Super Admin -> 200 OK across admin
    client.post("/api/auth/switch-user", json={"user_id": "user-admin-rahul"})
    admin_ok = client.get("/api/admin/organization-settings")
    assert admin_ok.status_code == 200

    # 3. Switch to Clinician -> 200 OK on care triage
    client.post("/api/auth/switch-user", json={"user_id": "user-care-ananya"})
    care_ok = client.get("/api/care/triage-queue")
    assert care_ok.status_code == 200





