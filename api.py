import asyncio
import uuid
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

from src.browser_automation import BrowserController
from src.deep_research import DeepSearch
from src.output_handler import save_to_obsidian
from src.prompts import GEMINI_GEM_XML_PROMPT, GEMINI_GEM_SIMPLE_PROMPT

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Open Gemini Deep Research API",
    description="An API to orchestrate deep research and analysis tasks using browser automation.",
    version="1.1.0"
)

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-Memory Job Storage ---
jobs: Dict[str, Dict[str, Any]] = {}

# --- Pydantic Models ---
class ResearchRequest(BaseModel):
    query: str
    mode: str = "balanced"

class YouTubeTranscriptRequest(BaseModel):
    url: str

class AnalyzeTranscriptRequest(BaseModel):
    url: str
    prompt_type: str = "xml" # 'xml' or 'simple'

# --- Background Task Functions ---
async def run_research_task(job_id: str, query: str, mode: str):
    """Runs the standard deep research background task."""
    jobs[job_id]["status"] = "running"
    try:
        async with BrowserController() as browser_controller:
            await browser_controller.navigate_to_gemini()
            deep_search = DeepSearch(browser_controller, mode=mode)

            breadth_and_depth = deep_search.determine_research_breadth_and_depth(query)
            jobs[job_id]["progress"] = "Determined breadth and depth."

            results = await deep_search.deep_research(query, breadth_and_depth["breadth"], breadth_and_depth["depth"])
            jobs[job_id]["progress"] = "Deep research complete. Generating report..."

            final_report = await deep_search.generate_final_report(query, results["learnings"])
            jobs[job_id]["progress"] = "Report generated. Saving to Obsidian..."

            filepath = save_to_obsidian(
                query=query,
                report_content=final_report,
                sources=list(results.get("visited_urls", {}).values())
            )

            jobs[job_id].update({"status": "completed", "result": {"report_path": filepath}, "progress": "Done"})
    except Exception as e:
        print(f"Error in job {job_id}: {e}")
        jobs[job_id].update({"status": "failed", "error": str(e)})

async def run_analysis_task(job_id: str, url: str, prompt_type: str):
    """Runs the YouTube transcript analysis background task."""
    jobs[job_id]["status"] = "running"
    try:
        async with BrowserController() as browser_controller:
            jobs[job_id]["progress"] = "Fetching transcript..."
            transcript = await browser_controller.get_youtube_transcript(url)
            if not transcript:
                raise ValueError("Failed to retrieve transcript.")

            jobs[job_id]["progress"] = "Transcript fetched. Analyzing..."

            prompt_template = GEMINI_GEM_XML_PROMPT if prompt_type == "xml" else GEMINI_GEM_SIMPLE_PROMPT
            full_prompt = prompt_template.replace("{{TRANSCRIPT_CONTENT_WILL_BE_APPENDED_HERE}}", transcript)

            await browser_controller.navigate_to_gemini()
            await browser_controller.send_prompt(full_prompt)

            # This is a long-running analysis, needs a significant wait
            await asyncio.sleep(45)
            analysis_result = await browser_controller.copy_last_response()

            jobs[job_id].update({"status": "completed", "result": {"analysis": analysis_result}, "progress": "Done"})
    except Exception as e:
        print(f"Error in job {job_id}: {e}")
        jobs[job_id].update({"status": "failed", "error": str(e)})

# --- API Endpoints ---
@app.post("/api/research", status_code=202)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "queued", "type": "research", "query": request.query}
    background_tasks.add_task(run_research_task, job_id, request.query, request.mode)
    return {"job_id": job_id}

@app.post("/api/analyze-transcript", status_code=202)
async def start_analysis(request: AnalyzeTranscriptRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "queued", "type": "analysis", "url": request.url}
    background_tasks.add_task(run_analysis_task, job_id, request.url, request.prompt_type)
    return {"job_id": job_id}

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return {"error": "Job not found"}
    return job

@app.post("/api/youtube-transcript")
async def get_raw_transcript(request: YouTubeTranscriptRequest):
    try:
        async with BrowserController() as browser_controller:
            transcript = await browser_controller.get_youtube_transcript(request.url)
            return {"transcript": transcript}
    except Exception as e:
        return {"error": str(e)}
