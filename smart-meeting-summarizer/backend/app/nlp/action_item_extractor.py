import re
from typing import List, Dict

ASSIGNEE_PATTERN = r"(Alice|Bob|Carol|Dave|Eve|[A-Z][a-z]+)"
DUE_PATTERN = r"(by\s+(Monday|Tuesday|Wednesday|Thursday|Friday|\\d{4}-\\d{2}-\\d{2}|\\d{1,2}\\s*[A-Za-z]+)|due\\s+(next\\s+\\w+|\\d{4}-\\d{2}-\\d{2}|\\w+day))"

IMPERATIVES = [
    "finish", "finalize", "prepare", "review", "send", "share", "set up", "schedule",
    "assign", "implement", "evaluate", "run", "analyze", "complete", "update", "ping",
]

def extract_action_items(transcript: str) -> List[Dict]:
    tasks: List[Dict] = []
    lines = [l.strip() for l in transcript.splitlines() if l.strip()]
    for line in lines:
        # pull speaker labels if present: "[00:10] Bob: ..."
        m = re.search(r"\\] (.+?):\\s*(.*)$", line)
        if m:
            speaker, text = m.group(1), m.group(2)
        else:
            speaker, text = None, line

        lower = text.lower()
        if any(imp in lower for imp in IMPERATIVES):
            # Try to extract assignee
            assignee = speaker
            if not assignee:
                m2 = re.search(ASSIGNEE_PATTERN, text)
                if m2:
                    assignee = m2.group(1)

            # Extract due
            due = None
            m3 = re.search(DUE_PATTERN, text, flags=re.I)
            if m3:
                due = m3.group(0)

            # Clean description
            desc = re.sub(r"^(I\\s+will\\s+|I'll\\s+|We\\s+will\\s+)", "", text, flags=re.I)
            tasks.append({
                "assignee": assignee,
                "description": desc.strip(),
                "due_date": due,
                "status": "open",
            })
    return dedupe(tasks)

def dedupe(tasks: List[Dict]) -> List[Dict]:
    seen = set()
    out: List[Dict] = []
    for t in tasks:
        key = (t["assignee"] or "", t["description"], t["due_date"] or "")
        if key not in seen:
            seen.add(key)
            out.append(t)
    return out
