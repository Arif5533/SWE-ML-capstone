from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import SessionLocal
from .. import models, schemas
from ..services.summarizer import analyze_meeting

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.MeetingOut)
def create_meeting(payload: schemas.MeetingCreate, db: Session = Depends(get_db)):
    m = models.Meeting(title=payload.title, transcript=payload.transcript)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.get("/", response_model=List[schemas.MeetingOut])
def list_meetings(db: Session = Depends(get_db)):
    return db.query(models.Meeting).order_by(models.Meeting.id.desc()).all()

@router.get("/{meeting_id}", response_model=schemas.MeetingDetail)
def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    m = db.query(models.Meeting).get(meeting_id)
    if not m:
        raise HTTPException(404, "Meeting not found")
    return m

@router.post("/{meeting_id}/analyze", response_model=schemas.MeetingDetail)
def analyze(meeting_id: int, db: Session = Depends(get_db)):
    m = db.query(models.Meeting).get(meeting_id)
    if not m:
        raise HTTPException(404, "Meeting not found")
    summary, tasks = analyze_meeting(m.transcript)
    m.summary = summary
    # Clear existing tasks
    db.query(models.Task).filter(models.Task.meeting_id == m.id).delete()
    for t in tasks:
        db.add(models.Task(meeting_id=m.id, **t))
    db.commit()
    db.refresh(m)
    return m
