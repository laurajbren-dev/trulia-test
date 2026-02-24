from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Trulia scrape test is running. Go to /test"

@app.route("/test")
def test_scrape():
    url = "https://www.trulia.com/home/715-e-4th-ave-denver-co-80203-13346848"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        has_jsonld = "application/ld+json" in r.text
        has_og = "og:title" in r.text
        price = ""
        beds = ""
        import re
        m = re.search(r'\$[\d,]+', r.text)
        if m:
            price = m.group(0)
        m2 = re.search(r'(\d+)\s*(?:bed|bd)', r.text, re.IGNORECASE)
        if m2:
            beds = m2.group(1)
        return jsonify({
            "status_code": r.status_code,
            "page_length": len(r.text),
            "has_jsonld": has_jsonld,
            "has_og_title": has_og,
            "found_price": price,
            "found_beds": beds,
            "blocked": "captcha" in r.text.lower() or "access denied" in r.text.lower()
        })
    except Exception as e:
        return jsonify({"error": str(e)})
