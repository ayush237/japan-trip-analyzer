This file captures the setup requirements and dependencies needed for your environment.
Project Requirements: Instagram Reel Analyzer Pipeline
Core Dependencies
•	Google Antigravity SDK: The Python framework to build and run the autonomous agents (pip install google-antigravity).
•	Google GenAI SDK: Required for uploading the scraped video to the Gemini File API (pip install google-genai).
•	Playwright: Required for extracting URLs from user's Instagram Saved folder (pip install playwright).
MCP Servers
•	Apify MCP Server: Required to securely scrape Instagram without manual authentication. The server URL is https://mcp.apify.com.
Environment Variables & Credentials
•	GEMINI_API_KEY: For Gemini multimodal video analysis.
•	APIFY_TOKEN: Required for the Apify MCP server to run the Instagram Reel Scraper.
Expected Output
An HTML file (final_spots_table.html) styled with a dark navy blue header titled "Bonus Offbeat Spots & Alternatives", containing the following columns: Spot Name, Location, Description, Booking & Access, Distance / Transit, Timing / Hours, and Original Reel Link.