import logging
import json
from config.settings import SLACK_WEBHOOK_URL
from core.intercept import VisitorInterceptor
from core.enrich import EnrichmentGraph
from core.dispatch import SlackDispatcher

# Configure standardized logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def run_pipeline():
    print("\n" + "="*60)
    logger.info("INITIALIZING RETELL GTM VISITOR INTERCEPT PIPELINE v1.0")
    print("="*60 + "\n")

    # Initialize Microservices
    interceptor = VisitorInterceptor()
    enricher = EnrichmentGraph()
    dispatcher = SlackDispatcher(webhook_url=SLACK_WEBHOOK_URL)

    # Load the simulated Webflow/Next.js incoming webhook payload
    with open("data/mock_payload.json", "r") as f:
        incoming_request = json.load(f)["incoming_webflow_request"]

    visitor_ip = incoming_request.get("visitor_ip")
    
    # --- PIPELINE STAGE 1: Intercept & Resolve ---
    domain = interceptor.resolve_corporate_asn(visitor_ip)
    if not domain:
        logger.info("Pipeline terminated at Intercept stage (No corporate match).")
        return

    # --- PIPELINE STAGE 2: Graph Enrichment ---
    leads = enricher.query_icp_personas(domain)
    if not leads:
        logger.info("Pipeline terminated at Enrich stage (No ICP leads found).")
        return

    # --- PIPELINE STAGE 3: Webhook Dispatch ---
    dispatcher.send_alert(domain=domain, page_data=incoming_request, leads=leads)

    print("\n" + "="*60)
    logger.info("PIPELINE EXECUTION COMPLETE. ENTERING STANDBY.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_pipeline()