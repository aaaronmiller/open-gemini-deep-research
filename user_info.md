date: 2025-09-17 15:42:00 PDT
ver: 1.0.0
author: lil-gimpy
model: perplexity-llm-2025-09
tags: [dom, selectors, user-info, gemini, configuration, html-ui, open-gemini-deep-research, integration, context]
***

## **All User-Specific DOM and Structural Information for open-gemini-deep-research Enhancement**

***

### **A. DOM Selectors for Automation (Gemini/Deep Research/Canvas/YTT)**

- **Gemini Generic Chat/Prompt Input:**
  `[contenteditable='true']`

- **Gemini Canvas Mode Selector:**
  `div.label:has-text("Canvas")`

- **Gemini Deep Research Selector:**
  `div.label:has-text("Deep Research")`

- **Gemini Add Files Button (attachment):**
  `mat-icon[fonticon="add_2"]`

- **Gemini Submit/Send Query:**
  `mat-icon[fonticon="send"]`

- **Gemini Start Research (after 15s):**
  `span.mdc-button__label:has-text("Start research")`

- **Gemini Copy to Clipboard (output):**
  `span.mat-mdc-list-item-title:has-text("Copy")`

- **Gemini Share Button (for copy/export):**
  `mat-icon[data-test-id="share-icon"]`

- **YTT Transcript “Copy” Button:**
  `span#copy-span`
  (For [youtubetotranscript.com/transcript](https://youtubetotranscript.com/transcript?v=YOUTUBE_ID))

***

### **B. User-Specific & System Information**

- **Obsidian vault path:**
  `~/documents/ChetaValut`
- **Obsidian YAML username:**
  `MacUser`
- **Gemini Canvas and Deep Research should be accessed via browser automation, not API, to maximize context windows and artifact handling.
- **Execution Environment:**
  - Local macOS, root available, Playwright and Python
  - Chrome/Chromium and VSCode/devcontainer supported
- **Notification system:**
  - Use `osascript`/`notify-send` or in-app JS popups
- **Response/Job Tagging:**
  - Every copied output gets a tag (from selection button or artifact source, mapped in HTML wrapper/start page for reference/error/history)
- **Pause/Queue Management:**
  - Workflow should respect 3-at-a-time limits for Deep Research, queue remaining, and handle delays
- **Start triggers:**
  - YT→Transcript can trigger from Chrome extension or local HTML interface; bulk jobs from HTML input
- **Output and error versioning:**
  - All agentic/canvas/Deep Research responses should be buffered with query UUID, batch, and timestamp

***

### **C. Not Yet in PRD (Additional Context)**

- **Content.js/background.js/ai-vault-mover.js provided:**
  - For Chrome extension integration, file move/watcher, and background artifact handling
- **HTML frontend to enable launch, query labeling, workflow selection:**
  - Plan to use/extend [fdarkaou/open-deep-research](https://github.com/fdarkaou/open-deep-research) HTML wrapper if further UI required
- **Sample prompts and prompt templates:**
  - (See earlier: 7-point Gemini instructions, YAML summary requests, etc.)
- **Research mode options**:
  - Should honor fast / balanced / comprehensive pipeline parameters

***

### **D. To Get Started**

- Map all selectors and config values to a single Python/config file for easy scripting and selector upgrades
- Generalize input for tag/UI-origin labeling for output files/artifacts
- Initialize error logger and notification channel in every agentic step
- Plumb Obsidian YAML generator/template as function or Jinja2 block for markdown output

***

**If any DOM selector changes (UI update or localization), update the config and rerun Pip/Playwright install.
All major workflow and context needs are above—Juules can start with this as their selector/config “Rosetta Stone.”**
