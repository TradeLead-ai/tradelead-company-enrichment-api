import os
import time
import argparse
import requests
import pandas as pd

# Configuration
API_KEY = os.environ.get("TRADELEAD_API_KEY")
BASE_URL = "https://data.tradelead.ai"

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def load_companies(file_path: str) -> list:
    """Read the file (CSV or Excel) and convert it into a list of dicts for the API."""
    print(f"📖 Reading {file_path}...")
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    companies = []
    for _, row in df.iterrows():
        # Clean up NaNs
        company_data = {}
        if pd.notna(row.get('Company Name')):
            company_data["name"] = str(row['Company Name'])
        if pd.notna(row.get('Country')):
            company_data["country"] = str(row['Country'])
            
        if "name" in company_data and company_data["name"].strip():
            companies.append(company_data)
            
    print(f"   Found {len(companies)} valid companies.")
    return companies

def submit_job(companies: list) -> str:
    """Submit the companies to the TradeLead API."""
    print("🚀 Submitting batch enrichment job...")
    
    # We can submit up to 1000 at once. The API auto-batches them into chunks of 10.
    payload = {"companies": companies}
    response = requests.post(f"{BASE_URL}/v1/enrich", headers=HEADERS, json=payload)
    
    if response.status_code != 202:
        raise Exception(f"Failed to submit job: {response.status_code} - {response.text}")
        
    job_id = response.json()["job_id"]
    print(f"✅ Job accepted! Job ID: {job_id}")
    return job_id

def poll_job(job_id: str) -> list:
    """Poll the API until the job is completed and retrieve paginated results."""
    print("⏳ Waiting for enrichment to complete...")
    
    # Poll until completed or failed
    while True:
        response = requests.get(f"{BASE_URL}/v1/enrich/jobs/{job_id}", headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"Error polling job: {response.status_code} - {response.text}")
            
        data = response.json()
        status = data["status"]
        
        if status == "completed":
            print("\n✨ Enrichment completed! Fetching results...")
            break
        elif status == "failed":
            raise Exception(f"❌ Enrichment failed: {data.get('error_message')}")
            
        # Display progress for multi-batch jobs
        batches = data.get("batches", {})
        if batches:
            completed = batches.get("completed", 0)
            total = batches.get("total", 0)
            print(f"   Progress: {completed}/{total} batches completed. Checking again in 5s...")
        else:
            print(f"   Status: {status}. Checking again in 5s...")
            
        time.sleep(5)
        
    # Fetch paginated results
    all_results = []
    page = 1
    while True:
        print(f"   Fetching page {page}...")
        resp = requests.get(f"{BASE_URL}/v1/enrich/jobs/{job_id}?page={page}&per_page=10", headers=HEADERS).json()
        
        results = resp.get("results", [])
        all_results.extend(results)
        
        pagination = resp.get("pagination", {})
        if page >= pagination.get("total_pages", 1):
            break
            
        page += 1
        
    return all_results

def flatten_result(result: dict) -> dict:
    """Flatten the nested API response into a flat dictionary suitable for a spreadsheet."""
    flat = {
        "Input Name": result.get("name"),
        "Canonical Name": result.get("canonical_name"),
        "Country": result.get("country"),
        "Sector": result.get("sector"),
        
        "Company Profile": result.get("company_profile"),
        "Product Description": result.get("product_description"),
        
        "Visibility Score (0-5)": result.get("online_visibility"),
        "Data Confidence": result.get("data_confidence"),
    }
    
    # Flatten firmographics
    fg = result.get("firmographics", {})
    flat.update({
        "Company Size": fg.get("company_size"),
        "Employees": fg.get("employee_count"),
        "Revenue": fg.get("revenue_range"),
        "Year Founded": fg.get("year_founded"),
        "Ownership": fg.get("ownership_type"),
    })
    
    # Flatten contacts
    contact = result.get("contact", {})
    flat.update({
        "Website": contact.get("website"),
        "Email": contact.get("email"),
        "Phone": contact.get("phone"),
        "Address": contact.get("address"),
        "LinkedIn": contact.get("linkedin_url"),
    })
    
    # Flatten trade data
    trade = result.get("trade", {})
    flat.update({
        "Trade Volume": trade.get("trade_volume"),
        "Trade Direction": trade.get("primary_trade_direction"),
        "HS Codes": ", ".join(trade.get("hs_codes", [])),
        "Trading Partners": ", ".join(trade.get("trading_partners", [])),
    })
    
    return flat

def save_results(results: list, output_path: str):
    """Save the enriched flat dictionaries to a CSV or Excel file."""
    flat_results = [flatten_result(r) for r in results]
    df_out = pd.DataFrame(flat_results)
    
    if output_path.endswith('.csv'):
        df_out.to_csv(output_path, index=False)
    else:
        df_out.to_excel(output_path, index=False)
    print(f"💾 Saved {len(flat_results)} enriched profiles to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Batch enrich companies from Excel")
    parser.add_argument("--input", required=True, help="Input Excel file path")
    parser.add_argument("--output", required=True, help="Output Excel file path")
    args = parser.parse_args()
    
    if not API_KEY:
        print("Error: Please set the TRADELEAD_API_KEY environment variable.")
        exit(1)
        
    try:
        companies = load_companies(args.input)
        if not companies:
            print("No valid companies found to enrich.")
            return
            
        job_id = submit_job(companies)
        results = poll_job(job_id)
        save_results(results, args.output)
        
        print("🎉 All done!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
