import re
import whois
import ssl
import math
from urllib.parse import urlparse
from datetime import datetime
from whois_cache import load_whois_cache, save_whois_cache

def subdomain_count(url):
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split('.')
    return len(domain_parts) - 2 if len(domain_parts) > 2 else 0

def calculate