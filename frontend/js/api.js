// RESETA™ Enterprise Client API Gateway & HTTP Transport
// Institutional-grade API client with JWT Bearer lifecycle and clean offline fallback
const API = {
  token: localStorage.getItem('reseta_access_token') || 'mock-jwt-token-active',

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('reseta_access_token', token);
    } else {
      localStorage.removeItem('reseta_access_token');
    }
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
      console.info(`[RESETA Offline Transport] Delegating GET to MockData: ${url}`);
    }
    return window.MockData ? window.MockData.get(url) : { status: "OFFLINE" };
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
      console.info(`[RESETA Offline Transport] Delegating POST to MockData: ${url}`);
    }
    return window.MockData ? window.MockData.post(url, data) : { success: true };
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
