import requests
from bs4 import BeautifulSoup

def get_page_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        html_content = soup.prettify()
        js_scripts = "\n".join([script.string for script in soup.find_all('script') if script.string])

        return {
            "html": html_content[:5000],  # batasi agar tidak terlalu panjang
            "javascript": js_scripts[:3000]
        }
    except Exception as e:
        return {"error": f"Gagal mengambil halaman: {str(e)}"}
