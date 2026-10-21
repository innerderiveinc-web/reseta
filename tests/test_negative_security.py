# RESETA™ Enterprise Brutal Audit Remediation & Negative Security Verification Suite
# Rigorous validation of P0 vulnerabilities, tenant isolation, and clinical safety guardrails
import os
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.security import create_access_token
from backend.engines.safety_firewall import SafetyFirewall
from backend.config import Settings

client = TestClient(app)

# ==============================================================================
# P0.1: Unauthenticated Employee Access Rejection
# ==============================================================================
def test_unauthenticated_employee_endpoints_return_401():
    """Verify missing, invalid, or expired tokens reject immediately with 401 (No Arjun fallback)."""
    # 1. Missing Authorization header
    res = client.post("/api/employee/checkin", json={"state_reported": "Overloaded"})
    assert res.status_code == 401
    assert "WWW-Authenticate" in res.headers

    # 2. Malformed token
    res_bad = client.post(
        "/api/employee/checkin",
        json={"state_reported": "Overloaded"},
        headers={"Authorization": "Bearer bad.token.here"}
    )
    assert res_bad.status_code == 401

    # 3. Personal relief map requires auth
    res_map = client.get("/api/employee/personal-relief-map")
    assert res_map.status_code == 401

    # 4. Autopilot proactive prompt requires auth
    res_prompt = client.get("/api/employee/autopilot/prompt")
    assert res_prompt.status_code == 401

    # 5. Export personal data requires auth
    res_export = client.get("/api/employee/dpdp/export")
    assert res_export.status_code == 401

# ==============================================================================
# P0.2: Switch-User Privilege Escalation Controls
# ==============================================================================
def test_switch_user_arbitrary_user_rejected():
    """Unauthorized impersonation into arbitrary or non-demo accounts must be rejected with 403."""
    res = client.post("/api/auth/switch-user", json={"user_id": "user-non-existent-or-victim"})
    assert res.status_code == 403
    assert "Unauthorized impersonation" in res.json()["detail"]

def test_switch_user_disabled_in_production(monkeypatch):
    """In production mode, persona switching must be strictly disabled."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    res = client.post("/api/auth/switch-user", json={"user_id": "user-emp-arjun"})
    assert res.status_code == 403
    assert "disabled in production" in res.json()["detail"]

# ==============================================================================
# P0.3: Login Rejects Every Wrong Password
# ==============================================================================
def test_login_wrong_password_rejected():
    """Verify wrong passwords explicitly return HTTP 401 (no pass fallthrough)."""
    # Wrong password for existing user
    res = client.post("/api/auth/login", json={
        "email": "arjun.sharma@technova.com",
        "password": "incorrect_password_123"
    })
    assert res.status_code == 401
    assert "Invalid enterprise email or password" in res.json()["detail"]

    # Wrong password with demo password string for different user
    res_fake = client.post("/api/auth/login", json={
        "email": "rahul.verma@technova.com",
        "password": "wrong_password_2026"
    })
    assert res_fake.status_code == 401

    # Non-existent user
    res_ghost = client.post("/api/auth/login", json={
        "email": "ghost.user@unknown.com",
        "password": "technova2026"
    })
    assert res_ghost.status_code == 401

# ==============================================================================
# P0.4: SCIM Endpoints Require Auth & Enforce Scopes
# ==============================================================================
def test_scim_endpoints_unauthenticated_rejected():
    """SCIM user list, single user, and groups must reject unauthenticated requests with 401."""
    # List users without token
    assert client.get("/api/scim/v2/Users").status_code == 401

    # Specific user without token
    assert client.get("/api/scim/v2/Users/user-emp-arjun").status_code == 401

    # Groups without token
    assert client.get("/api/scim/v2/Groups").status_code == 401

def test_scim_requires_privileged_role():
    """Standard employees cannot query SCIM directory (requires SUPER_ADMIN or HR_ADMIN)."""
    emp_token = create_access_token("user-emp-arjun", "EMPLOYEE", "org-technova-01")
    res = client.get("/api/scim/v2/Users", headers={"Authorization": f"Bearer {emp_token}"})
    assert res.status_code == 403

# ==============================================================================
# P1: Strict Cross-Tenant Isolation
# ==============================================================================
def test_cross_tenant_isolation_enforced():
    """Prove that Tenant B cannot access or enumerate Tenant A's data."""
    import uuid
    uid = uuid.uuid4().hex[:6]

    # 1. Onboard Tenant B
    reg_res = client.post("/api/auth/register-company", json={
        "company_name": f"Acme Tenant {uid}",
        "admin_name": f"Alice Admin {uid}",
        "admin_email": f"alice.{uid}@acmetenant.com",
        "password": "SecurePassword987!",
        "employee_count": 50
    })
    assert reg_res.status_code == 200
    tenant_b_data = reg_res.json()
    tenant_b_token = tenant_b_data["access_token"]
    tenant_b_headers = {"Authorization": f"Bearer {tenant_b_token}"}
    tenant_b_org_id = tenant_b_data["organization_id"]

    # 2. SCIM Users query from Tenant B MUST ONLY return Tenant B's users (1 admin), NOT TechNova's 20+ users
    scim_res = client.get("/api/scim/v2/Users", headers=tenant_b_headers)
    assert scim_res.status_code == 200
    scim_data = scim_res.json()
    assert scim_data["totalResults"] == 1
    assert scim_data["Resources"][0]["userName"] == f"alice.{uid}@acmetenant.com"

    # 3. Tenant B requesting TechNova's employee via SCIM by ID must return 404
    cross_user_res = client.get("/api/scim/v2/Users/user-emp-arjun", headers=tenant_b_headers)
    assert cross_user_res.status_code == 404

    # 4. Tenant B requesting organization settings receives Tenant B settings, NOT TechNova
    settings_res = client.get("/api/admin/organization-settings", headers=tenant_b_headers)
    assert settings_res.status_code == 200
    assert settings_res.json()["organization_id"] == tenant_b_org_id
    assert settings_res.json()["name"] == f"Acme Tenant {uid}"

    # 5. Tenant B requesting HR campaigns receives 0 campaigns, NOT TechNova's campaigns
    camp_res = client.get("/api/hr/campaigns", headers=tenant_b_headers)
    assert camp_res.status_code == 200
    assert len(camp_res.json()) == 0

    # 6. Tenant B requesting Audit logs receives Tenant B logs only
    audit_res = client.get("/api/admin/audit-logs", headers=tenant_b_headers)
    assert audit_res.status_code == 200
    for log_item in audit_res.json():
        assert log_item["actor_id"] == tenant_b_data["admin_user"]["id"]

# ==============================================================================
# Clinical Safety: Negation, Cultural Nuance & Output Sanitization
# ==============================================================================
def test_safety_firewall_negation_handling():
    """Verify that statements with explicit negations do not trigger false RED alarms."""
    # Negated suicide mention
    tier1, esc1, _ = SafetyFirewall.evaluate_input("I am not feeling suicidal, just overwhelmed by deadlines")
    assert tier1 != "RED"

    tier2, esc2, _ = SafetyFirewall.evaluate_input("I never thought of suicide, work is just stressful")
    assert tier2 != "RED"

    tier3, esc3, _ = SafetyFirewall.evaluate_input("kabhi marne ka nahi socha, bas kaam bahut zyada hai")
    assert tier3 != "RED"

    # Actual crisis triggers RED
    tier4, esc4, _ = SafetyFirewall.evaluate_input("I want to kill myself, I can't take this anymore")
    assert tier4 == "RED"
    assert esc4 is True

    tier5, esc5, _ = SafetyFirewall.evaluate_input("jaan de dunga, sab khatam ho gaya")
    assert tier5 == "RED"
    assert esc5 is True

def test_safety_firewall_prescription_sanitization():
    """Ensure pharmacological recommendations and diagnostic claims are scrubbed."""
    raw_output = "You should take antidepressants and increase your dosage because you have depression."
    cleaned = SafetyFirewall.sanitize_ai_output(raw_output)
    assert "antidepressants" not in cleaned.lower()
    assert "increase your dosage" not in cleaned.lower()
    assert "you have depression" not in cleaned.lower()
    assert "qualified professional" in cleaned

# ==============================================================================
# Production Hardening: Secret Key & Settings Validation
# ==============================================================================
def test_production_weak_secret_fails_startup():
    """Ensure startup fails when default secret is used in production mode."""
    with pytest.raises(ValueError) as excinfo:
        Settings(
            ENVIRONMENT="production",
            SECRET_KEY="reseta-enterprise-super-secure-secret-token-2026"
        )
    assert "FATAL SECURITY MISCONFIGURATION" in str(excinfo.value)
