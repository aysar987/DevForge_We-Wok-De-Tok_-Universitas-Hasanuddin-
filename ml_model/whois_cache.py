import json
import os

WHOIS_CACHE_FILE = 'whois_cache.json'

def load_whois_cache():
    """Load Whois cache"""
    if os.path.exists(WHOIS_CACHE_FILE):
        with open(WHOIS_CACHE_FILE, 'r') as file:
            return json.load(file)
    return {}  

def save_whois_cache(cache):
    """Save whois cache"""
    with open(WHOIS_CACHE_FILE, 'w') as file:
        json.dump(cache, file, indent=4)