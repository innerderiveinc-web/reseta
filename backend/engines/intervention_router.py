# RESETA™ Enterprise Intervention Router™
# Section 9, 10, 29: Clinically reviewed intervention catalog & interactive Do It With Me™ pacing
from typing import Dict, List, Any
from backend.schemas import StepScript

INTERVENTION_CATALOG: Dict[str, Dict[str, Any]] = {
    "mental_load_unload": {
        "id": "int_mental_load_unload",
        "name": "Mental Load Unload™",
        "target_state": "overloaded",
        "description": "Convert overwhelming mental clutter into clear buckets: Now, Scheduled, Waiting, Later, and Next.",
        "category": "Cognitive Clarification & Task Compression",
        "evidence": "Cognitive Offloading & Working Memory Capacity (Risko & Gilbert, 2016)",
        "reviewer": "Dr. Ananya Sharma, Lead Clinical Psychologist",
        "steps_by_duration": {
            2: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Pause & Step Back", "instruction": "Place your hands in your lap and take one slow, steady breath.", "duration_seconds": 25},
                {"timestamp_label": "00:25", "action_type": "UNLOAD", "title": "What's occupying the most space?", "instruction": "Pick the single heaviest task on your plate right now.", "duration_seconds": 45},
                {"timestamp_label": "01:10", "action_type": "REFLECT", "title": "Separate Now from Later", "instruction": "You don't need to resolve everything today. Only this one piece matters right now.", "duration_seconds": 30},
                {"timestamp_label": "01:40", "action_type": "MICRO_STEP", "title": "Your Next 5 Minutes", "instruction": "Decide on the first sentence or first 2 minutes of progress. Nothing else.", "duration_seconds": 20}
            ],
            5: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Physical Reset", "instruction": "Drop your shoulders away from your ears. Unclench your jaw. Rest your eyes.", "duration_seconds": 30},
                {"timestamp_label": "00:30", "action_type": "BREATHE", "title": "4-4 Paced Breath", "instruction": "Inhale gently for 4 counts... exhale slowly for 4 counts. Feel your feet on the ground.", "duration_seconds": 45},
                {"timestamp_label": "01:15", "action_type": "UNLOAD", "title": "Unload Everything", "instruction": "Notice the swirling tasks: deadlines, pending replies, meetings, unread messages.", "duration_seconds": 60},
                {"timestamp_label": "02:15", "action_type": "REFLECT", "title": "Filter What You Can Influence", "instruction": "Which part can you actually change in the next hour? Let go of what depends on others.", "duration_seconds": 60},
                {"timestamp_label": "03:15", "action_type": "MICRO_STEP", "title": "Lock In The Next Step", "instruction": "Select one single focus. Park the rest in your later bucket with full permission.", "duration_seconds": 60},
                {"timestamp_label": "04:15", "action_type": "PAUSE", "title": "Somatic Check", "instruction": "Take one final deep exhale. You are clear and ready to step back in.", "duration_seconds": 45}
            ],
            10: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Full Somatic Deceleration", "instruction": "Step back from your screen. Let your gaze rest on an object across the room.", "duration_seconds": 60},
                {"timestamp_label": "01:00", "action_type": "BREATHE", "title": "Box Breathing", "instruction": "Inhale for 4, hold for 4, exhale for 4, hold empty for 4. Repeat 3 times.", "duration_seconds": 90},
                {"timestamp_label": "02:30", "action_type": "UNLOAD", "title": "Complete Brain Dump", "instruction": "Pour out all internal tension and competing commitments into your unloaded buckets.", "duration_seconds": 150},
                {"timestamp_label": "05:00", "action_type": "REFLECT", "title": "Sort Control vs Reaction", "instruction": "Identify what is in your immediate circle of control versus waiting on third parties.", "duration_seconds": 120},
                {"timestamp_label": "07:00", "action_type": "MICRO_STEP", "title": "Single-Threaded Action Plan", "instruction": "Define your solitary priority for the next 45 minutes.", "duration_seconds": 120},
                {"timestamp_label": "09:00", "action_type": "PAUSE", "title": "Re-Entry Intention", "instruction": "Ground yourself with one full breath before returning to your workspace.", "duration_seconds": 60}
            ]
        }
    },
    "thought_dump": {
        "id": "int_thought_dump",
        "name": "Racing Thoughts Dump",
        "target_state": "racing_thoughts",
        "description": "Slow down hyperactive thoughts through paced verbal and cognitive offloading.",
        "category": "Cognitive De-escalation",
        "evidence": "Expressive Writing & Cognitive Inhibition (Pennebaker & Beall, 1986)",
        "reviewer": "Dr. Kabir Roy, Consulting Neuropsychologist",
        "steps_by_duration": {
            2: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Halt the Velocity", "instruction": "Close your eyes or look down. Tell yourself: 'Nothing needs an instant answer this second.'", "duration_seconds": 30},
                {"timestamp_label": "00:30", "action_type": "UNLOAD", "title": "Name the Core Loop", "instruction": "What thought keeps replaying in your mind?", "duration_seconds": 45},
                {"timestamp_label": "01:15", "action_type": "REFLECT", "title": "Park It On Paper", "instruction": "Acknowledge the thought without debating it. You have noted it down.", "duration_seconds": 45}
            ],
            5: [
                {"timestamp_label": "00:00", "action_type": "BREATHE", "title": "Physiological Sigh", "instruction": "Two quick inhales through the nose, followed by a long, slow sigh out through the mouth.", "duration_seconds": 45},
                {"timestamp_label": "00:45", "action_type": "UNLOAD", "title": "Stream of Consciousness", "instruction": "Let the words flow without grammar or editing. Release the mental buffer.", "duration_seconds": 90},
                {"timestamp_label": "02:15", "action_type": "REFLECT", "title": "Fact vs Story", "instruction": "Notice: which part is observable fact, and which is an imagined catastrophic story?", "duration_seconds": 75},
                {"timestamp_label": "03:30", "action_type": "MICRO_STEP", "title": "One Grounded Reality", "instruction": "Feel your feet pressing into the floor. You are right here, in this room, right now.", "duration_seconds": 90}
            ],
            10: [
                {"timestamp_label": "00:00", "action_type": "BREATHE", "title": "Extended Exhale Protocol", "instruction": "Inhale 4 counts, exhale 7 counts. Signal the parasympathetic nervous system to slow down.", "duration_seconds": 120},
                {"timestamp_label": "02:00", "action_type": "UNLOAD", "title": "Deep Narrative Release", "instruction": "Empty all pending mental loops onto the page.", "duration_seconds": 180},
                {"timestamp_label": "05:00", "action_type": "REFLECT", "title": "Distancing Reframe", "instruction": "Ask: 'If a close colleague had these thoughts, what reassuring perspective would I offer them?'", "duration_seconds": 150},
                {"timestamp_label": "07:30", "action_type": "MICRO_STEP", "title": "Anchored Return", "instruction": "Choose one single physical action to take next.", "duration_seconds": 150}
            ]
        }
    },
    "priority_compression": {
        "id": "int_priority_compression",
        "name": "Priority Compression™",
        "target_state": "work_pressure",
        "description": "Strip away false urgency and compress 10 demands down to 1 clear execution path.",
        "category": "Workplace Demand Regulation",
        "evidence": "Selective Attention Under Stress (Kahneman, 1973; Chajut & Algom, 2003)",
        "reviewer": "Dr. Ananya Sharma, Lead Clinical Psychologist",
        "steps_by_duration": {
            2: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "De-Escalate Urgency", "instruction": "Urgency is a feeling, not a rule. Breathe out.", "duration_seconds": 30},
                {"timestamp_label": "00:30", "action_type": "UNLOAD", "title": "Pick The Domino", "instruction": "If you could only accomplish ONE deliverable today, which one moves the needle?", "duration_seconds": 50},
                {"timestamp_label": "01:20", "action_type": "MICRO_STEP", "title": "Shield Your Focus", "instruction": "Mute notifications for 20 minutes to work on this one item.", "duration_seconds": 40}
            ],
            5: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Create Distance", "instruction": "Push your chair back 3 inches. Take a deep, deliberate breath.", "duration_seconds": 30},
                {"timestamp_label": "00:30", "action_type": "UNLOAD", "title": "List Competing Demands", "instruction": "Identify the top 3 demands creating pressure right now.", "duration_seconds": 60},
                {"timestamp_label": "01:30", "action_type": "REFLECT", "title": "Identify The Leverage Point", "instruction": "Which task actually alleviates pressure the most once finished?", "duration_seconds": 90},
                {"timestamp_label": "03:00", "action_type": "MICRO_STEP", "title": "Communicate or Execute", "instruction": "Either send a quick expectation update or begin the first 5 minutes of work.", "duration_seconds": 90},
                {"timestamp_label": "04:30", "action_type": "PAUSE", "title": "Clarity Check", "instruction": "Notice the quiet after setting boundaries.", "duration_seconds": 30}
            ],
            10: [
                {"timestamp_label": "00:00", "action_type": "BREATHE", "title": "Paced Breath Grounding", "instruction": "5 slow belly breaths.", "duration_seconds": 90},
                {"timestamp_label": "01:30", "action_type": "UNLOAD", "title": "Eisenhower Stress Matrix", "instruction": "Distinguish between true deadlines and manufactured panic.", "duration_seconds": 180},
                {"timestamp_label": "04:30", "action_type": "REFLECT", "title": "Scope Pruning", "instruction": "What can be done at 80% good enough instead of delayed perfectionism?", "duration_seconds": 150},
                {"timestamp_label": "07:00", "action_type": "MICRO_STEP", "title": "Execution Boundary", "instruction": "Block your calendar for protected work time.", "duration_seconds": 180}
            ]
        }
    },
    "two_min_activation": {
        "id": "int_2min_activation",
        "name": "2-Minute Activation",
        "target_state": "cant_start",
        "description": "Bypass task paralysis through micro-friction reduction and somatic activation.",
        "category": "Behavioral Activation",
        "evidence": "Implementation Intentions & Action Initiation (Gollwitzer, 1999)",
        "reviewer": "Dr. Kabir Roy, Consulting Neuropsychologist",
        "steps_by_duration": {
            2: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Lower The Bar", "instruction": "You don't have to finish the project. You only have to start for 120 seconds.", "duration_seconds": 30},
                {"timestamp_label": "00:30", "action_type": "MICRO_STEP", "title": "Define The Tiny Entry", "instruction": "Open the file or write one single draft bullet point.", "duration_seconds": 50},
                {"timestamp_label": "01:20", "action_type": "PAUSE", "title": "Momentum Spark", "instruction": "You have broken inertia. Keep moving forward.", "duration_seconds": 40}
            ],
            5: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Physical Shakedown", "instruction": "Stand up, stretch your arms overhead, shake out your wrists.", "duration_seconds": 45},
                {"timestamp_label": "00:45", "action_type": "REFLECT", "title": "Name The Resistance", "instruction": "Is the resistance boredom, fear of imperfection, or confusion? Acknowledge it without judgment.", "duration_seconds": 60},
                {"timestamp_label": "01:45", "action_type": "MICRO_STEP", "title": "The 10% Draft Rule", "instruction": "Give yourself explicit permission to write a messy first draft.", "duration_seconds": 90},
                {"timestamp_label": "03:15", "action_type": "MICRO_STEP", "title": "Set 3-Minute Timer", "instruction": "Work continuously on only this file until the chime sounds.", "duration_seconds": 105}
            ],
            10: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Somatic Activation Walk", "instruction": "Step away from desk and take 15 brisk steps.", "duration_seconds": 90},
                {"timestamp_label": "01:30", "action_type": "REFLECT", "title": "Identify Friction Points", "instruction": "Clear physical clutter from your desk space.", "duration_seconds": 120},
                {"timestamp_label": "03:30", "action_type": "MICRO_STEP", "title": "Micro-Task Breakdown", "instruction": "Divide the overwhelming project into 3 bite-sized sub-tasks.", "duration_seconds": 150},
                {"timestamp_label": "06:00", "action_type": "MICRO_STEP", "title": "Execute Step 1", "instruction": "Begin step 1 now with full presence.", "duration_seconds": 240}
            ]
        }
    },
    "pause_and_deescalate": {
        "id": "int_pause_deescalate",
        "name": "Pause & De-escalation",
        "target_state": "frustration",
        "description": "Cool sympathetic nervous arousal and prevent reactive workplace replies.",
        "category": "Emotional Regulation",
        "evidence": "Affect Labeling & Amygdala Regulation (Lieberman et al., 2007)",
        "reviewer": "Dr. Ananya Sharma, Lead Clinical Psychologist",
        "steps_by_duration": {
            2: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Do Not Send / Do Not Reply", "instruction": "Remove your fingers from the keyboard. Push back from the screen.", "duration_seconds": 30},
                {"timestamp_label": "00:30", "action_type": "BREATHE", "title": "Long Cool Exhale", "instruction": "Exhale as if blowing out a candle across the table.", "duration_seconds": 45},
                {"timestamp_label": "01:15", "action_type": "REFLECT", "title": "Pause Before Responding", "instruction": "Give it 20 minutes before sending any message. Your future self will thank you.", "duration_seconds": 45}
            ],
            5: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Hands Off The Keys", "instruction": "Step away or turn your chair around. Do not react right now.", "duration_seconds": 45},
                {"timestamp_label": "00:45", "action_type": "BREATHE", "title": "Cooling Exhales", "instruction": "Breathe in deeply, breathe out with an audible sigh.", "duration_seconds": 60},
                {"timestamp_label": "01:45", "action_type": "REFLECT", "title": "Label The Trigger", "instruction": "What part felt unfair, disrespectful, or frustrating? Name it silently.", "duration_seconds": 75},
                {"timestamp_label": "03:00", "action_type": "REFLECT", "title": "Intent vs Outcome", "instruction": "Could this be miscommunication rather than malice? What is the most constructive stance?", "duration_seconds": 75},
                {"timestamp_label": "04:15", "action_type": "PAUSE", "title": "Calm Composure", "instruction": "Return to your seat with quiet poise.", "duration_seconds": 45}
            ],
            10: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Physical Transition", "instruction": "Get a glass of cool water. Sip slowly.", "duration_seconds": 90},
                {"timestamp_label": "01:30", "action_type": "BREATHE", "title": "Vagus Nerve Activation", "instruction": "Paced breathing with prolonged exhalations.", "duration_seconds": 150},
                {"timestamp_label": "04:00", "action_type": "UNLOAD", "title": "Draft The Unsent Email", "instruction": "Type what you really want to say in a private notepad, then delete it.", "duration_seconds": 180},
                {"timestamp_label": "07:00", "action_type": "REFLECT", "title": "Diplomatic Reframe", "instruction": "Craft a 2-sentence objective reply focusing only on solutions.", "duration_seconds": 180}
            ]
        }
    },
    "mental_shutdown": {
        "id": "int_mental_shutdown",
        "name": "End-of-Day Mental Shutdown™",
        "target_state": "night_stress",
        "description": "Establish a firm psychological boundary between work hours and evening recovery.",
        "category": "Work-Life Transition & Boundary Setting",
        "evidence": "Psychological Detachment from Work (Sonnentag & Fritz, 2015)",
        "reviewer": "Dr. Kabir Roy, Consulting Neuropsychologist",
        "steps_by_duration": {
            2: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Close All Work Tabs", "instruction": "Explicitly close all browser windows and productivity tools.", "duration_seconds": 40},
                {"timestamp_label": "00:40", "action_type": "UNLOAD", "title": "Tomorrow's Landing Pad", "instruction": "Write down the first task you will touch tomorrow morning.", "duration_seconds": 40},
                {"timestamp_label": "01:20", "action_type": "PAUSE", "title": "Work Is Complete", "instruction": "Say to yourself: 'Work is paused for today. Evening belongs to me.'", "duration_seconds": 40}
            ],
            5: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "The Shutdown Ritual", "instruction": "Push in your desk chair and adjust the lighting in the room.", "duration_seconds": 45},
                {"timestamp_label": "00:45", "action_type": "UNLOAD", "title": "Unload Remaining Loops", "instruction": "Jot down any lingering thoughts or pending items on paper.", "duration_seconds": 75},
                {"timestamp_label": "02:00", "action_type": "REFLECT", "title": "Celebrate What Got Done", "instruction": "Notice 2 things you completed or advanced today, even small ones.", "duration_seconds": 60},
                {"timestamp_label": "03:00", "action_type": "MICRO_STEP", "title": "Lock Tomorrow's First Step", "instruction": "Set one clear focus for tomorrow morning so your mind doesn't have to worry tonight.", "duration_seconds": 60},
                {"timestamp_label": "04:00", "action_type": "PAUSE", "title": "Official Sign-Off", "instruction": "Log off. Your evening recovery begins now.", "duration_seconds": 60}
            ],
            10: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Physical Transition Away From Desk", "instruction": "Stand up and walk to another room.", "duration_seconds": 90},
                {"timestamp_label": "01:30", "action_type": "BREATHE", "title": "Decompression Breath", "instruction": "Slow diaphragmatic breathing.", "duration_seconds": 120},
                {"timestamp_label": "03:30", "action_type": "UNLOAD", "title": "Complete Work-Life Ledger", "instruction": "Catalogue all open threads into tomorrow's parking lot.", "duration_seconds": 180},
                {"timestamp_label": "06:30", "action_type": "REFLECT", "title": "Boundary Affirmation", "instruction": "Acknowledge that staying online will not improve tomorrow's output.", "duration_seconds": 120},
                {"timestamp_label": "08:30", "action_type": "PAUSE", "title": "Transition into Evening", "instruction": "Engage all senses in your home or personal environment.", "duration_seconds": 90}
            ]
        }
    },
    "paced_breathing_grounding": {
        "id": "int_paced_grounding",
        "name": "Grounding & Paced Breathing",
        "target_state": "general_tension",
        "description": "5-4-3-2-1 sensory grounding paired with resonance frequency breathing.",
        "category": "Somatic Autonomic Regulation",
        "evidence": "Resonance Frequency Breathing & Heart Rate Variability (Lehrer et al., 2000)",
        "reviewer": "Dr. Ananya Sharma, Lead Clinical Psychologist",
        "steps_by_duration": {
            2: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Ground Through The Soles", "instruction": "Press your heels and toes firmly into the floor. Feel the floor supporting you.", "duration_seconds": 30},
                {"timestamp_label": "00:30", "action_type": "BREATHE", "title": "Even 4-4 Breath", "instruction": "Inhale gently for 4... exhale smoothly for 4.", "duration_seconds": 60},
                {"timestamp_label": "01:30", "action_type": "PAUSE", "title": "Body Check", "instruction": "Notice tension releasing from your neck and forehead.", "duration_seconds": 30}
            ],
            5: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Postural Alignment", "instruction": "Sit comfortably with your spine tall but relaxed. Let your hands rest softly.", "duration_seconds": 30},
                {"timestamp_label": "00:30", "action_type": "REFLECT", "title": "5-4-3-2-1 Sensory Anchor", "instruction": "Name 3 things you can see, 2 things you can touch, and 1 sound you can hear.", "duration_seconds": 60},
                {"timestamp_label": "01:30", "action_type": "BREATHE", "title": "Coherent Breathing", "instruction": "Inhale for 5 seconds... exhale for 5 seconds. Repeat smoothly.", "duration_seconds": 120},
                {"timestamp_label": "03:30", "action_type": "PAUSE", "title": "Somatic Softening", "instruction": "Let your belly expand naturally with each breath without forcing.", "duration_seconds": 60},
                {"timestamp_label": "04:30", "action_type": "MICRO_STEP", "title": "Stepping Forward", "instruction": "Open your eyes gently, carrying this steady center into your next task.", "duration_seconds": 30}
            ],
            10: [
                {"timestamp_label": "00:00", "action_type": "PAUSE", "title": "Full Somatic Stillness", "instruction": "Find complete comfort and stillness.", "duration_seconds": 60},
                {"timestamp_label": "01:00", "action_type": "REFLECT", "title": "Progressive Sensory Grounding", "instruction": "Scan physical touchpoints: clothes, chair, floor, ambient air.", "duration_seconds": 120},
                {"timestamp_label": "03:00", "action_type": "BREATHE", "title": "6 Breaths Per Minute Resonance", "instruction": "Inhale 5 seconds, exhale 5 seconds for continuous vagal stimulation.", "duration_seconds": 240},
                {"timestamp_label": "07:00", "action_type": "PAUSE", "title": "Whole-Body Scan", "instruction": "Release subtle holding patterns in scalp, throat, and abdomen.", "duration_seconds": 120},
                {"timestamp_label": "09:00", "action_type": "MICRO_STEP", "title": "Calm Re-Engagement", "instruction": "Transition back to work feeling renewed and focused.", "duration_seconds": 60}
            ]
        }
    }
}

class InterventionRouter:
    """
    Selects the most suitable clinician-reviewed intervention
    based on identified state, user choice, and past personalization history.
    """

    STATE_TO_INTERVENTION_MAP = {
        "overloaded": "mental_load_unload",
        "racing_thoughts": "thought_dump",
        "work_pressure": "priority_compression",
        "cant_start": "two_min_activation",
        "rumination": "thought_dump",
        "frustration": "pause_and_deescalate",
        "night_stress": "mental_shutdown",
        "decision_overload": "priority_compression",
        "low_energy": "two_min_activation",
        "general_tension": "paced_breathing_grounding"
    }

    @classmethod
    def route(cls, state: str, duration_minutes: int = 5) -> Dict[str, Any]:
        duration = 5
        if duration_minutes in [2, 5, 10]:
            duration = duration_minutes

        intervention_key = cls.STATE_TO_INTERVENTION_MAP.get(state, "mental_load_unload")
        catalog_entry = INTERVENTION_CATALOG.get(intervention_key, INTERVENTION_CATALOG["mental_load_unload"])

        steps = catalog_entry["steps_by_duration"].get(duration, catalog_entry["steps_by_duration"][5])
        step_objs = [StepScript(**s) for s in steps]

        return {
            "intervention_id": catalog_entry["id"],
            "intervention_name": catalog_entry["name"],
            "target_state": state,
            "duration_minutes": duration,
            "description": catalog_entry["description"],
            "category": catalog_entry["category"],
            "evidence": catalog_entry["evidence"],
            "reviewer": catalog_entry["reviewer"],
            "steps": step_objs
        }
