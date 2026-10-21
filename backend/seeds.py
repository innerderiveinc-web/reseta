# RESETA™ Enterprise Realistic Seed Data
import uuid
import datetime
from sqlalchemy.orm import Session
from backend.database import SessionLocal, Base, engine
from backend.models import (
    Organization, OrganizationSetting, Department, Team, User, Consent,
    CheckIn, Intervention, InterventionSession, PersonalPattern,
    WorkplaceProgram, TeamRecoveryExperiment, HRCampaign, AuditLog, SafetyEvent
)
from backend.engines.intervention_router import INTERVENTION_CATALOG
from backend.security import hash_password

def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    default_pwd_hash = hash_password("technova2026")

    # Check if already seeded
    existing_org = db.query(Organization).filter(Organization.id == "org-technova-01").first()
    if existing_org:
        # Guarantee all existing seed users have cryptographic password hashes
        unhashed_users = db.query(User).filter((User.hashed_password == None) | (User.hashed_password == "")).all()
        if unhashed_users:
            for u in unhashed_users:
                u.hashed_password = default_pwd_hash
            db.commit()
        db.close()
        return

    print("Seeding RESETA™ Enterprise with realistic enterprise workplace dataset...")

    # 1. Organization
    org = Organization(
        id="org-technova-01",
        name="TechNova Solutions India",
        slug="technova",
        industry="Enterprise Software & AI Cloud",
        employee_count=850,
        logo_url="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=120&auto=format&fit=crop&q=80"
    )
    db.add(org)

    # 2. Organization Settings
    org_settings = OrganizationSetting(
        organization_id=org.id,
        min_cohort_size=5,
        sso_enabled=True,
        sso_provider="Microsoft Entra ID & Okta SAML 2.0",
        scim_enabled=True,
        privacy_policy_version="2026.1-DPDP",
        dpdp_compliance_enabled=True,
        allow_slack_integration=True,
        allow_teams_integration=True,
        tele_manas_enabled=True,
        plan_tier="ENTERPRISE",
        total_licenses=1000
    )
    db.add(org_settings)

    # 3. Departments & Teams
    dept_eng = Department(id="dept-eng", organization_id=org.id, name="Engineering", head_name="Vikram Seth")
    dept_prod = Department(id="dept-prod", organization_id=org.id, name="Product & Design", head_name="Meera Sen")
    dept_cs = Department(id="dept-cs", organization_id=org.id, name="Customer Success", head_name="Rohan Gupta")
    dept_hr = Department(id="dept-hr", organization_id=org.id, name="People & Culture", head_name="Kavita Mehta")
    dept_sales = Department(id="dept-sales", organization_id=org.id, name="Sales & Marketing", head_name="Amitabh Sen")

    db.add_all([dept_eng, dept_prod, dept_cs, dept_hr, dept_sales])

    team_platform = Team(id="team-platform", department_id=dept_eng.id, name="Platform & Cloud Infra", manager_id="user-mgr-priya")
    team_frontend = Team(id="team-frontend", department_id=dept_eng.id, name="Frontend Experience", manager_id="user-mgr-priya")
    team_product = Team(id="team-product", department_id=dept_prod.id, name="Core Product Team", manager_id="user-mgr-rohan")

    db.add_all([team_platform, team_frontend, team_product])

    # 4. Users (Covering all 7 RBAC roles from Section 38)
    user_emp = User(
        id="user-emp-arjun",
        organization_id=org.id,
        department_id=dept_eng.id,
        team_id=team_frontend.id,
        email="arjun.sharma@technova.com",
        full_name="Arjun Sharma",
        role="EMPLOYEE",
        hashed_password=default_pwd_hash,
        preferred_language="Hinglish",
        avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=120&auto=format&fit=crop&q=80"
    )

    user_mgr = User(
        id="user-mgr-priya",
        organization_id=org.id,
        department_id=dept_eng.id,
        team_id=team_frontend.id,
        email="priya.nair@technova.com",
        full_name="Priya Nair",
        role="MANAGER",
        hashed_password=default_pwd_hash,
        preferred_language="English",
        avatar_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=120&auto=format&fit=crop&q=80"
    )

    user_hr = User(
        id="user-hr-kavita",
        organization_id=org.id,
        department_id=dept_hr.id,
        team_id=None,
        email="kavita.mehta@technova.com",
        full_name="Kavita Mehta",
        role="HR_ADMIN",
        hashed_password=default_pwd_hash,
        preferred_language="English",
        avatar_url="https://images.unsplash.com/photo-1580489944761-15a19d654956?w=120&auto=format&fit=crop&q=80"
    )

    user_admin = User(
        id="user-admin-rahul",
        organization_id=org.id,
        department_id=dept_eng.id,
        team_id=None,
        email="rahul.verma@technova.com",
        full_name="Rahul Verma",
        role="SUPER_ADMIN",
        hashed_password=default_pwd_hash,
        preferred_language="English",
        avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=120&auto=format&fit=crop&q=80"
    )

    user_care = User(
        id="user-care-ananya",
        organization_id=org.id,
        department_id=None,
        team_id=None,
        email="ananya.sharma@reseta-care.internal",
        full_name="Dr. Ananya Sharma",
        role="CLINICIAN",
        hashed_password=default_pwd_hash,
        preferred_language="English",
        avatar_url="https://images.unsplash.com/photo-1594824813586-7a87640c4954?w=120&auto=format&fit=crop&q=80"
    )

    user_auditor = User(
        id="user-audit-suresh",
        organization_id=org.id,
        department_id=dept_hr.id,
        team_id=None,
        email="suresh.iyer@technova.com",
        full_name="Suresh Iyer",
        role="AUDITOR",
        hashed_password=default_pwd_hash,
        preferred_language="English",
        avatar_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=120&auto=format&fit=crop&q=80"
    )

    # Additional employees for k-anonymity validation
    extra_users = [
        User(id=f"user-emp-extra-{i}", organization_id=org.id, department_id=dept_eng.id, team_id=team_frontend.id,
             email=f"dev{i}@technova.com", full_name=f"Developer {i}", role="EMPLOYEE", hashed_password=default_pwd_hash)
        for i in range(1, 15)
    ]

    db.add_all([user_emp, user_mgr, user_hr, user_admin, user_care, user_auditor] + extra_users)

    # 5. Consents (DPDP Act, 2023 compliant)
    all_users = [user_emp, user_mgr, user_hr, user_admin, user_care, user_auditor] + extra_users
    for u in all_users:
        c1 = Consent(user_id=u.id, purpose="WELLNESS_INTERVENTIONS", granted=True, dpdp_notice_acknowledged=True)
        c2 = Consent(user_id=u.id, purpose="ANONYMIZED_WORKFORCE_AGGREGATION", granted=True, dpdp_notice_acknowledged=True)
        c3 = Consent(user_id=u.id, purpose="CONTEXTUAL_PROMPTS", granted=True, dpdp_notice_acknowledged=True)
        db.add_all([c1, c2, c3])

    # 6. Interventions catalog from INTERVENTION_CATALOG
    for key, data in INTERVENTION_CATALOG.items():
        inv = Intervention(
            id=data["id"],
            name=data["name"],
            target_state=data["target_state"],
            duration_minutes=5,
            category=data["category"],
            script=data["steps_by_duration"],
            evidence_references=data["evidence"],
            reviewer=data["reviewer"]
        )
        db.add(inv)

    # 7. Realistic historical recovery sessions (Generating over 140 realistic recovery moments)
    now = datetime.datetime.utcnow()
    departments_pool = [dept_eng.id, dept_prod.id, dept_cs.id, dept_sales.id]
    states_pool = ["overloaded", "work_pressure", "racing_thoughts", "frustration", "night_stress", "cant_start"]

    for i in range(1, 145):
        days_ago = (145 - i) % 28
        session_time = now - datetime.timedelta(days=days_ago, hours=(i % 12), minutes=(i * 7 % 60))
        target_st = states_pool[i % len(states_pool)]
        assigned_user = f"user-emp-extra-{(i % 14) + 1}" if i > 15 else "user-emp-arjun"
        assigned_dept = departments_pool[i % len(departments_pool)]

        stress_b = 7 + (i % 3) # 7, 8, 9
        stress_a = max(2, stress_b - (3 + (i % 3))) # drop by 3-5 points
        helped = "YES" if (i % 10 != 0) else "A_LITTLE"

        sess = InterventionSession(
            id=f"sess-hist-{i}",
            user_id=assigned_user,
            organization_id=org.id,
            department_id=assigned_dept,
            team_id=team_frontend.id if assigned_dept == dept_eng.id else None,
            channel="TEAMS" if i % 3 == 0 else ("SLACK" if i % 4 == 0 else "WEB"),
            duration_choice_minutes=5 if i % 2 == 0 else 2,
            starting_state=target_st,
            user_input_mode="VOICE" if i % 3 == 0 else "TEXT",
            private_raw_input="Client sprint deliverable and multiple sync calls creating heavy cognitive load." if assigned_user == "user-emp-arjun" else None,
            intervention_id="int_mental_load_unload" if "overload" in target_st else "int_priority_compression",
            intervention_name="Mental Load Unload™" if "overload" in target_st else "Priority Compression™",
            stress_before=stress_b,
            stress_after=stress_a,
            did_this_help=helped,
            is_successful_recovery=True,
            safety_tier="GREEN",
            started_at=session_time,
            completed_at=session_time + datetime.timedelta(minutes=5)
        )
        db.add(sess)

    # 8. Personal Relief Map for Arjun
    pattern1 = PersonalPattern(
        user_id=user_emp.id,
        pattern_type="EFFICIENT_INTERVENTION",
        situation="Work Overload & Competing Deadlines",
        recommended_intervention="Mental Load Unload™",
        avg_delta_relief=4.2,
        helpfulness_rate=0.92,
        observation_text="Deconstructing multi-task pressure into Now / Later consistently drops self-reported stress by 4+ points."
    )
    pattern2 = PersonalPattern(
        user_id=user_emp.id,
        pattern_type="TIME_OF_DAY_PEAK",
        situation="Afternoon Sprint Sync Clutter",
        recommended_intervention="Grounding & Paced Breathing",
        avg_delta_relief=3.0,
        helpfulness_rate=0.85,
        observation_text="Paced 4-4 breathing between consecutive client meetings restored cognitive focus."
    )
    db.add_all([pattern1, pattern2])

    # 9. Workplace Programs (Section 18)
    prog1 = WorkplaceProgram(
        id="prog-5day-reset",
        name="5-Day Stress Reset",
        description="Daily 5-minute micro-habits to de-escalate workplace cortisol and reclaim focus.",
        duration_days=5,
        target_audience="High-velocity teams & Individual Contributors",
        active_participants=340,
        completion_rate=0.82,
        steps=[
            {"day": 1, "title": "The Physical Sigh & Shoulder Drop", "minutes": 3},
            {"day": 2, "title": "Mental Load Unload™ Primer", "minutes": 5},
            {"day": 3, "title": "Decluttering Meeting Residue", "minutes": 4},
            {"day": 4, "title": "Boundary Affirmation Before 7 PM", "minutes": 5},
            {"day": 5, "title": "Consolidating Your Personal Relief Map", "minutes": 5}
        ]
    )
    prog2 = WorkplaceProgram(
        id="prog-meeting-overload",
        name="Meeting Overload Recovery",
        description="Rapid 2-minute transitions between back-to-back calendar invites to reset attention.",
        duration_days=3,
        target_audience="Cross-functional leads & Product Managers",
        active_participants=215,
        completion_rate=0.88,
        steps=[
            {"day": 1, "title": "The 60-Second Tab Shutdown", "minutes": 2},
            {"day": 2, "title": "Somatic Visual Grounding", "minutes": 2},
            {"day": 3, "title": "Async Priority Framing", "minutes": 3}
        ]
    )
    db.add_all([prog1, prog2])

    # 10. Team Recovery Lab Experiment (Section 25)
    exp1 = TeamRecoveryExperiment(
        id="exp-no-meeting-wednesday",
        organization_id=org.id,
        title="Meeting-Free Wednesday Afternoons",
        hypothesis="Protecting 4 hours of uninterrupted individual focus time will reduce peak mid-week cognitive overload.",
        intervention_type="Protected Focus Blocks",
        duration_weeks=4,
        target_departments=["Engineering", "Product & Design"],
        status="ACTIVE",
        baseline_recovery_score=5.4,
        current_recovery_score=7.6,
        participation_count=142,
        findings="Self-reported cognitive load dropped by 28% among participating engineers during protected blocks."
    )
    db.add(exp1)

    # 11. HR Campaign (Section 35)
    camp1 = HRCampaign(
        id="camp-reset-week-01",
        organization_id=org.id,
        title="5-Minute Reset Week",
        theme="Workplace Stress to Workplace Recovery",
        channels=["SLACK", "TEAMS", "EMAIL"],
        frequency_cap="Max 1 gentle nudge per 48 hours",
        status="RUNNING",
        total_reached=680,
        resets_triggered=412
    )
    db.add(camp1)

    # 12. Safety Events & Care Console Items (Section 26, 27)
    safe1 = SafetyEvent(
        id="safe-evt-01",
        organization_id=org.id,
        user_id_hash="anon-hash-8821a",
        tier="AMBER",
        trigger_type="Persistent emotional fatigue noted across multiple consecutive check-ins",
        tele_manas_notified=True,
        escalation_status="TRIAGED",
        clinical_notes="Confidential EAP referral link provided. Employee guided to optional counsellor consult."
    )
    db.add(safe1)

    # 13. Audit Log (Section 23, 42)
    audit_logs = [
        AuditLog(organization_id=org.id, actor_id=user_hr.id, actor_role="HR_ADMIN",
                 action="VIEW_AGGREGATE_REPORT", details="Generated Q1 Workforce Wellbeing Intelligence summary. Strict k=5 anonymity enforced."),
        AuditLog(organization_id=org.id, actor_id=user_admin.id, actor_role="SUPER_ADMIN",
                 action="SCIM_PROVISIONING_SYNC", details="SCIM 2.0 incremental directory sync completed. 20 identities reconciled."),
        AuditLog(organization_id=org.id, actor_id=user_mgr.id, actor_role="MANAGER",
                 action="VIEW_TEAM_AGGREGATE_INSIGHTS", details="Accessed Frontend Squad aggregate wellbeing themes (k=12)."),
        AuditLog(organization_id=org.id, actor_id=user_auditor.id, actor_role="AUDITOR",
                 action="EXPORT_DPDP_CONSENT_REGISTRY", details="Periodic verification of DPDP Act, 2023 consent compliance."),
        AuditLog(organization_id=org.id, actor_id=user_care.id, actor_role="CLINICIAN",
                 action="TRIAGE_SAFETY_EVENT", details="Reviewed confidential tele-MANAS crisis referral queue. Zero PII exposed.")
    ]
    db.add_all(audit_logs)

    db.commit()
    print("Database seeding completed successfully!")
    db.close()

if __name__ == "__main__":
    seed_database()
