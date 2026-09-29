# RESETA™ ENTERPRISE
## B2B Mental Wellness & Stress Recovery Platform

> **"Too much on your mind? Take 5. Reset."**  
> *From workplace stress to workplace recovery.*

---

## 1. Executive Overview

**RESETA™ Enterprise** is an AI-powered mental recovery system for modern workplaces.

It is **NOT**:
* An AI therapist
* A passive meditation library
* A mood tracker
* A surveillance tool
* A diagnostic system

RESETA owns **THE MOMENT OF NEED**:  
When an employee has 5 minutes and needs to get their head straight, RESETA delivers an interactive, clinically-reviewed reset protocol, measures whether it helped, and aggregates privacy-safe insights for leadership to improve working conditions.

---

## 2. The Core Engine: RELIEFLOOP™

$$\text{STRESS} \longrightarrow \text{UNDERSTAND} \longrightarrow \text{RESET} \longrightarrow \text{MEASURE} \longrightarrow \text{LEARN} \longrightarrow \text{PERSONALIZE}$$

1. **STRESS**: Employee opens in app, web, Teams, or Slack.
2. **UNDERSTAND (30–60s)**: Time selected (2, 5, or 10 min) + state identified (tap, type, or speak in Hinglish/Hindi/English).
3. **RESET (Do It With Me™)**: Paced, interactive guided somatic and cognitive deceleration.
4. **MEASURE (Relief Check™)**: Before (e.g. 8/10) vs After (e.g. 4/10) stress + "Did this help?".
5. **LEARN (Personal Relief Map™)**: System records what intervention works for which state for this employee.
6. **PERSONALIZE**: Mind Mirror™ observes self-reported recovery patterns over time.

---

## 3. The 7 Product Surfaces

1. **Employee App & Web**: Private personal sanctuary with hero **🔴 RESET ME**, **🎙 TALK IT OUT**, Mind Mirror™, and daily routines.
2. **Microsoft Teams & Slack Simulator**: In-flow `/reset` triggers with ephemeral privacy.
3. **Manager Experience**: Strictly aggregated squad insights (cohort $k \ge 5$) and **5-Minute Manager Coach** micro-scenarios.
4. **HR / People Dashboard**: Workforce wellbeing intelligence, North Star metric (**Successful Recovery Moments**), **Organizational Action Engine™**, and **Team Recovery Lab™** experiments.
5. **Enterprise Admin Console**: SSO (Entra ID, Okta SAML), SCIM provisioning, RBAC matrix, and audit logging.
6. **Care Console (RESETA Care™)**: Certified clinical escalation queue and 24/7 Tele-MANAS helpline integration.
7. **Trust Center**: India DPDP Act 2025 compliance, minimum cohort suppression, and anti-diagnosis pledge.

---

## 4. Key Architectural Pillars

### A. Safety Firewall™ (Sections 27, 28)
* **Independent Safety Screen**: Evaluates all inputs and outputs before and after model processing.
* **Tiers**:
  * **GREEN**: Everyday workplace stress.
  * **AMBER**: Persistent distress $\rightarrow$ confidential EAP referral.
  * **RED**: Imminent safety crisis $\rightarrow$ immediately suspends wellness flow and presents Govt. of India **Tele-MANAS (14416 / 1800-89-14416)** and crisis lifelines.
* **Anti-Diagnosis Guardrail**: Strictly prohibits clinical diagnoses ("You have ADHD", "You have depression"). Replaces with objective, non-diagnostic guidance.

### B. Employee Privacy Wall & India DPDP Act 2025 (Sections 19, 23, 43, 66)
* **Technical Privacy Wall**: Employee raw text, voice, and personal scores are isolated to the employee.
* **Minimum Cohort Threshold ($k \ge 5$)**: Suppression of small cells prevents individual re-identification.
* **Section 22 Mandate**: Never calls employees "high risk". Uses objective organizational terminology like *"workload-related recovery opportunity"*.

### C. Mental Load Unload™ (Section 11)
Converts cluttered thoughts into clear buckets:
* **NOW**: Single immediate focus item.
* **SCHEDULED**: Time-bound commitments.
* **WAITING**: Pending external replies.
* **LATER**: Inbox and non-urgent backlog.
* **NEXT**: A clear 10-minute micro-action.

### D. North Star Metric (Section 51)
* **Primary KPI**: **Successful Recovery Moments™**  
  *Definition: Completed intervention + user reports positive self-reported relief.*

---

## 5. Technology Stack

* **Backend**: Python 3.9+ · FastAPI · SQLAlchemy · Pydantic V2 · Uvicorn
* **Database**: SQLite (WAL mode) / PostgreSQL + pgvector ready
* **Frontend**: Vanilla ES6+ SPA · Actionable Calm Design System (Apple simplicity + Headspace warmth + Notion clarity)
* **Security**: Role-Based Access Control (7 roles), DPDP 2023 audit logging, CSRF/XSS hardened

---

## 6. Quick Start & Verification

### One-Click Launch (macOS)
Double-click or run:
```bash
./launch.command
```
This automatically verifies the virtual environment, executes the test suite, seeds the TechNova Solutions enterprise dataset, launches the server on `http://127.0.0.1:8123`, and opens the browser.

### Command Line Launch
```bash
./start.sh 8123
```

### Running Test Suite
```bash
PYTHONPATH=. .venv/bin/python -m pytest tests/ -v
```
All 24 tests validate:
1. `test_safety_firewall.py`: Green/Amber/Red tiers, Tele-MANAS escalation, anti-diagnosis sanitizer.
2. `test_intervention_router.py`: State classification, clinically reviewed protocols, Mental Load Unload decomposition.
3. `test_privacy_engine.py`: Minimum cohort size $k \ge 5$ suppression and HR language sanitization.
4. `test_red_team_suite.py`: Automated 10-vector security, privacy, and clinical red-team suite (100% pass rate).
5. `test_api_endpoints.py`: End-to-end user persona switching, check-in, reset planning, Relief Check™, HR metrics, Copilots, Autopilot, DPDP data export, Recovery Lab experiments, and HRIS directory sync.

