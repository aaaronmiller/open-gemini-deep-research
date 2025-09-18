import argparse
import asyncio
import time

from src.deep_research import DeepSearch
from src.browser_automation import BrowserController
from src.output_handler import save_to_obsidian

async def main():
    """
    Main asynchronous function to run the deep research process.
    This script is now a test harness for the refactored backend services.
    """
    parser = argparse.ArgumentParser(description='Run deep search queries using browser automation.')
    parser.add_argument('query', type=str, help='The initial research query.')
    parser.add_argument('--mode', type=str, choices=['fast', 'balanced', 'comprehensive'],
                        default='balanced', help='Research mode (default: balanced)')

    args = parser.parse_args()

    start_time = time.time()

    # Use the BrowserController to handle all web interactions
    async with BrowserController() as browser_controller:
        # Initialize the browser and navigate to Gemini
        await browser_controller.navigate_to_gemini()

        # Instantiate DeepSearch with the browser controller
        deep_search = DeepSearch(browser_controller, mode=args.mode)

        # Determine research parameters (simplified in the new version)
        breadth_and_depth = deep_search.determine_research_breadth_and_depth(args.query)
        breadth = breadth_and_depth["breadth"]
        depth = breadth_and_depth["depth"]
        print(f"Research Parameters: Breadth={breadth}, Depth={depth}")

        # For this test harness, we skip the interactive follow-up questions.
        # The UI will handle this in the final application.
        combined_query = args.query
        print(f"Starting research for: '{combined_query}'")

        # Run the deep research process
        results = await deep_search.deep_research(
            query=combined_query,
            breadth=breadth,
            depth=depth
        )

        # Generate the final report
        final_report = await deep_search.generate_final_report(
            query=combined_query,
            learnings=results["learnings"]
        )

        # Save the final report to the Obsidian vault
        save_to_obsidian(
            query=combined_query,
            report_content=final_report,
            sources=list(results["visited_urls"].values()),
            summary=f"A report on {combined_query} based on {len(results['learnings'])} learnings."
        )

    # Calculate and print elapsed time
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"\nTotal research time: {minutes} minutes and {seconds} seconds")

if __name__ == "__main__":
    # Run the main async function
    asyncio.run(main())
            