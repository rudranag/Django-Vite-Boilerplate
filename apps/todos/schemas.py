from ninja import Schema
from pydantic import ConfigDict, Field
from datetime import datetime

class TodoSchema(Schema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str = Field(..., max_length=200)
    description: str
    completed: bool
    created_at: datetime

class TodoCreateSchema(Schema):
    title: str = Field(..., max_length=200)
    description: str
    completed: bool = False
