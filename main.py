import logging
import json
from config.settings import SLACK_WEBHOOK_URL
from core.intercept import VisitorInterceptor
from core.enrich import EnrichmentGraph
from core.dispatch import SlackDispatcher

# --- INJECTING THE ICP ENGINE ---
from icp_engine.vectorizer import VectorEngine
from icp_engine.extractor import fetch_and_clean_url
import icp_engine.config as icp_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def run_pipeline():
    print("\n" + "="*60)
    logger.info("INITIALIZING UNIFIED GTM REVENUE ENGINE v2.0")
    print("="*60 + "\n")

    interceptor = VisitorInterceptor()
    enricher = EnrichmentGraph()
    dispatcher = SlackDispatcher(webhook_url=SLACK_WEBHOOK_URL)
    
    # Pre-load the Vector Engine matrix
    logger.info("Booting Vector Engine and training base matrix...")
    icp = VectorEngine()
    icp.train([icp_config.ICP_BLUEPRINT] + icp_config.CORPUS_NOISE)
    baseline_vector = icp.vectorize(icp_config.ICP_BLUEPRINT)

    with open("data/mock_payload.json", "r") as f:
        incoming_request = json.load(f)["incoming_webflow_request"]

    visitor_ip = incoming_request.get("visitor_ip")
    
    # --- STAGE 1: Intercept ---
    domain = interceptor.resolve_corporate_asn(visitor_ip)
    if not domain:
        logger.info("Pipeline terminated at Intercept stage.")
        return

    # --- STAGE 1.5: The Math Gate ---
    logger.info(f"Targeting {domain} for Mathematical ICP Qualification...")
    scraped_text = fetch_and_clean_url(domain)
    icp_score = 0.0
    
    if scraped_text.startswith("[ERROR]"):
        logger.warning(f"Failed to scrape {domain}: {scraped_text}. Halting pipeline.")
        return
    else:
        target_vector = icp.vectorize(scraped_text)
        icp_score = icp.calculate_similarity(baseline_vector, target_vector)
        logger.info(f"Mathematical ICP Match: {icp_score * 100:.2f}%")
        
        # Drop unqualified traffic instantly to save Apollo API credits
        if icp_score < icp_config.SIMILARITY_THRESHOLD:
            logger.warning(f"Domain {domain} failed ICP threshold. Halting pipeline.")
            return

    # --- STAGE 2: Graph Enrichment ---
    leads = enricher.query_icp_personas(domain)
    if not leads:
        logger.info("Pipeline terminated at Enrich stage.")
        return

    # --- STAGE 3: Slack Dispatch ---
    dispatcher.send_alert(domain=domain, page_data=incoming_request, leads=leads, icp_score=icp_score)

    print("\n" + "="*60)
    logger.info("PIPELINE EXECUTION COMPLETE. ENTERING STANDBY.")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_pipeline()