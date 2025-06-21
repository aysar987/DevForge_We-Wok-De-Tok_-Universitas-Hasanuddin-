import pandas as pd
from urllib.parse import urlparse
from extract_fitur import (
    subdomain_count,
    calculate_entropy,
    get_domain_age_days,
    is_ssl_valid,
    is_public_hosting
)
import os
from datetime import datetime


df = pd.read_excel("data_bal - 20000.xlsx")
df.columns = df.columns.str.strip().str.lower()
urls = df['urls']
labels = df['labels']


start_time = datetime.now()
print(f"Mulai ekstraksi pada: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")


CACHE_FILE = "Cleaned_PhishScan_Features.csv"
if os.path.exists(CACHE_FILE):
    done_df = pd.read_csv(CACHE_FILE)
    done_df.columns = done_df.columns.str.lower()
    done_urls = set(done_df['url'].tolist())
    feature_rows = done_df.to_dict(orient="records")
    print(f"Resume: {len(done_urls)} URL sudah diproses sebelumnya", flush=True)
else:
    done_urls = set()
    feature_rows = []

print("Mulai ekstraksi fitur... (tergantung WHOIS/SSL)\n", flush=True)

#Extract fitur ke csv
for i, url in enumerate(urls):
    if url in done_urls:
        continue

    try:
        label = labels[i] if pd.notna(labels[i]) else 0

        features = {
            'url': url,
            'label': label,
            'urllength': len(url),
            'hasatsymbol': int('@' in url),
            'hashyphen': int('-' in url),
            'hashttps': int(urlparse(url).scheme == 'https'),
            'digitcount': sum(c.isdigit() for c in url),
            'subdomaincount': subdomain_count(url),
            'urlentropy': calculate_entropy(url),
            'domainagedays': get_domain_age_days(url),
            'issslsecure': is_ssl_valid(url),
            'ispublichosting': is_public_hosting(url)
        }

        feature_rows.append(features)

        if len(feature_rows) % 100 == 0:
            pd.DataFrame(feature_rows).to_csv(CACHE_FILE, index=False)
            print(f"{len(feature_rows)} URL tersimpan sementara", flush=True)

    except Exception as e:
        print(f"Gagal ekstrak URL ke-{i}: {url} → {str(e)}", flush=True)


final_df = pd.DataFrame(feature_rows)
final_df.to_csv(CACHE_FILE, index=False)
print("Semua fitur berhasil diekstrak dan disimpan ke Cleaned_PhishScan_Features.csv", flush=True)


expected_columns = ['url', 'label', 'urllength', 'hasatsymbol', 'hashyphen', 'hashttps',
                    'digitcount', 'subdomaincount', 'urlentropy', 'domainagedays', 'issslsecure', 'ispublichosting']
missing_cols = set(expected_columns) - set(final_df.columns)
if missing_cols:
    print(f"WARNING: Ada kolom yang hilang → {missing_cols}")
else:
    print("Kolom lengkap dan sesuai")


end_time = datetime.now()
print(f"Selesai pada: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total waktu proses: {end_time - start_time}")
