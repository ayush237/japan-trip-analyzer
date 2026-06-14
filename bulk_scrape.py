import json
import requests
from apify_client import ApifyClient

# Get token from mcp_config.json
with open('mcp_config.json', 'r') as f:
    mcp_config = json.load(f)
token = mcp_config['mcpServers']['apify']['headers']['Authorization'].replace('Bearer ', '')

client = ApifyClient(token)

with open('config.json', 'r') as f:
    config = json.load(f)
    urls = config.get("urls", [])

# Read memory to find already processed ones
processed = set()
try:
    with open('.agents/memory.md', 'r') as f:
        for line in f:
            if '| https://' in line and 'Success' in line:
                url = line.split('|')[1].strip()
                processed.add(url)
except FileNotFoundError:
    pass

target_urls = [u for u in urls if u not in processed]
print(f"Found {len(target_urls)} unprocessed URLs.")

if not target_urls:
    print("All URLs processed!")
    exit(0)

# Run the Actor
print("Calling Apify Instagram Scraper for all URLs...")
run_input = {
    "directUrls": target_urls,
    "resultsType": "posts",
}
run = client.actor("apify/instagram-scraper").call(run_input=run_input)

# Fetch results
print("Fetching results...")
scraped_data = []
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    scraped_data.append({
        "url": item.get("url"),
        "caption": item.get("caption", ""),
        "locationName": item.get("locationName", ""),
        "displayUrl": item.get("displayUrl", "")
    })

with open('apify_results.json', 'w') as f:
    json.dump(scraped_data, f, indent=4)
    
print(f"Successfully saved {len(scraped_data)} results to apify_results.json")
