import json
import requests
from apify_client import ApifyClient
import os

# Get token from mcp_config.json
with open('mcp_config.json', 'r') as f:
    mcp_config = json.load(f)
token = mcp_config['mcpServers']['apify']['headers']['Authorization'].replace('Bearer ', '')

client = ApifyClient(token)

with open('config.json', 'r') as f:
    config = json.load(f)
    urls = config.get("urls", [])

if not urls:
    print("No URLs found in config.json")
    exit(1)

# Just process the first one for now
target_url = urls[0]
print(f"Scraping: {target_url}")

run_input = {
    "directUrls": [target_url],
    "resultsType": "posts",
    "searchType": "hashtag",
    "searchLimit": 1
}

# Run the Actor
print("Calling Apify Instagram Scraper...")
run = client.actor("apify/instagram-scraper").call(run_input=run_input)

# Fetch results
print("Fetching results...")
found = False
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    video_url = item.get("videoUrl")
    caption = item.get("caption", "")
    
    if video_url:
        print(f"Found video URL. Downloading...")
        r = requests.get(video_url)
        with open('temp_reel.mp4', 'wb') as f:
            f.write(r.content)
        
        with open('temp_caption.txt', 'w') as f:
            f.write(caption)
            
        print("Successfully downloaded temp_reel.mp4 and temp_caption.txt")
        found = True
        break

if not found:
    print("Failed to find video URL in the scraped data.")
