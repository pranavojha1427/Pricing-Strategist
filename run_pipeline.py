import json
import os
import sys
import re
from src.scripts.scraper import run_apify_scraper
from src.scripts.zynd_agent import process_competitor_prices

def sanitize_url(url):
    """Fixes common URL typos like https//: or missing protocols"""
    url = url.strip()
    if not url:
        return ""
    
    # Fix common typo https//: to https://
    url = re.sub(r'^https?//:?', 'https://', url)
    url = re.sub(r'^https?:/+', 'https://', url)
    
    # Add protocol if missing
    if not url.startswith('http'):
        url = 'https://' + url
        
    # Fix domain typos (e.g. .toscrap -> .toscrape.com)
    if 'toscrap' in url and '.com' not in url:
        url = url.replace('toscrap', 'toscrape.com')
        
    return url

def main():
    print("========================================")
    print("🤖 OmniStrike Storefront Generator")
    print("========================================\n")
    
    # Get user input for target link
    print("Please provide the target business information:")
    business_name = input("Enter your business name (e.g. The Vintage Bookshop): ").strip()
    raw_url = input("Enter target competitor URL to scrape: ").strip()
    
    target_url = sanitize_url(raw_url)
    if not target_url:
        target_url = "https://books.toscrape.com"
        
    if not business_name:
        business_name = "OmniStrike Store"
    
    print(f"\n✨ Cleaned URL: {target_url}")
    print(f"[1/3] Scraping Competitor Data...")
    
    scraped_data = run_apify_scraper(target_url)
    scraped_json = json.dumps(scraped_data)
    
    print("\n[2/3] Zynd AI applying 5% competitive discount & generating AI Images...")
    decision_json = process_competitor_prices(scraped_json)
    
    if not decision_json:
        print("❌ AI Analysis failed.")
        return

    print("\n[3/3] Assembling Storefront Database...")
    final_payload = {
        "store_name": business_name,
        "items": json.loads(decision_json)
    }
    
    data_path = os.path.join(os.path.dirname(__file__), 'src', 'data', 'store_data.json')
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    
    with open(data_path, 'w') as f:
        json.dump(final_payload, f, indent=4)
        
    print(f"✅ Successfully written to: {data_path}")
    print("\n🚀 Storefront generated! Refresh your browser to view your AI-powered store.")

if __name__ == "__main__":
    main()
