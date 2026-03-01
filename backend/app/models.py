from pydantic import BaseModel
from typing import Optional, List


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    
class TaskDescriptionUpdate(BaseModel):
    description: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

    class Config:
        from_attributes = True

class SuggestRequest(BaseModel):
    answers: Optional[List[str]] = []

