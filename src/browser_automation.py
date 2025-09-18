import asyncio
from playwright.async_api import async_playwright, Browser, Page, Playwright
from .config import Selectors, API  # Assuming config is in the same directory

class BrowserController:
    """
    Manages browser automation tasks using Playwright for interacting with
    Gemini and other web services as required by the PRD.
    """

    def __init__(self):
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.page: Page | None = None

    async def __aenter__(self):
        """Initializes Playwright and launches the browser."""
        self.playwright = await async_playwright().start()
        # Using Chromium as specified in the PRD. Headless=False for debugging, can be True for production.
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Closes the browser and stops Playwright."""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def navigate_to_gemini(self):
        """Navigates to the Gemini website."""
        if not self.page:
            raise ConnectionError("Browser is not running. Call within an async with block.")
        await self.page.goto("https://gemini.google.com")
        # Add a small delay to ensure the page loads, especially the complex JS UI
        await asyncio.sleep(3)

    async def send_prompt(self, prompt: str):
        """Types a prompt into the chat input and submits it."""
        if not self.page:
            raise ConnectionError("Browser is not running.")

        print(f"Sending prompt: {prompt[:100]}...")
        await self.page.fill(Selectors.GEMINI_CHAT_INPUT, prompt)
        await self.page.click(Selectors.GEMINI_SUBMIT_BUTTON)
        # Wait for the response to start generating. This is tricky,
        # as there's no perfect selector. We'll wait for the submit button to be re-enabled.
        # For now, a short, fixed delay is a pragmatic choice.
        await asyncio.sleep(5)
        print("Prompt sent.")

    async def copy_last_response(self) -> str:
        """Copies the last response from Gemini to the clipboard and returns it."""
        if not self.page:
            raise ConnectionError("Browser is not running.")

        print("Copying last response...")
        # This might require a more complex sequence, e.g., finding the last response block.
        # The PRD gives a general "Copy" button selector. Let's assume it copies the latest one.
        # The user might need to click the 'Share and Export' icon first.
        await self.page.click(Selectors.GEMINI_SHARE_BUTTON)
        await asyncio.sleep(1) # Wait for menu to appear
        await self.page.click(Selectors.GEMINI_COPY_BUTTON)

        # Now, read from clipboard. Note: This requires clipboard permissions to be granted in the browser context.
        clipboard_content = await self.page.evaluate("navigator.clipboard.readText()")
        print("Response copied.")
        return clipboard_content

    async def switch_to_deep_research(self):
        """Switches the research mode to 'Deep Research'."""
        if not self.page:
            raise ConnectionError("Browser is not running.")
        print("Switching to Deep Research mode...")
        await self.page.click(Selectors.DEEP_RESEARCH_MODE_SELECTOR)
        await asyncio.sleep(1)
        print("Mode switched.")

    async def switch_to_canvas(self):
        """Switches the research mode to 'Canvas'."""
        if not self.page:
            raise ConnectionError("Browser is not running.")
        print("Switching to Canvas mode...")
        await self.page.click(Selectors.CANVAS_MODE_SELECTOR)
        await asyncio.sleep(1)
        print("Mode switched.")

    async def get_youtube_transcript(self, url: str) -> str:
        """Navigates to youtubetotranscript.com and extracts the transcript."""
        if not self.page:
            raise ConnectionError("Browser is not running.")

        print(f"Getting transcript for {url}...")
        # Basic parsing of video ID from URL
        video_id = ""
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        else:
            raise ValueError("Invalid YouTube URL format.")

        transcript_url = f"https://youtubetotranscript.com/transcript?v={video_id}"

        await self.page.goto(transcript_url)
        await asyncio.sleep(3) # Wait for page to load and transcript to appear

        # Click the copy button provided in the PRD
        await self.page.click(Selectors.YTT_COPY_BUTTON)

        # Get content from clipboard
        transcript = await self.page.evaluate("navigator.clipboard.readText()")
        print("Transcript retrieved.")
        return transcript
