from pydantic import BaseModel
from typing import Optional, List

class TaskBase(BaseModel):
    assignee: Optional[str] = None
    description: str
    due_date: Optional[str] = None
    status: Optional[str] = "open"

class TaskOut(TaskBase):
    id: int
    class Config:
        from_attributes = True

class MeetingCreate(BaseModel):
    title: str
    transcript: str

class MeetingOut(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    class Config:
        from_attributes = True

class MeetingDetail(MeetingOut):
    transcript: str
    tasks: List[TaskOut] = []
