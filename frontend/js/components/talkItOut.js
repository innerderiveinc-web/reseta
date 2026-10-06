// RESETA™ TalkItOut Component: 🎙 TALK IT OUT™ (Section 16)
const TalkItOut = {
  isRecording: false,

  init() {
    this.modalEl = document.getElementById("talkModal");
    this.contentEl = document.getElementById("talkModalContent");
    this.closeBtn = document.getElementById("talkModalClose");

    if (this.closeBtn) {
      this.closeBtn.addEventListener("click", () => this.close());
    }
  },

  open() {
    this.modalEl.classList.add("active");
    this.renderInitial();
  },

  close() {
    this.modalEl.classList.remove("active");
  },

  renderInitial() {
    this.contentEl.innerHTML = `
      <div style="text-align: center;">
        <span class="brand-badge" style="background: var(--text-main);">RESETA TALK™</span>
        <h2 class="modal-step-title" style="margin-top: 10px;">🎙 Talk It Out</h2>
        <p class="modal-step-subtitle">Say whatever is on your mind in Hinglish, Hindi, or English.</p>

        <div class="voice-visualizer-bar" id="voiceWaveBar">
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
        </div>

        <div style="display: flex; justify-content: center; gap: 10px; margin-bottom: 16px;">
          <button id="speechToggleBtn" class="btn-primary" style="background: var(--brand-reset); display: flex; align-items: center; gap: 6px;" onclick="TalkItOut.toggleMicrophone()">
            🎙 <span id="speechBtnText">Start Speaking (Mic)</span>
          </button>
        </div>

        <div style="margin: 14px 0;">
          <textarea id="talkTranscriptInput" class="reset-input-area" placeholder="Speak or type what's on your mind... (e.g. 'Yaar aaj bohot zyada pressure feel ho raha hai, multiple tasks hain...')"></textarea>
        </div>

        <div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-bottom: 24px;">
          <span style="font-size: 11px; color: var(--text-muted); width: 100%;">Try quick prompt examples:</span>
          <button class="btn-small-pill" onclick="TalkItOut.fillSample('Yaar client deadline hai, 4 meetings scheduled hain, aur manager ne naya task de diya. Dimaag exhaust ho gaya.')">
            🗣 "Yaar client deadline hai aur dimaag full ho gaya..."
          </button>
          <button class="btn-small-pill" onclick="TalkItOut.fillSample('I have 5 deliverables due today and I feel completely stuck. Can not even start.')">
            🗣 "Stuck & task paralysis..."
          </button>
          <button class="btn-small-pill" onclick="TalkItOut.fillSample('Back-to-back calls from morning to evening, mind is spinning non stop.')">
            🗣 "Mind spinning after calls..."
          </button>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 12px; color: var(--recovery-teal); font-weight: 600;">
            🔒 100% Confidential to you.
          </span>
          <button class="btn-reset-hero" style="padding: 12px 28px; font-size: 15px;" onclick="TalkItOut.submitVoice()">
            Process & Reflect →
          </button>
        </div>
      </div>
    `;
  },

  recognition: null,

  toggleMicrophone() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      if (window.App && window.App.showToast) {
        window.App.showToast("Speech recognition is not supported in this browser. You can type below.");
      }
      return;
    }

    if (this.isRecording) {
      if (this.recognition) this.recognition.stop();
      this.isRecording = false;
      document.getElementById("speechBtnText").innerText = "Start Speaking (Mic)";
      document.getElementById("speechToggleBtn").style.background = "var(--brand-reset)";
      return;
    }

    try {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = true;
      this.recognition.interimResults = true;
      this.recognition.lang = "en-IN"; // Supports English/Indian accents and Hinglish phonetics

      this.recognition.onstart = () => {
        this.isRecording = true;
        document.getElementById("speechBtnText").innerText = "Listening... (Click to Stop)";
        document.getElementById("speechToggleBtn").style.background = "var(--recovery-emerald)";
      };

      this.recognition.onresult = (event) => {
        let transcript = "";
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          transcript += event.results[i][0].transcript;
        }
        const input = document.getElementById("talkTranscriptInput");
        if (input && transcript) {
          input.value = transcript;
        }
      };

      this.recognition.onerror = (e) => {
        console.warn("Speech recognition error:", e);
        this.isRecording = false;
        const btnText = document.getElementById("speechBtnText");
        if (btnText) btnText.innerText = "Start Speaking (Mic)";
      };

      this.recognition.onend = () => {
        this.isRecording = false;
        const btnText = document.getElementById("speechBtnText");
        if (btnText) btnText.innerText = "Start Speaking (Mic)";
      };

      this.recognition.start();
    } catch (err) {
      console.warn("Could not start speech recognition:", err);
    }
  },

  fillSample(text) {
    const input = document.getElementById("talkTranscriptInput");
    if (input) input.value = text;
  },

  async submitVoice() {
    const input = document.getElementById("talkTranscriptInput");
    const text = input ? input.value : "";
    if (!text.trim()) {
      if (window.App && window.App.showToast) {
        window.App.showToast("Please speak or enter what is on your mind.");
      }
      return;
    }

    this.contentEl.innerHTML = `
      <div style="text-align: center; padding: 40px 0;">
        <div class="breath-circle" style="margin: 0 auto 20px;">Listening...</div>
        <h3 style="font-size: 18px;">Taking in what you shared...</h3>
        <p style="font-size: 13px; color: var(--text-muted);">Creating a quiet space to decompress</p>
      </div>
    `;

    try {
      const res = await API.talkItOut({
        transcript_or_text: text,
        language: "Hinglish",
        audio_present: true
      });

      this.lastText = text;

      this.contentEl.innerHTML = `
        <div style="text-align: left;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <span class="brand-badge">${res.suggested_intervention_name}</span>
            <span style="font-size: 12px; color: var(--recovery-emerald); font-weight: 700;">🟢 Private & Grounded</span>
          </div>

          <div style="background: var(--bg-subtle); border-radius: var(--radius-md); padding: 20px; margin-bottom: 20px; border-left: 4px solid var(--recovery-teal);">
            <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: var(--recovery-teal); margin-bottom: 6px;">Empathetic Check-in:</div>
            <p style="font-size: 15px; line-height: 1.6; color: var(--text-main);">${res.reflection}</p>
          </div>

          <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: var(--radius-sm); padding: 14px 18px; margin-bottom: 24px; color: #166534; font-size: 14px;">
            ⚡ <strong>Next Step:</strong> ${res.action_prompt}
          </div>

          <div style="display: flex; justify-content: flex-end; gap: 12px;">
            <button class="btn-secondary" onclick="TalkItOut.renderInitial()">Speak Again</button>
            <button class="btn-reset-hero" style="padding: 12px 28px; font-size: 14px;" onclick="TalkItOut.launchFromTalk('${res.detected_state}')">
              Start 5-Min Reset 🔴
            </button>
          </div>
        </div>
      `;
    } catch (err) {
      if (window.App && window.App.showToast) {
        window.App.showToast("Error: " + err.message);
      }
      this.renderInitial();
    }
  },

  launchFromTalk(state, text) {
    const rawText = text || this.lastText || "";
    this.close();
    ResetModal.open(state);
    setTimeout(() => {
      const input = document.getElementById("resetRawInput");
      if (input) input.value = rawText;
    }, 100);
  }
};

window.TalkItOut = TalkItOut;
