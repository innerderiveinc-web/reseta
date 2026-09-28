// RESETA™ Enterprise Master Application Controller
const App = {
  activeSurface: "employee",
  currentUser: null,

  async init() {
    console.log("Initializing RESETA™ Enterprise Platform...");
    ResetModal.init();
    TalkItOut.init();

    await this.loadPersonas();
    await this.loadCurrentPersona();
    this.setupSurfaceNavigation();
    this.setupEventListeners();
    this.refreshActiveSurface();
  },

  async loadPersonas() {
    try {
      const users = await API.getUsers();
      const selectEl = document.getElementById("personaSelect");
      if (!selectEl) return;

      selectEl.innerHTML = users.map(u => `
        <option value="${u.id}">${u.full_name} (${u.role.replace('_', ' ')})</option>
      `).join('');

      selectEl.addEventListener("change", async (e) => {
        await this.switchPersona(e.target.value);
      });
    } catch (err) {
      console.error("Error loading personas:", err);
    }
  },

  async loadCurrentPersona() {
    try {
      this.currentUser = await API.getCurrentUser();
      const selectEl = document.getElementById("personaSelect");
      if (selectEl) selectEl.value = this.currentUser.id;

      const userNameEl = document.getElementById("currentUserName");
      if (userNameEl) userNameEl.innerText = this.currentUser.full_name;

      const userRoleEl = document.getElementById("currentUserRole");
      if (userRoleEl) userRoleEl.innerText = this.currentUser.role.replace('_', ' ');
    } catch (err) {
      console.error("Error fetching current user:", err);
    }
  },

  async switchPersona(userId) {
    try {
      this.currentUser = await API.switchUser(userId);
      const userNameEl = document.getElementById("currentUserName");
      if (userNameEl) userNameEl.innerText = this.currentUser.full_name;

      const userRoleEl = document.getElementById("currentUserRole");
      if (userRoleEl) userRoleEl.innerText = this.currentUser.role.replace('_', ' ');

      // Automatically pivot to the relevant surface if persona role changes
      if (this.currentUser.role === "EMPLOYEE") this.switchSurface("employee");
      else if (this.currentUser.role === "MANAGER") this.switchSurface("manager");
      else if (this.currentUser.role === "HR_ADMIN") this.switchSurface("hr");
      else if (this.currentUser.role === "SUPER_ADMIN" || this.currentUser.role === "AUDITOR") this.switchSurface("admin");
      else if (this.currentUser.role === "CLINICIAN") this.switchSurface("care");

      this.refreshActiveSurface();
    } catch (err) {
      alert("Error switching user persona: " + err.message);
    }
  },

  setupSurfaceNavigation() {
    const tabs = document.querySelectorAll(".surface-tab");
    tabs.forEach(tab => {
      tab.addEventListener("click", () => {
        tabs.forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        this.switchSurface(tab.dataset.surface);
      });
    });
  },

  switchSurface(surfaceId) {
    this.activeSurface = surfaceId;
    document.querySelectorAll(".view-panel").forEach(panel => {
      panel.classList.remove("active");
    });
    const targetPanel = document.getElementById(`view-${surfaceId}`);
    if (targetPanel) {
      targetPanel.classList.add("active");
    }

    // Update active tab style
    document.querySelectorAll(".surface-tab").forEach(tab => {
      if (tab.dataset.surface === surfaceId) tab.classList.add("active");
      else tab.classList.remove("active");
    });

    this.refreshActiveSurface();
  },

  refreshActiveSurface() {
    switch (this.activeSurface) {
      case "employee":
        this.loadEmployeeData();
        break;
      case "teams-slack":
        this.loadTeamsSlackData();
        break;
      case "manager":
        this.loadManagerData();
        break;
      case "hr":
        this.loadHrData();
        break;
      case "admin":
        this.loadAdminData();
        break;
      case "care":
        this.loadCareData();
        break;
      case "trust":
        // Static content / DPDP
        break;
    }
  },

  setupEventListeners() {
    // Hero Reset button
    const heroResetBtn = document.getElementById("heroResetBtn");
    if (heroResetBtn) {
      heroResetBtn.addEventListener("click", () => ResetModal.open("overloaded"));
    }

    // Hero Talk button
    const heroTalkBtn = document.getElementById("heroTalkBtn");
    if (heroTalkBtn) {
      heroTalkBtn.addEventListener("click", () => TalkItOut.open());
    }

    // Send a reset button
    const sendResetBtn = document.getElementById("sendResetBtn");
    if (sendResetBtn) {
      sendResetBtn.addEventListener("click", async () => {
        const name = prompt("Enter colleague's first name to send a gentle reset invite:", "Priya");
        if (name) {
          const res = await API.sendAReset(name);
          alert(`✅ Sent to ${name}!\n\nMessage: "${res.invite_text}"\n\nNo personal stress or health info is ever transmitted.`);
        }
      });
    }
  },

  // 1. Employee Surface Data
  async loadEmployeeData() {
    try {
      // Daily prompt
      const daily = await API.getDailyRecovery();
      const dailyBox = document.getElementById("dailyRoutineBox");
      if (dailyBox) {
        dailyBox.innerHTML = `
          <div class="routine-period-tag">${daily.period} Check-in</div>
          <div class="routine-headline">${daily.headline}</div>
          <div class="routine-desc">${daily.subtext}</div>
          <button class="btn-small-pill" onclick="ResetModal.open('general_tension')">
            ⚡ ${daily.suggested_action}
          </button>
        `;
      }

      // Autopilot Contextual Signal (Section 15)
      try {
        const autopilot = await API.getAutopilotPrompt(4);
        const autoCard = document.getElementById("autopilotCard");
        if (autoCard && autopilot) {
          autoCard.style.display = "block";
          document.getElementById("autopilotHeadline").innerText = autopilot.headline;
          document.getElementById("autopilotSubtext").innerText = autopilot.subtext;
          const autoBtn = document.getElementById("autopilotActionBtn");
          if (autoBtn) {
            autoBtn.innerText = `Start ${autopilot.recommended_minutes}-Min Reset 🔴`;
            autoBtn.onclick = () => ResetModal.open(autopilot.recommended_state);
          }
        }
      } catch (err) {
        console.warn("Autopilot prompt error:", err);
      }

      // Personal Relief Map & Mind Mirror
      this.refreshPersonalData();

      // Programs (Section 18, 63)
      this.cachedPrograms = await API.getPrograms();
      const progList = document.getElementById("workplaceProgramsList");
      if (progList) {
        progList.innerHTML = this.cachedPrograms.map(p => `
          <div class="program-item">
            <div>
              <div class="program-name">${p.name}</div>
              <div class="program-meta">${p.duration_days} Days · ${p.active_participants} colleagues enrolled · ${p.completion_rate_pct}% completion</div>
            </div>
            <button class="btn-small-pill" onclick="App.openProgramModal('${p.id}')">Explore & Enroll →</button>
          </div>
        `).join('');
      }
    } catch (err) {
      console.error("Error loading employee data:", err);
    }
  },

  async refreshPersonalData() {
    try {
      const data = await API.getPersonalReliefMap();
      const mm = data.mind_mirror;

      const mmBox = document.getElementById("mindMirrorBox");
      if (mmBox) {
        mmBox.innerHTML = `
          <div style="background: var(--bg-subtle); border-radius: var(--radius-sm); padding: 16px; margin-bottom: 16px;">
            <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--recovery-teal); margin-bottom: 6px;">
              Mind Mirror™ Observed Self-Reported Patterns:
            </div>
            <ul style="list-style: none; font-size: 13px; line-height: 1.6; color: var(--text-main);">
              ${mm.observations.map(obs => `<li style="margin-bottom: 8px;">🔹 ${obs}</li>`).join('')}
            </ul>
          </div>
          <div style="display: flex; gap: 16px; font-size: 13px; color: var(--text-muted);">
            <div><strong>Top Helpful Protocol:</strong> ${mm.top_intervention}</div>
            <div><strong>Avg Relief Drop:</strong> -${mm.avg_relief} pts</div>
          </div>
        `;
      }

      // Recent History
      const histTable = document.getElementById("personalHistoryTable");
      if (histTable && data.recent_history) {
        histTable.innerHTML = data.recent_history.map(h => `
          <tr>
            <td><strong>${h.intervention_name}</strong></td>
            <td>${h.starting_state}</td>
            <td>${h.duration} min</td>
            <td><span style="color: var(--brand-reset);">${h.stress_before}</span> → <span style="color: var(--recovery-teal);">${h.stress_after}</span> (-${h.delta})</td>
            <td><span style="font-size: 11px; background: #e0f2fe; color: #0284c7; padding: 2px 6px; border-radius: 4px;">${h.did_this_help}</span></td>
            <td style="color: var(--text-muted); font-size: 12px;">${h.date}</td>
          </tr>
        `).join('');
      }
    } catch (err) {
      console.error("Error refreshing personal data:", err);
    }
  },

  // 2. Teams / Slack Simulator
  async loadTeamsSlackData() {
    const chatContainer = document.getElementById("teamsSlackChatContainer");
    if (!chatContainer) return;
    chatContainer.innerHTML = `
      <div class="chat-message-bubble">
        <div class="chat-avatar">R</div>
        <div class="chat-bubble-content">
          <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <strong style="color: #fff;">RESETA Bot</strong>
            <span style="font-size: 11px; color: #949ba4;">APP · In-Flow Workspace</span>
          </div>
          <p style="font-size: 14px; margin-bottom: 8px;">
            Too much on your mind? Take 5. Reset.
          </p>
          <p style="font-size: 12px; color: #949ba4;">
            Visible only to you. You can launch in 1 tap without leaving your conversation window.
          </p>
          <div class="chat-buttons-row">
            <button class="chat-action-btn" onclick="ResetModal.open('work_pressure')">⚡ 2 Min Quick Reset</button>
            <button class="chat-action-btn primary" onclick="ResetModal.open('overloaded')">🌿 5 Min Optimal Reset</button>
            <button class="chat-action-btn" onclick="ResetModal.open('general_tension')">🧘 10 Min Grounding</button>
          </div>
        </div>
      </div>
    `;
  },

  // 3. Manager Experience
  async loadManagerData() {
    try {
      const data = await API.getTeamWellbeing();
      const banner = document.getElementById("managerPrivacyBanner");
      if (banner) banner.innerText = data.privacy_notice;

      const themesList = document.getElementById("managerThemesList");
      if (themesList) {
        themesList.innerHTML = data.top_workplace_themes.map(t => `
          <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--bg-subtle); border-radius: var(--radius-sm); margin-bottom: 8px;">
            <div>
              <strong>${t.theme_name}</strong>
              <div style="font-size: 12px; color: var(--text-muted);">${t.percentage}% of squad micro-resets related to this theme</div>
            </div>
            <span style="font-size: 11px; padding: 3px 8px; border-radius: 4px; background: ${t.status_indicator === 'Elevated' ? '#fef3c7' : '#e0f2fe'}; color: ${t.status_indicator === 'Elevated' ? '#b45309' : '#0369a1'}; font-weight: 700;">
              ${t.status_indicator}
            </span>
          </div>
        `).join('');
      }

      const actionsList = document.getElementById("managerSuggestedActions");
      if (actionsList) {
        actionsList.innerHTML = data.suggested_actions.map(a => `
          <div class="action-card">
            <div class="action-signal">Suggested Squad Action: ${a.category}</div>
            <div class="action-recommendation">${a.action}</div>
            <div class="action-meta-row"><span>Impact: ${a.impact}</span></div>
          </div>
        `).join('');
      }

      // Load 5-Minute Manager Coach Scenarios
      const scenarios = await API.getManagerCoachScenarios();
      const coachList = document.getElementById("managerCoachScenariosList");
      if (coachList) {
        coachList.innerHTML = scenarios.map(s => `
          <div style="border: 1px solid var(--border-light); border-radius: var(--radius-sm); padding: 16px; margin-bottom: 14px; background: var(--bg-surface);">
            <div style="font-size: 15px; font-weight: 700; margin-bottom: 6px;">${s.title}</div>
            <div style="font-size: 13px; color: var(--brand-reset); font-style: italic; margin-bottom: 10px;">${s.employee_signal}</div>
            <p style="font-size: 13px; color: var(--text-main); margin-bottom: 12px; line-height: 1.5;">${s.manager_guidance}</p>
            <div style="background: var(--bg-subtle); padding: 10px 14px; border-radius: var(--radius-sm); font-size: 12px; margin-bottom: 8px;">
              <strong>Recommended phrasing:</strong>
              <ul style="margin-left: 16px; margin-top: 4px;">
                ${s.recommended_phrases.map(p => `<li>"${p}"</li>`).join('')}
              </ul>
            </div>
            <div style="font-size: 11px; color: var(--red-crisis);">
              ⚠️ <strong>Avoid:</strong> ${s.what_to_avoid.join(" ")}
            </div>
          </div>
        `).join('');
      }
    } catch (err) {
      console.error("Error loading manager data:", err);
    }
  },

  // 4. HR Dashboard Data
  async loadHrData() {
    try {
      const data = await API.getWorkforceMetrics();

      document.getElementById("hrMetricWAU").innerText = data.active_waus;
      document.getElementById("hrMetricRecoveryMoments").innerText = data.successful_recovery_moments;
      document.getElementById("hrMetricTotalResets").innerText = data.total_resets_completed;
      document.getElementById("hrMetricAvgRelief").innerText = `-${data.avg_relief_delta} pts`;

      // Themes
      const hrThemesList = document.getElementById("hrAggregateThemesList");
      if (hrThemesList) {
        hrThemesList.innerHTML = data.aggregate_themes.map(t => `
          <div style="margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px;">
              <span><strong>${t.theme_name}</strong></span>
              <span>${t.percentage}% (${t.session_count} recovery moments)</span>
            </div>
            <div style="height: 8px; background: var(--bg-subtle); border-radius: 4px; overflow: hidden;">
              <div style="width: ${t.percentage}%; height: 100%; background: ${t.percentage > 30 ? 'var(--brand-reset)' : 'var(--recovery-teal)'};"></div>
            </div>
          </div>
        `).join('');
      }

      // Department Benchmarks
      const deptTable = document.getElementById("hrDeptBenchmarksTable");
      if (deptTable) {
        deptTable.innerHTML = data.department_benchmarks.map(d => `
          <tr>
            <td><strong>${d.department}</strong></td>
            <td>${d.active_employees}</td>
            <td>${d.recovery_moments}</td>
            <td>-${d.avg_relief_delta} pts</td>
            <td>${d.primary_theme}</td>
          </tr>
        `).join('');
      }

      // Action Engine recommendations
      const actionEngineList = document.getElementById("hrActionEngineList");
      if (actionEngineList) {
        actionEngineList.innerHTML = data.action_recommendations.map(a => `
          <div class="action-card">
            <div class="action-signal">Signal: ${a.signal}</div>
            <div class="action-recommendation">Organizational Action: ${a.recommended_action}</div>
            <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 8px;">
              <strong>Interpretation:</strong> ${a.possible_interpretation}
            </p>
            <div class="action-meta-row">
              <span>Owner: <strong>${a.owner}</strong></span>
              <span>Deadline: ${a.deadline}</span>
              <span>Re-measure: ${a.remeasure_date}</span>
            </div>
          </div>
        `).join('');
      }

      // Team Recovery Lab Experiments
      const exps = await API.getExperiments();
      const expList = document.getElementById("teamRecoveryLabList");
      if (expList) {
        expList.innerHTML = exps.map(e => `
          <div style="border: 1px solid var(--border-light); border-radius: var(--radius-sm); padding: 16px; margin-bottom: 12px; background: var(--bg-surface);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <strong style="font-size: 15px;">${e.title}</strong>
              <span class="brand-badge" style="background: var(--recovery-teal);">${e.status}</span>
            </div>
            <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 10px;">${e.hypothesis}</p>
            <div style="display: flex; gap: 20px; font-size: 12px; background: var(--bg-subtle); padding: 10px; border-radius: var(--radius-sm);">
              <div><strong>Target Groups:</strong> ${e.target_departments.join(", ")}</div>
              <div><strong>Participants:</strong> ${e.participation_count}</div>
              <div><strong>Baseline Score:</strong> ${e.baseline_recovery_score} → <strong>Current:</strong> ${e.current_recovery_score} (+${e.score_improvement})</div>
            </div>
            <div style="font-size: 12px; color: var(--recovery-emerald); font-weight: 600; margin-top: 8px;">
              Observed Shift: ${e.findings}
            </div>
          </div>
        `).join('');
      }

      // Campaigns
      const camps = await API.getCampaigns();
      const campList = document.getElementById("hrCampaignsList");
      if (campList) {
        campList.innerHTML = camps.map(c => `
          <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; border: 1px solid var(--border-light); border-radius: var(--radius-sm); margin-bottom: 8px;">
            <div>
              <strong>${c.title}</strong>
              <div style="font-size: 12px; color: var(--text-muted);">${c.theme} · Channels: ${c.channels.join(', ')} · ${c.frequency_cap}</div>
            </div>
            <div style="text-align: right;">
              <div style="font-size: 13px; font-weight: 700;">${c.resets_triggered} resets triggered</div>
              <span style="font-size: 11px; color: var(--recovery-teal); font-weight: 600;">Status: ${c.status}</span>
            </div>
          </div>
        `).join('');
      }
    } catch (err) {
      console.error("Error loading HR data:", err);
    }
  },

  // 5. Admin & Trust Surface Data
  async loadAdminData() {
    try {
      const org = await API.getOrgSettings();
      document.getElementById("adminOrgName").innerText = org.name;
      document.getElementById("adminOrgLicenses").innerText = `${org.employee_count} / ${org.total_licenses} seats allocated`;
      document.getElementById("adminSsoStatus").innerText = org.sso_provider;

      const dpdp = await API.getDpdpStatus();
      document.getElementById("adminDpdpConsents").innerText = `${dpdp.consent_count} active notices acknowledged`;
      document.getElementById("adminDpdpAuditCount").innerText = `${dpdp.audit_events_count} immutable log entries`;

      const logs = await API.getAuditLogs();
      const logTable = document.getElementById("adminAuditLogsTable");
      if (logTable) {
        logTable.innerHTML = logs.map(l => `
          <tr>
            <td><code>${l.timestamp}</code></td>
            <td><strong>${l.actor_role}</strong></td>
            <td>${l.action}</td>
            <td style="font-size: 12px; color: var(--text-muted);">${l.details}</td>
          </tr>
        `).join('');
      }

      // HRIS Connectors (Section 39)
      const connectors = await API.getHrisConnectors();
      const connList = document.getElementById("hrisConnectorsList");
      if (connList) {
        connList.innerHTML = connectors.map(c => `
          <div class="action-card" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                <div>
                  <strong style="font-size: 15px;">${c.name}</strong>
                  <div style="font-size: 12px; color: var(--text-muted);">${c.category}</div>
                </div>
                <span class="brand-badge" style="background: ${c.status === 'CONNECTED' ? 'var(--recovery-emerald)' : 'var(--bg-subtle)'}; color: ${c.status === 'CONNECTED' ? '#fff' : 'var(--text-muted)'};">
                  ${c.status}
                </span>
              </div>
              <div style="font-size: 12px; color: var(--text-muted); margin: 8px 0;">
                Mode: <strong>${c.sync_mode}</strong><br>
                Last Sync: <strong>${c.last_sync}</strong> · Users: <strong>${c.synced_users}</strong>
              </div>
              <div style="font-size: 11px; color: var(--recovery-teal); margin-bottom: 12px;">
                ✓ ${c.features.join(" · ")}
              </div>
            </div>
            <button class="btn-small-pill" onclick="App.syncHris('${c.provider_id}')" style="align-self: flex-start;">
              🔄 Sync Now
            </button>
          </div>
        `).join('');
      }

      // AI Release Checklist (Section 68)
      const checklist = await API.getAiReleaseChecklist();
      const checkCont = document.getElementById("aiReleaseChecklistContainer");
      if (checkCont) {
        checkCont.innerHTML = `
          <table class="data-table">
            <thead>
              <tr>
                <th>Criterion</th>
                <th>Certification Status</th>
                <th>Safety Verification Detail</th>
              </tr>
            </thead>
            <tbody>
              ${checklist.items.map(item => `
                <tr>
                  <td><strong>${item.criterion}</strong></td>
                  <td>
                    <span style="background: var(--recovery-emerald); color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">
                      ${item.status}
                    </span>
                  </td>
                  <td style="font-size: 13px; color: var(--text-muted);">${item.detail}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        `;
      }
    } catch (err) {
      console.error("Error loading admin data:", err);
    }
  },

  // 6. Care Console Data
  async loadCareData() {
    try {
      const triage = await API.getCareTriage();
      const triageTable = document.getElementById("careTriageTable");
      if (triageTable) {
        triageTable.innerHTML = triage.map(t => `
          <tr>
            <td><code>${t.created_at}</code></td>
            <td>
              <span style="background: ${t.tier === 'RED' ? 'var(--red-crisis)' : 'var(--amber-warn)'}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">
                ${t.tier}
              </span>
            </td>
            <td><code>${t.anonymized_reference}</code></td>
            <td>${t.trigger_type}</td>
            <td>${t.recommended_action}</td>
          </tr>
        `).join('');
      }
    } catch (err) {
      console.error("Error loading care data:", err);
    }
  },

  // 7. Dark Mode & Accessibility
  toggleTheme() {
    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    if (isDark) {
      document.documentElement.removeAttribute("data-theme");
      document.getElementById("themeToggleBtn").innerText = "🌙 Dark";
    } else {
      document.documentElement.setAttribute("data-theme", "dark");
      document.getElementById("themeToggleBtn").innerText = "☀️ Light";
    }
  },

  // 8. The 10-Second Sales Demo (Section 87)
  run10SecondDemo() {
    this.switchSurface("employee");
    ResetModal.open("overloaded");
    setTimeout(() => {
      ResetModal.setTime(5);
      ResetModal.renderStep2();
      setTimeout(() => {
        const input = document.getElementById("resetRawInput");
        if (input) {
          input.value = "Client presentation deadline tomorrow, 4 meetings back-to-back, inbox full, manager ne naya deliverable de diya.";
        }
        ResetModal.launchSession();
      }, 600);
    }, 400);
  },

  // 9. Copilots (Section 48, 49)
  async askManagerCopilot() {
    const input = document.getElementById("managerCopilotInput");
    const query = input ? input.value : "";
    if (!query.trim()) return;

    const answerBox = document.getElementById("managerCopilotAnswer");
    answerBox.classList.add("active");
    answerBox.innerHTML = `<em>Consulting RESETA Manager Copilot™...</em>`;

    try {
      const res = await API.queryManagerCopilot(query);
      answerBox.innerHTML = `
        <div style="font-weight: 700; color: var(--recovery-teal); margin-bottom: 6px;">${res.copilot_type}:</div>
        <div style="white-space: pre-line;">${res.answer}</div>
        <div style="font-size: 11px; color: var(--text-muted); margin-top: 8px;">🔒 ${res.privacy_guarantee}</div>
      `;
    } catch (err) {
      answerBox.innerHTML = `<span style="color: var(--red-crisis);">Error: ${err.message}</span>`;
    }
  },

  async askHrCopilot() {
    const input = document.getElementById("hrCopilotInput");
    const query = input ? input.value : "";
    if (!query.trim()) return;

    const answerBox = document.getElementById("hrCopilotAnswer");
    answerBox.classList.add("active");
    answerBox.innerHTML = `<em>Consulting RESETA Workforce Intelligence Copilot™...</em>`;

    try {
      const res = await API.queryHrCopilot(query);
      answerBox.innerHTML = `
        <div style="font-weight: 700; color: var(--brand-reset); margin-bottom: 6px;">${res.copilot_type}:</div>
        <div style="white-space: pre-line;">${res.answer}</div>
        <div style="font-size: 11px; color: var(--text-muted); margin-top: 8px;">🛡️ ${res.privacy_guarantee}</div>
      `;
    } catch (err) {
      answerBox.innerHTML = `<span style="color: var(--red-crisis);">Error: ${err.message}</span>`;
    }
  },

  // 10. Pilot Report Modal Viewer (Section 58)
  async openPilotReport() {
    const modal = document.getElementById("pilotReportModal");
    const content = document.getElementById("pilotReportContent");
    if (!modal || !content) return;

    modal.classList.add("active");
    content.innerHTML = `<div style="text-align: center; padding: 40px;">Generating Executive Workplace Recovery Report...</div>`;

    try {
      const report = await API.getPilotReport();
      const s = report.sections;

      content.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid var(--border-light); padding-bottom: 16px; margin-bottom: 24px;">
          <div>
            <span class="brand-badge">Executive Conversion Deliverable</span>
            <h1 style="font-size: 24px; font-weight: 800; margin-top: 8px;">${report.report_title}</h1>
            <p style="font-size: 13px; color: var(--text-muted);">${report.organization} · ${report.period} · ${report.pilot_cohort_size} Employees</p>
          </div>
          <button class="btn-primary" onclick="window.print()">🖨️ Print / Save as PDF</button>
        </div>

        <div class="metrics-summary-grid" style="margin-bottom: 20px;">
          <div class="metric-stat-card hero-metric">
            <div class="metric-label">Completed Recovery Moments</div>
            <div class="metric-value">${s["3_completed_recovery_moments"].total_recovery_moments}</div>
            <div class="metric-delta">${s["3_completed_recovery_moments"].percentage_of_all_sessions}% success rate</div>
          </div>
          <div class="metric-stat-card">
            <div class="metric-label">Workforce Activation</div>
            <div class="metric-value">${s["1_participation"].activation_rate_pct}%</div>
            <div class="metric-delta">${s["1_participation"].activated} activated employees</div>
          </div>
          <div class="metric-stat-card">
            <div class="metric-label">Average Relief Shift</div>
            <div class="metric-value">${s["5_outcome_trend"].average_drop} pts</div>
            <div class="metric-delta">${s["5_outcome_trend"].average_stress_before} → ${s["5_outcome_trend"].average_stress_after} / 10</div>
          </div>
        </div>

        <div class="report-section-card">
          <div class="report-section-title">4. Most-Used Interventions & Relief Efficacy</div>
          <ul style="list-style: none; font-size: 13px; line-height: 1.8;">
            ${s["4_most_used_interventions"].map(i => `
              <li style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--border-light); padding: 4px 0;">
                <span><strong>${i.name}</strong> (${i.usage_count} resets)</span>
                <span style="color: var(--recovery-teal); font-weight: 700;">Avg Relief: ${i.avg_relief_delta} pts</span>
              </li>
            `).join('')}
          </ul>
        </div>

        <div class="report-section-card">
          <div class="report-section-title">6. Aggregate Workplace Themes (No Individual Surveillance)</div>
          <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 8px;">
            ${s["6_aggregate_themes"].map(t => `
              <div style="background: var(--bg-surface); padding: 10px 14px; border-radius: var(--radius-sm); border: 1px solid var(--border-light); font-size: 13px;">
                <strong>${t.theme}</strong>: ${t.prevalence_pct}% prevalence
              </div>
            `).join('')}
          </div>
        </div>

        <div class="report-section-card">
          <div class="report-section-title">8. Recommended Organizational Experiments (SIGNAL → ACTION)</div>
          <ul style="list-style: none; font-size: 13px; line-height: 1.6;">
            ${s["8_recommended_experiments"].map(e => `
              <li style="margin-bottom: 8px;">
                🔹 <strong>${e.title}</strong> (${e.target}): <em>${e.expected_impact}</em>
              </li>
            `).join('')}
          </ul>
        </div>

        <div class="report-section-card" style="border-left: 4px solid var(--recovery-teal);">
          <div class="report-section-title">9. Next-Quarter Enterprise Roadmap</div>
          <ul style="list-style: none; font-size: 13px; line-height: 1.6;">
            ${s["9_next_quarter_roadmap"].map(r => `<li style="margin-bottom: 4px;">✅ ${r}</li>`).join('')}
          </ul>
        </div>
      `;
    } catch (err) {
      content.innerHTML = `<span style="color: var(--red-crisis);">Error loading report: ${err.message}</span>`;
    }
  },

  closePilotReport() {
    const modal = document.getElementById("pilotReportModal");
    if (modal) modal.classList.remove("active");
  },

  // 11. Program Walkthrough Modal (Section 18, 63)
  openProgramModal(progId) {
    const prog = (this.cachedPrograms || []).find(p => p.id === progId);
    if (!prog) return;

    const modal = document.getElementById("programModal");
    const content = document.getElementById("programModalContent");
    if (!modal || !content) return;

    modal.classList.add("active");
    content.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <span class="brand-badge">${prog.duration_days}-Day Program</span>
        <span style="font-size: 13px; color: var(--recovery-teal); font-weight: 600;">Active Enrollees: ${prog.active_participants}</span>
      </div>
      <h2 class="modal-step-title">${prog.name}</h2>
      <p class="modal-step-subtitle">${prog.description}</p>

      <div style="background: var(--bg-subtle); padding: 14px 18px; border-radius: var(--radius-sm); margin-bottom: 20px; font-size: 13px;">
        👥 <strong>Target Audience:</strong> ${prog.target_audience} · <strong>Completion Rate:</strong> ${prog.completion_rate_pct}%
      </div>

      <h4 style="font-size: 14px; font-weight: 700; margin-bottom: 12px;">Daily Guided Pathway:</h4>
      <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 24px;">
        ${(prog.steps || []).map((step, idx) => `
          <div style="border: 1px solid var(--border-light); border-radius: var(--radius-sm); padding: 14px; display: flex; justify-content: space-between; align-items: center; background: var(--bg-surface);">
            <div>
              <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--recovery-teal);">Day ${step.day} · ${step.minutes} Minutes</div>
              <div style="font-size: 14px; font-weight: 600; margin-top: 2px;">${step.title}</div>
            </div>
            <button class="btn-small-pill" onclick="App.startProgramStep(${step.day}, '${prog.name}', '${step.title}')">
              ${idx === 0 ? 'Start Day 1 🔴' : 'Preview'}
            </button>
          </div>
        `).join('')}
      </div>

      <div style="display: flex; justify-content: flex-end;">
        <button class="btn-secondary" onclick="App.closeProgramModal()">Close</button>
      </div>
    `;
  },

  startProgramStep(day, progName, stepTitle) {
    this.closeProgramModal();
    ResetModal.open("general_tension");
    setTimeout(() => {
      const input = document.getElementById("resetRawInput");
      if (input) input.value = `${progName} (Day ${day}): ${stepTitle}`;
    }, 150);
  },

  closeProgramModal() {
    const modal = document.getElementById("programModal");
    if (modal) modal.classList.remove("active");
  },

  // 12. Team Recovery Lab Experiment Modal (Section 25)
  openExperimentModal() {
    const modal = document.getElementById("experimentModal");
    if (modal) modal.classList.add("active");
  },

  async submitNewExperiment() {
    const title = document.getElementById("newExpTitle").value.trim();
    const hypothesis = document.getElementById("newExpHypothesis").value.trim();
    const protocol = document.getElementById("newExpProtocol").value;

    const depts = [];
    if (document.getElementById("expDeptEng")?.checked) depts.push("Engineering");
    if (document.getElementById("expDeptProd")?.checked) depts.push("Product & Design");
    if (document.getElementById("expDeptCS")?.checked) depts.push("Customer Success");
    if (document.getElementById("expDeptSales")?.checked) depts.push("Sales");

    if (!title || !hypothesis) {
      alert("Please fill in both the experiment title and hypothesis.");
      return;
    }

    try {
      await API.createExperiment({
        title,
        hypothesis,
        intervention_type: protocol,
        duration_weeks: 4,
        target_departments: depts
      });
      document.getElementById("experimentModal").classList.remove("active");
      await this.loadHrData();
      alert(`🧪 Experiment Launched: "${title}" is now active in the Team Recovery Lab!`);
    } catch (err) {
      alert("Error launching experiment: " + err.message);
    }
  },

  // 13. HR Campaign Dispatcher Modal (Section 35)
  openCampaignModal() {
    const modal = document.getElementById("campaignModal");
    if (modal) modal.classList.add("active");
  },

  async submitNewCampaign() {
    const title = document.getElementById("newCampTitle").value.trim();
    const theme = document.getElementById("newCampTheme").value.trim();
    const freq = document.getElementById("newCampFreq").value;

    const channels = [];
    if (document.getElementById("campChanSlack")?.checked) channels.push("SLACK");
    if (document.getElementById("campChanTeams")?.checked) channels.push("TEAMS");
    if (document.getElementById("campChanEmail")?.checked) channels.push("EMAIL");

    if (!title || !theme) {
      alert("Please enter title and theme.");
      return;
    }

    try {
      await API.createCampaign({
        title,
        theme,
        channels,
        frequency_cap: freq
      });
      document.getElementById("campaignModal").classList.remove("active");
      await this.loadHrData();
      alert(`📢 Campaign Activated: "${title}" deployed across ${channels.join(", ")}!`);
    } catch (err) {
      alert("Error activating campaign: " + err.message);
    }
  },

  // 14. India DPDP 2025 Data Subject Rights (Section 43)
  async openDpdpExport() {
    const modal = document.getElementById("dpdpExportModal");
    const content = document.getElementById("dpdpExportContent");
    if (!modal || !content) return;

    modal.classList.add("active");
    content.innerHTML = `<div style="text-align: center; padding: 30px;">Compiling DPDP Personal Data Archive...</div>`;

    try {
      const data = await API.exportDpdpArchive();
      content.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
          <div>
            <span class="brand-badge" style="background: var(--recovery-teal);">DPDP Act 2025 · Right to Data Portability</span>
            <h2 class="modal-step-title" style="margin-top: 6px;">Personal Data Archive</h2>
          </div>
          <button class="btn-primary" onclick="navigator.clipboard.writeText(JSON.stringify(window._lastDpdpExport, null, 2)); alert('Copied JSON archive to clipboard!');">📋 Copy JSON</button>
        </div>
        <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 16px;">
          Subject: <strong>${data.data_subject.name}</strong> (${data.data_subject.email}) · Organization: ${data.data_subject.organization_id}
        </p>
        <pre style="background: var(--bg-subtle); padding: 16px; border-radius: var(--radius-sm); font-size: 12px; overflow-x: auto; max-height: 380px; border: 1px solid var(--border-light); font-family: monospace;">${JSON.stringify(data, null, 2)}</pre>
        <div style="display: flex; justify-content: flex-end; margin-top: 20px;">
          <button class="btn-secondary" onclick="document.getElementById('dpdpExportModal').classList.remove('active')">Close</button>
        </div>
      `;
      window._lastDpdpExport = data;
    } catch (err) {
      content.innerHTML = `<span style="color: var(--red-crisis);">Error: ${err.message}</span>`;
    }
  },

  async toggleSampleConsent() {
    try {
      await API.toggleDpdpConsent("ANONYMIZED_WORKFORCE_AGGREGATION", false);
      alert("🔒 Consent updated: Anonymized aggregation for your account has been toggled in accordance with DPDP Rules 2025.");
    } catch (err) {
      alert("Error: " + err.message);
    }
  },

  async requestDataErasure() {
    const confirmErasure = confirm("Are you sure you want to invoke your Right to Erasure under the DPDP Act, 2025?\n\nThis will permanently delete all your private reflections, thought unload buckets, and learned personal patterns.");
    if (!confirmErasure) return;

    try {
      const res = await API.requestDpdpErasure();
      alert(`🗑️ ${res.message}`);
      await this.refreshPersonalData();
    } catch (err) {
      alert("Error requesting erasure: " + err.message);
    }
  },

  // 15. HRIS Directory Sync (Section 39)
  async syncHris(providerId) {
    try {
      const res = await API.syncHrisConnector(providerId);
      alert(`🏢 ${res.message}\nSynced ${res.synced_users} users and ${res.synced_departments} departments without surveillance telemetry.`);
      await this.loadAdminData();
    } catch (err) {
      alert("Error syncing directory: " + err.message);
    }
  },

  // 16. AI Safety Board Red-Team Audit (Section 67, 69)
  async runRedTeamAudit() {
    const summaryBox = document.getElementById("redTeamAuditSummary");
    const vectorsList = document.getElementById("redTeamVectorsList");
    const certStatus = document.getElementById("redTeamCertStatus");
    const passRate = document.getElementById("redTeamPassRate");

    if (summaryBox) {
      summaryBox.style.display = "block";
      vectorsList.innerHTML = `<div style="padding: 12px; color: var(--text-muted);">Executing 10-vector security, privacy, and clinical red-team suite...</div>`;
    }

    try {
      const res = await API.runRedTeamSuite();
      if (certStatus) certStatus.innerText = res.certification_status.replace(/_/g, " ");
      if (passRate) passRate.innerText = `${res.pass_rate_pct}% Pass Rate (${res.passed_count}/${res.total_vectors_tested})`;

      if (vectorsList) {
        vectorsList.innerHTML = res.tests.map(t => `
          <div style="background: var(--bg-surface); padding: 12px; border-radius: var(--radius-sm); border: 1px solid var(--border-light); display: flex; justify-content: space-between; align-items: flex-start; gap: 12px;">
            <div>
              <div style="display: flex; align-items: center; gap: 8px;">
                <code style="font-weight: 700; color: var(--brand-reset);">${t.vector_id}</code>
                <strong style="font-size: 13px;">${t.name}</strong>
              </div>
              <p style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">${t.details}</p>
            </div>
            <span style="background: ${t.status === 'PASSED' ? 'var(--recovery-emerald)' : 'var(--red-crisis)'}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700;">
              ${t.status}
            </span>
          </div>
        `).join('');
      }
    } catch (err) {
      if (vectorsList) vectorsList.innerHTML = `<span style="color: var(--red-crisis);">Error executing audit: ${err.message}</span>`;
    }
  }
};

window.App = App;
document.addEventListener("DOMContentLoaded", () => App.init());

