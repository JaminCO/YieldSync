import requests
import json
from typing import Dict, Any, List, Optional

POOLS_URL = "https://yields.llama.fi/pools"
PROTOCOL_URL_TMPL = "https://api.llama.fi/protocol/{slug}"

def fetch_pools(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    resp = requests.get(POOLS_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    pools = data.get("data", [])
    return pools[:limit] if limit else pools

def fetch_protocol_details(slug: str) -> Dict[str, Any]:
    resp = requests.get(PROTOCOL_URL_TMPL.format(slug=slug), timeout=30)
    resp.raise_for_status()
    return resp.json()

def apy_search(pool_id):
    url = f"https://yields.llama.fi/chart/{pool_id}"
    response = requests.get(url)
    data = response.json()
    pool_data = data.get("data", [])
    # Start from the latest and go backwards until apy is not 0
    latest_valid = None
    is_latest = True
    count = 0
    for entry in reversed(pool_data):
        count += 1
        apy = entry.get("apy")
        if apy and apy != 0:
            latest_valid = entry
            break
    if latest_valid is None and pool_data:
        # fallback: return the latest even if apy is 0
        latest_valid = pool_data[-1]
        count = 0
    if count > 1:
        is_latest = False
        latest_valid["main_apy"] = pool_data[-1]["apy"]
    latest_valid["latest"] = is_latest

    print(count)
    print(latest_valid)
    return latest_valid