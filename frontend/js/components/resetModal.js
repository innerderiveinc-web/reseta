// RESETA™ ResetModal Component: 🔴 RESET ME & RELIEFLOOP™
function playCalmBell(freq = 432) {
  try {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 1.4);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 1.4);
  } catch (e) {
    // Graceful fallback if AudioContext is blocked
  }
}

const ResetModal = {
  currentSession: null,
  currentStepIndex: 0,
  stepTimer: null,
  selectedTime: 5,
  selectedState: "overloaded",
  stressBefore: 8,
  stressAfter: 4,

  init() {
    this.modalEl = document.getElementById("resetModal");
    this.containerEl = document.getElementById("resetModalContent");
    this.closeBtn = document.getElementById("resetModalClose");

    if (this.closeBtn) {
      this.closeBtn.addEventListener("click", () => this.close());
    }
  },

  open(preselectedState = null) {
    if (preselectedState) this.selectedState = preselectedState;
    this.modalEl.classList.add("active");
    this.renderStep1();
  },

  close() {
    if (this.stepTimer) clearInterval(this.stepTimer);
    this.modalEl.classList.remove("active");
  },

  // Step 1: How much time do you have?
  renderStep1() {
    this.containerEl.innerHTML = `
      <div class="step-indicator-bar">
        <div class="step-dot active"></div>
        <div class="step-dot"></div>
        <div class="step-dot"></div>
      </div>
      <h2 class="modal-step-title">How much time do you have?</h2>
      <p class="modal-step-subtitle">No long lectures. Just enough time to reset your nervous system.</p>

      <div class="time-choice-row">
        <div class="time-btn ${this.selectedTime === 2 ? 'selected' : ''}" onclick="ResetModal.setTime(2)">
          <div class="time-btn-number">2</div>
          <div class="time-btn-label">Minutes · Micro Reset</div>
        </div>
        <div class="time-btn ${this.selectedTime === 5 ? 'selected' : ''}" onclick="ResetModal.setTime(5)">
          <div class="time-btn-number">5</div>
          <div class="time-btn-label">Minutes · Optimal Reset</div>
        </div>
        <div class="time-btn ${this.selectedTime === 10 ? 'selected' : ''}" onclick="ResetModal.setTime(10)">
          <div class="time-btn-number">10</div>
          <div class="time-btn-label">Minutes · Deep Grounding</div>
        </div>
      </div>

      <div style="display: flex; justify-content: flex-end; margin-top: 24px;">
        <button class="btn-primary" onclick="ResetModal.renderStep2()">Next: What's Going On? →</button>
      </div>
    `;
  },

  setTime(minutes) {
    this.selectedTime = minutes;
    document.querySelectorAll(".time-btn").forEach(btn => btn.classList.remove("selected"));
    event.currentTarget.classList.add("selected");
  },

  // Step 2: What's going on?
  renderStep2() {
    this.containerEl.innerHTML = `
      <div class="step-indicator-bar">
        <div class="step-dot"></div>
        <div class="step-dot active"></div>
        <div class="step-dot"></div>
      </div>
      <h2 class="modal-step-title">What's going on?</h2>
      <p class="modal-step-subtitle">Tap or describe your workload in English, Hindi, or Hinglish.</p>

      <div class="state-selector-grid" style="margin-bottom: 16px;">
        ${["Overloaded", "Racing Thoughts", "Work Pressure", "Can't Start", "Frustration", "Night Stress", "General Tension"]
          .map(st => `<div class="state-chip ${this.selectedState.toLowerCase() === st.toLowerCase().replace(/ /g, '_') ? 'selected' : ''}" onclick="ResetModal.selectState('${st}', this)">${st}</div>`)
          .join('')}
      </div>

      <textarea id="resetRawInput" class="reset-input-area" placeholder="e.g., Client deadline hai, 4 meetings back to back, inbox overflowing hai aur dimaag full ho gaya hai..."></textarea>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
        <span style="font-size: 12px; color: var(--recovery-teal); font-weight: 600;">
          🔒 Private to you: Not shared with managers or HR.
        </span>
        <button class="btn-reset-hero" style="padding: 12px 28px; font-size: 15px;" onclick="ResetModal.launchSession()">
          Start Reset 🔴
        </button>
      </div>
    `;
  },

  selectState(stateName, el) {
    this.selectedState = stateName.toLowerCase().replace(/ /g, '_').replace("'", "");
    document.querySelectorAll(".state-chip").forEach(c => c.classList.remove("selected"));
    el.classList.add("selected");
  },

  async launchSession() {
    const rawInputEl = document.getElementById("resetRawInput");
    const rawInput = rawInputEl ? rawInputEl.value : "";

    this.containerEl.innerHTML = `
      <div style="text-align: center; padding: 40px 0;">
        <div class="breath-circle" style="margin: 0 auto 20px;">Breathe...</div>
        <h3 style="font-size: 18px; margin-bottom: 6px;">Setting up your quiet space...</h3>
        <p style="font-size: 13px; color: var(--text-muted);">Finding the right breathing and decompression flow</p>
      </div>
    `;

    try {
      const plan = await API.planReset({
        time_choice_minutes: this.selectedTime,
        state: this.selectedState,
        input_mode: "TEXT",
        raw_input: rawInput,
        language: "Hinglish",
        channel: "WEB"
      });

      this.currentSession = plan;

      // Handle RED tier (Safety Escalation)
      if (plan.safety_tier === "RED") {
        this.renderRedTier(plan);
        return;
      }

      this.currentStepIndex = 0;
      playCalmBell(432);
      this.renderGuidedStep();
    } catch (err) {
      alert("Error starting reset: " + err.message);
      this.renderStep1();
    }
  },

  renderRedTier(plan) {
    this.containerEl.innerHTML = `
      <div style="background: var(--red-bg); border: 2px solid var(--red-crisis); border-radius: var(--radius-md); padding: 24px; text-align: left;">
        <h2 style="color: var(--red-crisis); font-size: 22px; margin-bottom: 12px;">🚨 ${plan.intervention_name}</h2>
        <p style="font-size: 14px; margin-bottom: 16px; line-height: 1.6;">${plan.closing_prompt}</p>
        
        <div style="background: white; border-radius: var(--radius-sm); padding: 16px; margin-bottom: 16px; color: #111;">
          <h4 style="font-size: 15px; margin-bottom: 6px;">Govt. of India Tele-MANAS Helpline (24/7):</h4>
          <p style="font-size: 20px; font-weight: 800; color: var(--red-crisis);">📞 14416 / 1800-89-14416</p>
          <p style="font-size: 12px; color: #666; margin-top: 4px;">Free, confidential psychological first aid in 20+ Indian languages.</p>
        </div>

        <div style="background: white; border-radius: var(--radius-sm); padding: 16px; margin-bottom: 20px; color: #111;">
          <h4 style="font-size: 14px; margin-bottom: 4px;">Vandrevala Foundation:</h4>
          <p style="font-size: 16px; font-weight: 700;">📞 +91 9999 666 555 (24/7)</p>
        </div>

        <button class="btn-primary" onclick="ResetModal.close()" style="width: 100%;">Close and Contact Care</button>
      </div>
    `;
  },

  // Step 3: Do It With Me™ interactive step player
  renderGuidedStep() {
    const session = this.currentSession;
    const step = session.steps[this.currentStepIndex];
    const totalSteps = session.steps.length;

    let unloadHtml = "";
    if (session.unload_result && this.currentStepIndex === Math.floor(totalSteps / 2)) {
      const u = session.unload_result;
      unloadHtml = `
        <div class="unload-quadrants-grid">
          <div class="unload-bucket">
            <span class="bucket-badge badge-now">Now (Single Focus)</span>
            <ul class="bucket-list">${u.now.map(item => `<li>${item}</li>`).join('')}</ul>
          </div>
          <div class="unload-bucket">
            <span class="bucket-badge badge-sched">Scheduled</span>
            <ul class="bucket-list">${u.scheduled.map(item => `<li>${item}</li>`).join('')}</ul>
          </div>
          <div class="unload-bucket">
            <span class="bucket-badge badge-wait">Waiting</span>
            <ul class="bucket-list">${u.waiting.map(item => `<li>${item}</li>`).join('')}</ul>
          </div>
          <div class="unload-bucket">
            <span class="bucket-badge badge-later">Later / Parked</span>
            <ul class="bucket-list">${u.later.map(item => `<li>${item}</li>`).join('')}</ul>
          </div>
        </div>
        <div class="next-action-callout">
          🎯 <strong>Immediate Micro-Action:</strong> ${u.next_action}
        </div>
      `;
    }

    this.containerEl.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <span class="brand-badge">${session.intervention_name}</span>
        <span style="font-size: 13px; font-weight: 600; color: var(--text-muted);">Step ${this.currentStepIndex + 1} of ${totalSteps}</span>
      </div>

      <div class="breath-container">
        <div class="breath-circle">${step.action_type}</div>
      </div>

      <div class="instruction-box">
        <div class="instruction-title">${step.title}</div>
        <div class="instruction-body">${step.instruction}</div>
      </div>

      ${unloadHtml}

      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 24px;">
        <div style="font-size: 12px; color: var(--text-muted);">
          ⏱ Duration: ~${step.duration_seconds}s
        </div>
        <div>
          ${this.currentStepIndex < totalSteps - 1 
            ? `<button class="btn-primary" onclick="ResetModal.nextStep()">Next Step →</button>`
            : `<button class="btn-reset-hero" style="padding: 10px 24px; font-size: 14px;" onclick="ResetModal.renderReliefCheck()">Finish & Check Relief →</button>`
          }
        </div>
      </div>
    `;
  },

  nextStep() {
    if (this.currentStepIndex < this.currentSession.steps.length - 1) {
      this.currentStepIndex++;
      this.renderGuidedStep();
    } else {
      this.renderReliefCheck();
    }
  },

  // Step 4: Relief Check™ (Section 12)
  renderReliefCheck() {
    const initialDelta = Math.max(0, this.stressBefore - this.stressAfter);
    this.containerEl.innerHTML = `
      <div class="relief-check-container">
        <h2 class="modal-step-title">Relief Check™</h2>
        <p class="modal-step-subtitle">Did this reset create breathing space in your head?</p>

        <div style="display: flex; justify-content: space-around; align-items: center; background: var(--bg-subtle); padding: 18px; border-radius: var(--radius-md); margin: 20px 0;">
          <div style="text-align: center;">
            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Before Stress</div>
            <div id="stressBeforeDisplay" style="font-size: 32px; font-weight: 800; color: var(--brand-reset);">${this.stressBefore}/10</div>
          </div>
          <div style="font-size: 24px; color: var(--text-muted);">→</div>
          <div style="text-align: center;">
            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">After Stress</div>
            <div id="stressAfterDisplay" style="font-size: 32px; font-weight: 800; color: var(--recovery-teal);">${this.stressAfter}/10</div>
          </div>
          <div style="text-align: center; border-left: 1px solid var(--border-light); padding-left: 16px;">
            <div style="font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Relief Shift</div>
            <div id="stressDeltaDisplay" style="font-size: 28px; font-weight: 800; color: var(--recovery-emerald);">-${initialDelta} pts</div>
          </div>
        </div>

        <div class="slider-group" style="margin-bottom: 16px;">
          <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 600;">
            <label>1. Rate your starting stress when you opened this:</label>
            <span id="sliderBeforeVal" style="color: var(--brand-reset); font-weight: 700;">${this.stressBefore}/10</span>
          </div>
          <input type="range" id="stressBeforeSlider" min="1" max="10" value="${this.stressBefore}" style="width: 100%; margin-top: 8px;" oninput="ResetModal.updateStressBeforeSlider(this.value)">
          <div class="slider-label-row">
            <span>1 · Mild Strain</span>
            <span>5 · Moderate Pressure</span>
            <span>10 · Severe Overload</span>
          </div>
        </div>

        <div class="slider-group">
          <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 600;">
            <label>2. Rate your stress right now (after this reset):</label>
            <span id="sliderAfterVal" style="color: var(--recovery-teal); font-weight: 700;">${this.stressAfter}/10</span>
          </div>
          <input type="range" id="stressAfterSlider" min="1" max="10" value="${this.stressAfter}" style="width: 100%; margin-top: 8px;" oninput="ResetModal.updateStressSlider(this.value)">
          <div class="slider-label-row">
            <span>1 · Deep Calm</span>
            <span>5 · Balanced</span>
            <span>10 · Overwhelmed</span>
          </div>
        </div>

        <div style="margin-top: 20px;">
          <label style="font-size: 13px; font-weight: 600;">Did this reset help?</label>
          <div class="relief-buttons-row">
            <button class="btn-relief-option selected" onclick="ResetModal.selectHelped('YES', this)">👍 Yes</button>
            <button class="btn-relief-option" onclick="ResetModal.selectHelped('A_LITTLE', this)">😐 A Little</button>
            <button class="btn-relief-option" onclick="ResetModal.selectHelped('NO', this)">👎 No</button>
          </div>
        </div>

        <button class="btn-primary" style="width: 100%; margin-top: 16px; padding: 14px;" onclick="ResetModal.submitCompletion()">
          Save to Personal Relief Map™ & Done
        </button>
      </div>
    `;
  },

  updateStressBeforeSlider(val) {
    this.stressBefore = parseInt(val);
    const display = document.getElementById("stressBeforeDisplay");
    const label = document.getElementById("sliderBeforeVal");
    if (display) display.innerText = `${val}/10`;
    if (label) label.innerText = `${val}/10`;
    this.updateDeltaDisplay();
  },

  updateStressSlider(val) {
    this.stressAfter = parseInt(val);
    const display = document.getElementById("stressAfterDisplay");
    const label = document.getElementById("sliderAfterVal");
    if (display) display.innerText = `${val}/10`;
    if (label) label.innerText = `${val}/10`;
    this.updateDeltaDisplay();
  },

  updateDeltaDisplay() {
    const delta = this.stressBefore - this.stressAfter;
    const deltaEl = document.getElementById("stressDeltaDisplay");
    if (deltaEl) {
      deltaEl.innerText = delta >= 0 ? `-${delta} pts` : `+${Math.abs(delta)} pts`;
      deltaEl.style.color = delta > 0 ? "var(--recovery-emerald)" : "var(--brand-reset)";
    }
  },

  selectedHelped: "YES",
  selectHelped(val, el) {
    this.selectedHelped = val;
    document.querySelectorAll(".btn-relief-option").forEach(b => b.classList.remove("selected"));
    el.classList.add("selected");
  },

  async submitCompletion() {
    try {
      const res = await API.completeReset({
        session_id: this.currentSession.session_id,
        stress_before: this.stressBefore,
        stress_after: this.stressAfter,
        did_this_help: this.selectedHelped
      });

      playCalmBell(528);

      this.containerEl.innerHTML = `
        <div style="text-align: center; padding: 30px 10px;">
          <div style="font-size: 48px; margin-bottom: 12px;">🌿</div>
          <h2 class="modal-step-title">Recovery Moment Logged</h2>
          <p style="font-size: 15px; color: var(--recovery-teal); font-weight: 600; margin-bottom: 14px;">
            Stress reduced by ${res.delta_relief} points!
          </p>
          <p style="font-size: 14px; color: var(--text-muted); margin-bottom: 20px; line-height: 1.6;">
            ${res.personal_insight}
          </p>
          <div style="background: var(--bg-subtle); padding: 14px; border-radius: var(--radius-sm); font-size: 13px; margin-bottom: 24px;">
            💡 <strong>Next Step:</strong> ${res.next_recommendation}
          </div>
          <button class="btn-primary" onclick="ResetModal.close(); window.App.refreshPersonalData();">
            Return to Work Space
          </button>
        </div>
      `;
    } catch (err) {
      alert("Error saving reset: " + err.message);
      this.close();
    }
  }
};

window.ResetModal = ResetModal;
