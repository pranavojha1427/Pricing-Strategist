import json
import os
import time
import requests
import urllib.parse
from hashlib import md5
from dotenv import load_dotenv

load_dotenv()

def get_ai_image_url(product_name):
    # Prompt for Pollinations AI
    encoded_prompt = urllib.parse.quote(f"Professional high-end product photography of {product_name}, studio lighting, 8k, clean background")
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=600&height=400&nologo=true&seed={int(time.time())}"

def save_image_locally(url, product_name):
    """
    Downloads the AI image and saves it to the local assets folder.
    Returns the relative path to the saved image.
    """
    try:
        # Create unique filename based on product name
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', product_name).lower()[:30]
        filename = f"{safe_name}.jpg"
        
        # Paths
        assets_dir = os.path.join('src', 'frontend', 'assets', 'images')
        os.makedirs(assets_dir, exist_ok=True)
        filepath = os.path.join(assets_dir, filename)
        
        # Relative path for frontend
        relative_path = f"/assets/images/{filename}"

        # Download if doesn't exist or force refresh
        print(f"📸 Saving AI Photography: {filename}...")
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return relative_path
    except Exception as e:
        print(f"Error saving image: {e}")
    
    return url # Return original URL as fallback

import re # Ensure re is imported for filename cleaning

def process_competitor_prices(competitor_data_json):
    try:
        competitor_data = json.loads(competitor_data_json)
        decisions = []
        
        for item in competitor_data:
            comp_price = item.get("price", 0)
            product_name = item.get("product_name", "")
            
            # AI Pricing Strategy: 5% Discount
            new_price = int(comp_price * 0.95)
            
            # Generate and SAVE the AI image
            ai_url = get_ai_image_url(product_name)
            local_image_path = save_image_locally(ai_url, product_name)
            
            decisions.append({
                "product_name": product_name,
                "original_price": comp_price,
                "new_price": new_price,
                "discount_applied": "5% OFF",
                "image_url": local_image_path
            })
            
        return json.dumps(decisions, indent=4)
    except Exception as e:
        print(f"Zynd AI Error: {e}")
        return json.dumps([], indent=4)
