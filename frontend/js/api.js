// RESETA™ Enterprise Client API Gateway
const API = {
  async get(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    return res.json();
  },

  async post(url, data) {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    return res.json();
  },

  // Auth & Personas
  getUsers: () => API.get('/api/auth/users'),
  getCurrentUser: () => API.get('/api/auth/me'),
  switchUser: (userId) => API.post('/api/auth/switch-user', { user_id: userId }),

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
  getPilotReport: () => API.get('/api/hr/pilot-report')
};

window.API = API;
