import json
import google.generativeai as genai

def analyze_phishing_url_gemini(model: genai.GenerativeModel, url: str) -> dict:
    """
    Menganalisis URL phishing menggunakan Gemini API berdasarkan struktur URL.
    Menerima objek model Gemini yang sudah dikonfigurasi sebelumnya (dari app.py).
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    prompt = f"""
    Anda adalah seorang ahli keamanan siber. Tugas Anda adalah menganalisis apakah URL berikut merupakan URL phishing atau bukan, hanya berdasarkan strukturnya (tanpa mengakses kontennya).
    Analisislah URL berikut:
    URL: {url}

    Gunakan indikator berikut sebagai referensi:
    1. **Simbol '@'** dalam URL, yang dapat menyembunyikan domain asli.
    2. **Jumlah subdomain berlebih**, misalnya 'secure.login.bank.com.phishing.tk'.
    3. **Penggunaan karakter non-standar atau menyerupai** (seperti ħ, ĸ, і, l vs 1).
    4. **TLD (Top-Level Domain)** yang umum dipakai phishing: .tk, .xyz, .buzz, .gq, .ml.
    5. **Panjang URL tidak wajar** (di atas 75 karakter bisa mencurigakan).
    6. **Banyaknya angka** dalam URL (digit count sangat tinggi bisa mencurigakan).
    7. **Penggunaan kata kunci umum phishing**, seperti: 'login', 'verify', 'secure', 'account', 'update', 'signin', 'webscr', 'authentication'.
    8. **Entropy tinggi**, yaitu kompleksitas karakter URL yang tidak biasa.
    9. **Domain baru didaftarkan (<7 hari)** menurut WHOIS info.
    10. **Tidak menggunakan HTTPS atau sertifikat SSL tidak valid.**
    11. **Hosting publik** yang dimana biasa digunakan untuk url phishing seperti Firebase, GitHub Pages, Heroku, Glitch, dll.

    Tentukan apakah URL tersebut mencurigakan sebagai phishing berdasarkan indikator di atas serta analisislah kemungkinan lain yang mencurigakan.

    Berikan hasil Anda dalam format JSON yang valid dan lengkap seperti berikut:
    {{
    "is_phishing": true/false,
    "confidence": "tinggi/sedang/rendah",
    "indicators": ["indikator1", "indikator2", "..."],
    "advice": "saran keamanan atau rekomendasi"
    }}
    Pastikan output adalah JSON murni, tanpa teks tambahan atau format lain di luar blok JSON.
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[len("```json"):].strip()
        if response_text.endswith("```"):
            response_text = response_text[:-len("```")].strip()

        try:
            parsed_json = json.loads(response_text)
            return parsed_json
        except json.JSONDecodeError as e:
            return {
                "is_phishing": False,
                "confidence": "gagal_parse",
                "indicators": [],
                "advice": f"Gemini mengembalikan teks yang tidak bisa di-parse sebagai JSON: {response_text[:200]}... Error: {str(e)}"
            }
    except Exception as e:
        return {
            "is_phishing": False,
            "confidence": "error",
            "indicators": [],
            "advice": f"Terjadi error saat berkomunikasi dengan Gemini API: {str(e)}"
        }

if __name__ == "__main__":
    import os
    print("--- Detektor URL Phishing dengan Gemini AI (Modul Tes Mandiri) ---")
    print("Modul ini dirancang untuk diimpor oleh app.py.")

    api_key_test = os.environ.get("GOOGLE_API_KEY")

    if not api_key_test:
        print("\nERROR: Variabel lingkungan 'GOOGLE_API_KEY' tidak ditemukan.")
        print("Silakan atur variabel ini untuk menjalankan tes mandiri.")
        exit()

    try:
        genai.configure(api_key=api_key_test)
        test_model = genai.GenerativeModel('gemini-1.5-flash')
        print("Gemini API berhasil dikonfigurasi untuk tes mandiri.")
    except Exception as e:
        print(f"ERROR: Gagal menginisialisasi Gemini API untuk tes mandiri: {str(e)}")
        exit()

    while True:
        user_input_url = input("\nMasukkan URL untuk dianalisis (ketik 'exit' untuk keluar): ")

        if user_input_url.lower() == 'exit':
            print("Selesai tes mandiri.")
            break

        if not user_input_url:
            print("URL tidak boleh kosong. Silakan masukkan URL yang valid.")
            continue

        print(f"\nMenganalisis URL: {user_input_url}")
        
        analysis_result = analyze_phishing_url_gemini(test_model, user_input_url)
        
        print("\n--- Hasil Analisis ---")
        if analysis_result["is_phishing"]:
            print("Status: KEMUNGKINAN PHISHING")
        else:
            print("Status: MUNGKIN AMAN (atau Tidak Terdeteksi Phishing)")
        
        print(f"Tingkat Keyakinan: {analysis_result['confidence'].upper()}")
        
        if analysis_result["indicators"]:
            print("Indikator Ditemukan:")
            for indicator in analysis_result["indicators"]:
                print(f"- {indicator}")
        else:
            print("Tidak ada indikator spesifik yang ditemukan.")

        print(f"\nSaran Keamanan: {analysis_result['advice']}")
        print("-" * 50)