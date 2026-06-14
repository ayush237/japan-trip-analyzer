import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    print("Starting Instagram Saved Reels Extractor...")
    async with async_playwright() as p:
        # Launch browser in non-headless mode so the user can interact
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto('https://www.instagram.com/')
        print("\n*** ACTION REQUIRED ***")
        print("1. Please log in to your Instagram account in the browser window.")
        print("2. Navigate to your 'Saved' folder and open the specific collection containing your Reels.")
        input("\nPress Enter here when you are ready for the script to auto-scroll and extract...")
        
        print("\nAuto-scrolling and extracting URLs... (Do not touch the mouse/keyboard)")
        reel_urls = set()
        
        # Instagram sometimes scrolls a specific container, but generally window scrolling works.
        last_height = await page.evaluate("document.body.scrollHeight")
        
        while True:
            # Get links currently in DOM
            links = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('a')).map(a => a.href);
            }''')
            
            for link in links:
                if '/reel/' in link or '/p/' in link:
                    base_url = link.split('?')[0]
                    reel_urls.add(base_url)
            
            print(f"Collected {len(reel_urls)} unique URLs so far...")
            
            # Scroll down
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000) # Wait for network requests/lazy loading
            
            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                # Try one more time to be safe
                await page.wait_for_timeout(3000)
                new_height = await page.evaluate("document.body.scrollHeight")
                if new_height == last_height:
                    print("Reached the bottom of the folder!")
                    break
            last_height = new_height
                
        urls_list = list(reel_urls)
        print(f"\nFinished! Found {len(urls_list)} unique Reel/Post URLs.")
        if len(urls_list) == 0:
            print("No URLs found. Make sure you are on the correct page.")
        else:
            # Save to config.json
            with open('config.json', 'w') as f:
                json.dump({"urls": urls_list}, f, indent=4)
            print("Successfully saved all URLs to config.json!")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
