const API_KEY = process.env.TRADELEAD_API_KEY;
const BASE_URL = "https://data.tradelead.ai";

if (!API_KEY) {
  console.error("Error: Please set the TRADELEAD_API_KEY environment variable.");
  process.exit(1);
}

const headers = {
  "X-API-Key": API_KEY,
  "Content-Type": "application/json",
};

/**
 * A simple helper to pause execution for a given number of milliseconds.
 */
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function main() {
  console.log("🚀 Submitting enrichment job...");

  // 1. Submit the job
  const payload = {
    companies: [
      { name: "Siemens AG", country: "Germany" },
      { name: "Robert Bosch GmbH", country: "Germany" }
    ],
  };

  const submitResponse = await fetch(`${BASE_URL}/v1/enrich`, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });

  if (submitResponse.status !== 202) {
    const text = await submitResponse.text();
    console.error(`Failed to submit job: ${submitResponse.status} - ${text}`);
    return;
  }

  const { job_id } = await submitResponse.json();
  console.log(`✅ Job accepted! Job ID: ${job_id}`);
  console.log("⏳ Waiting for enrichment to complete (this typically takes 5-15 seconds)...");

  // 2. Poll for results
  while (true) {
    const pollResponse = await fetch(`${BASE_URL}/v1/enrich/jobs/${job_id}`, { headers });
    
    if (!pollResponse.ok) {
      const text = await pollResponse.text();
      console.error(`Error polling job: ${pollResponse.status} - ${text}`);
      return;
    }

    const result = await pollResponse.json();
    const status = result.status;

    if (status === "completed") {
      console.log("\n✨ Enrichment completed!");
      console.log("--- Enriched Data ---");
      console.log(JSON.stringify(result.results, null, 2));
      break;
    } else if (status === "failed") {
      console.error(`\n❌ Enrichment failed: ${result.error_message}`);
      break;
    } else {
      console.log(`   Status: ${status}... checking again in 3 seconds.`);
      await sleep(3000);
    }
  }
}

main().catch(console.error);
