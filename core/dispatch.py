import logging
import requests
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class SlackDispatcher:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def _build_block_kit_payload(self, domain: str, page_data: Dict, leads: List[Dict], icp_score: Optional[float]) -> Dict:
        leads_text = ""
        for lead in leads:
            leads_text += f"• *{lead['name']}* — {lead['title']}\n  ✉️ `{lead['email']}` | 🔗 <https://{lead['linkedin']}|LinkedIn>\n\n"

        # Format the mathematical match score
        score_text = f"*{icp_score * 100:.1f}%* (Tier 1 Match)" if icp_score else "N/A"

        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": "🚨 HIGH-INTENT VISITOR DETECTED", "emoji": True}
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Company:*\n`{domain}`"},
                        {"type": "mrkdwn", "text": f"*Page URL:*\n<{page_data.get('page_viewed')}>"},
                        {"type": "mrkdwn", "text": f"*Time on Page:*\n{page_data.get('time_on_page_secs')} seconds"},
                        {"type": "mrkdwn", "text": f"*ICP Match Score:*\n{score_text}"}
                    ]
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*🎯 Enriched Decision Makers:*\n{leads_text}"}
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "⚡ Launch AI Voice Callback", "emoji": True},
                            "style": "primary",
                            "value": f"launch_callback_{domain}"
                        }
                    ]
                }
            ]
        }

    def send_alert(self, domain: str, page_data: Dict, leads: List[Dict], icp_score: Optional[float] = None):
        """Dispatches the Block Kit payload to the configured Slack webhook."""
        logger.info("[Dispatch] Formatting enriched data into Slack Block Kit payload...")
        
        if not self.webhook_url:
            logger.warning("[Dispatch] SLACK_WEBHOOK_URL not set. Printing payload locally (Dry Run).")
            return

        payload = self._build_block_kit_payload(domain, page_data, leads, icp_score)
        
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=5)
            response.raise_for_status()
            logger.info("[Dispatch] ✅ Slack alert delivered successfully to #bdr-leads channel.")
        except requests.exceptions.RequestException as e:
            logger.error(f"[Dispatch] Failed to deliver Slack alert: {e}")