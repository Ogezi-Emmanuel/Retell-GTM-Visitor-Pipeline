# Unified GTM Revenue Engine (v2.0)

A headless, end-to-end B2B pipeline architecture engineered from first principles.

This engine structurally bypasses legacy marketing funnels (inbound forms) by intercepting anonymous website traffic at the edge, mathematically scoring the corporate entity against an Ideal Customer Profile (ICP) using pure-Python linear algebra, and routing enriched decision-makers directly to sales teams in real-time.

Built to capture invisible high-intent traffic, eliminate SDR research hours, and mathematically seal the top of the funnel.

## ⚙️ The Core Architecture

The pipeline operates as a sequence of asynchronous microservices, orchestrated by a central runner.

1. **Stage 1: The Edge Interceptor (`core/intercept.py`)**
* Catches anonymous HTTP requests at the pricing page.
* Resolves the visitor's IP address to a corporate ASN.
* Instantly drops known residential ISPs (Comcast, Verizon, MTN) at the edge to protect downstream API budgets.


2. **Stage 1.5: The Mathematical Gate (`icp_engine/`)**
* A fault-tolerant network stripper hits the resolved corporate domain, drops non-semantic HTML noise (scripts, navs), and extracts the raw text payload.
* A custom-built, zero-dependency TF-IDF (Term Frequency-Inverse Document Frequency) vectorizer maps the text into a high-dimensional vector space.
* Calculates the Cosine Similarity against a hardcoded "ICP Blueprint."
* If the mathematical match is below the configured threshold (e.g., `< 15%`), the pipeline hard-stops. **No unqualified leads consume enrichment credits.**


3. **Stage 2: The Graph Enricher (`core/enrich.py`)**
* Once mathematically qualified, the engine queries a data graph (Apollo/Clearbit) to extract specific executive personas (e.g., "VP of Sales", "RevOps Director").


4. **Stage 3: The Dispatcher (`core/dispatch.py`)**
* Formats the enriched leads, the firmographic data, and the mathematical ICP Match Score into a highly structured JSON payload.
* Fires a real-time Block Kit alert directly into the designated Slack channel for immediate outbound execution.



## 📂 System Structure

```text
GTM-Visitor-Pipeline/
├── config/
│   └── settings.py          # Environment variables & webhooks
├── core/
│   ├── dispatch.py          # Slack Block Kit formatting & webhook execution
│   ├── enrich.py            # Graph traversal for executive personas
│   └── intercept.py         # ASN resolution & residential ISP dropping
├── data/
│   └── mock_payload.json    # Simulated Webflow/Next.js edge requests
├── icp_engine/
│   ├── __init__.py
│   ├── config.py            # ICP Blueprint, noise corpus, & math thresholds
│   ├── extractor.py         # HTML DOM stripper & fault-tolerant HTTP client
│   └── vectorizer.py        # Pure math TF-IDF & Cosine Similarity engine
├── main.py                  # The Master Orchestrator
└── README.md

```

## 🛠️ Philosophy & Tech Stack

This architecture is built strictly on **first principles engineering**.

Rather than gluing together bloated NLP frameworks like `spaCy` or `scikit-learn` for basic lead qualification, the `icp_engine` is engineered entirely from scratch using Python's standard libraries (`urllib`, `html.parser`, `math`, `collections`).

This keeps the microservice incredibly lightweight, blisteringly fast, and completely deterministic.

## 🚀 Execution

Clone the repository and set your environment variables:

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

```

To run a simulation of the full pipeline (Intercept ➔ Score ➔ Enrich ➔ Dispatch):

```bash
python main.py

```

### Example Terminal Output

```text
============================================================
2026-07-02 11:15:00 - INITIALIZING UNIFIED GTM REVENUE ENGINE v2.0
============================================================

2026-07-02 11:15:00 - Booting Vector Engine and training base matrix...
2026-07-02 11:15:01 - [Intercept] Analyzing incoming IP footprint: 199.23.112.4
2026-07-02 11:15:01 - [Intercept] Corporate ASN validated. Target locked: flexport.com
2026-07-02 11:15:01 - Targeting flexport.com for Mathematical ICP Qualification...
2026-07-02 11:15:03 - Mathematical ICP Match: 28.20%
2026-07-02 11:15:03 - [Enrich] Querying enrichment graph for targets at flexport.com...
2026-07-02 11:15:04 - [Enrich] Extracted 2 qualified leads for flexport.com.
2026-07-02 11:15:04 - [Dispatch] Formatting enriched data into Slack Block Kit payload...
2026-07-02 11:15:05 - [Dispatch] ✅ Slack alert delivered successfully to #bdr-leads channel.

============================================================
2026-07-02 11:15:05 - PIPELINE EXECUTION COMPLETE. ENTERING STANDBY.
============================================================

```