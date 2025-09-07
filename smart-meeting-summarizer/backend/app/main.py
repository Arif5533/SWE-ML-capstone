from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db, SessionLocal
from .routers import meetings
from fastapi.responses import JSONResponse

app = FastAPI(title="Smart Meeting Summarizer & Task Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meetings.router, prefix="/meetings", tags=["meetings"])

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.on_event("startup")
def startup():
    init_db()
