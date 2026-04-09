import requests
import os
import time

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "YOUR_RAPIDAPI_KEY_HERE")

def bulk_scan(domains: list[str], country_code: str = "US"):
    """
    Demonstrates how to scan a list of domains efficiently.
    If you are on the ULTRA or MEGA plan, you can run these concurrently.
    For BASIC/PRO plans, we recommend adding a small delay to avoid rate limits.
    """
    print(f"Starting bulk scan of {len(domains)} domains...")
    
    url = "https://xentic-comply-api.p.rapidapi.com/v1/scan"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "xentic-comply-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    results = []

    for domain in domains:
        print(f"Scanning {domain}...")
        payload = {"domain": domain, "country_code": country_code}
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            score = data.get("score")
            print(f"  → Score: {score}/100 ({data.get('grade')})")
            
            results.append({
                "domain": domain,
                "score": score,
                "grade": data.get("grade"),
                "status": "success"
            })
            
        except requests.exceptions.RequestException as e:
            print(f"  → Failed to scan {domain}: {e}")
            results.append({
                "domain": domain,
                "status": "error",
                "error_message": str(e)
            })
            
        # Optional: Add delay for lower tiers to prevent HTTP 429 Too Many Requests
        time.sleep(1) 

    # Generate a simple markdown report
    print("\n--- FINAL REPORT ---")
    for r in results:
        if r['status'] == 'success':
            warn = "⚠️ Needs attention!" if r['score'] < 75 else "✅ Passed"
            print(f"[{r['domain']}] Grade: {r['grade']} - {warn}")
        else:
            print(f"[{r['domain']}] Failed: {r['error_message']}")

if __name__ == "__main__":
    test_domains = ["google.com", "github.com", "example.com"]
    bulk_scan(test_domains, "US")
