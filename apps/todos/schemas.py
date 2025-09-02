from ninja import Schema
from datetime import datetime

class TodoSchema(Schema):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

class TodoCreateSchema(Schema):
    title: str
    description: str
    completed: bool = False
