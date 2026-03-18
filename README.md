<p align="center">
  <img src="assets/logo.png" alt="TradeLead.ai" width="480">
</p>

<h1 align="center">Company Enrichment API</h1>

<p align="center">
  <a href="examples/python/"><img src="https://img.shields.io/badge/python-3.8+-blue" alt="Python"></a>
  <a href="examples/javascript/"><img src="https://img.shields.io/badge/javascript-ES2020+-yellow" alt="JavaScript"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License: MIT"></a>
</p>

Welcome to the **TradeLead Company Enrichment API** usage repository. This repo contains documentation and runnable examples to help you integrate AI-powered company enrichment into your workflows.

> **Note:** For the complete API specification (endpoints, request/response schemas, and interactive testing), please refer to our **[Swagger Documentation](https://data.tradelead.ai/docs)**.

---

## 🚀 Setup & Requirements

To use the API, you need a TradeLead API key.

1. Create an account at [tradelead.ai](https://tradelead.ai)
2. Navigate to the **Developer** section in your dashboard.
3. Click **Generate API Key** (keys start with `tl_live_`).

For security, we recommend storing your key as an environment variable:

```bash
export TRADELEAD_API_KEY="tl_live_your_key_here"
```

## 🛠️ Usage

All API requests must include your API key in the `X-API-Key` header.

### 1. Submit a Job

```bash
curl -X POST https://data.tradelead.ai/v1/enrich \
  -H "X-API-Key: $TRADELEAD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "companies": [
      {"name": "Siemens AG", "country": "Germany"},
      {"name": "Robert Bosch GmbH"}
    ]
  }'
```

**Response (`202 Accepted`):**
```json
{
  "job_id": "b47e2a1f-8c3d-4e5a-9f6b-1a2b3c4d5e6f",
  "status": "pending",
  "total_companies": 2
}
```

### 2. Poll the Job Status

```bash
curl https://data.tradelead.ai/v1/enrich/jobs/b47e2a1f-8c3d-4e5a-9f6b-1a2b3c4d5e6f \
  -H "X-API-Key: $TRADELEAD_API_KEY"
```

**Response (`200 OK`):**
```json
{
  "job_id": "b47e2a1f-8c3d-4e5a-9f6b-1a2b3c4d5e6f",
  "status": "completed",
  "results": [
    {
      "name": "Siemens AG",
      "canonical_name": "Siemens Aktiengesellschaft",
      "country": "Germany",
      "sector": "Industrial Equipment & Machinery",
      "firmographics": { "company_size": "Multinational Enterprise", ... },
      "contact": { "website": "siemens.com", "email": "contact@siemens.com", ... },
      "trade": { "hs_codes": ["8501", "8504"], "is_importer": true, ... },
      "company_profile": "Global technology conglomerate...",
      "online_visibility": 5,
      "data_confidence": 0.95
    }
  ]
}
```
---

## 💻 Examples

We provide ready-to-use code examples in this repository.

### [Python: Excel Batch Processing](examples/python/)
Take an input Excel file (with `Company Name` and `Country` columns), submit it to the API, and output a fully enriched Excel file. 
- Ideal for bulk data enrichment and CRM operations.
- See the [Python README](examples/python/README.md) for setup and execution instructions.

### [JavaScript: Web Integration](examples/javascript/)
A minimal script showing how to trigger and poll an enrichment job from a Node.js script or directly within a browser page.
- Ideal for integrating enrichment into your own web app.
- See the [JavaScript README](examples/javascript/README.md) for the code.

---

## 💳 API Usage Notes

The TradeLead API uses a credit-based billing system:

- **Batched Process:** The enrichment api processes input companies with 10 items per batch. The usage credits are calculated accordingly.
- **Checking Balance:** You can check your remaining credits via the `/v1/usage` endpoint (see [Swagger](https://data.tradelead.ai/docs)).
- **Rate Limits:** Depending on your plan, you have daily request limits. Standard headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`) are returned on every response.


---

## 📋 Roadmap

- [x] Python quickstart example
- [x] Python Excel/CSV batch processing example
- [x] JavaScript Node.js example
- [x] JavaScript browser demo
- [ ] Python SDK (`pip install tradelead`)
- [ ] JavaScript/TypeScript SDK (`npm install tradelead`)
- [ ] Webhook integration example
- [ ] Async polling with exponential backoff utility
- [ ] Google Sheets integration example

---

## 🤝 Support

- **API Documentation:** [Swagger UI](https://data.tradelead.ai/docs)
- **Email:** support@tradelead.ai
- **Issues:** Please open a [GitHub Issue](https://github.com/tradelead/tradelead-company-enrichment-api/issues) if you encounter any bugs in these examples.
