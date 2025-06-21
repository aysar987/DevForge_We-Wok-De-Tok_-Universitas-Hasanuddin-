import json
import os

WHOIS_CACHE_FILE = 'whois_cache.json'

def load_whois_cache():
    """Load the WHOIS cache from a JSON file."""
    if os.path.exists(WHOIS_CACHE_FILE):
        with open(WHOIS_CACHE_FILE, 'r') as file:
            return json.load(file)
    return {}  

def save_whois_cache(cache):
    """Save the WHOIS cache to a JSON file."""
    with open(WHOIS_CACHE_FILE, 'w') as file:
        json.dump(cache, file, indent=4)