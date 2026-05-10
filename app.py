from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import re
from src.scripts.scraper import run_apify_scraper
from src.scripts.zynd_agent import process_competitor_prices

app = Flask(__name__, static_folder='src/frontend')
CORS(app)

def sanitize_url(url):
    url = url.strip()
    if not url: return ""
    url = re.sub(r'^https?//:?', 'https://', url)
    url = re.sub(r'^https?:/+', 'https://', url)
    if not url.startswith('http'): url = 'https://' + url
    if 'toscrap' in url and '.com' not in url: url = url.replace('toscrap', 'toscrape.com')
    return url

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/store.html')
def store():
    return send_from_directory(app.static_folder, 'store.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/src/data/<path:path>')
def data_proxy(path):
    return send_from_directory('src/data', path)

@app.route('/assets/<path:path>')
def assets_proxy(path):
    return send_from_directory('src/frontend/assets', path)

@app.route('/api/generate', methods=['POST'])
def generate_store():
    data = request.json
    business_name = data.get('business_name', 'OmniStrike Store')
    raw_url = data.get('target_url', '')
    
    target_url = sanitize_url(raw_url)
    if not target_url:
        return jsonify({"error": "Invalid URL"}), 400
        
    print(f"Generating store for {business_name} using {target_url}")
    
    # Run the existing pipeline logic
    scraped_data = run_apify_scraper(target_url)
    scraped_json = json.dumps(scraped_data)
    
    decision_json = process_competitor_prices(scraped_json)
    
    final_payload = {
        "store_name": business_name,
        "items": json.loads(decision_json)
    }
    
    # Update the data file
    data_path = os.path.join('src', 'data', 'store_data.json')
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    with open(data_path, 'w') as f:
        json.dump(final_payload, f, indent=4)
        
    return jsonify(final_payload)

if __name__ == '__main__':
    print("🚀 OmniStrike Backend starting on http://localhost:5000")
    app.run(port=5000, debug=True)
