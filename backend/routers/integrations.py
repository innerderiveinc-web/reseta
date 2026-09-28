# RESETA™ Enterprise Integrations (Teams & Slack) Router
# Section 33, 34, 61, 62: In-Flow workplace experience, bot webhooks, calendar-aware prompts
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(prefix="/api/integrations", tags=["Workplace Integrations"])

class SlackSlashCommandRequest(BaseModel):
    command: str = "/reset"
    text: str = ""
    user_name: str = "arjun.sharma"
    channel_name: str = "direct-message"

@router.post("/slack/slash-reset")
def handle_slack_slash_command(req: SlackSlashCommandRequest):
    """
    Simulates the Slack /reset command (Section 34).
    Launches private in-flow reset modal:
    2 min | 5 min | 10 min
    """
    return {
        "response_type": "ephemeral", # Visible ONLY to the employee
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "🔴 RESETA: Workplace Recovery"}
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "*Too much on your mind? Take a moment to reset.*"}
            },
            {
                "type": "actions",
                "elements": [
                    {"type": "button", "text": {"type": "plain_text", "text": "⚡ 2 Min Quick Reset"}, "value": "2"},
                    {"type": "button", "text": {"type": "plain_text", "text": "🌿 5 Min Full Reset"}, "value": "5", "style": "primary"},
                    {"type": "button", "text": {"type": "plain_text", "text": "🧘 10 Min Deep Reset"}, "value": "10"}
                ]
            }
        ]
    }

@router.get("/contextual-prompt")
def get_contextual_recovery_prompt():
    """
    Desktop & In-Flow Recovery Moment (Section 62):
    e.g., 'Back-to-back day? Take 2 min'
    """
    return {
        "should_prompt": True,
        "trigger_type": "CALENDAR_BACK_TO_BACK",
        "title": "Back-to-back day?",
        "subtitle": "You just completed 3 consecutive meetings without a break.",
        "prompt": "Take 2 min to clear meeting residue before your next task.",
        "recommended_minutes": 2,
        "action_label": "Start 2-Min Reset"
    }
