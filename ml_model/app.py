from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS
from urllib.parse import urlparse
from feature_extractor import get_subdomain_count, calculate_entropy, get_domain_age_days, is_ssl_valid
from rule_based import rule_based_check
from deepseek_layer import analyze_phishing_url  # pastikan file ini ada

app = Flask(__name__)
CORS(app)
model = joblib.load('model.pkl')

# 🔐 Tambahkan API Key Anda di sini
DEEPSEEK_API_KEY = "sk-00d33e105ea14389a67862430fd3a178"

def extract_features_from_url(url):
    return [
        len(url),
        int('@' in url),
        int('-' in url),
        int(urlparse(url).scheme == 'https'),
        sum(c.isdigit() for c in url),
        get_subdomain_count(url),
        calculate_entropy(url),
        get_domain_age_days(url),
        is_ssl_valid(url)
    ]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'Missing "url" in request body'}), 400

        url = data['url']
        print(f"🔍 Scanning URL: {url}")

        # Layer 1 - Rule-Based
        rule_result = rule_based_check(url)
        if rule_result["is_suspicious"]:
            return jsonify({
                "isPhishing": True,
                "source": "rule-based",
                "suspicionScore": rule_result["suspicion_score"],
                "rulesViolated": rule_result["rules_violated"]
            })

        # Layer 2 - Machine Learning
        features = np.array([extract_features_from_url(url)])
        prediction = model.predict(features)[0]
        prob = model.predict_proba(features)[0][1]

        if 0.4 <= prob <= 0.6:
            # Layer 3 - DeepSeek AI (only for ambiguous cases)
            result = analyze_phishing_url(DEEPSEEK_API_KEY, url)
            return jsonify({
                "isPhishing": result.get("is_phishing", False),
                "source": "deepseek",
                "confidence": result.get("confidence", "unknown"),
                "indicators": result.get("indicators", []),
                "advice": result.get("advice", "Tidak tersedia")
            })

        # Kembalikan hasil ML jika confidence tinggi/rendah
        return jsonify({
            'isPhishing': bool(prediction),
            'source': 'ml-model',
            'predictionScore': float(round(prob, 2))
        })

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
