import json
import logging
import time
import os
from typing import List, Dict

logger = logging.getLogger(__name__)

class EnrichmentGraph:
    def __init__(self, mock_data_path: str = "data/mock_payload.json"):
        self.mock_data_path = mock_data_path

    def _load_mock_data(self) -> dict:
        if not os.path.exists(self.mock_data_path):
            logger.error(f"[Enrich] Mock data file missing at {self.mock_data_path}")
            return {}
        with open(self.mock_data_path, 'r') as f:
            return json.load(f)

    def query_icp_personas(self, domain: str) -> List[Dict]:
        """
        Simulates querying the Apollo.io or People Data Labs graph for specific ICP titles.
        """
        logger.info(f"[Enrich] Querying enrichment graph for Call Center ICP targets at {domain}...")
        time.sleep(1.2) # Simulate graph traversal latency

        data = self._load_mock_data()
        apollo_mocks = data.get("apollo_mock_response", {})
        
        leads = apollo_mocks.get(domain, [])
        if not leads:
            logger.warning(f"[Enrich] No high-intent personas found for {domain}. Halting.")
            return []

        logger.info(f"[Enrich] Extracted {len(leads)} qualified leads for {domain}.")
        return leads