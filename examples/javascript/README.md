# JavaScript Examples

This directory contains examples of how to use the TradeLead Company Enrichment API with JavaScript.

## Setup

Set your API key as an environment variable (for Node.js):
```bash
export TRADELEAD_API_KEY="tl_live_your_key_here"
```

## Examples

### 1. `enrich.mjs`
A modern Node.js script using the native `fetch` API. It submits a batch of companies, polls the API with a small delay between checks, and logs the fully enriched data to the console.

**Run it:**
```bash
# Requires Node.js 18+
node enrich.mjs
```

### 2. `enrich.html`
A self-contained browser example. You can open this file directly in any modern browser to see how to trigger enrichments from a frontend application.

*Note: For production, you should never expose your API key directly in client-side HTML. Your frontend should communicate with your backend, which then securely holds the API key and communicates with TradeLead.*

**Run it:**
```bash
open enrich.html
```
