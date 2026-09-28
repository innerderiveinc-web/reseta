# RESETA™ Enterprise Pydantic Schemas
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import datetime

# User & Auth
class UserProfile(BaseModel):
    id: str
    organization_id: str
    department_id: Optional[str] = None
    team_id: Optional[str] = None
    email: str
    full_name: str
    role: str
    preferred_language: str
    avatar_url: Optional[str] = None
    access_token: Optional[str] = None

class SwitchUserRequest(BaseModel):
    user_id: str

# Check-in
class CheckInRequest(BaseModel):
    state_reported: str
    time_of_day: Optional[str] = None

class CheckInResponse(BaseModel):
    success: bool
    state_reported: str
    suggested_time_minutes: int
    prompt_message: str

# ReliefLoop™ Engine Schemas
class ResetIntentRequest(BaseModel):
    time_choice_minutes: int = 5 # 2, 5, 10
    state: str # "overloaded", "racing_thoughts", "work_pressure", "cant_start", "rumination", "frustration", "night_stress", "decision_overload", "low_energy", "general_tension"
    input_mode: str = "TEXT" # "TEXT", "VOICE", "TAP"
    raw_input: Optional[str] = None # Private employee text or speech transcript
    language: str = "Hinglish" # "English", "Hindi", "Hinglish"
    channel: str = "WEB" # "WEB", "MOBILE", "TEAMS", "SLACK"

class UnloadCategory(BaseModel):
    now: List[str]
    scheduled: List[str]
    waiting: List[str]
    later: List[str]
    next_action: str

class StepScript(BaseModel):
    timestamp_label: str
    action_type: str # "PAUSE", "BREATHE", "UNLOAD", "REFLECT", "MICRO_STEP"
    title: str
    instruction: str
    voice_cue: Optional[str] = None
    duration_seconds: int

class ResetSessionPlanResponse(BaseModel):
    session_id: str
    intervention_id: str
    intervention_name: str
    target_state: str
    duration_minutes: int
    safety_tier: str # "GREEN", "AMBER", "RED"
    escalation_needed: bool = False
    crisis_resources: Optional[Dict[str, Any]] = None
    steps: List[StepScript]
    unload_result: Optional[UnloadCategory] = None
    closing_prompt: Optional[str] = "You've created breathing room. Take a sip of water before returning to your work."

class CompleteResetRequest(BaseModel):
    session_id: str
    stress_before: int = Field(..., ge=1, le=10)
    stress_after: int = Field(..., ge=1, le=10)
    did_this_help: str # "YES", "A_LITTLE", "NO"
    feedback_notes: Optional[str] = None

class CompleteResetResponse(BaseModel):
    success: bool
    session_id: str
    delta_relief: int
    is_successful_recovery: bool
    personal_insight: str
    next_recommendation: str

# Talk It Out™
class TalkItOutRequest(BaseModel):
    transcript_or_text: str
    language: str = "Hinglish"
    audio_present: bool = False

class TalkItOutResponse(BaseModel):
    reflection: str
    safety_tier: str
    detected_state: str
    recommended_time_minutes: int
    action_prompt: str
    suggested_intervention_id: str
    suggested_intervention_name: str
    crisis_info: Optional[Dict[str, Any]] = None

# Manager Experience Schemas
class TeamInsightResponse(BaseModel):
    team_name: str
    team_size: int
    cohort_meets_threshold: bool
    privacy_notice: str
    participation_rate: float
    top_workplace_themes: List[Dict[str, Any]]
    suggested_actions: List[Dict[str, Any]]

class ManagerCoachScenario(BaseModel):
    scenario_id: str
    title: str
    employee_signal: str
    manager_guidance: str
    recommended_phrases: List[str]
    what_to_avoid: List[str]
    suggested_follow_up: str

# HR / People Dashboard Schemas
class WorkforceMetricsResponse(BaseModel):
    organization_name: str
    total_employees: int
    active_waus: int
    activation_rate: float
    total_resets_completed: int
    successful_recovery_moments: int # NORTH STAR METRIC
    avg_relief_delta: float
    cohort_threshold_enforced: int
    aggregate_themes: List[Dict[str, Any]]
    department_benchmarks: List[Dict[str, Any]]
    weekly_trends: List[Dict[str, Any]]
    action_recommendations: List[Dict[str, Any]]

class CreateExperimentRequest(BaseModel):
    title: str
    hypothesis: str
    intervention_type: str
    duration_weeks: int = 4
    target_departments: List[str]

class CreateCampaignRequest(BaseModel):
    title: str
    theme: str
    channels: List[str]
    frequency_cap: str

# Care Console
class CareEscalationItem(BaseModel):
    id: str
    created_at: str
    tier: str
    anonymized_reference: str
    trigger_type: str
    tele_manas_notified: bool
    status: str
    recommended_action: str

# Trust & DPDP Schemas
class DPDPStatusResponse(BaseModel):
    act_name: str
    rules_version: str
    consent_count: int
    withdrawn_count: int
    audit_events_count: int
    minimum_cohort_enforced: int
    privacy_wall_active: bool
