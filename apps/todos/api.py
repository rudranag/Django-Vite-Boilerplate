from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from apps.todos.models import Todo
from apps.todos.schemas import TodoSchema, TodoCreateSchema
from ninja.security import SessionAuth

api = Router(auth=SessionAuth())

@api.get("/", response=List[TodoSchema])
def list_todos(request):
    return Todo.objects.filter(user=request.auth)

@api.post("/", response=TodoSchema)
def create_todo(request, payload: TodoCreateSchema):
    todo = Todo.objects.create(**payload.dict(), user=request.auth)
    return todo

@api.get("/{todo_id}", response=TodoSchema)
def get_todo(request, todo_id: int):
    todo = get_object_or_404(Todo, id=todo_id, user=request.auth)
    return todo

@api.put("/{todo_id}", response=TodoSchema)
def update_todo(request, todo_id: int, payload: TodoCreateSchema):
    todo = get_object_or_404(Todo, id=todo_id, user=request.auth)
    for attr, value in payload.dict().items():
        setattr(todo, attr, value)
    todo.save()
    return todo

@api.delete("/{todo_id}", response={204: None})
def delete_todo(request, todo_id: int):
    todo = get_object_or_404(Todo, id=todo_id, user=request.auth)
    todo.delete()
    return 204, None
