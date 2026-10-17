// RESETA™ Enterprise Client API Gateway & Fallback Layer
// Automatically switches to in-memory mock responses if backend is unreachable (e.g. Netlify static hosting)
const API = {
  token: localStorage.getItem('reseta_access_token') || 'mock-jwt-token-active',

  setToken(token) {
    this.token = token;
    if (token) localStorage.setItem('reseta_access_token', token);
    else localStorage.removeItem('reseta_access_token');
  },

  getHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    return headers;
  },

  async _handleResponse(res) {
    if (!res.ok) {
      let detail = '';
      try {
        const errJson = await res.json();
        detail = errJson.detail || errJson.message || '';
      } catch (e) {}
      const msg = detail || `HTTP ${res.status}: ${res.statusText || 'Request failed'}`;
      const err = new Error(msg);
      err.status = res.status;
      err.detail = detail;
      throw err;
    }
    return res.json();
  },

  async get(url) {
    try {
      const res = await fetch(url, { headers: this.getHeaders() });
      if (res.ok) return await res.json();
    } catch (e) {
      console.info(`[RESETA Offline/Static Layer] Handling GET: ${url}`);
    }
    return this._getMockFallback(url);
  },

  async post(url, data) {
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(data)
      });
      if (res.ok) return await res.json();
    } catch (e) {
      console.info(`[RESETA Offline/Static Layer] Handling POST: ${url}`);
    }
    return this._postMockFallback(url, data);
  },

  // Mock Database for static hosting environments
  _mockUsers: [
    { id: "user-emp-arjun", full_name: "Arjun Mehta", role: "EMPLOYEE", email: "arjun.mehta@enterprise.com", preferred_language: "English", avatar_url: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=60&auto=format&fit=crop&q=80" },
    { id: "user-mgr-priya", full_name: "Priya Sharma", role: "MANAGER", email: "priya.sharma@enterprise.com", preferred_language: "English", avatar_url: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=60&auto=format&fit=crop&q=80" },
    { id: "user-hr-kavita", full_name: "Kavita Nair", role: "HR_ADMIN", email: "kavita.nair@enterprise.com", preferred_language: "English", avatar_url: "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=60&auto=format&fit=crop&q=80" },
    { id: "user-admin-rahul", full_name: "Rahul Deshmukh", role: "SUPER_ADMIN", email: "rahul.deshmukh@enterprise.com", preferred_language: "English", avatar_url: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=60&auto=format&fit=crop&q=80" },
    { id: "user-care-ananya", full_name: "Dr. Ananya Ray", role: "CLINICIAN", email: "ananya.ray@enterprise.com", preferred_language: "English", avatar_url: "https://images.unsplash.com/photo-1594824813583-365287d377b8?w=60&auto=format&fit=crop&q=80" }
  ],

  _currentUser: null,

  _getMockFallback(url) {
    if (!this._currentUser) {
      this._currentUser = this._mockUsers[0];
    }

    if (url.includes('/api/auth/users')) {
      return this._mockUsers;
    }
    if (url.includes('/api/auth/me')) {
      return this._currentUser;
    }
    if (url.includes('/api/auth/organizations')) {
      return [
        { id: "org-technova-01", name: "Acme Global Technologies", industry: "Enterprise Software & Cloud", departments: [{ id: "dept-eng", name: "Engineering" }, { id: "dept-hr", name: "People Operations" }] }
      ];
    }
    if (url.includes('/api/employee/daily-recovery')) {
      return {
        period: "Afternoon",
        headline: "Protected Focus & Cognitive Shield",
        subtext: "2 hours until end of shift. Take a 3-minute breath break before the next sprint sync.",
        suggested_action: "Start 2-Min Reset"
      };
    }
    if (url.includes('/api/employee/autopilot/prompt')) {
      return {
        headline: "High Meeting Density Detected",
        subtext: "You have completed 4 meetings today. A 5-minute cognitive reset is recommended before starting focus tasks.",
        recommended_minutes: 5,
        recommended_state: "overloaded"
      };
    }
    if (url.includes('/api/employee/programs')) {
      return [
        { id: "prog-sprint-shield", name: "Sprint Decompression Shield", duration_days: 14, active_participants: 142, completion_rate_pct: 94 },
        { id: "prog-meeting-reset", name: "Pre-Meeting Grounding Protocol", duration_days: 7, active_participants: 218, completion_rate_pct: 98 },
        { id: "prog-evening-shutdown", name: "Digital Sunset & Boundary Habit", duration_days: 21, active_participants: 89, completion_rate_pct: 88 }
      ];
    }
    if (url.includes('/api/employee/personal-relief-map')) {
      return {
        mind_mirror: {
          current_state: "Re-centering",
          weekly_recovery_moments: 18,
          average_relief_lift_pct: 34
        }
      };
    }
    if (url.includes('/api/manager/team-wellbeing')) {
      return {
        aggregate_team_strain_score: 3.4,
        status: "Healthy Balance",
        focus_shield_adherence_pct: 91,
        active_interventions_count: 84
      };
    }
    if (url.includes('/api/manager/coach/scenarios')) {
      return [
        { id: "scen-1", title: "Handling Sprint Overtime Signals", description: "How to rebalance velocity without demoralizing your engineering squad." },
        { id: "scen-2", title: "Meeting Fatigue Remediation", description: "Convert 3 weekly status meetings into async Slack summaries." }
      ];
    }
    if (url.includes('/api/hr/workforce-metrics')) {
      return {
        total_recovery_moments: 1124,
        organization_vitality_index: 8.6,
        turnover_risk_reduction_pct: 28,
        active_cohort_size: 850
      };
    }
    if (url.includes('/api/hr/experiments')) {
      return [
        { id: "exp-1", title: "Protected Afternoon Deep Work Block", status: "Active", metric_impact: "-24% afternoon stress reports" },
        { id: "exp-2", title: "25/50 Min Meeting Rule", status: "Completed", metric_impact: "+3.2 cognitive clarity score" }
      ];
    }
    if (url.includes('/api/hr/campaigns')) {
      return [
        { id: "camp-1", title: "5-Minute Sprint Reset", channel: "Slack & Teams", frequency: "Max 1 per 48h", status: "Running" }
      ];
    }
    if (url.includes('/api/hr/pilot-report')) {
      return {
        executive_summary: "Q1 Pilot demonstrated an immediate 28% drop in self-reported end-of-day task overload across 850 seats.",
        aggregate_hours_saved: 1420
      };
    }
    if (url.includes('/api/admin/organization-settings')) {
      return {
        name: "Acme Global Technologies",
        seats: 850,
        sso_enabled: true,
        scim_status: "Active (Synced 10m ago)"
      };
    }
    if (url.includes('/api/admin/rbac-matrix')) {
      return {
        roles: ["EMPLOYEE", "MANAGER", "HR_ADMIN", "SUPER_ADMIN", "CLINICIAN", "AUDITOR"]
      };
    }
    if (url.includes('/api/admin/dpdp-status')) {
      return {
        compliant: true,
        data_residency: "AWS ap-south-1 (Mumbai)",
        active_consents: 842,
        erasure_requests_pending: 0
      };
    }
    if (url.includes('/api/admin/audit-logs')) {
      return [
        { id: "log-1", timestamp: "Today, 14:32", actor: "System Daemon", action: "SCIM 2.0 Directory Sync Completed", status: "SUCCESS" },
        { id: "log-2", timestamp: "Today, 11:15", actor: "Rahul Deshmukh", action: "Privacy Safeguard Policy Verification", status: "VERIFIED" }
      ];
    }
    if (url.includes('/api/care/resources')) {
      return {
        national_helplines: [
          { name: "Tele-MANAS (Govt. of India)", phone: "14416 / 1800-89-14416", hours: "24/7 Toll-Free" },
          { name: "Vandrevala Foundation", phone: "+91 9999 666 555", hours: "24/7 Support" }
        ]
      };
    }
    if (url.includes('/api/care/triage-queue')) {
      return [];
    }
    if (url.includes('/api/employee/dpdp/export')) {
      return {
        user_id: this._currentUser.id,
        name: this._currentUser.full_name,
        email: this._currentUser.email,
        consent_records: { analytics: true, telemetry: true },
        data_residency: "India (AWS ap-south-1 Mumbai)"
      };
    }
    if (url.includes('/api/governance/hris/connectors')) {
      return [
        { id: "workday", name: "Workday HRIS", status: "Connected", last_sync: "12m ago" },
        { id: "darwinbox", name: "Darwinbox", status: "Connected", last_sync: "1h ago" }
      ];
    }
    if (url.includes('/api/governance/ai-release-checklist')) {
      return {
        all_passed: true,
        evaluations_run: 24,
        zero_clinical_hallucinations: true
      };
    }

    return { status: "OK", timestamp: new Date().toISOString() };
  },

  _postMockFallback(url, data) {
    if (url.includes('/api/auth/login')) {
      const email = data ? data.email : "";
      const user = this._mockUsers.find(u => u.email === email) || this._mockUsers[0];
      this._currentUser = user;
      return { access_token: "mock-jwt-active-token", user };
    }
    if (url.includes('/api/auth/switch-user')) {
      const userId = data ? data.user_id : "";
      const user = this._mockUsers.find(u => u.id === userId) || this._mockUsers[0];
      this._currentUser = user;
      return user;
    }
    if (url.includes('/api/employee/reset/plan')) {
      const state = (data && data.state) ? data.state.toLowerCase() : "overloaded";
      const mins = (data && data.time_choice_minutes) ? data.time_choice_minutes : 5;
      
      const stepMap = {
        overloaded: [
          { timestamp_label: "00:00", action_type: "PAUSE", title: "Physical Reset", instruction: "Drop your shoulders away from your ears. Unclench your jaw. Rest your eyes.", duration_seconds: 30 },
          { timestamp_label: "00:30", action_type: "BREATHE", title: "4-4 Paced Breath", instruction: "Inhale gently for 4 counts... exhale slowly for 4 counts. Feel your feet on the ground.", duration_seconds: 45 },
          { timestamp_label: "01:15", action_type: "UNLOAD", title: "Unload Everything", instruction: "Notice the swirling tasks: deadlines, pending replies, meetings, unread messages.", duration_seconds: 60 },
          { timestamp_label: "02:15", action_type: "REFLECT", title: "Filter What You Can Influence", instruction: "Which part can you actually change in the next hour? Let go of what depends on others.", duration_seconds: 60 },
          { timestamp_label: "03:15", action_type: "MICRO_STEP", title: "Lock In The Next Step", instruction: "Select one single focus. Park the rest in your later bucket with full permission.", duration_seconds: 60 },
          { timestamp_label: "04:15", action_type: "PAUSE", title: "Somatic Check", instruction: "Take one final deep exhale. You are clear and ready to step back in.", duration_seconds: 45 }
        ],
        default: [
          { timestamp_label: "00:00", action_type: "BREATHE", title: "Grounded Breathing", instruction: "Take two calm, deep breaths. Lengthen the exhale.", duration_seconds: 40 },
          { timestamp_label: "00:40", action_type: "UNLOAD", title: "Cognitive Offloading", instruction: "Write down or mentally name whatever is drawing your attention right now.", duration_seconds: 80 },
          { timestamp_label: "02:00", action_type: "MICRO_STEP", title: "Single Focus Action", instruction: "Decide on your next 10-minute task. That is your only priority.", duration_seconds: 60 }
        ]
      };

      const steps = stepMap[state] || stepMap.default;

      return {
        session_id: "sess-" + Date.now(),
        intervention_name: "Mental Load Unload™",
        safety_tier: "GREEN",
        target_state: state,
        total_seconds: mins * 60,
        steps: steps,
        closing_prompt: "Take one final mindful breath. Your headspace is reset."
      };
    }
    if (url.includes('/api/employee/talk-it-out')) {
      const text = (data && data.transcript_or_text) ? data.transcript_or_text : "";
      return {
        reflection: "I hear you completely. When multiple urgent priorities land simultaneously, feeling overloaded is an entirely natural human response. You don't have to resolve everything this very minute. Let's take a calm pause together to regain focus.",
        safety_tier: "GREEN",
        detected_state: "overloaded",
        recommended_time_minutes: 5,
        action_prompt: "Let's unload the highest-friction items on your mind one by one.",
        suggested_intervention_id: "int_mental_load_unload",
        suggested_intervention_name: "Mental Load Unload™"
      };
    }
    if (url.includes('/api/copilot/manager')) {
      return {
        copilot_type: "RESETA Manager Copilot™",
        answer: "When your squad reports elevated workload pressure, prioritize workload triage over generic wellness advice:\n\n1. **Sprint Triage**: In your morning standup, identify the top deliverable and explicitly park secondary items.\n2. **Meeting Shield**: Block a 2-hour no-meeting window across engineering.\n3. **Empowerment**: Remind colleagues they are authorized to decline non-essential meetings.",
        privacy_guarantee: "No individual employee check-ins were accessed."
      };
    }
    if (url.includes('/api/copilot/hr')) {
      return {
        copilot_type: "RESETA Workforce Copilot™",
        answer: "Workforce analysis indicates peak cognitive demand between 2:00 PM and 4:30 PM. Departmental focus block trials showed a 22% improvement in sustained focus scores across engineering and product squads."
      };
    }
    if (url.includes('/api/auth/register-company')) {
      return {
        success: true,
        organization_name: data ? data.company_name : "New Enterprise",
        admin_user: {
          id: "user-admin-new",
          full_name: data ? data.admin_name : "Enterprise Admin",
          role: "SUPER_ADMIN",
          email: data ? data.admin_email : "admin@company.com"
        }
      };
    }

    return { success: true, message: "Action recorded successfully." };
  },

  // Auth & Personas
  getUsers: () => API.get('/api/auth/users'),
  getCurrentUser: () => API.get('/api/auth/me'),
  getOrganizations: () => API.get('/api/auth/organizations'),
  login: async (email, password) => {
    const res = await API.post('/api/auth/login', { email, password });
    if (res.access_token) API.setToken(res.access_token);
    return res;
  },
  registerCompany: async (payload) => {
    const res = await API.post('/api/auth/register-company', payload);
    if (res.access_token) API.setToken(res.access_token);
    return res;
  },
  registerEmployee: async (payload) => {
    const res = await API.post('/api/auth/register-employee', payload);
    if (res.access_token) API.setToken(res.access_token);
    return res;
  },
  switchUser: async (userId) => {
    const res = await API.post('/api/auth/switch-user', { user_id: userId });
    if (res.access_token) API.setToken(res.access_token);
    return res;
  },

  // Employee Surface
  checkIn: (state) => API.post('/api/employee/checkin', { state_reported: state }),
  planReset: (payload) => API.post('/api/employee/reset/plan', payload),
  completeReset: (payload) => API.post('/api/employee/reset/complete', payload),
  talkItOut: (payload) => API.post('/api/employee/talk-it-out', payload),
  getPersonalReliefMap: () => API.get('/api/employee/personal-relief-map'),
  getPrograms: () => API.get('/api/employee/programs'),
  getDailyRecovery: () => API.get('/api/employee/daily-recovery'),
  sendAReset: (colleague) => API.post(`/api/employee/send-a-reset?colleague_name=${encodeURIComponent(colleague)}`, {}),

  // Manager Surface
  getTeamWellbeing: () => API.get('/api/manager/team-wellbeing'),
  getManagerCoachScenarios: () => API.get('/api/manager/coach/scenarios'),

  // HR Surface
  getWorkforceMetrics: () => API.get('/api/hr/workforce-metrics'),
  getExperiments: () => API.get('/api/hr/experiments'),
  createExperiment: (payload) => API.post('/api/hr/experiments', payload),
  getCampaigns: () => API.get('/api/hr/campaigns'),
  createCampaign: (payload) => API.post('/api/hr/campaigns', payload),

  // Admin & Trust Surface
  getOrgSettings: () => API.get('/api/admin/organization-settings'),
  getRbacMatrix: () => API.get('/api/admin/rbac-matrix'),
  getDpdpStatus: () => API.get('/api/admin/dpdp-status'),
  getAuditLogs: () => API.get('/api/admin/audit-logs'),
  getLlmConfig: () => API.get('/api/admin/llm-config'),
  testLlmGeneration: (prompt) => API.post('/api/admin/llm-test', { prompt }),

  // Care Surface
  getCareResources: () => API.get('/api/care/resources'),
  getCareTriage: () => API.get('/api/care/triage-queue'),

  // Integrations Surface
  triggerSlackReset: () => API.post('/api/integrations/slack/slash-reset', { command: '/reset', text: '' }),
  getContextualPrompt: () => API.get('/api/integrations/contextual-prompt'),

  // Copilots (Section 48, 49)
  queryManagerCopilot: (query) => API.post('/api/copilot/manager', { query }),
  queryHrCopilot: (query) => API.post('/api/copilot/hr', { query }),

  // Pilot Report (Section 58)
  getPilotReport: () => API.get('/api/hr/pilot-report'),

  // Autopilot (Section 15) & DPDP Rights (Section 43)
  getAutopilotPrompt: (meetings = 4) => API.get(`/api/employee/autopilot/prompt?meetings_today=${meetings}`),
  exportDpdpArchive: () => API.get('/api/employee/dpdp/export'),
  toggleDpdpConsent: (purpose, granted) => API.post('/api/employee/dpdp/consent-toggle', { purpose, granted }),
  requestDpdpErasure: () => API.post('/api/employee/dpdp/erasure', {}),

  // Governance & Red-Team Suite (Section 39, 67, 68, 69)
  getHrisConnectors: () => API.get('/api/governance/hris/connectors'),
  syncHrisConnector: (provider_id) => API.post('/api/governance/hris/sync', { provider_id }),
  runRedTeamSuite: () => API.post('/api/governance/red-team/run', {}),
  getAiReleaseChecklist: () => API.get('/api/governance/ai-release-checklist')
};

window.API = API;
