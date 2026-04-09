import requests
import json
import os

# Get your rapidapi key from https://rapidapi.com/xentic-xentic-default/api/xentic-comply-api
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "YOUR_RAPIDAPI_KEY_HERE")

def scan_domain(domain: str, country_code: str = "EU"):
    print(f"Scanning {domain} under {country_code} jurisdiction...")
    
    url = "https://xentic-comply-api.p.rapidapi.com/v1/scan"

    payload = {
        "domain": domain,
        "country_code": country_code,
        "include_pdf": False # Requires PRO+ plan
    }
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "xentic-comply-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        # Pretty print results
        print("\n--- SCAN COMPLETE ---")
        print(f"Score:  {result.get('score')}/100")
        print(f"Grade:  {result.get('grade')}")
        print("\nSummary:")
        
        summary = result.get("summary", {})
        print(f"  Passed checks: {summary.get('passed')}/{summary.get('total_checks')}")
        print(f"  Critical Failures: {summary.get('critical_failures')}")
        
        if summary.get('critical_failures') > 0:
            print("\nCritical Issues Found:")
            for check in result.get("checks"):
                if not check.get("passed") and check.get("severity") == "critical":
                    print(f"  ❌ {check.get('name')}: {check.get('detail')}")
                    print(f"     Recommended Fix: {check.get('recommendation')}")
                    print(f"     Compliance Rule: {check.get('rule_reference')}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)

if __name__ == "__main__":
    scan_domain("example.com", "EU")
