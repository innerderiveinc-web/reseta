# RESETA™ Enterprise Pytest Centralized Test Fixtures
# Standardized fixtures for client, tenant tokens, and cryptographic headers
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.security import create_access_token
from backend.seeds import seed_database

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Ensure clean seeded state across test session."""
    seed_database()

@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    return TestClient(app)

@pytest.fixture
def employee_token():
    return create_access_token("user-emp-arjun", "EMPLOYEE", "org-technova-01")

@pytest.fixture
def auth_headers_employee(employee_token):
    return {"Authorization": f"Bearer {employee_token}"}

@pytest.fixture
def admin_token():
    return create_access_token("user-admin-rahul", "SUPER_ADMIN", "org-technova-01")

@pytest.fixture
def auth_headers_admin(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

@pytest.fixture
def hr_token():
    return create_access_token("user-hr-kavita", "HR_ADMIN", "org-technova-01")

@pytest.fixture
def auth_headers_hr(hr_token):
    return {"Authorization": f"Bearer {hr_token}"}

@pytest.fixture
def manager_token():
    return create_access_token("user-mgr-priya", "MANAGER", "org-technova-01")

@pytest.fixture
def auth_headers_manager(manager_token):
    return {"Authorization": f"Bearer {manager_token}"}

@pytest.fixture
def care_token():
    return create_access_token("user-care-ananya", "CLINICIAN", "org-technova-01")

@pytest.fixture
def auth_headers_care(care_token):
    return {"Authorization": f"Bearer {care_token}"}
