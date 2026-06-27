# Retell AI — Anonymous Visitor Intercept Pipeline (Mock)

**[🎥 Watch the 25-second live execution demo on YouTube](https://youtu.be/48ZNFg8OJ48)**

A modular, headless Python microservice designed to transform anonymous pricing page traffic into actionable, enriched Slack alerts for the Retell BDR team. 

This repository was built as a proof-of-concept for the "Turn anonymous website visitors into actionable leads" backlog item for the Retell AI GTM Engineering role.

## Architecture & Logic Flow

Rather than building a redundant frontend UI that forces BDRs out of their workflow, this system operates entirely statelessly as a background webhook processor. 

1. **`core/intercept.py`**: Ingests raw HTTP headers from Webflow/Next.js. Drops residential ISP traffic (Comcast, AT&T) immediately to protect the enrichment API budget, parsing only verified corporate ASNs.
2. **`core/enrich.py`**: Takes the resolved domain (e.g., `flexport.com`) and queries the Apollo graph strictly for the Top 2 ICP Personas (VP of Call Center Operations, Head of Support).
3. **`core/dispatch.py`**: Formats the enriched JSON into a rich Slack Block Kit card, pushing the actionable leads directly to the BDR team's `#leads` channel with a 1-click trigger to initiate a Retell Voice AI callback.

## Why this structure?
- **Headless:** Fits natively into existing sales workflows (Slack) without requiring a new Vercel dashboard.
- **Decoupled:** The `EnrichmentGraph` module can be swapped seamlessly between Clearbit, RB2B, or Apollo depending on API cost constraints.
- **Defensive:** Residential checks happen *before* the expensive enrichment calls are made, optimizing CAC.

## Local Execution
Clone the repo, add your Slack webhook to `.env`, and run:
`python main.py`