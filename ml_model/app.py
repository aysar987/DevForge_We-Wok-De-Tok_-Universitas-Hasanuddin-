from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS
from urllib.parse import urlparse
from extract_fitur import subdomain_count, calculate_entropy, get_domain_age_days, is_ssl_valid, is_public_hosting
from rule_based import rule_based_check
from check_html_js import get_page_content
from gemini_layer import analyze_phishing_url_gemini
import google.generativeai as genai
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

app = Flask(__name__)
CORS(app)
model = joblib.load('model.pkl')

GEMINI_API_KEY = "AIzaSyDzd0RbY_fjLxz6c4skGyHCDoODMPtwsng"

gemini_model = None


if not GEMINI_API_KEY:
    print("⚠️ Peringatan: Variabel lingkungan GOOGLE_API_KEY tidak ditemukan.")
    print("Fungsi Gemini API mungkin tidak akan bekerja.")
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-2.5-flash')
        print("Gemini AI Model berhasil diinisialisasi.")
    except Exception as e:
        print(f"Error saat inisialisasi Gemini AI Model: {str(e)}")
        gemini_model = None

#Database
uri = "mongodb+srv://Mirai:Mirai1405@cluster0.mh9axhq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["PhishScan"]
collection = db["TesURL"]


def extract_features_from_url(url):
    return [
        len(url),
        int('@' in url),
        int('-' in url),
        int(urlparse(url).scheme == 'https'),
        sum(c.isdigit() for c in url),
        subdomain_count(url),
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
        print(f"Scanning URL: {url}")

        # Layer 1 untuk Rule-Based
        rule_result = rule_based_check(url)
        if rule_result["is_suspicious"]:

            #Insert ke Database untuk Rule-Based
            log_data = {
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "source": "rule-based",
                "suspicion_score": rule_result["suspicion_score"],
                "rule_violations": rule_result["rules_violated"] if rule_result["is_suspicious"] else None,
                "is_phishing": True if rule_result["is_suspicious"] else bool(prediction)
            }
            collection.insert_one(log_data)

            return jsonify({
                "isPhishing": True,
                "source": "rule-based",
                "suspicionScore": rule_result["suspicion_score"],
                "rulesViolated": rule_result["rules_violated"]
            })

        # Layer 2 untuk Machine Learning
        features = np.array([extract_features_from_url(url)])
        prediction = model.predict(features)[0]
        prob = model.predict_proba(features)[0][1]
        
        # Layer 3 untuk Gemini
        if 0.1 <= prob <= 0.6:
            if gemini_model:
                print("Memanggil Gemini AI untuk analisis lebih lanjut (kasus ambigu ML)...")

                result = analyze_phishing_url_gemini(gemini_model, url)
                
                print(f"  Respon Gemini: is_phishing={result.get('is_phishing', 'N/A')}, confidence={result.get('confidence', 'N/A')}")

                #Insert ke Database untuk Gemini
                log_data = {
                    "url": url,
                    "timestamp": datetime.now().isoformat(),
                    "source": "gemini-ai",
                    "ml_score": float(round(prob, 2)),
                    "gemini_confidence": result.get("confidence", "unknown"),
                    "gemini_indicators": result.get("indicators", []),
                    "gemini_advice": result.get("advice", "Tidak tersedia"),
                    "is_phishing": result.get("is_phishing", False)
                }
                collection.insert_one(log_data)

                return jsonify({
                    "isPhishing": result.get("is_phishing", False),
                    "source": "gemini-ai",
                    "confidence": result.get("confidence", "unknown"),
                    "indicators": result.get("indicators", []),
                    "advice": result.get("advice", "Tidak tersedia")
                })
            else:
                print("Gemini AI Model tidak tersedia, melewatkan Layer 3.")
                return jsonify({
                    'isPhishing': bool(prediction),
                    'source': 'ml-model',
                    'predictionScore': float(round(prob, 2)),
                    'message': 'Gemini AI tidak dapat diinisialisasi, hasil dari ML Model.'
                })
        #Insert ke Database untuk machine Learning
        log_data = {
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "source": "ml-model",
                "ml_score": float(round(prob, 2)),
                "is_phishing": bool(prediction)
            }
        collection.insert_one(log_data)
        
        return jsonify({
            'isPhishing': bool(prediction),
            'source': 'ml-model',
            'predictionScore': float(round(prob, 2))
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

    


if __name__ == '__main__':
    app.run(port=5001)
