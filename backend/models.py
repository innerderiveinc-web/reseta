# RESETA™ Enterprise SQLAlchemy Models
import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from backend.database import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(128), unique=True, index=True, nullable=False)
    logo_url = Column(String(512), nullable=True)
    industry = Column(String(128), default="Technology")
    employee_count = Column(Integer, default=500)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    settings = relationship("OrganizationSetting", back_populates="organization", uselist=False)
    departments = relationship("Department", back_populates="organization")
    users = relationship("User", back_populates="organization")
    experiments = relationship("TeamRecoveryExperiment", back_populates="organization")
    campaigns = relationship("HRCampaign", back_populates="organization")

class OrganizationSetting(Base):
    __tablename__ = "organization_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    organization_id = Column(String(64), ForeignKey("organizations.id"), unique=True)
    min_cohort_size = Column(Integer, default=5)
    sso_enabled = Column(Boolean, default=True)
    sso_provider = Column(String(64), default="Microsoft Entra ID / Okta")
    scim_enabled = Column(Boolean, default=True)
    privacy_policy_version = Column(String(32), default="2026.1-DPDP")
    dpdp_compliance_enabled = Column(Boolean, default=True)
    allow_slack_integration = Column(Boolean, default=True)
    allow_teams_integration = Column(Boolean, default=True)
    tele_manas_enabled = Column(Boolean, default=True)
    plan_tier = Column(String(32), default="ENTERPRISE")
    total_licenses = Column(Integer, default=1000)

    organization = relationship("Organization", back_populates="settings")

class Department(Base):
    __tablename__ = "departments"

    id = Column(String(64), primary_key=True, index=True)
    organization_id = Column(String(64), ForeignKey("organizations.id"), index=True)
    name = Column(String(128), nullable=False)
    head_name = Column(String(128), nullable=True)

    organization = relationship("Organization", back_populates="departments")
    teams = relationship("Team", back_populates="department")
    users = relationship("User", back_populates="department")

class Team(Base):
    __tablename__ = "teams"

    id = Column(String(64), primary_key=True, index=True)
    department_id = Column(String(64), ForeignKey("departments.id"), index=True)
    name = Column(String(128), nullable=False)
    manager_id = Column(String(64), nullable=True) # User ID of manager

    department = relationship("Department", back_populates="teams")
    users = relationship("User", back_populates="team")

class User(Base):
    __tablename__ = "users"

    id = Column(String(64), primary_key=True, index=True)
    organization_id = Column(String(64), ForeignKey("organizations.id"), index=True)
    department_id = Column(String(64), ForeignKey("departments.id"), nullable=True)
    team_id = Column(String(64), ForeignKey("teams.id"), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(32), default="EMPLOYEE") # SUPER_ADMIN, HR_ADMIN, WELLNESS_ADMIN, MANAGER, CLINICIAN, AUDITOR, EMPLOYEE
    avatar_url = Column(String(512), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    preferred_language = Column(String(16), default="Hinglish") # English, Hindi, Hinglish

    organization = relationship("Organization", back_populates="users")
    department = relationship("Department", back_populates="users")
    team = relationship("Team", back_populates="users")
    consents = relationship("Consent", back_populates="user")
    sessions = relationship("InterventionSession", back_populates="user")
    patterns = relationship("PersonalPattern", back_populates="user")

class Consent(Base):
    __tablename__ = "consents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), ForeignKey("users.id"), index=True)
    purpose = Column(String(128), nullable=False) # "WELLNESS_INTERVENTIONS", "ANONYMIZED_WORKFORCE_AGGREGATION", "CONTEXTUAL_PROMPTS"
    granted = Column(Boolean, default=True)
    granted_at = Column(DateTime, default=datetime.datetime.utcnow)
    withdrawn_at = Column(DateTime, nullable=True)
    dpdp_notice_acknowledged = Column(Boolean, default=True)

    user = relationship("User", back_populates="consents")

class CheckIn(Base):
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), ForeignKey("users.id"), index=True)
    organization_id = Column(String(64), ForeignKey("organizations.id"), index=True)
    department_id = Column(String(64), nullable=True) # for privacy-safe aggregate only
    state_reported = Column(String(64), nullable=False) # "Stressed", "Overloaded", "Overthinking", "Irritated", "Exhausted", "Work Pressure", "Heavy", "Don't Know"
    time_of_day = Column(String(32)) # "Morning", "Midday", "Evening", "Night"
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    target_state = Column(String(64), nullable=False)
    duration_minutes = Column(Integer, default=5) # 2, 5, 10
    category = Column(String(64), default="Cognitive & Somatic Reset")
    script = Column(JSON, nullable=False)
    voice_script = Column(Text, nullable=True)
    suitable_context = Column(Text, nullable=True)
    exclusion_criteria = Column(Text, nullable=True)
    evidence_references = Column(Text, nullable=True)
    reviewer = Column(String(128), default="Dr. Ananya Sharma, Lead Clinical Psychologist")
    review_date = Column(String(32), default="2026-01-15")
    version = Column(String(16), default="2.1")
    approval_status = Column(String(32), default="APPROVED")

class InterventionSession(Base):
    """
    Core Reliefloop™ session entity.
    NOTE: Detailed user text/transcripts remain securely scoped to the employee
    and are NEVER exposed to organization-level analytics dashboards.
    """
    __tablename__ = "intervention_sessions"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(64), ForeignKey("users.id"), index=True)
    organization_id = Column(String(64), ForeignKey("organizations.id"), index=True)
    department_id = Column(String(64), nullable=True)
    team_id = Column(String(64), nullable=True)
    channel = Column(String(32), default="WEB") # "MOBILE", "WEB", "TEAMS", "SLACK"

    duration_choice_minutes = Column(Integer, default=5)
    starting_state = Column(String(64), nullable=False)
    user_input_mode = Column(String(16), default="TEXT") # "TEXT", "VOICE", "TAP"
    private_raw_input = Column(Text, nullable=True) # PRIVATE to employee only
    
    intervention_id = Column(String(64), ForeignKey("interventions.id"))
    intervention_name = Column(String(128))

    # Mental Load Unload structured outcome
    unload_data = Column(JSON, nullable=True) # NOW, SCHEDULED, WAITING, LATER, NEXT

    # Relief Check™ Metrics
    stress_before = Column(Integer, default=8) # 1 - 10
    stress_after = Column(Integer, default=4) # 1 - 10
    did_this_help = Column(String(16), default="YES") # "YES", "A_LITTLE", "NO"
    is_successful_recovery = Column(Boolean, default=True) # stress_after < stress_before and helped

    # Safety
    safety_tier = Column(String(16), default="GREEN") # "GREEN", "AMBER", "RED"
    escalated_to_care = Column(Boolean, default=False)

    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="sessions")

class PersonalPattern(Base):
    """Personal Relief Map™ & Mind Mirror™ observations"""
    __tablename__ = "personal_patterns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), ForeignKey("users.id"), index=True)
    pattern_type = Column(String(64)) # "EFFICIENT_INTERVENTION", "TIME_OF_DAY_PEAK", "RECOVERY_RATE"
    situation = Column(String(128))
    recommended_intervention = Column(String(128))
    avg_delta_relief = Column(Float, default=3.5)
    helpfulness_rate = Column(Float, default=0.88)
    observation_text = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="patterns")

class SafetyEvent(Base):
    __tablename__ = "safety_events"

    id = Column(String(64), primary_key=True, index=True)
    organization_id = Column(String(64), ForeignKey("organizations.id"), index=True)
    user_id_hash = Column(String(64), index=True) # Anonymized or hashed to protect employee privacy
    tier = Column(String(16), nullable=False) # "AMBER", "RED"
    trigger_type = Column(String(64))
    tele_manas_notified = Column(Boolean, default=True)
    escalation_status = Column(String(32), default="TRIAGED")
    clinical_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class WorkplaceProgram(Base):
    __tablename__ = "workplace_programs"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    duration_days = Column(Integer, default=5)
    target_audience = Column(String(128), default="All Employees")
    steps = Column(JSON) # Array of day/step objects
    active_participants = Column(Integer, default=0)
    completion_rate = Column(Float, default=0.74)

class TeamRecoveryExperiment(Base):
    """Team Recovery Lab™ - Section 25"""
    __tablename__ = "team_recovery_experiments"

    id = Column(String(64), primary_key=True)
    organization_id = Column(String(64), ForeignKey("organizations.id"), index=True)
    title = Column(String(255), nullable=False)
    hypothesis = Column(Text)
    intervention_type = Column(String(128)) # e.g., "Meeting-Free Wednesdays", "Protected Focus Blocks"
    duration_weeks = Column(Integer, default=4)
    target_departments = Column(JSON) # ["Engineering", "Product"]
    status = Column(String(32), default="ACTIVE") # "ACTIVE", "COMPLETED", "PLANNED"
    baseline_recovery_score = Column(Float, default=5.4)
    current_recovery_score = Column(Float, default=7.6)
    participation_count = Column(Integer, default=142)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    findings = Column(Text, nullable=True)

    organization = relationship("Organization", back_populates="experiments")

class HRCampaign(Base):
    """HR Campaign Engine - Section 35"""
    __tablename__ = "hr_campaigns"

    id = Column(String(64), primary_key=True)
    organization_id = Column(String(64), ForeignKey("organizations.id"), index=True)
    title = Column(String(255), nullable=False)
    theme = Column(String(128))
    channels = Column(JSON) # ["SLACK", "TEAMS", "EMAIL"]
    frequency_cap = Column(String(64), default="Once every 48 hours")
    status = Column(String(32), default="RUNNING")
    total_reached = Column(Integer, default=620)
    resets_triggered = Column(Integer, default=384)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    organization = relationship("Organization", back_populates="campaigns")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    organization_id = Column(String(64), index=True)
    actor_id = Column(String(64), nullable=False)
    actor_role = Column(String(32), nullable=False)
    action = Column(String(128), nullable=False) # e.g. "VIEW_AGGREGATE_REPORT", "EXPORT_METRICS", "DPDP_CONSENT_AUDIT"
    details = Column(Text, nullable=True)
    ip_address = Column(String(64), default="127.0.0.1")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
