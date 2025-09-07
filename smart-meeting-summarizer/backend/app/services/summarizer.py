import os
import re
from typing import List, Tuple, Dict
import numpy as np

try:
    import httpx
except Exception:
    httpx = None

from ..nlp.action_item_extractor import extract_action_items

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = "You are an assistant that writes concise meeting summaries and action items."

def call_openai(transcript: str) -> Tuple[str, List[Dict]]:
    if not OPENAI_API_KEY or not httpx:
        raise RuntimeError("OpenAI not configured")
    prompt = f\"\"\"Summarize the meeting in 5-7 bullets. Then list action items as JSON with fields: assignee, description, due_date (string or null).
Transcript:
{transcript}
\"\"\"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    r = httpx.post("https://api.openai.com/v1/chat/completions", json=payload, timeout=60)
    r.raise_for_status()
    content = r.json()["choices"][0]["message"]["content"]
    # Very light parsing: split summary and JSON block if present
    # Fall back to heuristic if parsing fails
    try:
        # try to find a JSON block
        json_match = re.search(r"\[\s*{.*}\s*\]", content, flags=re.S)
        tasks = []
        if json_match:
            import json
            tasks = json.loads(json_match.group(0))
        # summary is content with json removed
        if json_match:
            summary_text = content[:json_match.start()].strip()
        else:
            summary_text = content.strip()
        return summary_text, tasks
    except Exception:
        return content.strip(), []

def heuristic_summary(transcript: str, max_sentences: int = 6) -> str:
    # Simple TextRank-ish scoring using sentence position + keyword boosts
    sentences = re.split(r"(?<=[.!?])\s+", transcript.strip())
    if len(sentences) <= max_sentences:
        return " ".join(sentences)
    keywords = ["action", "decide", "risk", "deadline", "due", "assign", "launch", "goal"]
    scores = []
    for i, s in enumerate(sentences):
        kw = sum(1 for k in keywords if k.lower() in s.lower())
        score = kw + 1.0 / (i + 1)  # early sentences get a tiny boost
        scores.append((score, i, s))
    top = sorted(scores, reverse=True)[: max_sentences * 2]
    # diversify by keeping order but picking every ~n
    selected = [s for _, _, s in sorted(top, key=lambda x: x[1])][:max_sentences]
    return " ".join(selected)

def analyze_meeting(transcript: str) -> Tuple[str, List[Dict]]:
    # Prefer OpenAI if configured; otherwise use heuristic
    if OPENAI_API_KEY and httpx is not None:
        try:
            summary, tasks = call_openai(transcript)
            if tasks:
                return summary, tasks
        except Exception:
            pass
    summary = heuristic_summary(transcript)
    tasks = extract_action_items(transcript)
    return summary, tasks
