# This file contains all the configuration for the Open Gemini Deep Research tool.

# --- User-Specific Information ---
# As provided in user_info.md and corrected by the user.
OBSIDIAN_VAULT_PATH = "/Users/macuser/Documents/ChetasVault"
OBSIDIAN_YAML_USERNAME = "MacUser"

# --- DOM Selectors for Browser Automation ---
# All selectors are based on the user-provided 'user_info.md'.
class Selectors:
    # Gemini General
    GEMINI_CHAT_INPUT = "[contenteditable='true']"
    GEMINI_SUBMIT_BUTTON = "mat-icon[fonticon='send']"
    GEMINI_SHARE_BUTTON = "mat-icon[data-test-id='share-icon']"
    GEMINI_COPY_BUTTON = "span.mat-mdc-list-item-title:has-text('Copy')"

    # Gemini Mode Selectors
    CANVAS_MODE_SELECTOR = "div.label:has-text('Canvas')"
    DEEP_RESEARCH_MODE_SELECTOR = "div.label:has-text('Deep Research')"

    # Gemini Specific Actions
    ADD_FILES_BUTTON = "mat-icon[fonticon='add_2']"
    START_RESEARCH_BUTTON = "span.mdc-button__label:has-text('Start research')"

    # YouTube to Transcript (youtubetotranscript.com)
    YTT_COPY_BUTTON = "span#copy-span"

# --- Research Parameters ---
class Research:
    # Defines the number of concurrent queries for Deep Research
    # as specified in the PRD.
    MAX_CONCURRENT_QUERIES = 3

# --- API & Frontend ---
class API:
    HOST = "127.0.0.1"
    PORT = 8000

# --- Notification Settings ---
# For macOS, osascript is used. For Linux, notify-send would be the equivalent.
# This can be expanded later.
class Notifications:
    # A simple notification command for macOS.
    MACOS_COMMAND = 'osascript -e \'display notification "{}" with title "{}"\''
    DEFAULT_TITLE = "Gemini Research"
