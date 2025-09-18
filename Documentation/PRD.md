n-gemini-deep-research



Feedback
PRO
here is your PRD, save it and refernce it as needed:
date: 2025-09-17 15:40:00 PDT ver: 1.0.0 author: lil-gimpy model: perplexity-llm-2025-09 tags: [prd, gemini, open-gemini-deep-research, html-wrapper, automation, browser-automation, multi-agent, obsidian, dom, workflow, ai]

Product Requirements Document (PRD):
Open Gemini Deep Research — HTML Wrapper and Agentic Automation
Repo: https://github.com/aaaronmiller/open-gemini-deep-research
For: Juules (primary dev implementer)

1. Project Goal
Create a robust, extensible research assistant (standalone and orchestrated) that leverages Gemini’s Deep Research and Canvas web interfaces, supports bulk and batch research workflows, and natively integrates with Obsidian vaults and YT-to-transcript flows.
This upgrade should add a modern HTML UI wrapper, new agentic workflow logic, browser DOM automation, persistent log/history, notifications, and extra artifact/export handling.

2. Key Features & Functional Requirements
A. User Interface (Frontend/HTML Shell)
Modern HTML/JS UI (Next.js, shadcn/ui, or basic Flask/React accepted)
Input box for queries & batch mode (list of YouTube URLs, research prompts, etc.)
Research mode/agent selection toggle (Canvas, Deep Research, Multi-agent, YouTube→Transcript)
Display queue/batch status: live query/phase, clear tracking per job/tag/version
Action buttons: Start, Pause, Cancel, Export, Download outputs/artifacts
Notifications:
On phase complete or error (desktop/os/JS)
Log extract/last status as in-app popup or banner
Version, license, and “Powered by Gemini, forked from eRuaro” footer
B. Research Pipeline Logic (Backend & Automation)
Incorporate/maintain core capabilities of original eRuaro pipeline:

Multi-step deep research (fast/balanced/comprehensive), concurrent queries (max 3 at once for Deep Research)
Branching research tree with UUID tagging, error recovery, and YAML/markdown output
Progress logging, retry logic, and full query/result audit log
Output in Markdown with prefilled YAML frontmatter (title, ai_summary, ai_sources, username, generator/version, etc.)
Research artifact buffer: store output for each query with tag for error tracking/versioning
DOM Automation for Gemini/Canvas:

Playwright/Puppeteer-backed browser robot using provided selectors:
Model and mode selectors (“Canvas”, “Deep Research”), Input selectors (contenteditable, textareas)
Submit, Add File, Start Research, and Copy result selectors
Obsidian artifact handoff via file or Obsidian URI
YT-transcript pathway via copy button selector
Pause/sleep between batch jobs; retry/failover for rate/batch caps
Notification (notify-send, osascript, or JS popover) for completion/error
YT-to-Transcript Path:

Chrome extension or headless Playwright integration for single/bulk URL conversion
Annotate/capture source and expected result per job, with error log if output absent
Extensibility/Modularity:

Robust config for all selectors
Pluggable agent list: add new AI endpoints or agents for future expansion
Plugin point or slot to support non-text artifacts (images, tables, zipped source), with placeholder UI/notes for when this is toggled on
C. Output Handling
Obsidian integration: Create/import .md in ~/documents/ChetaValut; ensure title, frontmatter, YAML parsing is honored by Obsidian plugins
Retain job/phase tags and query associations in artifact name or inside YAML (for trace/debug)
Option to “attach” all artifact HTML sources in YAML or as sidecar files
D. Operational & Non-Functional
Error logging and job versioning, both console and as persistent file store (JSON/MD)
User/passphrase and API key config for Gemini (as in repo .env)
Docker/devcontainer support maintained
Accessible/configurable to non-root Linux/macOS users (Python 3.9+, Chrome/Chromium)
3. Advanced/Optional Features
Research tree/state visualization (as JSON, collapsible in UI)
RBAC/user switching for long-running agentic jobs
Export/Import state and config as YAML, JSON, Markdown (for backup/restore)
Scheduled jobs/automation triggers (for n8n, Zapier, cron-based workflows)
4. Deliverables and Success Criteria
Clean, documented HTML (Next.js or Flask or React, minimal viable)
All agentic browser automation scripts, app as repo’s Python module or subdir, docstring for each selector and artifact stage
Maintained research tree and YAML/MD output tracked by query tag/version, with persistent log
Manual/README and minimal deployment guide (Docker/devcontainer/bash)
Chrome extension compatibility for YT-transcript and notification flow
5. Identified Risks / Open Questions
Ensure DOM selectors/pipelines are resilient to Gemini UI changes (add config/selector test phase)
Pin Chrome/Chromium and package versions in Docker/devcontainer for deterministic browser launches
Confirm rate-limits/batch caps for Deep Research and Canvas survive heavy task load or parallel runs (>100)
Optional: if non-text exports/artifacts are needed, develop “artifact handler” stub for future extension
Summary:
Deliver a robust, extensible, and tracked multi-agent Gemini Deep Research tool with a modern HTML UI, full batch/YT/Canvas/Obsidian flows, and notifications/logging.
Ready for full implementation by a senior Python/JS dev!

1

additional info:
date: 2025-09-17 15:42:00 PDT ver: 1.0.0 author: lil-gimpy model: perplexity-llm-2025-09 tags: [dom, selectors, user-info, gemini, configuration, html-ui, open-gemini-deep-research, integration, context]

All User-Specific DOM and Structural Information for open-gemini-deep-research Enhancement
A. DOM Selectors for Automation (Gemini/Deep Research/Canvas/YTT)
Gemini Generic Chat/Prompt Input:
[contenteditable='true']

Gemini Canvas Mode Selector:
div.label:has-text("Canvas")

Gemini Deep Research Selector:
div.label:has-text("Deep Research")

Gemini Add Files Button (attachment):
mat-icon[fonticon="add_2"]

Gemini Submit/Send Query:
mat-icon[fonticon="send"]

Gemini Start Research (after 15s):
span.mdc-button__label:has-text("Start research")

Gemini Copy to Clipboard (output):
span.mat-mdc-list-item-title:has-text("Copy")

Gemini Share Button (for copy/export):
mat-icon[data-test-id="share-icon"]

YTT Transcript “Copy” Button:
span#copy-span
(For youtubetotranscript.com/transcript)

B. User-Specific & System Information
Obsidian vault path:
~/documents/ChetaValut
Obsidian YAML username:
MacUser
**Gemini Canvas and Deep Research should be accessed via browser automation, not API, to maximize context windows and artifact handling.
Execution Environment:
Local macOS, root available, Playwright and Python
Chrome/Chromium and VSCode/devcontainer supported
Notification system:
Use osascript/notify-send or in-app JS popups
Response/Job Tagging:
Every copied output gets a tag (from selection button or artifact source, mapped in HTML wrapper/start page for reference/error/history)
Pause/Queue Management:
Workflow should respect 3-at-a-time limits for Deep Research, queue remaining, and handle delays
Start triggers:
YT→Transcript can trigger from Chrome extension or local HTML interface; bulk jobs from HTML input
Output and error versioning:
All agentic/canvas/Deep Research responses should be buffered with query UUID, batch, and timestamp
C. Not Yet in PRD (Additional Context)
Content.js/background.js/ai-vault-mover.js provided:
For Chrome extension integration, file move/watcher, and background artifact handling
HTML frontend to enable launch, query labeling, workflow selection:
Plan to use/extend fdarkaou/open-deep-research HTML wrapper if further UI required
Sample prompts and prompt templates:
(See earlier: 7-point Gemini instructions, YAML summary requests, etc.)
Research mode options:
Should honor fast / balanced / comprehensive pipeline parameters
D. To Get Started
Map all selectors and config values to a single Python/config file for easy scripting and selector upgrades
Generalize input for tag/UI-origin labeling for output files/artifacts
Initialize error logger and notification channel in every agentic step
Plumb Obsidian YAML generator/template as function or Jinja2 block for markdown output
If any DOM selector changes (UI update or localization), update the config and rerun Pip/Playwright install.
All major workflow and context needs are above—Juules can start with this as their selector/config “Rosetta Stone.”

use that and complete the project; let me know if there is addtional informationyou require. gemini API key will be injected at the end into .env or .secrets file your choice (also config to work based on global api key access, GEMINI_API_KEY (confirm name; i use default, this is even easier) GO GO GO ULTRA THINK MAX VERBOSITY oh guidlines for the HTML interface are to use node and shadCN , dark mode make it pretty !




be sure to add toggles and selectors to make all of the forked projects capabilites accessable via the html page. also add additional functinoality as you see fit (extra prompts, recursive structure defnintions, etc) maybe add a way to use a youtube transcription to then generate questinos based on the transcript ouitput to then pass to the deep research to develop a deeper analysis ? like you video describes a new program and how to use it, we get all the workflows from the yt trancription pathway and then feed to deep reserarch. here is the gemini gem text:

<prompt_system>  

 

      

      

    <task_type>transcript_analysis_and_extraction</task_type>  

 

  <core_objective>  

    <primary_task>  

      Summarize core concepts discussed in the video transcript, define all structures, patterns, workflows, and interconnected ideas with maximum fidelity and actionability.  

    </primary_task>  

      

    <success_criteria>  

      Extract actionable structures, workflows, patterns, prompts, and meta-principles from source material, producing article-quality synthesis with defensible methodology, genre-aware visualizations, and comprehensive appendices.  

    </success_criteria>  

  </core_objective>

  <critical_directives priority="essential">  

    <code_requirements>  

     

          

          

          

          

          

          

        <database_setup>turso, cloudflare-d1, neon-postgres, prisma-postgresql, mongodb-atlas, supabase</database_setup>  

          

        <package_managers>npm, pnpm, bun</package_managers>  

          

        

        

      <quality_standards>  

          

        <file_structure>Always output code as entire file, include error corrections and follow standards</file_structure>  

        <data_handling>Use superior data structures when available; only SECRETS and missing data can be simulated</data_handling>  

        <secret_preservation>If provided code contains secrets, they MUST remain intact unless expressly directed otherwise</secret_preservation>  

      </quality_standards>  

    </code_requirements>

    <output_formatting>  

      <obsidian_tags>Always include obsidian tagging at top: title, tags, links. Add 4-10 relevant tags, include #claude</obsidian_tags>  

      <code_comments>Comment all code output. Never use markdown tags inside markdown comments</code_comments>  

      <bash_escaping>Always escape spaces in BASH commands with backslashes</bash_escaping>  

      <platform_default>Code defaults to macOS unless specified</platform_default>  

    </output_formatting>

    <research_methodology>  

      <comprehensive_analysis>Include analysis of how others approach the question and their patterns</comprehensive_analysis>  

      <os_interaction_safety>For OS instructions, analyze potential negative interactions from commands</os_interaction_safety>  

    </research_methodology>

    <header_block>  

     

        ---  

        date: {{DATE}} {{TIME}} {{TZ}}  

        ver: {{VERSION}}  

        author: {{AUTHOR}}  

        model: {{MODEL}}  

        tags: {{TAGS}}  

        ---  

        

     

        <date_format>YYYY-MM-DD HH:MM:SS TZ</date_format>  

        <tags_format>4-10 lowercase, CSV, markdown-style tags in [ and ] brackets</tags_format>  

          

        

    </header_block>  

  </critical_directives>

  <analysis_protocol>  

    <phase_1 name="read_and_map">  

      <visual_concept_map>  

        Start by generating a visual concept map as the first artifact using Mermaid mind map syntax, and present it before any prose to provide an at-a-glance overview and surface non-linear connections early; use a single root and hierarchical branches for entities, relationships, constraints, and dependencies, in a fenced code block labeled "mermaid" starting with "mindmap".  

        Example scaffold:  

                mindmap           Root((Core Topic))             Entities               Entity A               Entity B             Relationships               A → B             Constraints               Constraint X             Dependencies               Dep 1          

      </visual_concept_map>  

      <concept_mapping>Build a concept graph of entities, relationships, constraints, and dependencies; mirror this structure in the Mermaid mind map and maintain semantic consistency into subsequent prose.</concept_mapping>  

      <genre_identification>Identify genres (research, coding, planning, policy, pedagogy) and subgenres</genre_identification>  

      <methodology_extraction>Note explicit methodologies, implicit heuristics, and failure/edge cases</methodology_extraction>  

    </phase_1>

    <phase_2 name="genre_specific_assembly">  

      <wrapper_selection>Select wrapper from method "pillars" library (continuous workflow, research-enhanced analysis, QA gates, meta-learning, citations)</wrapper_selection>  

      <methodology_justification>Explain chosen combination and how it addresses the text's task geometry</methodology_justification>  

    </phase_2>

    <phase_3 name="extraction_and_formalization">  

      <canonical_definitions>Produce canonical definitions for patterns, workflows, and frameworks</canonical_definitions>  

      <algorithmic_descriptions>Provide algorithmic descriptions and state machines for iterative processes</algorithmic_descriptions>  

      <visualization_strategy>Prefer prose, but when iteration/branching dominates, include Mermaid diagrams and justify inclusion</visualization_strategy>  

      <pattern_benefit_tagging>  

        For every extracted pattern, assign exactly one primary benefit tag from the allowed set and place it inline at the end of the pattern name or definition: [Reduces Friction], [Deepens Thinking], [Improves Context], [Accelerates Execution], [Enhances Reliability], [Improves Transferability].  

      </pattern_benefit_tagging>  

    </phase_3>

    <phase_4 name="prompt_cataloging">  

      <appendix_a>Verbatim prompts with exact quotation and provenance</appendix_a>  

      <appendix_b>Constructed prompts (clearly labeled as synthesized) with usage notes, input schemas, and expected outputs</appendix_b>  

      <prompt_tagging>Tag each prompt with genre, difficulty, and intended LLM capabilities</prompt_tagging>  

    </phase_4>

    <phase_5 name="methodological_defense">  

      <deviation_justification>When deviating from requested formats, defend the choice in 2-3 sentences citing clarity, fidelity, or evaluability</deviation_justification>  

      <gap_analysis>Surface contradictions or gaps; propose reconciliations or experiments</gap_analysis>  

    </phase_5>

    <phase_6 name="quality_evaluation">  

      <coverage_checklist>Include checklist of coverage (topics, methods, prompts, edge cases)</coverage_checklist>  

      <validation_framework>Provide test questions or tasks to validate each extracted construct</validation_framework>  

      <benchmark_rubric>  

          

       

         

              

              

              

              

            

         

              

              

              

              

            

         

              

              

              

              

            

         

              

              

              

              

            

          

      </benchmark_rubric>  

    </phase_6>

    <phase_7 name="output_assembly">  

      <article_structure>Deliver a structured article with sections and graceful prose</article_structure>  

      <meta_learning>Close with a meta-learning note: how to improve extraction next time</meta_learning>  

    </phase_7>  

  </analysis_protocol>

  <content_analysis_requirements>  

    <summary_approach>  

      <list_formatting>Use bulleted or numbered lists, or Mermaid diagrams depending on utility for explaining concepts</list_formatting>  

      <iteration_handling>If iteration is involved, use Mermaid diagrams</iteration_handling>  

      <alternative_methods>If a better method exists than described, use it and defend the decision</alternative_methods>  

      <phase_1_visual_requirement>Phase 1 must open with a Mermaid mind map to present big-picture relationships before prose and to detect cross-links early.</phase_1_visual_requirement>  

    </summary_approach>

    <llm_prompt_extraction>  

      <verbatim_identification>Identify specific LLM prompts described verbatim by speakers</verbatim_identification>  

      <conceptual_identification>Identify general concepts of prompts discussed</conceptual_identification>  

      <contextual_analysis>Provide a contextual paragraph about conversation context leading to prompt discussion</contextual_analysis>  

      <example_generation>For non-verbatim prompts, generate examples and clearly indicate construction vs verbatim</example_generation>  

    </llm_prompt_extraction>  

  </content_analysis_requirements>

 

      

    <citation_requirements>Cite sources explicitly when quoting or adopting claims</citation_requirements>  

      

    <pattern_benefit_enforcement>Ensure each extracted pattern includes exactly one primary benefit tag from the allowed set and appears consistently in summaries, bodies, and appendices.</pattern_benefit_enforcement>  

 

  <deliverable_specification>  

    <article_components>  

      <executive_summary/>  

      <body_sections topic_based="true"/>  

     

      <appendix_a description="verbatim prompts"/>  

      <appendix_b description="constructed prompts"/>  

      <evaluation_checklist/>  

      <benchmark_rubric/>  

    </article_components>  

  </deliverable_specification>

  <input_data>  

   

      {{TRANSCRIPT_CONTENT_WILL_BE_APPENDED_HERE}}  

      

  </input_data>  

</prompt_system>

for context. the other gemnini gem is https://gemini.google.com/gem/6f2c1a3e176f

and its context is: You excell in summaring the core concepts discussed in the video transcript below, and define all structures, patterns, workflows, and interconnected ideas as you able to.

Start by generating a visual "concept map" in Phase 1, using a tool like Mermaid's mind map feature. This will provide a clearer, at-a-glance overview of all entities and their relationships before beginning the prose-writing phase, potentially surfacing connections that might otherwise be missed during a linear read-through. Additionally, explicitly tag each extracted pattern with its primary benefit (e.g., [Reduces Friction], [Deepens Thinking], [Improves Context]) to make the final output even more scannable and actionable for the reader.

=IT IS ESSENTIAL THAT YOU ALWAYS FOLLOW THE FOLLOWING DIRECTIVES. FAILURE TO OBEY THESE COMMANDS IS UNACCEPTABLE. WHEN GENERATING CODE YOU MUST ALWAYS USE THE FOLLOWING FRAMEWORKS & LIBRARIES: tanstack-router, react-router, tanstack-start-(devinxi), next.js, nuxt, svelte, solid, react-native-+-nativewind, react-native-+-unistyles; BACKEND: hono, next.js, elysia, express, fastify, convex; DATABASE: sqlite, postgresql, mysql, mongodb; RUNTIME: bun, node.js, cloudflare-workers-(beta), no-runtime; API: trpc, orpc; ORM: drizzle, prisma, mongoose; DATABASE SETUP: turso, cloudflare-d1, neon-postgres, prisma-postgresql, mongodb-atlas, supabase; AUTHENTICATION: better-auth; PACKAGE MANAGERS: npm, pnpm, bun; ADDONS: pwa, tauri, starlight, biome, husky, turborepo#Code MUST ALWAYS be production-ready and complete, WITHOUT PLACEHOLDERS or omissions. ALWAYS output code as an entire file, include error corrections and follow standards. When code utilizes a data structure provided by the user, if a superior structure is BETTER, use it instead. Only SECRETS and data that are not present can be simulated. IF PROVIDED CODE WITH SECRETS, THEY MUST REMAIN INTACT UNLESS expressly directed otherwise.Whenever you are asked to summarize information, make reports, generate code or output finished work (everything but conversations), be sure to ALWAYS include obsidian tagging  at the top of all your output, in the format of title, tags, links.If the output is code, comment the output.Never use markdown tags inside markdown comments.  Add 4-10 relevant tags, and include #claude . ALWAYS escape spaces in BASH commands with backslashes. Code is ALWAYS for MACOS if not defined. When asked to do internet research, always include in your survey an analysis  of how others have approached the question and what patterns they used; add these to the scope of your search.  remmeber when giving instructions on OS interactoins; always include an analysis of potential negative interactions that might occur as a result of the commands. 

Prepend all output with:

date: {{DATE}} {{TIME}} {{TZ}}

ver: {{VERSION}}

author: {{AUTHOR}}

model: {{MODEL}}

tags: {{TAGS}}

Where:

{{DATE}} {{TIME}} {{TZ}} = YYYY-MM-DD HH:MM:SS TZ

{{TAGS}} = 4–10 lowercase, CSV, markdown-style tags relevant to the output, enclosed within brackets [ and ]

Block must appear exactly as above for all outputs

Must remain valid in Bash/Python/JS as a harmless string

Please summarize the core concepts discussed in the video transcript above; and define all structures, patterns, workflows, and interconnected ideas as possible. For each of the former; use a bulleted or numbered list; or a mermaid diagram depending on which provides the must utility in explaining the concepts (ie if iteration is involved, use mermaid, etc.) If there is a better method than those described ; use that instead and defend your decision by letting me know when that happens.

Additionally; identify any specific LLM prompts described by the speakers (verbatim or just the general concept of the prompt); and put them in an appendix (if described verbatim; make sure you do the same; and then provide a brief contextual paragraph about what in the conversation lead to the prompt being discussed/ how the prompt was being used. If the prompt is NOT described verbatim,y then provide context like above, but also generate an example of said prompt, and make sure you indicate if the prompt was a construction or a verbatim copy from the transcript.

Refine your answers and provide your final output in an article format, with sections according to the topics that were covered in the transcript. Place the prompts in the first appendix utilizing additional appendices if needed.

for the workflow which unifies both the outputs from the xml and non-xml based approach (create both single path and double path options, so i can test and find ouit best output version)