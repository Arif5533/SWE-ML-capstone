# 📝 Smart Meeting Summarizer & Task Generator

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-success?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-ff4b4b?logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A **cloud-based web application** that transforms meeting transcripts into **concise summaries** and **actionable task lists**.  

- **FastAPI (RESTful backend)** provides clean API endpoints for meetings and tasks.  
- **PostgreSQL** stores meetings, transcripts, summaries, and tasks.  
- **Streamlit (frontend)** offers a simple and interactive UI.  
- **Summarization Engine** supports two modes:  
  - ✅ **Heuristic NLP pipeline** (offline, no API key required)  
  - 🤖 **LLM-powered mode** (optional, via OpenAI API)  

The entire system is containerized with **Docker Compose** for quick setup.

---

## ✨ Features

- 📄 **Automatic Summarization** – Condense long transcripts into readable summaries.  
- ✅ **Task Extraction** – Identify assignees, action items, and deadlines.  
- 👥 **Task Tracking** – Persist open/closed tasks for each meeting.  
- 💾 **PostgreSQL Database** – Durable storage for meetings and tasks.  
- 🌐 **RESTful API (FastAPI)** – CRUD endpoints with auto-generated OpenAPI docs.  
- 🎨 **Streamlit UI** – Upload/view transcripts, summaries, and tasks.  
- 🐳 **Dockerized Deployment** – Run backend, database, and UI with one command.  

---

## 🚀 Tech Stack

- **Backend**: FastAPI (Python), RESTful API architecture  
- **Database**: PostgreSQL (via SQLAlchemy ORM)  
- **Frontend**: Streamlit  
- **NLP Engine**:  
  - Heuristic pipeline (extractive summarization + regex task mining)  
  - Optional LLM integration (OpenAI GPT models)  
- **DevOps**: Docker, Docker Compose  
- **Testing**: Pytest  

---

## 🏗️ Architecture

```
                ┌───────────────────────┐
                │   Streamlit Frontend   │
                │  (User uploads text)   │
                └───────────┬───────────┘
                            │ REST API calls
                            ▼
                ┌───────────────────────┐
                │ FastAPI REST Backend  │
                │  (CRUD + Orchestration) │
                └───────────┬───────────┘
                            │
      ┌─────────────────────┴─────────────────────┐
      │                                           │
┌───────────────┐                        ┌───────────────────┐
│ Heuristic NLP │                        │ OpenAI API (LLM) │
│ (Default)     │                        │ (Optional)       │
└───────────────┘                        └───────────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │    PostgreSQL DB      │
                │  (Meetings & Tasks)   │
                └───────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/smart-meeting-summarizer.git
cd smart-meeting-summarizer
```

### 2. Configure Environment
Copy the example file and update values:
```bash
cp .env.example .env
```

- `DATABASE_URL` → PostgreSQL connection string  
- `OPENAI_API_KEY` → (optional) for LLM-powered mode  
- `OPENAI_MODEL` → defaults to `gpt-4o-mini`  

### 3. Run with Docker
```bash
docker compose up --build
```

Access:
- API Docs → [http://localhost:8000/docs](http://localhost:8000/docs)  
- Streamlit UI → [http://localhost:8501](http://localhost:8501)  

---

## 🧑‍💻 Local Development (without Docker)

### Backend (FastAPI)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
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

## 📡 RESTful API Endpoints

- `POST /meetings/` → Create a new meeting (with transcript)  
- `GET /meetings/` → Retrieve all meetings  
- `GET /meetings/{id}` → Retrieve one meeting with tasks  
- `POST /meetings/{id}/analyze` → Run summarization + task extraction  
- `GET /tasks/` → List all tasks  

Swagger UI available at `/docs`.

---

## 🗄️ Database Schema

**Meeting**
- `id`, `title`, `transcript`, `summary`, `created_at`

**Task**
- `id`, `meeting_id`, `assignee`, `description`, `due_date`, `status`

---

## 🧠 How It Works

- **LLM Mode** (requires `OPENAI_API_KEY`):  
  Uses GPT models for advanced summarization + structured task extraction.  

- **Heuristic Mode** (default, no API key required):  
  - Extractive summarization (sentence ranking with keyword boosts)  
  - Regex-based task mining (imperative verbs, assignees, due dates)  

This dual design ensures the project is **demo-ready out of the box** and extensible with LLMs.

---

## 🧪 Testing

```bash
cd backend
pytest -q
```

---







## 📜 License

Licensed under the **MIT License** – free to use, modify, and distribute.
