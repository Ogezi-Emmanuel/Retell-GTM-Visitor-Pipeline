# config.py

# --- PIPELINE THRESHOLDS ---
SIMILARITY_THRESHOLD = 0.15  # Minimum cosine similarity to flag as ICP (Adjust based on testing)
REQUEST_TIMEOUT = 8          # Seconds before dropping a stalled connection
MAX_RETRIES = 2              # Network fault tolerance for the edge extractor

# --- NETWORK CONFIGURATION ---
# HTTP Headers to bypass basic bot-protection (Cloudflare/Akamai)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

# --- THE MATHEMATICAL BASELINE ---
# This is the exact definition of your Ideal Customer Profile.
ICP_BLUEPRINT = """
We provide enterprise B2B SaaS solutions for revenue operations, 
sales enablement, and pipeline velocity. Our software integrates 
with CRMs to handle data routing, compliance, predictive analytics, 
and artificial intelligence modeling for Chief Revenue Officers and VPs of Sales.
"""

# Background noise to balance the Inverse Document Frequency (IDF) weights.
# This prevents common business words from skewing the math.
CORPUS_NOISE = [
    "We sell consumer skincare products, face wash, and cosmetics directly to buyers.",
    "Local plumbing services, HVAC repair, and residential maintenance.",
    "Crypto trading platform, blockchain tokenomics, and web3 NFT drops."
]