import asyncio
from google.antigravity import Agent, LocalAgentConfig

async def main():
    # Antigravity reads AGENTS.md and.agents/rules/ automatically from the local workspace
    config = LocalAgentConfig() 
    
    async with Agent(config) as agent:
        # Define the target reel
        target_url = "https://www.instagram.com/reel/YOUR_REEL_ID/"
        
        print(f"Starting analysis for: {target_url}")
        
        # Trigger the orchestrator defined in AGENTS.md
        prompt = f"Execute the Reel Analysis Pipeline outlined in AGENTS.md for this URL: {target_url}"
        response = await agent.chat(prompt)
        
        print("\nPipeline Complete. Check the generated final_spots_table.html file.")
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())