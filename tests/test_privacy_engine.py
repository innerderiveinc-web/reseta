# Unit tests for Privacy Engine & DPDP k-anonymity
import pytest
from backend.engines.privacy_engine import PrivacyEngine
from backend.database import SessionLocal
from backend.seeds import seed_database

def test_hr_language_sanitization():
    # Section 22: Do not call everything "risk"
    raw_statement = "We have 35 high-risk employees in the engineering org who have burnout risk."
    sanitized = PrivacyEngine.sanitize_hr_language(raw_statement)
    assert "high-risk employees" not in sanitized
    assert "burnout risk" not in sanitized
    assert "participating team members experiencing elevated workplace strain" in sanitized

def test_privacy_cohort_aggregation():
    db = SessionLocal()
    try:
        # Organization with > 5 users should return themes safely
        res = PrivacyEngine.aggregate_workforce_themes(db, organization_id="org-technova-01")
        assert res["cohort_meets_threshold"] is True
        assert res["cohort_size"] >= 5
        assert len(res["themes"]) > 0

        # Non-existent or empty department should enforce suppression (k < 5)
        res_empty = PrivacyEngine.aggregate_workforce_themes(db, organization_id="org-technova-01", department_id="dept-nonexistent")
        assert res_empty["cohort_meets_threshold"] is False
        assert "suppressed" in res_empty["privacy_message"].lower()
    finally:
        db.close()
