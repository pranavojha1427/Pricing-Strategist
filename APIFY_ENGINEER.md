# 🛠️ Member 1: The Data Engineer
**Mission:** Autonomous Market Intelligence & Data Ingestion

## 📋 Overview
The Data Engineer is responsible for the first stage of the OmniStrike pipeline. This role ensures that raw HTML from any business website is converted into a structured, clean JSON format that the AI can understand.

## 🚀 Implementation Strategy
- **Tooling:** Python, BeautifulSoup4, Requests, and Apify SDK.
- **Direct Scraping:** Uses a high-speed `requests` engine to pull data directly from target URLs, bypassing cloud delays.
- **Precision Extraction:** Implements a "Smart Attribute Hunter" that extracts full product names from HTML `title` and `alt` attributes to avoid truncated text.
- **Resilient Fallback:** If a site is heavily protected, the engineer has a built-in domain-aware fallback that generates relevant mock data based on the business name.

## 📂 Key Outputs
- `src/scripts/scraper.py`: The core extraction engine.
- `JSON Payload`: `{"product_name": string, "price": integer}`
