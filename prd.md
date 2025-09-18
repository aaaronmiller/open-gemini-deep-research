date: 2025-09-17 15:40:00 PDT
ver: 1.0.0
author: lil-gimpy
model: perplexity-llm-2025-09
tags: [prd, gemini, open-gemini-deep-research, html-wrapper, automation, browser-automation, multi-agent, obsidian, dom, workflow, ai]
***

# Product Requirements Document (PRD):
## **Open Gemini Deep Research — HTML Wrapper and Agentic Automation**
**Repo:** https://github.com/aaaronmiller/open-gemini-deep-research
**For:** Juules (primary dev implementer)

***

## **1. Project Goal**

Create a robust, extensible research assistant (standalone and orchestrated) that leverages Gemini’s **Deep Research** and **Canvas** web interfaces, supports bulk and batch research workflows, and natively integrates with Obsidian vaults and YT-to-transcript flows.
This upgrade should add a modern HTML UI wrapper, new agentic workflow logic, browser DOM automation, persistent log/history, notifications, and extra artifact/export handling.

***

## **2. Key Features & Functional Requirements**

### **A. User Interface (Frontend/HTML Shell)**
- **Modern HTML/JS UI** (Next.js, shadcn/ui, or basic Flask/React accepted)
  - Input box for queries & batch mode (list of YouTube URLs, research prompts, etc.)
  - Research mode/agent selection toggle (Canvas, Deep Research, Multi-agent, YouTube→Transcript)
  - Display queue/batch status: live query/phase, clear tracking per job/tag/version
  - Action buttons: Start, Pause, Cancel, Export, Download outputs/artifacts
  - Notifications:
    - On phase complete or error (desktop/os/JS)
    - Log extract/last status as in-app popup or banner
  - Version, license, and “Powered by Gemini, forked from eRuaro” footer

### **B. Research Pipeline Logic (Backend & Automation)**
- **Incorporate/maintain core capabilities of original eRuaro pipeline:**
  - Multi-step deep research (fast/balanced/comprehensive), concurrent queries (max 3 at once for Deep Research)
  - Branching research tree with UUID tagging, error recovery, and YAML/markdown output
  - Progress logging, retry logic, and full query/result audit log
  - Output in Markdown with prefilled YAML frontmatter (title, ai_summary, ai_sources, username, generator/version, etc.)
  - Research artifact buffer: store output for each query with tag for error tracking/versioning

- **DOM Automation for Gemini/Canvas:**
  - Playwright/Puppeteer-backed browser robot using provided selectors:
    - Model and mode selectors (“Canvas”, “Deep Research”), Input selectors (contenteditable, textareas)
    - Submit, Add File, Start Research, and Copy result selectors
    - Obsidian artifact handoff via file or Obsidian URI
    - YT-transcript pathway via copy button selector
  - Pause/sleep between batch jobs; retry/failover for rate/batch caps
  - Notification (notify-send, osascript, or JS popover) for completion/error

- **YT-to-Transcript Path:**
  - Chrome extension or headless Playwright integration for single/bulk URL conversion
  - Annotate/capture source and expected result per job, with error log if output absent

- **Extensibility/Modularity:**
  - Robust config for all selectors
  - Pluggable agent list: add new AI endpoints or agents for future expansion
  - Plugin point or slot to support non-text artifacts (images, tables, zipped source), with placeholder UI/notes for when this is toggled on

### **C. Output Handling**
- Obsidian integration: Create/import .md in `~/documents/ChetaValut`; ensure title, frontmatter, YAML parsing is honored by Obsidian plugins
- Retain job/phase tags and query associations in artifact name or inside YAML (for trace/debug)
- Option to “attach” all artifact HTML sources in YAML or as sidecar files

### **D. Operational & Non-Functional**
- Error logging and job versioning, both console and as persistent file store (JSON/MD)
- User/passphrase and API key config for Gemini (as in repo .env)
- Docker/devcontainer support maintained
- Accessible/configurable to non-root Linux/macOS users (Python 3.9+, Chrome/Chromium)

***

## **3. Advanced/Optional Features**

- Research tree/state visualization (as JSON, collapsible in UI)
- RBAC/user switching for long-running agentic jobs
- Export/Import state and config as YAML, JSON, Markdown (for backup/restore)
- Scheduled jobs/automation triggers (for n8n, Zapier, cron-based workflows)

***

## **4. Deliverables and Success Criteria**

- Clean, documented HTML (Next.js or Flask or React, minimal viable)
- All agentic browser automation scripts, app as repo’s Python module or subdir, docstring for each selector and artifact stage
- Maintained research tree and YAML/MD output tracked by query tag/version, with persistent log
- Manual/README and minimal deployment guide (Docker/devcontainer/bash)
- Chrome extension compatibility for YT-transcript and notification flow

***

## **5. Identified Risks / Open Questions**

- Ensure DOM selectors/pipelines are resilient to Gemini UI changes (add config/selector test phase)
- Pin Chrome/Chromium and package versions in Docker/devcontainer for deterministic browser launches
- Confirm rate-limits/batch caps for Deep Research and Canvas survive heavy task load or parallel runs (>100)
- Optional: if non-text exports/artifacts are needed, develop “artifact handler” stub for future extension

***

**Summary:**
Deliver a robust, extensible, and tracked multi-agent Gemini Deep Research tool with a modern HTML UI, full batch/YT/Canvas/Obsidian flows, and notifications/logging.
**Ready for full implementation by a senior Python/JS dev!**

[1](https://github.com/aaaronmiller/open-gemini-deep-research)
