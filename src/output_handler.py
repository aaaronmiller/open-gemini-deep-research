import os
import re
import datetime
from .config import OBSIDIAN_VAULT_PATH, OBSIDIAN_YAML_USERNAME

def generate_sanitized_filename(query: str) -> str:
    """Generates a safe filename from a query string."""
    # Remove special characters
    sanitized = re.sub(r'[^\w\s-]', '', query).strip()
    # Replace spaces with hyphens
    sanitized = re.sub(r'[-\s]+', '-', sanitized)
    # Truncate to a reasonable length
    return sanitized[:80]

def save_to_obsidian(query: str, report_content: str, sources: list[dict], summary: str = "AI-generated summary to be added."):
    """
    Formats the report with YAML frontmatter and saves it to the Obsidian vault.

    Args:
        query (str): The original research query, used for the title.
        report_content (str): The main body of the research report.
        sources (list[dict]): A list of source dictionaries, each with 'title' and 'url'.
        summary (str): A brief summary for the YAML frontmatter.
    """
    print("Saving report to Obsidian vault...")

    # Expand the user's home directory in the path
    vault_path = os.path.expanduser(OBSIDIAN_VAULT_PATH)

    # Ensure the vault directory exists
    if not os.path.exists(vault_path):
        print(f"Warning: Obsidian vault path does not exist: {vault_path}. Creating it.")
        os.makedirs(vault_path)

    # Create YAML frontmatter
    timestamp = datetime.datetime.now().isoformat()
    sources_yaml = "\n".join([f"  - \"{s.get('title', '')}: {s.get('url', '')}\"" for s in sources]) if sources else ""

    yaml_frontmatter = f"""---
title: "{query}"
date: {timestamp}
ai_summary: "{summary}"
ai_sources:
{sources_yaml}
username: "{OBSIDIAN_YAML_USERNAME}"
generator: "Open Gemini Deep Research v1.0"
---
"""

    # Combine frontmatter and content
    full_content = yaml_frontmatter + "\n" + report_content

    # Create a safe filename
    filename = generate_sanitized_filename(query) + ".md"
    filepath = os.path.join(vault_path, filename)

    # Save the file
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"Successfully saved report to: {filepath}")
    except Exception as e:
        print(f"Error saving report to Obsidian: {e}")

    return filepath
