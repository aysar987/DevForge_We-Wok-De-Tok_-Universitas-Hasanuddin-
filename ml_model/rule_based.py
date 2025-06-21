from urllib.parse import urlparse
import re
from extract_fitur import get_domain_age_days

PHISHING_KEYWORDS = ["login", "secure", "update", "account", "verify", "bank", "signin", "webscr", "ebayisapi", "paypal"]

SUSPICIOUS_TLDS = [".xyz", ".top", ".gq", ".ml", ".tk", ".cf", ".ga", ".click", ".link", ".sbs"]

NEW_DOMAIN_DAYS_THRESHOLD = 7

def rule_based_check(url):
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    tld = "." + hostname.split(".")[-1] if "." in hostname else ""

    domain_age = get_domain_age_days(url)
    domain_is_new = domain_age != -1 and domain_age <= NEW_DOMAIN_DAYS_THRESHOLD

    rules = {
        "has_at_symbol": {
            "triggered": "@" in url,
            "description": "URL contains '@' which can obscure the real link"
        },
        "has_ip_address": {
            "triggered": bool(re.match(r"^http[s]?://(\d{1,3}\.){3}\d{1,3}", url)),
            "description": "URL uses IP address instead of domain"
        },
        "is_http": {
            "triggered": parsed.scheme == "http",
            "description": "URL does not use secure HTTPS protocol"
        },
        "has_long_url": {
            "triggered": len(url) > 75,
            "description": "URL is unusually long (> 75 characters)"
        },
        "has_many_subdomains": {
            "triggered": hostname.count(".") > 2,
            "description": "URL has multiple subdomains which may indicate obfuscation"
        },
        "contains_phishing_keywords": {
            "triggered": any(keyword in url.lower() for keyword in PHISHING_KEYWORDS),
            "description": "URL contains common phishing-related keywords"
        },
        "suspicious_tld": {
            "triggered": tld.lower() in SUSPICIOUS_TLDS,
            "description": f"TLD ({tld}) is known for being used in phishing domains"
        },
        "newly_registered_domain": {
            "triggered": domain_is_new,
            "description": f"Domain was registered recently ({domain_age} days ago)"
        }
    }

    # Ambil semua rules yang terpenuhi
    violated = {k: v["description"] for k, v in rules.items() if v["triggered"]}
    score = len(violated)
    is_suspicious = score >= 2 

    return {
        "rules_violated": violated,
        "suspicion_score": score,
        "is_suspicious": is_suspicious
    }
