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
