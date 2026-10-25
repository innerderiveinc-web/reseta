# RESETA™ Enterprise Domain Enums & Controlled Vocabularies
# Standardized type-safe definitions for RBAC, Safety Tiers, and Clinical States
from enum import Enum

class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    HR_ADMIN = "HR_ADMIN"
    WELLNESS_ADMIN = "WELLNESS_ADMIN"
    MANAGER = "MANAGER"
    CLINICIAN = "CLINICIAN"
    AUDITOR = "AUDITOR"
    EMPLOYEE = "EMPLOYEE"

class SafetyTier(str, Enum):
    GREEN = "GREEN"
    AMBER = "AMBER"
    RED = "RED"

class ReportedState(str, Enum):
    STRESSED = "Stressed"
    OVERLOADED = "Overloaded"
    OVERTHINKING = "Overthinking"
    IRRITATED = "Irritated"
    EXHAUSTED = "Exhausted"
    WORK_PRESSURE = "Work Pressure"
    HEAVY = "Heavy"
    DONT_KNOW = "Don't Know"

class ConsentPurpose(str, Enum):
    WELLNESS_INTERVENTIONS = "WELLNESS_INTERVENTIONS"
    ANONYMIZED_WORKFORCE_AGGREGATION = "ANONYMIZED_WORKFORCE_AGGREGATION"
    CONTEXTUAL_PROMPTS = "CONTEXTUAL_PROMPTS"

class PlanTier(str, Enum):
    ENTERPRISE = "ENTERPRISE"
    GROWTH = "GROWTH"
    PILOT = "PILOT"

class ResetInputMode(str, Enum):
    TAP = "TAP"
    TEXT = "TEXT"
    VOICE = "VOICE"
