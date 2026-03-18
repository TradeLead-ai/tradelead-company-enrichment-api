import os
import time
import requests
import json

# Configuration
API_KEY = os.environ.get("TRADELEAD_API_KEY")
BASE_URL = "https://data.tradelead.ai"

if not API_KEY:
    print("Error: Please set the TRADELEAD_API_KEY environment variable.")
    exit(1)

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def main():
    print("🚀 Submitting enrichment job...")
    
    # 1. Submit the job
    payload = {
        "companies": [
            {"name": "Siemens AG", "country": "Germany"}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/v1/enrich", headers=HEADERS, json=payload)
    
    if response.status_code != 202:
        print(f"Failed to submit job: {response.status_code} - {response.text}")
        return

    job_data = response.json()
    job_id = job_data["job_id"]
    print(f"✅ Job accepted! Job ID: {job_id}")
    print("⏳ Waiting for enrichment to complete (this typically takes 5-15 seconds)...")
    
    # 2. Poll for results
    while True:
        poll_response = requests.get(f"{BASE_URL}/v1/enrich/jobs/{job_id}", headers=HEADERS)
        
        if poll_response.status_code != 200:
            print(f"Error polling job: {poll_response.status_code} - {poll_response.text}")
            return
            
        result = poll_response.json()
        status = result["status"]
        
        if status == "completed":
            print("✨ Enrichment completed!\n")
            print("--- Enriched Data ---")
            print(json.dumps(result.get("results", []), indent=2))
            break
        elif status == "failed":
            print(f"❌ Enrichment failed: {result.get('error_message')}")
            break
        else:
            # Status is 'pending' or 'processing'
            print(f"   Status: {status}... checking again in 3 seconds.")
            time.sleep(3)

if __name__ == "__main__":
    main()
