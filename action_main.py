import os
import sys
import json
import re
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup

def main():
    issue_body = os.environ.get("ISSUE_BODY", "")
    # Extract URL from issue body
    url_match = re.search(r'(https://www\.instagram\.com/reel/[\w-]+/?|https://www\.instagram\.com/p/[\w-]+/?)', issue_body)
    if not url_match:
        print("No valid Instagram URL found in the issue body.")
        sys.exit(1)
        
    target_url = url_match.group(1)
    print(f"Analyzing URL: {target_url}")
    
    apify_token = os.environ.get("APIFY_API_TOKEN")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    
    if not apify_token or not gemini_key:
        print("Missing API tokens in Secrets!")
        sys.exit(1)
        
    # 1. Scrape with Apify
    apify_url = f"https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync-get-dataset-items?token={apify_token}"
    payload = {"directUrls": [target_url], "resultsType": "details"}
    print("Calling Apify...")
    resp = requests.post(apify_url, json=payload)
    if resp.status_code != 200 and resp.status_code != 201:
        print(f"Apify Error: {resp.text}")
        sys.exit(1)
        
    data = resp.json()
    if not data:
        print("No data returned from Apify.")
        sys.exit(1)
        
    item = data[0]
    caption = item.get("caption", "")
    video_url = item.get("videoUrl", "")
    
    if not video_url:
        print("No video URL found.")
        sys.exit(1)
        
    # Download video
    print("Downloading video...")
    vid_resp = requests.get(video_url)
    with open("temp_vid.mp4", "wb") as f:
        f.write(vid_resp.content)
        
    # 2. Analyze with Gemini
    print("Analyzing with Gemini...")
    genai.configure(api_key=gemini_key)
    video_file = genai.upload_file(path="temp_vid.mp4")
    
    # Wait for processing
    import time
    while video_file.state.name == "PROCESSING":
        time.sleep(2)
        video_file = genai.get_file(video_file.name)
        
    prompt = f"""
    Analyze this Instagram Reel video and its caption.
    Caption: {caption}
    
    Extract the following details as a JSON object:
    {{
        "spot_name": "Name of the place/activity",
        "location": "Location (City, Area)",
        "description": "Short description of what makes it offbeat",
        "booking_access": "How to book or enter, pricing",
        "distance_transit": "Distance/Transit info",
        "timing_hours": "Opening hours or best timing",
        "highlights_romantic": "Why it's romantic or special",
        "deep_dive_facts": "Any historical or interesting facts",
        "deep_dive_special_notes": "Etiquette, dress code, warnings",
        "deep_dive_links": "Official website URL or 'N/A'"
    }}
    Return ONLY valid JSON.
    """
    
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    result = model.generate_content([video_file, prompt])
    
    json_text = result.text.strip()
    if json_text.startswith("```json"):
        json_text = json_text[7:-3].strip()
    elif json_text.startswith("```"):
        json_text = json_text[3:-3].strip()
        
    try:
        spot_data = json.loads(json_text)
    except Exception as e:
        print("Failed to parse JSON:", json_text)
        sys.exit(1)
        
    # 3. Add to index.html
    html_file = "index.html"
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    tbody = soup.find('tbody')
    if not tbody:
        print("Could not find tbody in index.html")
        sys.exit(1)
        
    # Determine the next row id
    existing_rows = soup.find_all('tr', class_='main-row')
    new_id = len(existing_rows)
    
    main_row_html = f"""
<tr class="main-row" onclick="toggleDetails('row-{new_id}')">
<td data-label="Spot Name"><strong>{spot_data.get('spot_name', '')}</strong></td>
<td data-label="Location">{spot_data.get('location', '')}</td>
<td data-label="Description">{spot_data.get('description', '')}</td>
<td data-label="Booking &amp; Access">{spot_data.get('booking_access', '')}</td>
<td data-label="Distance / Transit">{spot_data.get('distance_transit', '')}</td>
<td data-label="Timing / Hours">{spot_data.get('timing_hours', '')}</td>
<td data-label="Highlights &amp; Romantic Features">{spot_data.get('highlights_romantic', '')}</td>
<td data-label="Original Reel Link"><a href="{target_url}" target="_blank">View Reel</a></td>
</tr>
    """
    
    link_html = f'<a href="{spot_data.get("deep_dive_links", "")}" target="_blank">Official Link / More Info</a>' if spot_data.get("deep_dive_links") and spot_data.get("deep_dive_links") != "N/A" else "N/A"
    details_row_html = f"""
<tr class="details-row hidden" id="row-{new_id}"><td colspan="8"><div class="expanded-card"><h4>Deep Dive</h4><p><strong>Facts: </strong>{spot_data.get('deep_dive_facts', '')}</p><p><strong>Special Notes: </strong>{spot_data.get('deep_dive_special_notes', '')}</p><p><strong>Reference Links: </strong>{link_html}</p></div></td></tr>
    """
    
    main_soup = BeautifulSoup(main_row_html, 'html.parser')
    details_soup = BeautifulSoup(details_row_html, 'html.parser')
    
    tbody.insert(0, details_soup)
    tbody.insert(0, main_soup)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print("Successfully added new row to index.html")
    
if __name__ == "__main__":
    main()
