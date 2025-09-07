# Smart Meeting Summarizer & Task Generator

Cloud-based web platform that uses LLMs (or a robust offline heuristic) to:
- Summarize meeting transcripts
- Identify key action items
- Auto-assign tasks and due dates
- Persist meeting history to PostgreSQL
- Offer an interactive UI (Streamlit)

**Tech stack**: FastAPI, PostgreSQL, SQLAlchemy, Pydantic, Streamlit, Docker, Docker Compose.  
**Optional**: OpenAI API integration via `OPENAI_API_KEY`. Falls back to a fast, deterministic offline heuristic when no key is provided.

---

## Quick Start (Docker)

1. **Set environment variables** (copy `.env.example` -> `.env` and edit if needed).
2. **Build & run**:
   ```bash
   docker compose up --build
   ```
3. Open:
   - API docs: http://localhost:8000/docs
   - Streamlit UI: http://localhost:8501

> The first run will create tables automatically and seed a sample meeting.

---

## Local Dev (no Docker)

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend (Streamlit)
```bash
cd streamlit_app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

---

## API Overview

- `POST /meetings/` – create a meeting (with raw transcript text)
- `GET /meetings/` – list meetings
- `GET /meetings/{id}` – get one
- `POST /meetings/{id}/analyze` – run summarization + action item extraction
- `GET /tasks/` – list generated tasks
- `GET /healthz` – health check

Open API docs at `/docs`.

---

## Data Model

- **Meeting**: id, title, transcript, summary, created_at
- **Task**: id, meeting_id, assignee, description, due_date, status

---

## Heuristic vs LLM

- If `OPENAI_API_KEY` is present, the service will call the OpenAI Chat Completions API (GPT-4o-mini default; configurable) for summaries & tasks.
- Otherwise, it uses an offline pipeline:
  - Clean transcript (speaker tags, timestamps)
  - Extractive summary (TextRank-ish scoring + sentence diversity)
  - Action-item mining using imperative-verb patterns + assignee/due-date parsing

This offline pipeline is designed to be **fast and testable**, and can reach good accuracy on structured transcripts. For public claims, please evaluate on your own dataset.

---

## Testing

```bash
cd backend
pytest -q
```

---

## Repository Structure

```
smart-meeting-summarizer/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ db.py
│  │  ├─ models.py
│  │  ├─ schemas.py
│  │  ├─ routers/
│  │  │  └─ meetings.py
│  │  ├─ services/
│  │  │  └─ summarizer.py
│  │  ├─ nlp/
│  │  │  └─ action_item_extractor.py
│  │  └─ tests/
│  │     └─ test_pipeline.py
├─ streamlit_app/
│  └─ app.py
├─ sample_data/
│  └─ meeting_01.txt
├─ docker-compose.yml
├─ Dockerfile.api
├─ Dockerfile.web
├─ .env.example
├─ .gitignore
├─ LICENSE (MIT)
└─ README.md
```

---

## Screenshots (optional)

Add your own screenshots or recordings demonstrating:
- Uploading a transcript
- Getting a summary + tasks
- Assigning tasks and marking done

---

## License

MIT
