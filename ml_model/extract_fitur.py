import re
import whois
import ssl
import socket
import math
from urllib.parse import urlparse
from datetime import datetime
from whois_cache import load_whois_cache, save_whois_cache

def subdomain_count(url):
    try:
        hostname = urlparse(url).hostname
        if hostname is None:
            return 0
        return hostname.count('.') - 1
    except Exception:
        return 0

def calculate_entropy(s):
    try:
        prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
        entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
        return round(entropy, 3)
    except Exception:
        return 0.0

whois_cache = load_whois_cache()

def get_domain_age_days(url):
    try:
        domain = urlparse(url).netloc
        if not domain:
            return -1

        if domain in whois_cache:
            w = whois_cache[domain]
        else:
            w_raw = whois.whois(domain)
            w = {
                "creation_date": str(w_raw.creation_date[0] if isinstance(w_raw.creation_date, list) else w_raw.creation_date)
            }
            whois_cache[domain] = w
            save_whois_cache(whois_cache)

        creation_str = w.get("creation_date")
        if not creation_str:
            return -1
        creation_date = datetime.fromisoformat(creation_str)
        return (datetime.now() - creation_date).days

    except Exception:
        return -1

def is_ssl_valid(url):
    try:
        hostname = urlparse(url).hostname
        if hostname is None:
            return 0

        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssock.getpeercert()
                return 1
    except Exception:
        return 0

PUBLIC_HOSTINGS = [
    "pages.dev", "web.app", "github.io", "herokuapp.com", "glitch.me", "firebaseapp.com", "000webhostapp.com",
    "netlify.app", "surge.sh", "githubusercontent.com", "repl.co", "replit.app", "fly.dev", "render.com"
]

def is_public_hosting(url):
    hostname = urlparse(url).hostname or ""
    return int(any(hosting in hostname for hosting in PUBLIC_HOSTINGS))