// RESETA™ ResetModal Component: 🔴 RESET ME & RELIEFLOOP™
// Enterprise Web Audio Harmonic Sound Engine (Tibetan Singing Bowl & Solfeggio Frequencies)
const SoundEngine = {
  ctx: null,
  enabled: true,

  unlock() {
    try {
      if (!this.ctx) {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        if (AudioContextClass) {
          this.ctx = new AudioContextClass();
        }
      }
      if (this.ctx && this.ctx.state === "suspended") {
        this.ctx.resume();
      }
    } catch (e) {
      console.warn("Audio unlock warning:", e);
    }
  },

  playBell(freq = 432, duration = 2.2) {
    if (!this.enabled) return;
    this.unlock();
    try {
      const ctx = this.ctx;
      if (!ctx) return;
      const now = ctx.currentTime;

      // Primary oscillator (Fundamental frequency)
      const osc1 = ctx.createOscillator();
      const gain1 = ctx.createGain();
      osc1.type = "sine";
      osc1.frequency.setValueAtTime(freq, now);

      // Secondary overtone oscillator (Harmonic fifth for acoustic resonance)
      const osc2 = ctx.createOscillator();
      const gain2 = ctx.createGain();
      osc2.type = "sine";
      osc2.frequency.setValueAtTime(freq * 1.5, now);

      // Natural acoustic bell envelope (soft attack, warm decay)
      gain1.gain.setValueAtTime(0.001, now);
      gain1.gain.linearRampToValueAtTime(0.28, now + 0.04);
      gain1.gain.exponentialRampToValueAtTime(0.0001, now + duration);

      gain2.gain.setValueAtTime(0.001, now);
      gain2.gain.linearRampToValueAtTime(0.08, now + 0.04);
      gain2.gain.exponentialRampToValueAtTime(0.0001, now + (duration * 0.7));

      osc1.connect(gain1);
      gain1.connect(ctx.destination);
      osc2.connect(gain2);
      gain2.connect(ctx.destination);

      osc1.start(now);
      osc2.start(now);
      osc1.stop(now + duration);
      osc2.stop(now + duration);
    } catch (err) {
      console.warn("SoundEngine playBell error:", err);
    }
  },

  playStepTick() {
    if (!this.enabled) return;
    this.unlock();
    try {
      const ctx = this.ctx;
      if (!ctx) return;
      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sine";
      osc.frequency.setValueAtTime(587.33, now); // D5 soft chime
      gain.gain.setValueAtTime(0.001, now);
      gain.gain.linearRampToValueAtTime(0.12, now + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.35);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.35);
    } catch (e) {}
  },

  playReliefChime() {
    if (!this.enabled) return;
    this.playBell(528, 2.4); // 528Hz Solfeggio frequency
    setTimeout(() => this.playBell(660, 1.8), 220);
  },

  // ==========================================================
  // Continuous Ambient Soundscape with 4 Scientific Presets:
  // 1. zen_bowl: 432Hz Solfeggio & 136.1Hz Om (Grounding & anti-stress)
  // 2. binaural_alpha: 10Hz Alpha Waves (Hemispheric synchronization & calm focus)
  // 3. ocean_waves: Coastal Surf with 8s breathing tide (Heart-rate variability coherence)
  // 4. forest_rain: Biophilic Green Noise & 528Hz Clarity (Cognitive restoration)
  // ==========================================================
  ambientNodes: null,
  isAmbientPlaying: false,
  ambientVolume: 0.22,
  ambientPreset: "zen_bowl",

  getPresetName(preset = this.ambientPreset) {
    switch (preset) {
      case "zen_bowl": return "432Hz Zen Bowl & Om";
      case "binaural_alpha": return "10Hz Binaural Alpha Waves";
      case "ocean_waves": return "Ocean Breath Surf";
      case "forest_rain": return "Forest Rain & 528Hz";
      default: return "Calm Ambient Soundscape";
    }
  },

  setPreset(preset) {
    this.ambientPreset = preset;
    if (this.isAmbientPlaying) {
      this.stopAmbientSoundscape(0.3);
      setTimeout(() => this.startAmbientSoundscape(preset), 350);
    }
  },

  startAmbientSoundscape(preset = this.ambientPreset) {
    if (!this.enabled) return;
    if (this.isAmbientPlaying) return;
    this.unlock();
    try {
      const ctx = this.ctx;
      if (!ctx) return;
      const now = ctx.currentTime;
      this.ambientPreset = preset;

      // 1. Master ambient gain with smooth 1.8s fade-in
      const masterGain = ctx.createGain();
      masterGain.gain.setValueAtTime(0.0001, now);
      masterGain.gain.linearRampToValueAtTime(this.ambientVolume, now + 1.8);
      masterGain.connect(ctx.destination);

      // 2. Breath-sync gain node (undulates softly with 8-second breathing pace)
      const breathGain = ctx.createGain();
      breathGain.gain.setValueAtTime(0.82, now);
      breathGain.connect(masterGain);

      // 3. Gentle 0.125 Hz LFO (8.0s breathing cycle: 4s inhale swell, 4s exhale ebb)
      const lfo = ctx.createOscillator();
      const lfoDepth = ctx.createGain();
      lfo.type = "sine";
      lfo.frequency.setValueAtTime(0.125, now);
      lfoDepth.gain.setValueAtTime(preset === "ocean_waves" ? 0.32 : 0.18, now);
      lfo.connect(lfoDepth);
      lfoDepth.connect(breathGain.gain);

      // 4. Low-pass soothing acoustic filter (cuts harsh frequencies)
      const filter = ctx.createBiquadFilter();
      filter.type = "lowpass";
      filter.frequency.setValueAtTime(preset === "forest_rain" ? 750 : 540, now);
      filter.Q.setValueAtTime(1.1, now);
      filter.connect(breathGain);

      // 5. Preset-specific Oscillators
      const oscRoot = ctx.createOscillator();
      const gainRoot = ctx.createGain();
      oscRoot.type = "sine";

      const oscFifth = ctx.createOscillator();
      const gainFifth = ctx.createGain();
      oscFifth.type = "sine";

      const oscShimmer = ctx.createOscillator();
      const gainShimmer = ctx.createGain();
      oscShimmer.type = "sine";

      const oscClarity = ctx.createOscillator();
      const gainClarity = ctx.createGain();
      oscClarity.type = "sine";

      // Configure Frequencies based on selected Scientific Acoustic Preset
      if (preset === "binaural_alpha") {
        // 10 Hz difference for true Alpha Brainwave Entrainment (226Hz - 216Hz = 10Hz)
        oscRoot.frequency.setValueAtTime(108.0, now); // grounding sub
        gainRoot.gain.setValueAtTime(0.24, now);

        oscFifth.frequency.setValueAtTime(216.0, now); // base carrier
        gainFifth.gain.setValueAtTime(0.26, now);

        oscShimmer.frequency.setValueAtTime(226.0, now); // 10Hz beat offset
        gainShimmer.gain.setValueAtTime(0.26, now);

        oscClarity.frequency.setValueAtTime(432.0, now); // harmonic overtone
        gainClarity.gain.setValueAtTime(0.06, now);
      } else if (preset === "ocean_waves") {
        // Subtle underlying chord with focus on surf rhythm
        oscRoot.frequency.setValueAtTime(108.0, now);
        gainRoot.gain.setValueAtTime(0.18, now);

        oscFifth.frequency.setValueAtTime(162.0, now);
        gainFifth.gain.setValueAtTime(0.12, now);

        oscShimmer.frequency.setValueAtTime(216.0, now);
        gainShimmer.gain.setValueAtTime(0.06, now);

        oscClarity.frequency.setValueAtTime(324.0, now);
        gainClarity.gain.setValueAtTime(0.03, now);
      } else if (preset === "forest_rain") {
        // 528 Hz Solfeggio clarity pad with soft resonant intervals
        oscRoot.frequency.setValueAtTime(176.0, now);
        gainRoot.gain.setValueAtTime(0.18, now);

        oscFifth.frequency.setValueAtTime(264.0, now);
        gainFifth.gain.setValueAtTime(0.14, now);

        oscShimmer.frequency.setValueAtTime(352.0, now);
        gainShimmer.gain.setValueAtTime(0.10, now);

        oscClarity.frequency.setValueAtTime(528.0, now);
        gainClarity.gain.setValueAtTime(0.08, now);
      } else {
        // "zen_bowl" Default: 136.1 Hz Om + 204.15 Hz Fifth + 432 Hz + 528 Hz
        oscRoot.frequency.setValueAtTime(136.1, now);
        gainRoot.gain.setValueAtTime(0.32, now);

        oscFifth.frequency.setValueAtTime(204.15, now);
        gainFifth.gain.setValueAtTime(0.20, now);

        oscShimmer.frequency.setValueAtTime(432.0, now);
        gainShimmer.gain.setValueAtTime(0.08, now);

        oscClarity.frequency.setValueAtTime(528.0, now);
        gainClarity.gain.setValueAtTime(0.04, now);
      }

      oscRoot.connect(gainRoot);
      gainRoot.connect(filter);
      oscFifth.connect(gainFifth);
      gainFifth.connect(filter);
      oscShimmer.connect(gainShimmer);
      gainShimmer.connect(filter);
      oscClarity.connect(gainClarity);
      gainClarity.connect(filter);

      // 6. Pink/White noise generator (surf/rain/breeze texture)
      const bufferSize = ctx.sampleRate * 2;
      const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const output = noiseBuffer.getChannelData(0);
      let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
      for (let i = 0; i < bufferSize; i++) {
        const white = Math.random() * 2 - 1;
        b0 = 0.99886 * b0 + white * 0.0555179;
        b1 = 0.99332 * b1 + white * 0.0750759;
        b2 = 0.96900 * b2 + white * 0.1538520;
        b3 = 0.86650 * b3 + white * 0.3104856;
        b4 = 0.55000 * b4 + white * 0.5329522;
        b5 = -0.7616 * b5 - white * 0.0168980;
        output[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.04;
        b6 = white * 0.115926;
      }
      const noiseSource = ctx.createBufferSource();
      noiseSource.buffer = noiseBuffer;
      noiseSource.loop = true;

      const noiseFilter = ctx.createBiquadFilter();
      noiseFilter.type = preset === "forest_rain" ? "highpass" : "bandpass";
      noiseFilter.frequency.setValueAtTime(preset === "forest_rain" ? 650 : (preset === "ocean_waves" ? 220 : 260), now);
      noiseFilter.Q.setValueAtTime(0.9, now);

      const noiseGain = ctx.createGain();
      const nGainVal = preset === "ocean_waves" ? 0.16 : (preset === "forest_rain" ? 0.11 : 0.045);
      noiseGain.gain.setValueAtTime(nGainVal, now);

      noiseSource.connect(noiseFilter);
      noiseFilter.connect(noiseGain);
      noiseGain.connect(breathGain);

      // Start all audio components
      oscRoot.start(now);
      oscFifth.start(now);
      oscShimmer.start(now);
      oscClarity.start(now);
      lfo.start(now);
      noiseSource.start(now);

      this.ambientNodes = {
        masterGain,
        breathGain,
        filter,
        oscRoot,
        oscFifth,
        oscShimmer,
        oscClarity,
        lfo,
        noiseSource
      };
      this.isAmbientPlaying = true;
    } catch (e) {
      console.warn("Could not start ambient soundscape:", e);
    }
  },

  stopAmbientSoundscape(fadeSeconds = 1.2) {
    if (!this.isAmbientPlaying || !this.ambientNodes) return;
    try {
      const ctx = this.ctx;
      const nodes = this.ambientNodes;
      if (ctx && nodes && nodes.masterGain) {
        const now = ctx.currentTime;
        nodes.masterGain.gain.cancelScheduledValues(now);
        nodes.masterGain.gain.setValueAtTime(nodes.masterGain.gain.value, now);
        nodes.masterGain.gain.linearRampToValueAtTime(0.0001, now + fadeSeconds);
        setTimeout(() => {
          try {
            nodes.oscRoot.stop();
            nodes.oscFifth.stop();
            nodes.oscShimmer.stop();
            nodes.oscClarity.stop();
            nodes.lfo.stop();
            nodes.noiseSource.stop();
          } catch (e) {}
        }, fadeSeconds * 1000 + 100);
      }
    } catch (e) {
      console.warn("Could not stop ambient soundscape:", e);
    }
    this.ambientNodes = null;
    this.isAmbientPlaying = false;
  },

  toggleAmbient() {
    if (this.isAmbientPlaying) {
      this.stopAmbientSoundscape(0.5);
      return false;
    } else {
      this.startAmbientSoundscape();
      return true;
    }
  }
};

window.SoundEngine = SoundEngine;

// ==========================================================
// VoiceCoach: Soothing Audio Narration (Web Speech API)
// Speaks instructions out loud so users can keep eyes closed!
// ==========================================================
const VoiceCoach = {
  enabled: true,
  currentUtterance: null,

  speak(text) {
    if (!this.enabled || !('speechSynthesis' in window)) return;
    try {
      window.speechSynthesis.cancel(); // Stop any pending speech
      const cleanText = text
        .replace(/<[^>]*>/g, '')
        .replace(/[\*\#\_]/g, '')
        .trim();

      if (!cleanText) return;

      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.rate = 0.86; // calm, unhurried, mindful breathing pace
      utterance.pitch = 0.98; // warm, grounded tone

      const voices = window.speechSynthesis.getVoices();
      if (voices && voices.length > 0) {
        const preferredVoice = voices.find(v => 
          v.lang.includes("en-IN") || v.lang.includes("hi-IN") || v.name.includes("Natural") || v.name.includes("Google") || v.name.includes("Samantha")
        );
        if (preferredVoice) utterance.voice = preferredVoice;
      }

      window.speechSynthesis.speak(utterance);
      this.currentUtterance = utterance;
    } catch (e) {
      console.warn("VoiceCoach speech error:", e);
    }
  },

  stop() {
    if ('speechSynthesis' in window) {
      try {
        window.speechSynthesis.cancel();
      } catch (e) {}
    }
  },

  toggle() {
    this.enabled = !this.enabled;
    if (!this.enabled) this.stop();
    return this.enabled;
  }
};

window.VoiceCoach = VoiceCoach;

// Unlock audio context on any user interaction with the document
document.addEventListener("click", () => SoundEngine.unlock(), { once: false });
document.addEventListener("keydown", () => SoundEngine.unlock(), { once: false });

function playCalmBell(freq = 432) {
  SoundEngine.playBell(freq);
}

const ResetModal = {
  currentSession: null,
  currentStepIndex: 0,
  stepTimer: null,
  stepSecondsRemaining: 0,
  isAutoPlay: true, // Hands-Free Auto-Step mode: active by default so eyes stay closed!
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
    VoiceCoach.stop();
    SoundEngine.stopAmbientSoundscape(0.3);
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

      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 24px;">
        <button type="button" class="btn-small-pill" onclick="SoundEngine.playBell(432); window.App?.showToast('🔔 Tibetan singing bowl bell (432Hz) playing');" style="display: flex; align-items: center; gap: 6px; font-weight: 600; cursor: pointer; border-color: var(--recovery-teal); color: var(--recovery-teal);" title="Test audio playback">
          🔊 <span>Test Bell Sound</span>
        </button>
        <button class="btn-primary" onclick="ResetModal.renderStep2()">Next: What's Going On? →</button>
      </div>
    `;
  },

  setTime(minutes) {
    this.selectedTime = minutes;
    SoundEngine.playStepTick();
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
          Start Reset →
        </button>
      </div>
    `;
  },

  selectState(stateName, el) {
    this.selectedState = stateName.toLowerCase().replace(/ /g, '_').replace("'", "");
    SoundEngine.playStepTick();
    document.querySelectorAll(".state-chip").forEach(c => c.classList.remove("selected"));
    el.classList.add("selected");
  },

  async launchSession() {
    // Unlock and play bell synchronously on click gesture
    SoundEngine.playBell(432, 2.4);

    // Start continuous, pleasant, mind-refreshing background soundscape!
    SoundEngine.startAmbientSoundscape();

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
        SoundEngine.stopAmbientSoundscape(0.3);
        this.renderRedTier(plan);
        return;
      }

      this.currentStepIndex = 0;
      this.renderGuidedStep();
    } catch (err) {
      SoundEngine.stopAmbientSoundscape(0.3);
      if (window.App && window.App.showToast) {
        window.App.showToast("Could not start reset: " + err.message);
      }
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

    // 1. Spoken Audio Voice Narration (so user can keep eyes closed)
    VoiceCoach.speak(`${step.title}. ${step.instruction}`);

    // 2. Start Hands-Free auto countdown timer
    this.startStepTimer(step.duration_seconds);

    this.containerEl.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <span class="brand-badge">${session.intervention_name}</span>
        <span style="font-size: 13px; font-weight: 600; color: var(--text-muted);">Step ${this.currentStepIndex + 1} of ${totalSteps}</span>
      </div>

      <!-- Peaceful Eyes-Closed Mode Banner -->
      <div style="background: rgba(13, 148, 136, 0.08); border: 1px solid rgba(13, 148, 136, 0.22); border-radius: var(--radius-sm); padding: 9px 12px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; gap: 10px;">
        <div style="display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--recovery-teal); font-weight: 600;">
          <span style="font-size: 16px;">🧘</span>
          <span><strong>Eyes-Closed Mode:</strong> Voice coach instructions out loud & steps advance automatically.</span>
        </div>
        <div style="display: flex; gap: 6px; align-items: center;">
          <button id="modalVoiceBtn" class="btn-small-pill" onclick="ResetModal.toggleVoiceGuide()" style="font-size: 11px; padding: 4px 8px; cursor: pointer; border-color: ${VoiceCoach.enabled ? 'var(--recovery-teal)' : 'var(--border-light)'}; color: ${VoiceCoach.enabled ? 'var(--recovery-teal)' : 'var(--text-muted)'};" title="Toggle audio voice narration">
            ${VoiceCoach.enabled ? "🎙️ Voice: ON" : "🔇 Voice: OFF"}
          </button>
          <button id="autoPlayToggleBtn" class="btn-small-pill" onclick="ResetModal.toggleAutoPlay()" style="font-size: 11px; padding: 4px 8px; cursor: pointer; border-color: ${this.isAutoPlay ? 'var(--recovery-emerald)' : 'var(--border-light)'}; color: ${this.isAutoPlay ? 'var(--recovery-emerald)' : 'var(--text-muted)'};" title="Toggle hands-free auto advancing">
            ${this.isAutoPlay ? "⏱️ Auto-Flow: ON" : "⏸️ Auto-Flow: PAUSED"}
          </button>
        </div>
      </div>

      <!-- Continuous Mind-Refreshing Ambient Soundscape Bar with Scientific Presets -->
      <div style="background: rgba(79, 70, 229, 0.07); border: 1px solid rgba(79, 70, 229, 0.18); border-radius: var(--radius-sm); padding: 10px 14px; margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <div style="display: flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 600; color: var(--brand-reset);">
            <span id="modalAmbientIndicator" style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: ${SoundEngine.isAmbientPlaying ? '#10B981' : '#9CA3AF'}; box-shadow: ${SoundEngine.isAmbientPlaying ? '0 0 8px rgba(16, 185, 129, 0.6)' : 'none'}; animation: breathePaced 4s infinite;"></span>
            <span>Soundscape: <strong id="activeSoundscapeTitle">${SoundEngine.getPresetName()}</strong></span>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 11px; color: var(--text-muted); font-weight: 700;">Next in: <span id="stepTimerDisplay" style="color: var(--brand-reset);">${this.stepSecondsRemaining}s</span></span>
            <button id="modalAmbientBtn" class="btn-small-pill" onclick="ResetModal.toggleAmbientSound()" style="font-size: 11px; padding: 4px 10px; cursor: pointer; border-color: ${SoundEngine.isAmbientPlaying ? 'var(--brand-reset)' : 'var(--border-light)'}; color: ${SoundEngine.isAmbientPlaying ? 'var(--brand-reset)' : 'var(--text-muted)'};">
              ${SoundEngine.isAmbientPlaying ? '🔊 Sound: Playing' : '🔇 Muted'}
            </button>
          </div>
        </div>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
          <button class="sound-chip ${SoundEngine.ambientPreset === 'zen_bowl' ? 'active' : ''}" data-preset="zen_bowl" onclick="ResetModal.changeSoundPreset('zen_bowl')" title="Tibetan 432Hz bell + 136.1Hz Om (Grounding & calm)">🧘 432Hz Zen Bowl</button>
          <button class="sound-chip ${SoundEngine.ambientPreset === 'binaural_alpha' ? 'active' : ''}" data-preset="binaural_alpha" onclick="ResetModal.changeSoundPreset('binaural_alpha')" title="10Hz difference wave for deep Alpha relaxation">🧠 10Hz Alpha Waves</button>
          <button class="sound-chip ${SoundEngine.ambientPreset === 'ocean_waves' ? 'active' : ''}" data-preset="ocean_waves" onclick="ResetModal.changeSoundPreset('ocean_waves')" title="8-second natural coastal tide pacing">🌊 Ocean Breath Surf</button>
          <button class="sound-chip ${SoundEngine.ambientPreset === 'forest_rain' ? 'active' : ''}" data-preset="forest_rain" onclick="ResetModal.changeSoundPreset('forest_rain')" title="Gentle rain and 528Hz mental clarity pad">🌧️ Forest Rain & 528Hz</button>
        </div>
      </div>

      <!-- Step Countdown Progress Bar -->
      <div style="width: 100%; height: 4px; background: var(--border-light); border-radius: 2px; overflow: hidden; margin-bottom: 16px;">
        <div id="stepProgressBar" style="height: 100%; width: 0%; background: linear-gradient(90deg, var(--brand-reset), var(--recovery-teal)); transition: width 0.9s linear;"></div>
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
          ⏱ Step Duration: ~${step.duration_seconds}s (Auto-advancing hands-free)
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

  startStepTimer(durationSeconds) {
    if (this.stepTimer) clearInterval(this.stepTimer);
    this.stepSecondsRemaining = Math.max(10, durationSeconds || 15);
    this.updateTimerDisplay();

    if (!this.isAutoPlay) return;

    this.stepTimer = setInterval(() => {
      this.stepSecondsRemaining--;
      this.updateTimerDisplay();

      if (this.stepSecondsRemaining <= 0) {
        clearInterval(this.stepTimer);
        this.stepTimer = null;
        this.nextStep(true); // Automatically advance hands-free!
      }
    }, 1000);
  },

  updateTimerDisplay() {
    const timeEl = document.getElementById("stepTimerDisplay");
    const barEl = document.getElementById("stepProgressBar");
    if (timeEl) {
      timeEl.innerText = `${this.stepSecondsRemaining}s`;
    }
    if (barEl && this.currentSession && this.currentSession.steps) {
      const step = this.currentSession.steps[this.currentStepIndex];
      const total = Math.max(10, (step ? step.duration_seconds : 15));
      const pct = Math.max(0, Math.min(100, ((total - this.stepSecondsRemaining) / total) * 100));
      barEl.style.width = `${pct}%`;
    }
  },

  toggleAutoPlay() {
    this.isAutoPlay = !this.isAutoPlay;
    if (this.isAutoPlay) {
      const step = this.currentSession.steps[this.currentStepIndex];
      this.startStepTimer(this.stepSecondsRemaining || (step ? step.duration_seconds : 15));
    } else {
      if (this.stepTimer) clearInterval(this.stepTimer);
    }
    const btn = document.getElementById("autoPlayToggleBtn");
    if (btn) {
      btn.innerHTML = this.isAutoPlay ? "⏱️ Auto-Flow: ON" : "⏸️ Auto-Flow: PAUSED";
      btn.style.color = this.isAutoPlay ? "var(--recovery-emerald)" : "var(--text-muted)";
      btn.style.borderColor = this.isAutoPlay ? "var(--recovery-emerald)" : "var(--border-light)";
    }
  },

  toggleVoiceGuide() {
    const isVoiceOn = VoiceCoach.toggle();
    const btn = document.getElementById("modalVoiceBtn");
    if (btn) {
      btn.innerHTML = isVoiceOn ? "🎙️ Voice: ON" : "🔇 Voice: OFF";
      btn.style.color = isVoiceOn ? "var(--recovery-teal)" : "var(--text-muted)";
      btn.style.borderColor = isVoiceOn ? "var(--recovery-teal)" : "var(--border-light)";
    }
    if (isVoiceOn && this.currentSession && this.currentSession.steps) {
      const step = this.currentSession.steps[this.currentStepIndex];
      VoiceCoach.speak(`${step.title}. ${step.instruction}`);
    }
  },

  toggleAmbientSound() {
    const isPlaying = SoundEngine.toggleAmbient();
    const btn = document.getElementById("modalAmbientBtn");
    const indicator = document.getElementById("modalAmbientIndicator");
    if (btn) {
      btn.innerHTML = isPlaying ? "🔊 Sound: Playing" : "🔇 Sound: Muted";
      btn.style.color = isPlaying ? "var(--brand-reset)" : "var(--text-muted)";
      btn.style.borderColor = isPlaying ? "var(--brand-reset)" : "var(--border-light)";
    }
    if (indicator) {
      indicator.style.background = isPlaying ? "#10B981" : "#9CA3AF";
      indicator.style.boxShadow = isPlaying ? "0 0 8px rgba(16, 185, 129, 0.6)" : "none";
    }
  },

  changeSoundPreset(preset) {
    SoundEngine.setPreset(preset);
    document.querySelectorAll(".sound-chip").forEach(c => {
      c.classList.toggle("active", c.dataset.preset === preset);
    });
    const titleEl = document.getElementById("activeSoundscapeTitle");
    if (titleEl) titleEl.innerText = SoundEngine.getPresetName(preset);
  },

  nextStep(isAuto = false) {
    if (this.stepTimer) {
      clearInterval(this.stepTimer);
      this.stepTimer = null;
    }
    VoiceCoach.stop();
    SoundEngine.playStepTick();
    if (this.currentStepIndex < this.currentSession.steps.length - 1) {
      this.currentStepIndex++;
      this.renderGuidedStep();
    } else {
      this.renderReliefCheck();
    }
  },

  // Step 4: Relief Check™ (Section 12)
  renderReliefCheck() {
    if (this.stepTimer) {
      clearInterval(this.stepTimer);
      this.stepTimer = null;
    }
    VoiceCoach.speak("Reset session complete. You can gently open your eyes. Take a breath and let us check your relief.");
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
    if (this.stepTimer) clearInterval(this.stepTimer);
    VoiceCoach.stop();
    SoundEngine.stopAmbientSoundscape(1.0);
    SoundEngine.playReliefChime();
    try {
      const res = await API.completeReset({
        session_id: this.currentSession.session_id,
        stress_before: this.stressBefore,
        stress_after: this.stressAfter,
        did_this_help: this.selectedHelped
      });

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
      if (window.App && window.App.showToast) {
        window.App.showToast("Could not save reset: " + err.message);
      }
      this.close();
    }
  }
};

window.ResetModal = ResetModal;
