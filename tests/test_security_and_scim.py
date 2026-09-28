# Tests for RESETA™ Enterprise Security, JWT, LLM Provider, and SCIM 2.0
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.security import create_access_token, decode_access_token, hash_password, verify_password
from backend.engines.llm_provider import LLMProvider

client = TestClient(app)

def test_jwt_token_creation_and_decoding():
    token = create_access_token(user_id="user-test-01", role="EMPLOYEE", org_id="org-test")
    assert token is not None
    assert len(token.split(".")) == 3

    payload = decode_access_token(token)
    assert payload["sub"] == "user-test-01"
    assert payload["role"] == "EMPLOYEE"
    assert payload["org_id"] == "org-test"
    assert "exp" in payload

def test_password_hashing_and_verification():
    raw_pass = "SecurePass@2026"
    stored_hash = hash_password(raw_pass)
    assert verify_password(raw_pass, stored_hash) is True
    assert verify_password("WrongPassword", stored_hash) is False

def test_scim_service_provider_config():
    res = client.get("/api/scim/v2/ServiceProviderConfig")
    assert res.status_code == 200
    data = res.json()
    assert "ServiceProviderConfig" in data["schemas"][0]
    assert data["patch"]["supported"] is True

def test_scim_users_collection():
    res = client.get("/api/scim/v2/Users?count=10")
    assert res.status_code == 200
    data = res.json()
    assert data["totalResults"] >= 6
    assert len(data["Resources"]) > 0
    first_user = data["Resources"][0]
    assert "userName" in first_user
    assert "emails" in first_user

def test_scim_groups_collection():
    res = client.get("/api/scim/v2/Groups")
    assert res.status_code == 200
    data = res.json()
    assert data["totalResults"] >= 5
    assert any(g["displayName"] == "Engineering" for g in data["Resources"])

def test_llm_provider_offline_safe_fallback():
    res = LLMProvider.generate_chat_response(
        system_prompt="You are a clinical assistant.",
        user_prompt="I am overwhelmed with tasks.",
        fallback_response="Let's take a 5-minute break."
    )
    assert "text" in res
    assert res["status"] in ["LIVE_LLM_GENERATED", "DETERMINISTIC_OFFLINE_SAFETY_FALLBACK"]
    assert res["provider"] in ["OPENAI_GPT4O", "GOOGLE_GEMINI", "RESETA_CLINICAL_HEURISTIC_ENGINE"]

def test_login_endpoint_and_jwt_issuance():
    res = client.post("/api/auth/login", json={"email": "arjun@technova.com", "password": "technova2026"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "arjun.sharma@technova.com"
    # Verify token decodes properly
    payload = decode_access_token(data["access_token"])
    assert payload["sub"] == data["user"]["id"]

def test_admin_llm_config_and_inference():
    token = create_access_token("user-admin-rahul", "SUPER_ADMIN", "org-technova-01")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test config
    cfg = client.get("/api/admin/llm-config", headers=headers)
    assert cfg.status_code == 200
    cfg_data = cfg.json()
    assert "active_provider" in cfg_data
    assert "supported_providers" in cfg_data

    # Test inference endpoint
    inf = client.post("/api/admin/llm-test", json={"prompt": "How to decompress quickly?"}, headers=headers)
    assert inf.status_code == 200
    inf_data = inf.json()
    assert "text" in inf_data
    assert "provider" in inf_data

def test_admin_dpdp_genuine_status():
    token = create_access_token("user-admin-rahul", "SUPER_ADMIN", "org-technova-01")
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/api/admin/dpdp-status", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["act_name"] == "Digital Personal Data Protection Act, 2023 / Rules 2025"
    assert data["minimum_cohort_enforced"] == 5
    assert data["privacy_wall_active"] is True
    # Verify genuine non-padded counts
    assert isinstance(data["consent_count"], int)
    assert isinstance(data["audit_events_count"], int)

